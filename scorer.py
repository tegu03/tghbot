def score_token(token_info):
    score = 0
    reasons = []

    # Age (60 detik – 600 detik / 1-10 menit)
    age_seconds = token_info.get('age_seconds', 0)
    if 60 <= age_seconds <= 600:
        score += 1
        reasons.append('✅ Age OK')
    else:
        reasons.append('❌ Age not ideal')

    # MarketCap ($15K – $75K)
    mc = token_info.get('marketcap', 0)
    if 15000 <= mc <= 75000:
        score += 1
        reasons.append('✅ Marketcap OK')
    else:
        reasons.append(f'❌ Marketcap not ideal (${mc})')

    # Liquidity (≥ $30K)
    lp = token_info.get('liquidity', 0)
    if lp >= 30000:
        score += 1
        reasons.append('✅ Liquidity OK')
    else:
        reasons.append(f'❌ Liquidity too low (${lp})')

    # Volume 1h (≥ $20K)
    vol = token_info.get('volume', 0)
    if vol >= 20000:
        score += 1
        reasons.append('✅ Volume OK')
    else:
        reasons.append(f'❌ Volume too low (${vol})')

    # MC/LP Ratio (ideal: 1.8 – 2.8)
    if lp > 0:
        ratio = mc / lp
        if 1.8 <= ratio <= 2.8:
            score += 1
            reasons.append(f'✅ MC/LP ratio OK ({ratio:.2f})')
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

    # Whale check (≥ 150 SOL)
    whale_sol = token_info.get('whale_wallet_sol', 0)
    if whale_sol >= 150:
        score += 1
        reasons.append(f'✅ Whale wallet {whale_sol} SOL')
    else:
        reasons.append('❌ No strong whale')

    # Sniper warning (skip jika terlalu banyak sniper)
    sniper_count = token_info.get('sniper_count', 0)
    sniper_percent = token_info.get('sniper_percent', 0)

    if sniper_count >= 20 and sniper_percent > 20:
        score -= 1
        reasons.append(f'⚠️ High sniper activity ({sniper_count} snipers / {sniper_percent:.1f}%)')

    return max(score, 0), reasons
