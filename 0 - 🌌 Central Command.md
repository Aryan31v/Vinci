# 🌌 Central Command
> *"The Control Center of The Construct."*

---

## 🏗️ System Status
```dataview
TABLE without id file.link as "Agent/Context", file.mtime as "Last Active"
FROM "1 - 🧠 The Construct/🧠 Contexts"
SORT file.name ASC
```

## 🚨 Active Friction Points (Last 3 Days)
> ✅ No active friction points.

---

## 🔄 Core Protocols & Habit Tracker
```dataviewjs
// 1. Auto-Discover Active Rituals
const protocols = dv.pages('"1 - 🧠 The Construct/⚔️ Battle Rituals"')
    .where(p => p.Status === "ACTIVE" && p.file.name != "Index")
    .sort(p => p.Type);

// 2. Fetch Tasks (Journal + Ritual Files)
const journal = dv.page('1 - 🧠 The Construct/📜 The Saga/2026-01-January.md');
const journalTasks = journal ? journal.file.tasks.where(t => t.completed) : [];

// 3. Build the Table
dv.table(
    ["Protocol", "Type", "Current Streak", "Progress", "Status"],
    protocols.map(p => {
        // Source A: Journal Matches (Strip Emojis for better matching)
        // Regex removes non-word chars except spaces, allowing text-only matching
        const cleanName = p.file.name.replace(/[^\w\s]/g, "").trim();
        const cleanProtocol = (p.Protocol || "").replace(/[^\w\s]/g, "").trim();
        const matchTerms = [cleanName, cleanProtocol].filter(t => t.length > 0);

        const journalCount = journalTasks.filter(t => 
            matchTerms.some(term => t.text.toLowerCase().includes(term.toLowerCase()))
        ).length;

        // Source B: Internal Log (e.g. Bridge Protocol)
        const fileTasks = p.file.tasks.where(t => t.completed).length;
        
        const totalCount = journalCount + fileTasks;
        
        // Formatting
        const progress = p.Target ? `Day ${totalCount}/${p.Target}` : `${totalCount} Total`;
        const streakEmoji = totalCount > 0 ? `🔥 ${totalCount}` : "—";
        
        return [
            p.file.link,
            p.Type,
            streakEmoji,
            progress,
            "`ACTIVE`"
        ];
    })
);
```

## 📅 Daily Focus (Today)
- [ ] **[05:30 PM] Shiva Sadhana:** Day 7/11 (108x). **MANDATORY.**
- [ ] **Journaling:** Complete all pending journal entries for today. #priority
- [ ] **Physics Deep Dive:** Apply Spacetime Budget concepts to daily energy management.

## 📂 Vault Map
- **The Saga:** [[1 - 🧠 The Construct/📜 The Saga/2026-01-January|Current Journal]] | [[1 - 🧠 The Construct/📜 The Saga/💤 Dream Journal|💤 Dream Journal]] | [[1 - 🧠 The Construct/📊 Social Media Tracker|📊 Social Media Tracker]]
- **The Brain:** [[1 - 🧠 The Construct/🤖 AI Core/⚙️ System Specifications|⚙️ System Specifications]] | [[1 - 🧠 The Construct/🤖 AI Core/📊 Analytics Dashboard|📊 Analytics Dashboard]] | [[1 - 🧠 The Construct/🤖 AI Core/📊 System Analytics & Logs|📊 System Analytics & Logs]] | [[1 - 🧠 The Construct/🤖 AI Core/🤖 Prime Directive|🤖 Prime Directive]] | [[1 - 🧠 The Construct/🤖 AI Core/🧬 Identity Matrix|🧬 Identity Matrix]] | [[1 - 🧠 The Construct/🎭 Hall of Mirrors/Guide|🎭 Hall of Mirrors]]
- **Contexts:** [[1 - 🧠 The Construct/🧠 Contexts/⚙️ Context Automation Engineer|⚙️ Context Automation Engineer]] | [[1 - 🧠 The Construct/🧠 Contexts/🎓 Context Academic Tutor|🎓 Context Academic Tutor]] | [[1 - 🧠 The Construct/🧠 Contexts/🎨 Context Muse|🎨 Context Muse]] | [[1 - 🧠 The Construct/🧠 Contexts/🎭 Context Simulator|🎭 Context Simulator]] | [[1 - 🧠 The Construct/🧠 Contexts/🏗️ Context Architect|🏗️ Context Architect]] | [[1 - 🧠 The Construct/🧠 Contexts/📚 Context Librarian|📚 Context Librarian]] | [[1 - 🧠 The Construct/🧠 Contexts/🔬 Context Scholar|🔬 Context Scholar]] | [[1 - 🧠 The Construct/🧠 Contexts/🧘 Context Sage|🧘 Context Sage]]
- **Blueprints:** [[The Blueprints/🎓 Master Study Template|🎓 Master Study Template]] | [[The Blueprints/🏷️ Tagging Standard|🏷️ Tagging Standard]] | [[The Blueprints/📚 Scholar Note Standard|📚 Scholar Note Standard]] | [[The Blueprints/🔥 Protocol True Learning|🔥 Protocol True Learning]] | [[The Blueprints/🧠 Deep Dive Project Template|🧠 Deep Dive Project Template]]
- **The Academy:** [[0 - Academic/🎓 BAMS Master Dashboard|🎓 BAMS Master Dashboard]]

---

> [!example]- 🛠️ System Toolbox
> 
> | Script | Command | Function |
> | :--- | :--- | :--- |
> | `morning_cron.py` | `morning` | **Daily Rollover.** Journal Gen, Git Sync, Sunday Archival/Backup, Health Audits. |
> | `system_sync.py` | `syncvault` | **Connectivity.** Scans Core/Contexts for broken links & updates Dashboard. |
> | `analytics_engine.py` | *(Auto)* | **Phase 3 Intelligence.** v2.2: Pearson Correlation & Reliability Metrics. |
> | `validate_system.py`| `morning` | **Internal.** Core sanity check for files, scripts, and dependencies. |
> | `link_auditor.py` | *(Auto)* | **Vault Hygiene.** Scans for missing links and semantic disconnects. |
> | `log_dispatch.py` | *(Auto)* | **Audit.** Logs agent actions to `📋 Dispatch Log.md`. |
> | `tag_predictor.py` | `predict [text]` | **Cognitive.** Suggests tags based on vault history frequency. |
> | `yt_notes.py` | `ytnotes [URL]` | **Video Intelligence.** Fetches transcripts (long-video safe), summarizes. |
> | `pdf-notes.sh` | `pdfnotes` | **Document Intelligence.** OCRs/Extracts text from PDFs. |
> | `web_notes.py` | `webnotes [URL]` | **Web Clipper.** Fetches article text via Trafilatura. |
> | `camera_scan.sh` | `scan` | **Quick Capture.** OCRs physical text via camera to 1 - 🌀 Chaos Stream. |
> | `anki_generator.py` | `anki [Note]` | **Memory Injection.** Converts notes into Anki decks. |
> | `webhook_listener.py`| `listener` | **Mobile.** Listens for external data and appends to 2 - 🧩 Input Stream. |
> | `vault_auditor.py` | *(Auto)* | **System Health.** Scans for broken links or orphans (Librarian). |
> | `backup_system.sh` | *(Manual)* | **Resilience.** Creates a full snapshot of Core, Contexts, and Scripts. |
> | `sync_frequent.sh` | `vsync` | **Phase 4 Sync.** Redundant git-syncing for fault tolerance. |
> | `health_check.py` | `python scripts/health_check.py` | **Phase 4 Health.** Audits all system scripts for presence and functionality. |
> | `publish.py` | `python scripts/publish.py [file]` | **Phase 4 Export.** Converts Obsidian notes to clean Markdown. |
> | `dispatcher.py` | `python scripts/dispatcher.py [text]` | **Phase 4 Router.** Identifies the correct agent for a specific task. |
> | `vault_graph.py` | `python scripts/vault_graph.py` | **Phase 4 Intelligence.** Suggests backlinks based on shared tags/topics. |
| `memory_cleanup.py` | `python scripts/memory_cleanup.py` | **Phase 4 Hygiene.** Prunes outdated memories from agent contexts. |
| `canvas_generator.py` | `python scripts/canvas_generator.py [file]` | **Visualizer.** Converts Markdown/JSON into Obsidian Canvas maps. |
| `simulator.py` | `python scripts/simulator.py` | **Social.** Launcher for the social roleplay simulation. |
> | `smart-notes.sh` | `notes` | **Master Menu.** Interactive selection for all tools. |

---
> [!tip] Architect's Note
> This dashboard updates automatically via Dataview.