# utils.py

import json
import os
import re

def load_json(filename, default=None):
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        return default

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def parse_number(s):
    s = s.replace(',', '').strip().upper()
    if s.endswith('K'):
        return float(s[:-1]) * 1_000
    elif s.endswith('M'):
        return float(s[:-1]) * 1_000_000
    elif s.endswith('B'):
        return float(s[:-1]) * 1_000_000_000
    else:
        return float(s)

def parse_age(age_str):
    age_str = age_str.lower()
    total_seconds = 0
    time_units = {
        'mo': 2592000,
        'w': 604800,
        'd': 86400,
        'h': 3600,
        'm': 60,
        's': 1
    }

    matches = re.findall(r'(\d+)\s*(mo|w|d|h|m|s)', age_str)
    for value, unit in matches:
        total_seconds += int(value) * time_units.get(unit, 0)

    return total_seconds
