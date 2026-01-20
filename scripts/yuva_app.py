import streamlit as st
import os
import datetime
import subprocess
import re

# --- Configuration ---
VAULT_ROOT = "/storage/emulated/0/Download/Vinci"
CENTRAL_CMD = os.path.join(VAULT_ROOT, "0 - 🌌 Central Command.md")
CHAOS_STREAM = os.path.join(VAULT_ROOT, "1 - 🌀 Chaos Stream.md")
SCRIPTS_DIR = os.path.join(VAULT_ROOT, "scripts")

st.set_page_config(page_title="Yuva", page_icon="🤖", layout="wide")

# --- Styles ---
st.markdown(r'''
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #262730;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: monospace;
    }
    .terminal-output {
        background-color: #000000;
        color: #00FF00;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        white-space: pre-wrap;
    }
    </style>
    ''', unsafe_allow_html=True)

# --- Helper Functions ---
def read_file(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return "File not found."

def append_to_file(path, text):
    timestamp = datetime.datetime.now().strftime("[%I:%M %p]")
    entry = f"\n- `{timestamp}` {text}"
    with open(path, 'a', encoding='utf-8') as f:
        f.write(entry)

def run_script(script_name):
    cmd = f"python {os.path.join(SCRIPTS_DIR, script_name)}"
    return run_terminal_command(cmd)

def run_terminal_command(cmd):
    try:
        # Run command in the Vault Root
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=VAULT_ROOT)
        output = result.stdout
        if result.stderr:
            output += "\n[STDERR]\n" + result.stderr
        return output
    except Exception as e:
        return str(e)

def get_todays_journal():
    today = datetime.date.today()
    month = today.strftime("%B")
    year_month = today.strftime("%Y-%m")
    path = os.path.join(VAULT_ROOT, "1 - 🧠 The Construct/📜 The Saga", f"{year_month}-{month}.md")
    
    if not os.path.exists(path):
        return "No journal found for this month."
        
    content = read_file(path)
    header = f"## 📅 {today.strftime('%A, %d')}"
    if header in content:
        parts = content.split(header)
        if len(parts) > 1:
            today_content = parts[1].split("## 📅")[0]
            return f"# 📅 {today.strftime('%A, %d')}\n" + today_content
    return f"Entry for {header} not found."

# --- UI Layout ---

st.title("🤖 Yuva System Interface")

# Sidebar
with st.sidebar:
    st.header("⚡ Quick Actions")
    if st.button("🌅 Morning Protocol"):
        with st.spinner("Running..."):
            st.code(run_script("morning_cron.py"))
    if st.button("🕷️ Sync Vault"):
        with st.spinner("Syncing..."):
            st.code(run_script("system_sync.py"))
    
    st.markdown("---")
    st.markdown("**System Status**")
    st.caption(f"📅 {datetime.date.today()}")
    st.caption(f"📍 {VAULT_ROOT}")

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs(["💻 Terminal", "🌀 Stream", "🌌 Dashboard", "📜 Journal"])

with tab1:
    st.subheader("💻 System Terminal")
    st.markdown("Execute shell commands directly inside Termux.")
    
    # Session state to keep output visible
    if 'term_output' not in st.session_state:
        st.session_state.term_output = ""

    with st.form("terminal_form"):
        cmd_input = st.text_input("Command (e.g., 'ls -la', 'git status')", placeholder="Enter command...")
        submitted = st.form_submit_button("Run")
        
        if submitted and cmd_input:
            st.session_state.term_output = run_terminal_command(cmd_input)
    
    if st.session_state.term_output:
        st.markdown(f'<div class="terminal-output">{st.session_state.term_output}</div>', unsafe_allow_html=True)

with tab2:
    st.subheader("📥 Input Stream")
    with st.form("chaos_input"):
        text_input = st.text_area("Log thoughts, tasks, or observations...", height=150)
        submitted = st.form_submit_button("🚀 Log to Chaos Stream")
        
        if submitted and text_input:
            append_to_file(CHAOS_STREAM, text_input)
            st.success("Logged successfully.")
            
    st.subheader("Recent Stream")
    stream_content = read_file(CHAOS_STREAM)
    st.text(stream_content[-1500:] if len(stream_content) > 1500 else stream_content)

with tab3:
    st.subheader("🌌 Central Command")
    content = read_file(CENTRAL_CMD)
    clean_content = re.sub(r'```dataviewjs.*?```', '*(Dataview Tables are not renderable in Yuva yet)*', content, flags=re.DOTALL)
    st.markdown(clean_content)

with tab4:
    st.subheader("📖 Today's Saga")
    st.markdown(get_todays_journal())