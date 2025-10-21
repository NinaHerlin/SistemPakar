import streamlit as st
from inference_engine.engine import infer
from inference_engine.data_loader import load_rules

# --- Load data rules ---
data = load_rules()
gejala = data["gejala"]
penyakit_dict = data["penyakit"]

# --- Konfigurasi halaman ---
st.set_page_config(
    page_title="Sistem Pakar Osteoporosis",
    page_icon="🦴",
    layout="centered"
)

# --- Judul utama ---
st.title("🩺 Sistem Pakar Diagnosa Osteoporosis")
st.write("Pilih gejala yang Anda alami, kemudian klik **Diagnosa** untuk melihat hasilnya.")

# --- Input Gejala (Checkbox) ---
st.subheader("🧩 Pilih Gejala")
user_input = {}

# Bagi checkbox dalam dua kolom biar rapi
cols = st.columns(2)
for i, (kode, deskripsi) in enumerate(gejala.items()):
    with cols[i % 2]:
        user_input[kode] = st.checkbox(deskripsi)

# --- Tombol Diagnosa ---
if st.button("🔍 Diagnosa"):
    hasil, log = infer(user_input, trace=True)

    st.subheader("📊 Hasil Diagnosa")

    if not hasil:
        st.warning("Tidak ditemukan penyakit yang cocok berdasarkan gejala Anda.")
    else:
        # Urutkan hasil berdasarkan CF tertinggi
        hasil_sorted = dict(sorted(hasil.items(), key=lambda x: x[1], reverse=True))

        # Tambahkan toggle untuk menampilkan semua hasil
        show_all = st.checkbox("Tampilkan semua kemungkinan penyakit", value=False)

        # Ambil penyakit dengan CF tertinggi
        penyakit_tertinggi, cf_tertinggi = next(iter(hasil_sorted.items()))
        nama_penyakit = penyakit_dict.get(penyakit_tertinggi, penyakit_tertinggi)

        if show_all:
            for kode, cf in hasil_sorted.items():
                nama = penyakit_dict.get(kode, kode)
                persentase = cf * 100
                st.markdown(
                    f"<div style='background-color:#0f3a2e;padding:12px;border-radius:8px;margin-bottom:8px;'>"
                    f"<b>{nama}</b> → {persentase:.2f}% tingkat kepercayaan"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.success(f"🩺 **Diagnosis Anda: {nama_penyakit}**")
            st.progress(cf_tertinggi)
            st.write(f"Tingkat kepercayaan: **{cf_tertinggi*100:.2f}%**")

    # --- Detail Perhitungan CF ---
    with st.expander("🧮 Lihat Detail Perhitungan CF"):
        st.text(log)

# --- Footer ---
st.markdown("---")
st.caption("Dibuat oleh: **Sistem Pakar Osteoporosis** | Metode Certainty Factor (CF)")
