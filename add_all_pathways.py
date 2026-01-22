import re

file_path = "0 - Academic/🦴 Rachana Sharir/2 - Nervous System/04 - Cranial Nerves.md"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Helper function to insert pathway before Clinical section
def insert_pathway(nerve_header, pathway_block, content):
    # Find the section for the specific nerve
    # Pattern: Header -> content -> Clinical
    # We want to insert 'pathway_block' before '- **Clinical:**'
    
    # Regex to find the Clinical line specifically under the given header
    # We scan from the header until the next header or end of file
    header_pattern = re.escape(nerve_header)
    
    # 1. Split content by the header to find the chunk
    parts = re.split(f"({header_pattern})", content, maxsplit=1)
    
    if len(parts) < 3:
        print(f"Warning: Header {nerve_header} not found.")
        return content
        
    pre_header = parts[0]
    header = parts[1]
    post_header = parts[2]
    
    # 2. In post_header, find the next "## " to limit scope
    next_section_split = re.split(r"(^## .*?)", post_header, maxsplit=1, flags=re.MULTILINE)
    
    nerve_content = next_section_split[0]
    rest_of_file = "".join(next_section_split[1:]) if len(next_section_split) > 1 else ""
    
    # 3. Insert Pathway inside nerve_content before "Clinical:"
    # Use simple string replacement on the first occurrence of Clinical in this block
    if "- **Clinical:**" in nerve_content:
        nerve_content = nerve_content.replace("- **Clinical:**", f"{pathway_block}
- **Clinical:**", 1)
    else:
        # If no clinical section, append to end of nerve content
        nerve_content += f"
{pathway_block}
"
        
    return pre_header + header + nerve_content + rest_of_file

# Definitions of Pathways

path_3 = """
- **Pathway:**
```mermaid
graph LR
    A[Midbrain (Ventral)] --> B(Lat. Wall of Cavernous Sinus)
    B --> C(Sup. Orbital Fissure)
    C --> D[Orbit]
```
"""

path_4 = """
- **Pathway:**
```mermaid
graph LR
    A[Midbrain (Dorsal)] -->|Decussation| B(Lat. Wall of Cavernous Sinus)
    B --> C(Sup. Orbital Fissure)
    C --> D[Sup. Oblique Muscle]
```
"""

path_5 = """
- **Pathway:**
```mermaid
graph TD
    A[Pons] --> B{Trigeminal Ganglion}
    B -->|V1| C(Sup. Orbital Fissure)
    B -->|V2| D(Foramen Rotundum)
    B -->|V3| E(Foramen Ovale)
```
"""

path_6 = """
- **Pathway:**
```mermaid
graph LR
    A[Pons] --> B(Dorello's Canal)
    B --> C(Inside Cavernous Sinus)
    C --> D(Sup. Orbital Fissure)
    D --> E[Lat. Rectus Muscle]
```
"""

path_8 = """
- **Pathway:**
```mermaid
graph LR
    A[Pons] --> B(Int. Acoustic Meatus)
    B --> C[Inner Ear]
```
"""

path_9 = """
- **Pathway:**
```mermaid
graph LR
    A[Medulla] --> B(Jugular Foramen)
    B --> C[Pharynx / Tongue]
```
"""

path_10 = """
- **Pathway:**
```mermaid
graph TD
    A[Medulla] --> B(Jugular Foramen)
    B --> C[Carotid Sheath]
    C --> D[Thorax / Abdomen]
```
"""

path_11 = """
- **Pathway:**
```mermaid
graph LR
    A[Medulla / Spine] --> B(Jugular Foramen)
    B --> C[SCM / Trapezius]
```
"""

path_12 = """
- **Pathway:**
```mermaid
graph LR
    A[Medulla] --> B(Hypoglossal Canal)
    B --> C[Tongue Muscles]
```
"""

# Execute insertions
content = insert_pathway("## 👁️ III. Oculomotor Nerve", path_3, content)
content = insert_pathway("## 👁️ IV. Trochlear Nerve", path_4, content)
content = insert_pathway("## 🦷 V. Trigeminal Nerve", path_5, content)
content = insert_pathway("## 👁️ VI. Abducens Nerve", path_6, content)
content = insert_pathway("## 👂 VIII. Vestibulocochlear Nerve", path_8, content)
content = insert_pathway("## 👅 IX. Glossopharyngeal Nerve", path_9, content)
content = insert_pathway("## 🫀 X. Vagus Nerve", path_10, content)
content = insert_pathway("## 💪 XI. Accessory Nerve", path_11, content)
content = insert_pathway("## 👅 XII. Hypoglossal Nerve", path_12, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("All pathways updated.")
