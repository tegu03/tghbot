def parse_number(s):
    """Konversi string seperti '34.1K' menjadi float"""
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s).replace('$', '').replace(',', '').strip().upper()
    multiplier = 1
    if s.endswith('K'):
        multiplier = 1_000
        s = s[:-1]
    elif s.endswith('M'):
        multiplier = 1_000_000
        s = s[:-1]
    try:
        return float(s) * multiplier
    except ValueError:
        return 0.0

def score_token(token_info):
    score = 0
    reasons = []

    # Age (30 detik – 20 menit)
    age_seconds = parse_number(token_info.get('age_seconds', 0))
    if 30 <= age_seconds <= 1200:
        score += 1
        reasons.append('✅ Age OK')
    else:
        reasons.append('❌ Age not ideal')

    # MarketCap (< $100K)
    mc = parse_number(token_info.get('marketcap', 0))
    if 0 < mc < 100_000:
        score += 1
        reasons.append('✅ Marketcap OK')
    else:
        reasons.append('❌ Marketcap too high')

    # Liquidity (min $25K)
    lp = parse_number(token_info.get('liquidity', 0))
    if lp >= 25000:
        score += 1
        reasons.append('✅ LP OK')
    else:
        reasons.append('❌ LP too low')

    # Volume 1h (> $10K)
    vol = parse_number(token_info.get('volume', 0))
    if vol > 10000:
        score += 1
        reasons.append('✅ Volume OK')
    else:
        reasons.append('❌ Volume too low')

    # Ratio MC/LP (ideal 1.5–3)
    if lp > 0:
        ratio = mc / lp
        if 1.5 <= ratio <= 3:
            score += 1
            reasons.append('✅ MC/LP ratio OK')
        else:
            reasons.append(f'❌ MC/LP ratio off ({ratio:.2f})')
    else:
        reasons.append('❌ LP is 0, cannot compute ratio')

    # Renounced check
    renounced_raw = token_info.get('renounced', '')
    renounced = str(renounced_raw).lower()
    if 'renounced' in renounced or '🔒' in renounced or renounced == 'true':
        score += 1
        reasons.append('✅ Renounced')
    else:
        reasons.append('❌ Not renounced')

    # Whale check (> 100 SOL)
    whale_sol = parse_number(token_info.get('whale_wallet_sol', 0))
    if whale_sol >= 100:
        score += 1
        reasons.append(f'✅ Whale wallet {whale_sol} SOL')
    else:
        reasons.append('❌ No strong whale')

    # Sniper warning
    sniper_count = parse_number(token_info.get('sniper_count', 0))
    sniper_percent = parse_number(token_info.get('sniper_percent', 0))
    if sniper_count >= 20 and sniper_percent > 20:
        reasons.append('⚠️ High sniper activity detected')
        score -= 1

    return max(score, 0), reasons
