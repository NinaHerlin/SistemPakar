from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from inference_engine.engine import infer
from inference_engine.data_loader import load_rules

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load data once at startup
data = load_rules()
gejala = data["gejala"]
penyakit_dict = data["penyakit"]

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'data': {
            'status': 'healthy',
            'total_symptoms': len(gejala),
            'total_diseases': len(penyakit_dict)
        }
    })

@app.route('/symptoms')
def get_symptoms():
    """Get all available symptoms"""
    try:
        symptoms_list = []
        for kode, deskripsi in gejala.items():
            symptoms_list.append({
                'id': kode,
                'name': deskripsi,
                'description': deskripsi
            })
        
        return jsonify({
            'success': True,
            'data': symptoms_list,
            'total': len(symptoms_list)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/diagnose', methods=['POST'])
def diagnose():
    """Perform diagnosis based on selected symptoms"""
    try:
        data_request = request.get_json()
        
        if not data_request:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Get symptoms from request
        symptoms = data_request.get('symptoms', [])
        
        if not symptoms:
            return jsonify({
                'success': False,
                'error': 'No symptoms selected'
            }), 400
        
        # Prepare input for inference engine
        user_input = {}
        for symptom_id in symptoms:
            if symptom_id in gejala:
                user_input[symptom_id] = True
        
        # Perform inference
        hasil, log = infer(user_input, trace=True)
        
        # Prepare diagnosis results
        diagnosis_results = []
        
        if hasil:
            # Sort by confidence (CF value)
            sorted_hasil = dict(sorted(hasil.items(), key=lambda x: x[1], reverse=True))
            
            # Take only the highest confidence result for main diagnosis
            penyakit_tertinggi, cf_tertinggi = next(iter(sorted_hasil.items()))
            nama_penyakit = penyakit_dict.get(penyakit_tertinggi, penyakit_tertinggi)
            
            # Determine severity and recommendations based on disease type and confidence
            severity, recommendation_level, recommendations = get_disease_info(penyakit_tertinggi, cf_tertinggi)
            
            diagnosis_results.append({
                'disease_code': penyakit_tertinggi,
                'disease_name': nama_penyakit,
                'confidence': cf_tertinggi,
                'confidence_percentage': f"{cf_tertinggi*100:.1f}",
                'description': get_disease_description(penyakit_tertinggi),
                'severity': severity,
                'recommendation_level': recommendation_level,
                'recommendations': recommendations
            })
        
        return jsonify({
            'success': True,
            'data': {
                'diagnosis': diagnosis_results,
                'selected_symptoms': symptoms,
                'calculation_log': log,
                'total_symptoms': len(symptoms)
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def get_disease_description(disease_code):
    """Get detailed description for each disease"""
    descriptions = {
        'P01': 'Kondisi ini menunjukkan bahwa Anda tidak mengalami osteoporosis berdasarkan gejala yang dipilih. Namun, tetap penting untuk menjaga kesehatan tulang dengan pola hidup sehat.',
        'P02': 'Osteoporosis primer adalah jenis osteoporosis yang paling umum, biasanya terkait dengan penuaan dan perubahan hormonal, terutama pada wanita setelah menopause.',
        'P03': 'Osteoporosis sekunder adalah osteoporosis yang disebabkan oleh kondisi medis lain atau penggunaan obat-obatan tertentu seperti kortikosteroid jangka panjang.',
        'P04': 'Osteoporosis idiopatik adalah jenis osteoporosis yang terjadi tanpa penyebab yang jelas, sering terjadi pada orang dewasa muda atau anak-anak.'
    }
    return descriptions.get(disease_code, 'Deskripsi tidak tersedia untuk kondisi ini.')

def get_disease_info(disease_code, confidence):
    """Get severity level and recommendations based on disease and confidence"""
    
    # Determine severity based on confidence level
    if confidence >= 0.8:
        severity = "Tinggi"
    elif confidence >= 0.6:
        severity = "Sedang"
    elif confidence >= 0.4:
        severity = "Rendah"
    else:
        severity = "Sangat Rendah"
    
    # Base recommendations for all conditions
    base_recommendations = [
        "Konsultasikan hasil ini dengan dokter spesialis",
        "Lakukan pemeriksaan densitometri tulang (DEXA scan)",
        "Konsumsi makanan kaya kalsium dan vitamin D",
        "Lakukan olahraga weight bearing secara teratur"
    ]
    
    # Disease-specific recommendations
    disease_recommendations = {
        'P01': [
            "Pertahankan pola hidup sehat untuk mencegah osteoporosis",
            "Rutin melakukan pemeriksaan kesehatan tulang",
            "Hindari faktor risiko seperti merokok dan konsumsi alkohol berlebihan"
        ],
        'P02': [
            "Terapi penggantian hormon mungkin diperlukan (konsultasi dokter)",
            "Suplemen kalsium dan vitamin D sesuai anjuran dokter",
            "Hindari aktivitas berisiko tinggi jatuh",
            "Pertimbangkan terapi obat anti-osteoporosis"
        ],
        'P03': [
            "Evaluasi dan kelola kondisi medis yang mendasari",
            "Review penggunaan obat-obatan yang dapat mempengaruhi tulang",
            "Terapi khusus sesuai penyebab osteoporosis sekunder",
            "Monitoring ketat perkembangan kondisi tulang"
        ],
        'P04': [
            "Pemeriksaan menyeluruh untuk mencari penyebab tersembunyi",
            "Konsultasi dengan endokrinolog atau rheumatologist",
            "Evaluasi komprehensif metabolisme tulang",
            "Pemantauan jangka panjang kondisi tulang"
        ]
    }
    
    # Combine recommendations
    recommendations = base_recommendations + disease_recommendations.get(disease_code, [])
    
    # Recommendation level based on severity
    if confidence >= 0.7:
        recommendation_level = "Segera konsultasi dengan dokter"
    elif confidence >= 0.5:
        recommendation_level = "Disarankan konsultasi dengan dokter"
    else:
        recommendation_level = "Pantau gejala dan pertimbangkan konsultasi dokter"
    
    return severity, recommendation_level, recommendations

# Serve static files (HTML, CSS, JS)
@app.route('/')
def serve_index():
    return send_from_directory('ui', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('ui', filename)

if __name__ == '__main__':
    # Ensure ui directory exists
    if not os.path.exists('ui'):
        os.makedirs('ui')
    
    print("Starting Sistem Pakar Osteoporosis Flask Server...")
    print("API Endpoints:")
    print("- GET /health - Health check")
    print("- GET /symptoms - Get all symptoms")
    print("- POST /diagnose - Perform diagnosis")
    print("- GET / - Serve web interface")
    print()
    print("Server will be available at: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)