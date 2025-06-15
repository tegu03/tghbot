# scorer.py

def score_token(token_info):
    score = 0
    reasons = []

    # 1. Age (30 detik – 20 menit)
    age_seconds = token_info.get('age', 0)
    if 30 <= age_seconds <= 1200:
        score += 1
        reasons.append('✅ Age OK')
    else:
        reasons.append('❌ Age not ideal')

    # 2. MarketCap ($20K–$50K)
    mc = token_info.get('mc', 0)
    if 20000 <= mc <= 50000:
        score += 1
        reasons.append('✅ MC OK')
    else:
        reasons.append('❌ MC not in range')

    # 3. Liquidity (min $25K)
    lp = token_info.get('lp', 0)
    if lp >= 25000:
        score += 1
        reasons.append('✅ LP OK')
    else:
        reasons.append('❌ LP too low')

    # 4. Volume 1h (> $10K)
    volume = token_info.get('volume', 0)
    if volume > 10000:
        score += 1
        reasons.append('✅ Volume OK')
    else:
        reasons.append('❌ Volume too low')

    # 5. Ratio MC/LP (ideal 2:1, toleransi 1.5–3)
    if lp > 0:
        ratio = mc / lp
        if 1.5 <= ratio <= 3:
            score += 1
            reasons.append('✅ MC/LP ratio OK')
        else:
            reasons.append(f'❌ MC/LP ratio off ({ratio:.2f})')
    else:
        reasons.append('❌ LP is 0, cannot compute ratio')

    # 6. Renounced
    if token_info.get('renounced', False):
        score += 1
        reasons.append('✅ Renounced')
    else:
        reasons.append('❌ Not renounced')

    # 7. Whale check > 100 SOL
    whale = token_info.get('wallet', 0)
    if whale >= 100:
        score += 1
        reasons.append(f'✅ Whale wallet: {whale} SOL')
    else:
        reasons.append('❌ No strong whale')

    # ❗ Bonus filter: Hindari sniper mencurigakan
    if token_info.get('sniper_count', 0) >= 20 and token_info.get('sniper_percent', 0) > 20:
        reasons.append('⚠️ Warning: High sniper presence')
        score -= 1  # penalti

    return max(score, 0), "\n".join(reasons)
