from inference_engine.engine import infer
from inference_engine.data_loader import load_rules

# daftar gejala (G01–G23)
gejala_list = {
    "G01": "Usia lebih dari 40 tahun",
    "G02": "Kelebihan berat badan",
    "G03": "Memiliki riwayat patah tulang",
    "G04": "Memiliki riwayat penyakit anggota keluarga yang mengidap osteoporosis",
    "G05": "Mengalami menopause",
    "G06": "Merasakan sakit punggung berkepanjangan",
    "G07": "Sering merokok",
    "G08": "Nyeri pada sendi",
    "G09": "Kekurangan hormon testosteron",
    "G10": "Sering konsumsi minuman keras",
    "G11": "Keretakan pada tulang punggung",
    "G12": "Konsumsi obat-obatan golongan steroid seperti Glukokortikoid",
    "G13": "Mengidap penyakit hipertiroidisme",
    "G14": "Rendahnya asupan kalsium harian",
    "G15": "Kurangnya aktivitas fisik",
    "G16": "Kekurangan vitamin D",
    "G17": "Riwayat penggunaan kortikosteroid jangka panjang",
    "G18": "Mengidap penyakit autoimun",
    "G19": "Tinggi badan menurun seiring bertambahnya usia",
    "G20": "Fraktur tulang tanpa trauma berat",
    "G21": "Penggunaan obat antikonvulsan",
    "G22": "Gangguan makan seperti anorexia",
    "G23": "Hiperparatiroidisme"
}

print("=== SISTEM PAKAR DIAGNOSA OSTEOPOROSIS ===")
print("Jawab dengan 'y' jika gejala dirasakan, atau 'n' jika tidak.\n")

user_input = {}

# ambil input dari terminal
for kode, deskripsi in gejala_list.items():
    jawab = input(f"Apakah Anda mengalami {deskripsi}? (y/n): ").strip().lower()
    user_input[kode] = True if jawab == 'y' else False

# jalankan inference engine (dengan trace)
hasil, log = infer(user_input, trace=True)

# ambil nama penyakit dari rules.json
data = load_rules()
penyakit_dict = data["penyakit"]

# tampilkan hasil diagnosa
print("\n=== HASIL DIAGNOSA ===")
if not hasil:
    print("Tidak ditemukan penyakit yang cocok berdasarkan gejala Anda.")
else:
    for kode, cf in hasil.items():
        nama_penyakit = penyakit_dict.get(kode, "Tidak diketahui")
        persentase = cf * 100
        print(f"{nama_penyakit}: {persentase:.2f}% tingkat kepercayaan")

# tampilkan log detail perhitungan CF
print("\n=== DETAIL PERHITUNGAN ===")
print(log)

# simpan hasil ke file teks
with open("hasil_diagnosa.txt", "w", encoding="utf-8") as f:
    f.write("=== HASIL DIAGNOSA ===\n")
    for kode, cf in hasil.items():
        nama_penyakit = penyakit_dict.get(kode, "Tidak diketahui")
        f.write(f"{nama_penyakit}: {cf*100:.2f}% tingkat kepercayaan\n")
    f.write("\n=== DETAIL PERHITUNGAN ===\n")
    f.write(log)

print("\nHasil diagnosa juga disimpan di file 'hasil_diagnosa.txt'.")
print("Terima kasih telah menggunakan sistem pakar ini!")
