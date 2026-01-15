<%*
let title = tp.file.title
if (title.startsWith("Untitled")) {
    title = await tp.system.prompt("Deep Dive Subject");
    await tp.file.rename(title);
}
%>
---
tags:
  - deep-dive
  - learning/project
  - status/active
creation_date: <% tp.date.now("YYYY-MM-DD") %>
---

# 🧠 Project: <% title %>
> "The map is not the territory."
> **Guide:** [[The Blueprints/🔥 Protocol True Learning|🔥 Protocol True Learning]]

## 🎯 The Objective
- **The Question:** [What specific question am I answering?]
- **The Scope:** [How deep? 1 Week? 1 Month?]
- **Success Metric:** [I know I've learned this when...]

---

## 📥 Research & Gathering (The Sweep)
*Collect sources before reading deep.*
- [ ] [Source 1](https://www.youtube.com/)
- [ ] [Source 2](https://scholar.google.com/)

---

## 🪞 CONTEXT & DRIVERS
...
---

## ✅ COMPLETED (History)
- [ ] 

---

# 🎭 Archetype Template Section
> Use this structure when deconstructing archetypes in the Hall of Mirrors.

## 🌟 Core Traits
- **Trait 1:** Description.
- **Trait 2:** Description.

## 🧠 Psychology
- **Motivation:** What drives them?
- **Friction:** What do they fear?

## 🏆 Winning Moves
- **Application:** How can I use this trait?

---
#template #project #learning #archetype
