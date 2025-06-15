# scorer.py

def score_token(token):
    """
    Menilai token berdasarkan data: MC, LP, age (detik), dan rasio MC/LP.
    Return tuple: (total_score, alasan_list)
    """

    score = 0
    reasons = []

    # Saring jika datanya tidak lengkap
    if token is None or any(key not in token for key in ["mc", "lp", "age"]):
        reasons.append("❌ Data tidak lengkap")
        return (score, reasons)

    mc = token["mc"]
    lp = token["lp"]
    age = token["age"]

    # Skor MC
    if 15_000 <= mc <= 30_000:
        score += 1
        reasons.append("✅ MC ideal ($15K–$30K)")
    else:
        reasons.append("❌ MC di luar batas")

    # Skor LP
    if lp >= 1_000:
        score += 1
        reasons.append("✅ LP aman (≥ $1K)")
    else:
        reasons.append("❌ LP terlalu kecil")

    # Skor umur token
    if 30 <= age <= 300:
        score += 1
        reasons.append("✅ Umur token ideal (30s–5m)")
    else:
        reasons.append("❌ Umur terlalu baru/lama")

    # Rasio MC/LP
    try:
        ratio = mc / lp if lp > 0 else 0
        if 10 <= ratio <= 30:
            score += 1
            reasons.append(f"✅ Rasio MC/LP sehat ({ratio:.1f})")
        else:
            reasons.append(f"❌ Rasio MC/LP tidak sehat ({ratio:.1f})")
    except:
        reasons.append("❌ Gagal hitung rasio MC/LP")

    # Bonus: jika symbol/token name pendek (biasanya lebih legit)
    if len(token.get("symbol", "")) <= 5:
        score += 1
        reasons.append("✅ Symbol pendek")

    return (score, reasons)
