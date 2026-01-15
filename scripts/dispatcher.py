import sys

ROSTER = {
    "🏗️ Architect": ["structure", "system", "vault", "links", "maintenance", "debug"],
    "🎓 Academic Tutor": ["bams", "sanskrit", "exam", "syllabus", "study", "memorize"],
    "🧘 Sage": ["psychology", "mind", "pattern", "meditation", "feeling", "anxiety", "sadhana"],
    "🔬 Scholar": ["chess", "philosophy", "deep dive", "research", "hobby"],
    "🎭 Simulator": ["social", "practice", "conversation", "roleplay", "persona"],
    "📚 Librarian": ["folder", "tag", "clean", "organize", "archive"],
    "⚙️ Automation Engineer": ["script", "code", "python", "automate", "error", "api"],
    "🎨 Muse": ["creative", "idea", "brainstorm", "dream", "expansion"]
}

def route_task(task_text):
    task_text = task_text.lower()
    matches = []
    
    for agent, keywords in ROSTER.items():
        if any(kw in task_text for kw in keywords):
            matches.append(agent)
            
    if not matches:
        return ["🏗️ Architect (Default)"]
    return matches

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/dispatcher.py [task_description]")
    else:
        task = " ".join(sys.argv[1:])
        recommendations = route_task(task)
        print("🎯 Recommended Specialist(s):")
        for rec in recommendations:
            print(f"- {rec}")
