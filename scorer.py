# scorer.py

def score_token(token):
    """
    Menilai token berdasarkan kriteria:
    - MC $20K–$50K
    - LP minimal $25K (ideal $30K+)
    - Volume 1 jam > $10K
    - Rasio MC/LP ideal 2:1 (maksimal 3:1)
    - Renounced: ada kata 'Renounced' atau 🔒
    - Whale Wallet >100 SOL
    - Age: ideal 30 detik – 5 menit
    Return: (score, alasan_list)
    """
    score = 0
    reasons = []

    if token is None:
        return (score, ["❌ Token tidak valid"])

    # Marketcap
    mc = token.get("mc", 0)
    if 20_000 <= mc <= 50_000:
        score += 1
        reasons.append(f"✅ MC ideal (${mc:,})")
    else:
        reasons.append(f"❌ MC di luar range (${mc:,})")

    # LP
    lp = token.get("lp", 0)
    if lp >= 30_000:
        score += 1
        reasons.append(f"✅ LP sangat aman (${lp:,})")
    elif lp >= 25_000:
        score += 0.5
        reasons.append(f"🟡 LP cukup (${lp:,})")
    else:
        reasons.append(f"❌ LP terlalu rendah (${lp:,})")

    # Volume 1 jam terakhir
    vol = token.get("volume_1h", 0)
    if vol >= 10_000:
        score += 1
        reasons.append(f"✅ Volume tinggi (${vol:,})")
    else:
        reasons.append(f"❌ Volume rendah (${vol:,})")

    # Rasio MC/LP
    if lp > 0:
        ratio = mc / lp
        if 1.5 <= ratio <= 3:
            score += 1
            reasons.append(f"✅ Rasio MC/LP sehat ({ratio:.2f})")
        else:
            reasons.append(f"❌ Rasio tidak ideal ({ratio:.2f})")
    else:
        reasons.append("❌ LP 0, tidak bisa hitung rasio")

    # Renounced (ikon 🔒 atau teks)
    renounced = token.get("renounced", "").lower()
    if "renounced" in renounced or "🔒" in renounced:
        score += 1
        reasons.append("✅ Renounced contract")
    else:
        reasons.append("❌ Belum renounced")

    # Whale wallet
    if token.get("has_whale", False):
        score += 1
        reasons.append("✅ Ada wallet >100 SOL")
    else:
        reasons.append("❌ Tidak ada whale wallet")

    # Age (umur token dalam detik)
    age = token.get("age", 0)
    if 30 <= age <= 300:
        score += 1
        reasons.append(f"✅ Umur token ideal ({age} detik)")
    else:
        reasons.append(f"❌ Umur token kurang ideal ({age} detik)")

    return (score, reasons)
