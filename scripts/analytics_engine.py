#!/usr/bin/env python3
"""
📊 Vinci Analytics Engine v2.2 (Statistical Update)
------------------------------
Added: Pearson Correlation Coefficients for deep pattern recognition.
"""

import os
import re
import datetime
import math
from collections import defaultdict

VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
SAGA_DIR = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/📜 The Saga")
DISPATCH_LOG = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/🤖 AI Core/📋 Dispatch Log.md")
OUTPUT_FILE = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/🤖 AI Core/📊 Analytics Dashboard.md")

def calculate_correlation(x, y):
    """Calculates Pearson Correlation Coefficient (r)."""
    n = len(x)
    if n != len(y) or n < 2: return 0
    
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_sq = sum(i*i for i in x)
    sum_y_sq = sum(i*i for i in y)
    sum_xy = sum(i*j for i, j in zip(x, y))
    
    numerator = (n * sum_xy) - (sum_x * sum_y)
    denominator = math.sqrt((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))
    
    if denominator == 0: return 0
    return numerator / denominator

def parse_dispatch_log():
    if not os.path.exists(DISPATCH_LOG): return None
    with open(DISPATCH_LOG, 'r', encoding='utf-8') as f: content = f.read()
    rows = content.split('\n')
    total, success = 0, 0
    for row in rows:
        if "|" in row and "Timestamp" not in row and ":---" not in row:
            total += 1
            if "✅" in row: success += 1
    if total == 0: return None
    return (success / total) * 100

def parse_journals():
    data = []
    tag_trends = defaultdict(lambda: defaultdict(int))
    
    re_energy = re.compile(r"\**Energy:\**.*?(\d+)(?:/10)?", re.IGNORECASE)
    re_mood = re.compile(r"\**Mood:\**.*?(\d+)(?:/10)?", re.IGNORECASE)
    re_tag = re.compile(r"#([\w/-]+)")
    
    if not os.path.exists(SAGA_DIR): return [], {}

    for filename in os.listdir(SAGA_DIR):
        if not filename.endswith(".md") or "Time Capsule" in filename: continue
        filepath = os.path.join(SAGA_DIR, filename)
        year_month = filename.split("-")[:2]
        if len(year_month) < 2: continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
        except: continue
            
        days = content.split("## 📅")
        for day_block in days[1:]:
            header_line = day_block.split('\n')[0]
            day_num_match = re.search(r"(\d+)", header_line)
            if not day_num_match: continue
            
            day_num = day_num_match.group(1)
            date_str = f"{year_month[0]}-{year_month[1]}-{day_num.zfill(2)}"
            
            energy = int(re_energy.search(day_block).group(1)) if re_energy.search(day_block) else None
            mood = int(re_mood.search(day_block).group(1)) if re_mood.search(day_block) else None
            
            all_tags = re_tag.findall(day_block)
            friction_count = len([t for t in all_tags if "friction" in t])
            win_count = len([t for t in all_tags if "win" in t])
            
            for t in all_tags: tag_trends[date_str][t] += 1
            
            data.append({
                'date': date_str, 'energy': energy, 'mood': mood, 
                'friction': friction_count, 'wins': win_count
            })
            
    data.sort(key=lambda x: x['date'], reverse=True)
    return data, tag_trends

def generate_dashboard(data, tag_trends, reliability):
    total_days = len(data)
    if total_days == 0: return "# 📊 Analytics Dashboard\n\n> No data found."
        
    energy_vals = [d['energy'] for d in data if d['energy'] is not None]
    mood_vals = [d['mood'] for d in data if d['mood'] is not None]
    avg_energy = sum(energy_vals)/len(energy_vals) if energy_vals else 0
    avg_mood = sum(mood_vals)/len(mood_vals) if mood_vals else 0
    
    out = [f"# 📊 Analytics Dashboard", f"> **Sync:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    out.append("## 📈 Vital Signs")
    out.append("| Metric | Average | Status |")
    out.append("| :--- | :--- | :--- |")
    out.append(f"| **⚡ Energy** | **{avg_energy:.1f}**/10 | {'🟢 High' if avg_energy > 7 else '🟡 Moderate'} |")
    out.append(f"| **🧠 Mood** | **{avg_mood:.1f}**/10 | {'🟢 Stable' if avg_mood > 6 else '🔴 Low'} |")
    if reliability is not None:
        rel_status = '🟢 Healthy' if reliability > 90 else '🟡 Degraded'
        out.append(f"| **⚙️ Reliability** | **{reliability:.1f}%** | {rel_status} |")
    out.append("")

    out.append("## 🗺️ Pattern Map")
    out.append("| Tag | Frequency | Context |")
    out.append("| :--- | :--- | :--- |")
    global_tags = defaultdict(int)
    for date in sorted(tag_trends.keys(), reverse=True)[:7]:
        for tag, count in tag_trends[date].items():
            if tag not in ["task", "insight", "question"]: global_tags[tag] += count
    for tag, count in sorted(global_tags.items(), key=lambda x: x[1], reverse=True)[:7]:
        ctx = "🛑 Friction" if "friction" in tag else "🏆 Win" if "win" in tag else "🧩 Other"
        out.append(f"| `#{tag}` | {count} | {ctx} |")
    out.append("")

    out.append("## 🔬 Correlation Engine")
    # Prepare datasets for correlation
    valid_ef = [(d['energy'], d['friction']) for d in data if d['energy'] is not None]
    valid_mw = [(d['mood'], d['wins']) for d in data if d['mood'] is not None]

    if len(valid_ef) < 3:
        out.append("> [!warning] Insufficient Data (Need 3+ entries with Energy data).")
    else:
        # Energy vs Friction
        corr_ef = calculate_correlation([x[0] for x in valid_ef], [x[1] for x in valid_ef])
        strength_ef = "Strong" if abs(corr_ef) > 0.5 else "Weak"
        rel_ef = "Inverse" if corr_ef < 0 else "Direct"
        out.append(f"- **Energy ↔ Friction:** `r={corr_ef:.2f}` ({strength_ef} {rel_ef}).")
        if corr_ef < -0.3: out.append("  - *Insight:* Higher energy significantly reduces friction.")

        # Mood vs Wins
        corr_mw = calculate_correlation([x[0] for x in valid_mw], [x[1] for x in valid_mw])
        strength_mw = "Strong" if abs(corr_mw) > 0.5 else "Weak"
        rel_mw = "Inverse" if corr_mw < 0 else "Direct"
        out.append(f"- **Mood ↔ Wins:** `r={corr_mw:.2f}` ({strength_mw} {rel_mw}).")
    out.append("")

    out.append("## 📅 Timeline")
    out.append("| Date | Energy | Mood | Wins | Friction |")
    out.append("| :--- | :--- | :--- | :--- | :--- |")
    for d in data[:7]:
        out.append(f"| {d['date']} | {d['energy'] or '-'} | {d['mood'] or '-'} | {d['wins']} | {d['friction']} |")

    return "\n".join(out)

def main():
    data, trends = parse_journals()
    reliability = parse_dispatch_log()
    report = generate_dashboard(data, trends, reliability)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print("✅ Analytics Dashboard Updated.")

if __name__ == "__main__":
    main()