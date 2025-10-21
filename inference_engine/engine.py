from .data_loader import load_rules
from .cf_utils import cf_from_mb_md, combine_cf

def infer(user_input, trace=False):
    data = load_rules()
    rules = data["rules"]
    mb_md = data["mb_md"]
    penyakit_dict = data["penyakit"]

    penyakit_cf = {}
    log_detail = []

    for rule in rules:
        gejala_aktif = [g for g in rule["if"] if user_input.get(g)]
        if len(gejala_aktif) == 0:
            continue

        # Hitung CF tiap gejala
        cf_values = []
        for g in gejala_aktif:
            mb, md = mb_md[g]
            cf = cf_from_mb_md(mb, md)
            cf_values.append(cf)
            if trace:
                log_detail.append(f"{g}: MB={mb}, MD={md}, CF={cf}")

        # Kombinasi CF seperti rumus manual
        cf_rule = cf_values[0]
        kode_penyakit = rule["then"]
        nama_penyakit = penyakit_dict.get(kode_penyakit, kode_penyakit)

        if trace:
            log_detail.append(f"\n--- Menghitung CF Kombinasi untuk {nama_penyakit} ---")
            log_detail.append(f"CF1 = {cf_rule}")

        for i, cf_next in enumerate(cf_values[1:], start=2):
            lama = cf_rule
            cf_rule = combine_cf(cf_rule, cf_next)
            if trace:
                log_detail.append(
                    f"CF Kombinasi (CF{i-1}, CF{i}) = {lama:.4f} + {cf_next:.4f} * (1 - {lama:.4f}) = {cf_rule:.5f}"
                )

        # Simpan hasil CF akhir per penyakit
        if kode_penyakit in penyakit_cf:
            penyakit_cf[kode_penyakit] = combine_cf(penyakit_cf[kode_penyakit], cf_rule)
        else:
            penyakit_cf[kode_penyakit] = cf_rule

        if trace:
            log_detail.append(f"Hasil akhir CF {nama_penyakit} = {cf_rule:.5f}\n")

    if trace:
        return penyakit_cf, "\n".join(log_detail)
    return penyakit_cf
