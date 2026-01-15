#!/usr/bin/env python3
"""
🎨 Canvas Generator v2.0 (canvas_generator.py)
----------------------------------------------
Production-grade engine for generating Obsidian Canvas files.
Domain-agnostic with specific presets for Anatomy, Concepts, Workflows, etc.

Features:
- Dynamic Spacing (Collision Avoidance)
- Content-Aware Sizing
- Smart Arrow Routing (Edge-to-Edge optimization)
- Domain Presets (Anatomy, Concept Map, Linear, Tree)
- Quality Validation

Usage:
    python scripts/canvas_generator.py "path/to/note.md"
    python scripts/canvas_generator.py "path/to/data.json" --preset anatomy
"""

import sys
import os
import json
import math
import argparse
import re

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# --- Presets & Configuration ---

LAYOUT_PRESETS = {
    "anatomy": {
        "type": "radial",
        "center": {"width": 600, "height": 300, "color": "1"}, # Red
        "tier2":  {"width": 400, "height": 300, "color": "4"}, # Teal/Purple
        "tier3":  {"width": 350, "height": 250, "color": "2"}, # Orange
        "base_radii": [0, 800, 1400],
        "buffer": 100
    },
    "concept_map": {
        "type": "radial",
        "center": {"width": 500, "height": 250, "color": "3"}, # Yellow
        "tier2":  {"width": 350, "height": 250, "color": "6"}, 
        "tier3":  {"width": 300, "height": 200, "color": "5"},
        "base_radii": [0, 600, 1100],
        "buffer": 80
    },
    "default": {
        "type": "radial",
        "center": {"width": 500, "height": 300, "color": "1"},
        "tier2":  {"width": 400, "height": 250, "color": "2"},
        "tier3":  {"width": 350, "height": 200, "color": "3"},
        "base_radii": [0, 700, 1200],
        "buffer": 100
    }
}

# --- Helper Logic ---

def calculate_card_dimensions(text, tier_cfg):
    """
    Adjusts card height based on text content length.
    """
    base_w = tier_cfg['width']
    min_h = tier_cfg['height']
    
    # Estimate lines (approx 40 chars per line for standard width)
    lines = text.split('\n')
    line_count = len(lines)
    for line in lines:
        line_count += len(line) // 40
        
    # Approx 25px per line + padding
    calc_h = (line_count * 25) + 80
    final_h = min(max(calc_h, min_h), 600) # Cap at 600px height
    
    return base_w, final_h

def calculate_smart_edge_sides(source, target):
    """
    Determines optimal connection sides to minimize crossings.
    Returns (fromSide, toSide).
    """
    dx = target['x'] - source['x']
    dy = target['y'] - source['y']
    angle = math.degrees(math.atan2(dy, dx))
    
    # Normalize angle to 0-360
    if angle < 0: angle += 360
    
    # Quadrant-based logic
    # Right cone: -45 to 45 (315 to 45)
    if (angle >= 315 or angle < 45):
        return "right", "left"
    # Bottom cone: 45 to 135
    elif (angle >= 45 and angle < 135):
        return "bottom", "top"
    # Left cone: 135 to 225
    elif (angle >= 135 and angle < 225):
        return "left", "right"
    # Top cone: 225 to 315
    else:
        return "top", "bottom"

def get_radial_pos(angle_rad, radius, width, height):
    """Calculates top-left (x,y) for a node centered at polar coord."""
    cx = radius * math.cos(angle_rad)
    cy = radius * math.sin(angle_rad)
    return int(cx - width/2), int(cy - height/2)

# --- Layout Engine ---

def layout_radial_hierarchical(tree, preset_name="anatomy"):
    """
    Executes the Tiered Radial Layout algorithm.
    """
    cfg = LAYOUT_PRESETS.get(preset_name, LAYOUT_PRESETS["default"])
    nodes = []
    edges = []
    
    # --- Tier 1: Root ---
    root_w, root_h = calculate_card_dimensions(tree['text'], cfg['center'])
    root_node = {
        "id": "root",
        "x": int(-root_w/2), "y": int(-root_h/2),
        "width": root_w, "height": root_h,
        "type": "text", "text": tree['text'], "color": cfg['center']['color']
    }
    nodes.append(root_node)
    
    # --- Tier 2: Major Branches ---
    major_branches = tree.get('children', [])
    if not major_branches:
        return {"nodes": nodes, "edges": edges}
    
    # 1. Dynamic Radius Calculation (Collision Avoidance)
    # Circumference needed = NumCards * (Width + Buffer)
    t2_count = len(major_branches)
    t2_w_avg = cfg['tier2']['width']
    t2_circumference = t2_count * (t2_w_avg + cfg['buffer'])
    t2_min_radius = t2_circumference / (2 * math.pi)
    t2_radius = max(cfg['base_radii'][1], t2_min_radius)
    
    angle_step = (2 * math.pi) / t2_count
    
    for i, branch in enumerate(major_branches):
        branch_id = f"tier2_{i}"
        
        # Calculate Dimensions
        b_w, b_h = calculate_card_dimensions(branch['text'], cfg['tier2'])
        
        # Calculate Position
        angle = i * angle_step
        bx, by = get_radial_pos(angle, t2_radius, b_w, b_h)
        
        branch_node = {
            "id": branch_id, "x": bx, "y": by,
            "width": b_w, "height": b_h,
            "type": "text", "text": branch['text'], "color": cfg['tier2']['color'],
            "angle": angle # Store for child calculations
        }
        nodes.append(branch_node)
        
        # Edge: Root -> Branch
        fs, ts = calculate_smart_edge_sides(root_node, branch_node)
        edges.append({
            "id": f"e_root_{i}", "fromNode": "root", "fromSide": fs,
            "toNode": branch_id, "toSide": ts
        })
        
        # --- Tier 3: Details ---
        details = branch.get('children', [])
        if not details: continue
            
        t3_count = len(details)
        # Constrain children to the parent's angular sector
        # To avoid overlapping neighbors, we limit the arc to 80% of the parent's step
        sector_arc = angle_step * 0.8
        start_angle = angle - (sector_arc / 2)
        
        # Dynamic Radius for Tier 3
        # We need enough arc length at radius R3 to fit N cards
        t3_w_avg = cfg['tier3']['width']
        needed_arc_len = t3_count * (t3_w_avg + (cfg['buffer'] * 0.5))
        # arc_len = r * theta  => r = arc_len / theta
        t3_min_radius_sector = needed_arc_len / sector_arc
        t3_radius = max(cfg['base_radii'][2], t3_min_radius_sector)
        
        sub_step = sector_arc / max(1, t3_count - 1) if t3_count > 1 else 0
        
        for j, detail in enumerate(details):
            detail_id = f"tier3_{i}_{j}"
            
            # Sub-angle
            sub_angle = angle if t3_count == 1 else start_angle + (j * sub_step)
            
            d_w, d_h = calculate_card_dimensions(detail['text'], cfg['tier3'])
            dx, dy = get_radial_pos(sub_angle, t3_radius, d_w, d_h)
            
            detail_node = {
                "id": detail_id, "x": dx, "y": dy,
                "width": d_w, "height": d_h,
                "type": "text", "text": detail['text'], "color": cfg['tier3']['color']
            }
            nodes.append(detail_node)
            
            # Edge: Branch -> Detail
            fs, ts = calculate_smart_edge_sides(branch_node, detail_node)
            edges.append({
                "id": f"e_{i}_{j}", "fromNode": branch_id, "fromSide": fs,
                "toNode": detail_id, "toSide": ts
            })
            
    return {"nodes": nodes, "edges": edges}

# --- Parsers ---

def parse_markdown(file_path):
    """
    Parses Markdown into a hierarchical tree (H1 -> H2 -> H3).
    Ignores horizontal rules '---' and separators.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    tree = {"text": "Untitled", "children": []}
    current_h2 = None
    current_h3 = None
    buffer = []
    
    def flush_buffer():
        nonlocal buffer, current_h3, current_h2, tree
        if not buffer: return
        text = "".join(buffer).strip()
        if not text: return
        
        if current_h2 is None:
            tree["text"] += f"\n\n{text}"
        elif current_h3 is None:
            current_h2["text"] += f"\n\n{text}"
        else:
            current_h3["text"] += f"\n\n{text}"
        buffer = []

    for line in lines:
        stripped = line.strip()
        
        # Skip horizontal rules or empty separator lines
        if stripped == "---" or re.match(r'^-{3,}$', stripped) or re.match(r'^_{3,}$', stripped):
            continue

        if stripped.startswith("# "):
            flush_buffer()
            tree["text"] = stripped.replace("# ", "")
            continue
            
        if stripped.startswith("## "):
            flush_buffer()
            current_h2 = {"text": stripped.replace("## ", ""), "children": []}
            tree["children"].append(current_h2)
            current_h3 = None
            continue
            
        if stripped.startswith("### "):
            flush_buffer()
            if current_h2 is None:
                 # Recover orphan H3
                current_h2 = {"text": stripped.replace("### ", ""), "children": []}
                tree["children"].append(current_h2)
            current_h3 = {"text": stripped.replace("### ", ""), "children": []}
            current_h2["children"].append(current_h3)
            continue
            
        buffer.append(line)
        
    flush_buffer()
    return tree

def parse_structured_input(file_path):
    """
    Parses JSON or YAML input.
    Expected Schema:
    {
        "title": "...",
        "preset": "anatomy",
        "nodes": [ ... ] OR "tree": { ... }
    }
    For now, maps simple recursive structure same as MD.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        if file_path.endswith('.yaml') or file_path.endswith('.yml'):
            if HAS_YAML:
                data = yaml.safe_load(f)
            else:
                print("❌ Error: PyYAML not installed. Install with 'pip install pyyaml'")
                sys.exit(1)
        else:
            data = json.load(f)
            
    # Normalize to tree if needed (not fully implemented for custom graph yet)
    # Assuming the input is already a tree or similar structure for this version
    return data

# --- Validator ---

def validate_quality(canvas_data):
    """
    Basic quality checks.
    """
    issues = []
    nodes = canvas_data['nodes']
    
    # 1. Overlap Check (Simple Bounding Box)
    # O(N^2) - okay for small N (<100)
    for i, n1 in enumerate(nodes):
        for j, n2 in enumerate(nodes):
            if i >= j: continue
            
            # Pad with 10px to be safe
            pad = 10
            overlap = not (
                n1['x'] + n1['width'] + pad < n2['x'] - pad or
                n1['x'] - pad > n2['x'] + n2['width'] + pad or
                n1['y'] + n1['height'] + pad < n2['y'] - pad or
                n1['y'] - pad > n2['y'] + n2['height'] + pad
            )
            
            if overlap:
                issues.append(f"Overlap detected: '{n1['text'][:10]}...' and '{n2['text'][:10]}...'")
                
    return issues

# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Generate Obsidian Canvas v2.0")
    parser.add_argument("input", help="Input file (.md, .json, .yaml)")
    parser.add_argument("--preset", default="anatomy", choices=LAYOUT_PRESETS.keys(), help="Layout preset")
    args = parser.parse_args()
    
    input_path = args.input
    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        sys.exit(1)
        
    # 1. Parse
    print(f"🏗️ Parsing: {input_path}")
    if input_path.endswith(".md"):
        tree_data = parse_markdown(input_path)
    else:
        # Assuming structural input
        raw_data = parse_structured_input(input_path)
        # Support direct tree structure or wrapped
        tree_data = raw_data.get('tree', raw_data) 
        # Override preset if in file
        if 'preset' in raw_data:
            args.preset = raw_data['preset']

    # 2. Layout
    print(f"📐 Calculating Layout (Preset: {args.preset})...")
    canvas_data = layout_radial_hierarchical(tree_data, preset_name=args.preset)
    
    # 3. Validate
    issues = validate_quality(canvas_data)
    if issues:
        print("⚠️ Quality Issues Detected:")
        for issue in issues[:5]: # Limit output
            print(f"  - {issue}")
    else:
        print("✨ Quality Check Passed.")
        
    # 4. Output
    base_output = input_path.rsplit('.', 1)[0]
    output_path = base_output + ".canvas"
    
    # Auto-Versioning Logic
    if os.path.exists(output_path):
        counter = 2
        while True:
            # Check for _vX pattern to avoid Note_v2_v3.canvas
            # If base is "Clavicle", try "Clavicle_v2"
            # If base is "Clavicle_v2", we might want "Clavicle_v3" if smart, 
            # but simple appending is safer: "Clavicle_v2_v2" (maybe too messy?)
            
            # Smart versioning: Check if filename ends with _vX
            match = re.search(r'_v(\d+)$', base_output)
            if match:
                # If input was "Clavicle_v2", we start looking at v3
                version = int(match.group(1))
                root_name = base_output[:match.start()]
                candidate = f"{root_name}_v{counter}.canvas"
                # If counter is lower than existing version, bump it
                if counter <= version:
                    counter = version + 1
                    continue
            else:
                candidate = f"{base_output}_v{counter}.canvas"
                
            if not os.path.exists(candidate):
                output_path = candidate
                break
            counter += 1

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(canvas_data, f, indent=4)
        
    print(f"✅ Canvas created: {output_path}")

if __name__ == "__main__":
    main()