# scorer.py

def score_token(token_info):
    score = 0
    reasons = []

    # Age (30 detik – 20 menit)
    age_seconds = token_info.get('age_seconds', 0)
    if 30 <= age_seconds <= 1200:
        score += 1
        reasons.append('✅ Age OK')
    else:
        reasons.append('❌ Age not ideal')

    # MarketCap (< $100K)
    mc = token_info.get('marketcap', 0)
    if 0 < mc < 100_000:
        score += 1
        reasons.append('✅ Marketcap OK')
    else:
        reasons.append('❌ Marketcap too high')

    # Liquidity (min $25K)
    lp = token_info.get('liquidity', 0)
    if lp >= 25000:
        score += 1
        reasons.append('✅ LP OK')
    else:
        reasons.append('❌ LP too low')

    # Volume 1h (> $10K)
    vol = token_info.get('volume_1h', 0)
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
    whale_sol = token_info.get('whale_wallet', 0)
    if whale_sol >= 100:
        score += 1
        reasons.append(f'✅ Whale wallet {whale_sol} SOL')
    else:
        reasons.append('❌ No strong whale')

    # Sniper warning
    if token_info.get('sniper_count', 0) >= 20 and token_info.get('sniper_percent', 0) > 20:
        reasons.append('⚠️ High sniper activity detected')
        score -= 1

    return max(score, 0), reasons
