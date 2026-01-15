# ⚙️ System Specifications v1.3
> "The technical toolbox and user manual for The Construct."
> **Merged:** Capabilities + Manual + Connectivity Protocol.

---

## 🛠️ 1. Permanent Automation Suite


**Dependencies:** `python`, `ffmpeg`, `yt-dlp`, `trafilatura`, `youtube-transcript-api`.

---

## ⚙️ 2. The Connectivity Logic (The Sync)
*How data flows into [[0 - 🌌 Central Command]].*

### A. Friction Radar
- Scans last 3 days of Journal for `#friction` tags.
- Displays top 5 recent blocks on Dashboard.

### B. Heads-Up Display (HUD)
- Regex match for Today's To-Do list (`- [ ]`) in the Journal.
- Mirrors active tactical queue to Central Command.

### C. Toolbox Sync
- Extracts the "Automation Suite" table from this file and injects it into Central Command.

---

## 🔗 2.5 Hub & Spoke Protocol (Habit Tracking)
**Rule:** The System is "Self-Healing" and "Auto-Connecting."
1.  **The Spoke (Ritual File):** Every recurring habit MUST have a dedicated file in `1 - 🧠 The Construct/⚔️ Battle Rituals/`.
    - **Frontmatter Requirement:**
      ```yaml
      Protocol: "Exact Name Matches Journal Task"
      Status: "ACTIVE"  <-- Trigger for Central Command
      Type: "Category"
      ```
2.  **The Hub (Central Command):** The dashboard auto-discovers any file with `Status: ACTIVE`. No manual table editing allowed.
3.  **The Log (Journal):** Daily Tasks MUST match the `Protocol` name (or File Name) to be counted.
    - *Format:* `- [x] **Protocol Name:** Details...`
    - *Emoji Safety:* The Tracker ignores emojis, but text must match.

---

## ⚖️ 3. Protocol: Script vs. Prompt Logic
| Feature | Use **SCRIPT** (Code) | Use **PROMPT** (AI) |
| :--- | :--- | :--- |
| **Data Fetching** | ✅ **YES.** (Downloads, OCR, Scraping). | ❌ NO. |
| **Analysis** | ❌ NO. Code is rigid. | ✅ **YES.** (Summarizing, Strategy). |
| **Formatting** | ⚠️ **CONDITIONAL.** Simple = Code. | ✅ **YES.** "Make this beautiful". |
| **Math/Logic** | ✅ **YES.** (Timestamps, counts). | ❌ NO. AI hallucinates math. |

---

## 🧹 4. Maintenance Protocols
1. **The Table Rule:** ALWAYS use `[[Link\|Alias]]` in Markdown tables.
2. **Renaming:** Use **Emoji + Space** standard for all files.
3. **Hygiene:** Delete temporary repair scripts and reports after use.
4. **Integration:** New blueprints MUST scan AI Core/Contexts for integration points.

---

## 🚀 5. Comprehensive System Features & Capabilities

### 🧠 A. Core Intelligence (The AI Core)
*The fundamental operating system and psychological foundation.*
- **[[🤖 Prime Directive|🤖 Prime Directive]]:** Central kernel and mission control; manages the Ignition Sequence and system-wide roadmaps.
- **[[🧬 Identity Matrix|🧬 Identity Matrix]]:** Detailed psychological blueprint; tracks the "Architect's" winning moves, core narrative, and first-principles learning style.
- **[[⚙️ System Specifications|⚙️ System Specifications]]:** The technical manual and toolbox; manages script logic and connectivity protocols.
- **[[📊 System Analytics & Logs|📊 System Analytics & Logs]]:** Phase 3 intelligence; tracks Pearson correlation and reliability metrics for system performance.
- **[[0 - 🌌 Central Command|0 - 🌌 Central Command]]:** The Heads-Up Display (HUD); automatically updates with Dataview to show active friction, stream status, and daily focus.

### 🎭 B. Specialized Workforce (The Contexts)
*Eight specialized AI agents with dedicated directives and persistent memories.*
- **🏗️ Architect:** System administration, structure management, and "Objective Mirror" analysis.
- **🎓 Academic Tutor:** BAMS syllabus mastery, Sanskrit tutoring, and exam-prep engineering.
- **🧘 Sage:** Deep psychological pattern matching, meditation analysis, and emotional grounding.
- **🔬 Scholar:** Non-academic deep dives, philosophical connections, and immersive learning.
- **🎭 Simulator:** Social anxiety sandbox; provides roleplay training against 6 levels of social friction.
- **📚 Librarian:** Vault hygiene, file organization, tagging audits, and link integrity.
- **⚙️ Automation Engineer:** Script maintenance, technical error handling, and data pipeline management.
- **🎨 Muse:** Creative expansion, brainstorming, and "Yes, and..." flow-state guidance.

### ⚙️ C. Automation Engine (The Scripts)
*Functional tools for data extraction and system maintenance.*
- **`morning_cron.py`:** Automated daily rollover; generates journals, commits to local git, and pushes to GitHub.
- **`yt_notes.py`:** Fetches full raw transcripts from YouTube URLs for deep analysis.
- **`web_notes.py`:** Extracts clean article text from any web URL.
- **`pdf-notes.sh`:** Document intelligence; extracts text and insights from PDFs.
- **`camera_scan.sh`:** Quick-capture OCR; moves physical text into the `Chaos Stream`.
- **`anki_generator.py`:** Injects notes directly into the Anki ecosystem for spaced repetition.
- **`system_sync.py`:** Scans for broken links and updates the Central Command HUD.
- **`tag_predictor.py`:** Suggests relevant tags based on vault history and semantic frequency.
- **`vault_auditor.py`:** Proactively finds orphans and broken links to maintain graph hygiene.
- **`analytics_engine.py`:** Statistical analysis of habits and thought patterns.
- **`health_check.py`:** Phase 4: Audits all system scripts for presence and functionality.
- **`publish.py`:** Phase 4: Converts Obsidian-specific syntax to clean Markdown for external sharing.
- **`sync_frequent.sh`:** `vsync` | Phase 4: Redundant git-syncing for fault tolerance (every 4 hours).
- **`dispatcher.py`:** Phase 4: Meta-context router for identifying the correct agent for a task.
- **`vault_graph.py`:** Phase 4: Semantic intelligence for suggesting backlinks and clusters.
| `memory_cleanup.py` | `python scripts/memory_cleanup.py` | **Phase 4 Hygiene.** Prunes outdated memories from agent contexts. |
| `md_to_canvas.py` | `python scripts/md_to_canvas.py [file]` | **Visualizer.** Converts Markdown notes into Canvas maps. |

### 📐 D. Knowledge Architecture (Blueprints & Standards)
*Structured frameworks for information processing.*
- **[[🔥 Protocol True Learning|🔥 Protocol True Learning]]:** Universal strategy for deep acquisition (Deconstruct -> Select -> Sequence -> Feynman).
- **[[🧠 Deep Dive Project Template|🧠 Deep Dive Project Template]]:** Standardized framework for deep research, including the **🎭 Archetype Template Section**.
- **[[📚 Scholar Note Standard|📚 Scholar Note Standard]]:** Rules for high-quality note output (Frameworks, Anchors, Tensions).
- **[[🎓 Master Study Template|🎓 Master Study Template]]:** NCISM-aligned structure for BAMS academic notes.
- **[[🏷️ Tagging Standard|🏷️ Tagging Standard]]:** Mandatory nomenclature for vault categorization.

### Canvas Generator v2.0
**Script:** `canvas_generator.py`
**Input:** Markdown (.md) or Structure (.json/.yaml)
**Output:** Obsidian .canvas file
**Features:**
- Layout presets (anatomy, concept_map, default)
- Auto-collision detection (Dynamic Spacing)
- Content-aware card sizing
- Smart Arrow optimization (Edge-to-Edge)
- Quality validation

**Usage:**
```bash
python scripts/canvas_generator.py "note.md" --preset anatomy
```

### ⚡ E. Autonomous Protocols (The "Quiet" Features)
*Processes that execute automatically via the Ignition Sequence.*
- **Ignition Sequence v2.1:** Forces a scan of Core Nodes and Streams at every session start.
- **Autonomous Memory Sync:** Automatically updates `Agent Memory` sections with new insights and preferences.
- **Append-First Rule:** Strict directive to prioritize data growth over data replacement.
- **Friction Radar:** Scans the last 3 days of logs to identify and display mental/social blocks on the dashboard.
- **The Pattern Alarm:** Visual warning if negative thought loops persist for 3+ days.
- **The Objective Mirror:** Direct, data-driven counter-analysis to subjective self-judgment in the journal.
- **Beautiful Formatting Standard:** Mandates Callouts, thematic dividers, and Emoji Nomenclature for all system-generated files.
- **Phase 4: Meta-Context Routing:** Automatically identifies and routes complex tasks to the correct specialized agent memory.
- **Phase 4: Semantic Inter-Note Intelligence:** Background analysis of tag and keyword relationships to suggest hidden links and concept clusters.
- **Phase 4: Context Hygiene & Pruning:** Automated archival of agent memories older than 30 days to prevent "context drift" and maintain high-speed processing.
- **Phase 4: Fault Tolerance (Audit & Redundancy):** Automated daily script health checks and frequent redundant syncing via the `vsync` alias.
- **Phase 4: External Export Protocol:** Strips Obsidian-specific complexity from notes to produce clean, shareable Markdown.

