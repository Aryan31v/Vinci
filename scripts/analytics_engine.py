#!/usr/bin/env python3
import os, re, datetime, math
from collections import defaultdict

VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
SAGA_DIR = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/📜 The Saga")
COMPENDIUM_FILE = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/🤖 AI Core/01 - System Core Compendium.md")

def calculate_correlation(x, y):
    n = len(x)
    if n != len(y) or n < 2: return 0
    sum_x, sum_y = sum(x), sum(y)
    sum_x_sq = sum(i*i for i in x)
    sum_y_sq = sum(i*i for i in y)
    sum_xy = sum(i*j for i, j in zip(x, y))
    num = (n * sum_xy) - (sum_x * sum_y)
    den = math.sqrt((n * sum_x_sq - sum_x**2) * (n * sum_y_sq - sum_y**2))
    return num / den if den != 0 else 0

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
        with open(filepath, "r", encoding="utf-8") as f: content = f.read()
        days = content.split("## 📅")
        for day_block in days[1:]:
            header_line = day_block.split("\n")[0]
            day_num_match = re.search(r"(\d+)", header_line)
            if not day_num_match: continue
            date_str = f"{year_month[0]}-{year_month[1]}-{day_num_match.group(1).zfill(2)}"
            e_m, m_m = re_energy.search(day_block), re_mood.search(day_block)
            energy = int(e_m.group(1)) if e_m else None
            mood = int(m_m.group(1)) if m_m else None
            all_tags = re_tag.findall(day_block)
            data.append({"date": date_str, "energy": energy, "mood": mood, "friction": len([t for t in all_tags if "friction" in t]), "wins": len([t for t in all_tags if "win" in t])})
            for t in all_tags: tag_trends[date_str][t] += 1
    data.sort(key=lambda x: x["date"], reverse=True)
    return data, tag_trends

def generate_report(data, tag_trends):
    ev = [d["energy"] for d in data if d["energy"] is not None]
    mv = [d["mood"] for d in data if d["mood"] is not None]
    ae, am = sum(ev)/len(ev) if ev else 0, sum(mv)/len(mv) if mv else 0
    P = chr(124)
    out = ["## 📈 Vital Signs & Pattern Map", f"{P} Metric {P} Average {P} Status {P}", f"{P} :--- {P} :--- {P} :--- {P}"]
    out.append(f"{P} **⚡ Energy** {P} **{ae:.1f}**/10 {P} {'🟢 High' if ae > 7 else '🟡 Moderate'} {P}")
    out.append(f"{P} **🧠 Mood** {P} **{am:.1f}**/10 {P} {'🟢 Stable' if am > 6 else '🔴 Low'} {P}\n")
    out.append(f"{P} Tag {P} Frequency {P} Context {P}")
    out.append(f"{P} :--- {P} :--- {P} :--- {P}")
    global_tags = defaultdict(int)
    for date in sorted(tag_trends.keys(), reverse=True)[:7]:
        for tag, count in tag_trends[date].items():
            if tag not in ["task", "insight", "question", "priority"]: global_tags[tag] += count
    for tag, count in sorted(global_tags.items(), key=lambda x: x[1], reverse=True)[:7]:
        ctx = "🛑 Friction" if "friction" in tag else "🏆 Win" if "win" in tag else "🧩 Other"
        out.append(f"{P} `#{tag}` {P} {count} {P} {ctx} {P}")
    out.append("\n## 🔬 Correlation Engine")
    vef = [(d["energy"], d["friction"]) for d in data if d["energy"] is not None]
    vmw = [(d["mood"], d["wins"]) for d in data if d["mood"] is not None]
    if len(vef) < 3: out.append("> [!warning] Insufficient Data.")
    else:
        out.append(f"- **Energy ↔ Friction:** `r={calculate_correlation([x[0] for x in vef], [x[1] for x in vef]):.2f}`")
        out.append(f"- **Mood ↔ Wins:** `r={calculate_correlation([x[0] for x in vmw], [x[1] for x in vmw]):.2f}`")
    out.append(f"\n## 📅 Performance Timeline\n{P} Date {P} Wins {P} Friction {P} Mood {P} Energy {P}\n{P} :--- {P} :--- {P} :--- {P} :--- {P} :--- {P}")
    for d in data[:7]: out.append(f"{P} {d['date']} {P} {d['wins']} {P} {d['friction']} {P} {d['mood'] or '-'} {P} {d['energy'] or '-'} {P}")
    out.append("\n## 📋 Dispatch Log (AI Actions)")
    return "\n".join(out)

def update_compendium(report):
    if not os.path.exists(COMPENDIUM_FILE): return
    with open(COMPENDIUM_FILE, "r", encoding="utf-8") as f: content = f.read()
    parts = re.split(r"^# 📊 Section 4: Analytics & Logs", content, flags=re.MULTILINE)
    if len(parts) < 2: return
    # Find start of Dispatch Log table to preserve it
    dispatch_header = "## 📋 Dispatch Log (AI Actions)"
    if dispatch_header in parts[1]:
        log_content = dispatch_header + parts[1].split(dispatch_header)[1]
    else:
        log_content = dispatch_header + "\n(No log found)"
    new_content = parts[0] + "# 📊 Section 4: Analytics & Logs\n" + f"> *Last Sync: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n" + report.split(dispatch_header)[0] + log_content
    with open(COMPENDIUM_FILE, "w", encoding="utf-8") as f: f.write(new_content)
    print("✅ Compendium Updated.")

def main():
    data, trends = parse_journals()
    report = generate_report(data, trends)
    update_compendium(report)

if __name__ == "__main__": main()
