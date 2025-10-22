# Sistem Pakar Diagnosa Osteoporosis

Sistem pakar untuk membantu mendiagnosa risiko osteoporosis berdasarkan gejala dan faktor risiko menggunakan metode Forward Chaining dan Certainty Factor.

## 🚀 Fitur Utama

- **Interface Web Modern**: UI responsif dengan tab navigasi (Konsultasi, Informasi, Tentang)
- **Diagnosis Interaktif**: Pilih gejala dan dapatkan diagnosis dengan tingkat kepercayaan
- **API Backend**: RESTful API menggunakan Flask untuk integrasi yang mudah
- **Informasi Edukasi**: Informasi lengkap tentang osteoporosis dan pencegahan
- **Sistem Rekomendasi**: Saran tindakan berdasarkan hasil diagnosis

## 🛠️ Teknologi

- **Backend**: Python Flask dengan Flask-CORS
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: JSON file untuk rules dan data
- **Algoritma**: Forward Chaining dengan Certainty Factor

## 📋 Prerequisites

- Python 3.7 atau lebih baru
- pip (Python package installer)

## 🚀 Instalasi dan Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/NinaHerlin/SistemPakar.git
cd SistemPakar
```

### 2. Install Dependencies
```bash
pip install flask flask-cors
```
atau
```bash
pip install -r requirements.txt
```

### 3. Jalankan Server
```bash
python app.py
```
atau di Windows:
```bash
py app.py
```

### 4. Akses Aplikasi
Buka browser dan akses: `http://localhost:5000`

## 📁 Struktur Project

```
SistemPakar/
├── .gitignore            # Git ignore file
├── app.py                # Flask backend server
├── rules.json           # Database rules dan gejala
├── requirements.txt     # Python dependencies
├── README.md            # Dokumentasi project
├── ui/                  # Frontend files
│   ├── index.html       # Main HTML file
│   ├── style.css        # Styling
│   └── script.js        # JavaScript logic
├── ui_backup/           # Backup UI Streamlit lama
│   └── app_streamlit.py # UI Streamlit original
└── inference_engine/    # Logic engine
    ├── engine.py        # Main inference logic
    ├── cf_utils.py      # Certainty Factor utilities
    └── data_loader.py   # Data loading utilities
```

## 🔄 API Endpoints

### Health Check
```
GET /health
```
Response: Status server dan informasi sistem

### Get Symptoms
```
GET /symptoms
```
Response: Daftar semua gejala dan faktor risiko

### Perform Diagnosis
```
POST /diagnose
Content-Type: application/json

{
  "symptoms": ["G01", "G02", "G03"]
}
```
Response: Hasil diagnosis dengan tingkat kepercayaan dan rekomendasi

## 🩺 Cara Penggunaan

### Web Interface
1. Buka `http://localhost:5000` di browser
2. Pilih tab **Konsultasi**
3. Centang gejala dan faktor risiko yang sesuai
4. Klik **Lakukan Diagnosis**
5. Lihat hasil diagnosis di panel kanan
6. Baca rekomendasi dan saran tindakan

### Tab Informasi
- Informasi umum tentang osteoporosis
- Gejala-gejala yang perlu diperhatikan
- Tips pencegahan
- Kelompok berisiko

### Tab Tentang
- Penjelasan cara kerja sistem
- Teknologi yang digunakan
- Disclaimer medis

## ⚠️ Disclaimer

**PENTING**: Sistem ini hanya untuk bantuan skrining awal dan **TIDAK MENGGANTIKAN** diagnosis medis profesional. Selalu konsultasikan dengan dokter spesialis untuk diagnosis dan penanganan yang tepat.

## 📊 Data dan Rules

Sistem menggunakan 23 gejala/faktor risiko (G01-G23) dan 4 jenis diagnosis:
- **P01**: Bukan Osteoporosis
- **P02**: Osteoporosis Primer
- **P03**: Osteoporosis Sekunder  
- **P04**: Osteoporosis Idiopatik

## 🔧 Development

### Menambah Gejala Baru
Edit file `rules.json` dan tambahkan gejala baru di section `"gejala"` dengan format:
```json
"G24": "Deskripsi gejala baru"
```

### Menambah Rules Baru
Tambahkan rule baru di section `"rules"` dengan format:
```json
{
  "if": ["G01", "G02"],
  "then": "P01"
}
```

### Mengubah Nilai MB/MD
Edit section `"mb_md"` untuk mengatur nilai kepercayaan setiap gejala:
```json
"G01": [0.7, 0.2]  // [MB, MD]
```

## 🤝 Kontribusi

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👥 Tim Pengembang

- **Nina Herlin** - Initial work - [NinaHerlin](https://github.com/NinaHerlin)

## 📞 Support

Jika ada pertanyaan atau masalah, silakan buat issue di GitHub repository.

---

**© 2024 Sistem Pakar Osteoporosis. Dikembangkan untuk tujuan edukasi.**