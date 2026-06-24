"""
Keystroke Logger — In-Page Typing Activity Logger
A single-file Flask app: Python backend + embedded HTML/CSS/JS frontend.

IMPORTANT — what this is and isn't:
This logs keystrokes typed into the text box ON THIS PAGE only, while the
page is open and focused, and writes them to a local log file. It does NOT
run in the background, does NOT capture keys outside the browser tab, and
does NOT hide itself — a real keylogger does all three, which is what makes
that kind of tool a surveillance/malware risk. This project teaches the same
underlying skills (key event capture, timestamps, file I/O) in a contained,
consent-based way: only your own typing, into your own open tab, is logged.

Run:
    pip install flask --break-system-packages
    python typing_logger_app.py
Then open http://127.0.0.1:5000
"""

import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

LOG_FILE = Path("keystroke_log.txt")


@app.route("/")
def index():
    return render_template_string(PAGE_TEMPLATE)


@app.route("/api/log", methods=["POST"])
def api_log():
    """Receives one keystroke event from the page and appends it to a file."""
    data = request.get_json(silent=True) or {}
    key = data.get("key", "")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    if not key:
        return jsonify({"error": "no key provided"}), 400

    display_key = key if len(key) > 1 else key  # special keys already named e.g. "Backspace"
    line = f"[{timestamp}] {display_key}\n"

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

    return jsonify({"ok": True, "logged": display_key, "time": timestamp})


@app.route("/api/log", methods=["GET"])
def api_get_log():
    """Returns the full log so the page can display it back to the user."""
    if not LOG_FILE.exists():
        return jsonify({"lines": []})
    lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
    return jsonify({"lines": lines[-200:]})  # last 200 entries


@app.route("/api/log", methods=["DELETE"])
def api_clear_log():
    if LOG_FILE.exists():
        LOG_FILE.unlink()
    return jsonify({"ok": True})


PAGE_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Keystroke Logger — In-Page Only</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  :root{
    --charcoal:#1c1b1a;
    --charcoal-2:#242220;
    --brass:#c8932b;
    --steel:#5c7a8a;
    --bone:#ece7dd;
    --bone-dim:#a8a299;
    --danger:#b9523f;
    --success:#6b9450;
    --line: rgba(236,231,221,0.12);
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html,body{
    background:var(--charcoal);
    color:var(--bone);
    font-family:'JetBrains Mono', monospace;
    min-height:100vh;
    -webkit-font-smoothing:antialiased;
  }
  body{
    display:flex;
    flex-direction:column;
    align-items:center;
    padding:5vh 6vw 8vh;
    background-image: radial-gradient(circle at 15% 10%, rgba(200,147,43,0.06), transparent 40%);
  }
  .wrap{ width:100%; max-width:640px; }
  .eyebrow{
    font-size:11px; letter-spacing:0.22em; text-transform:uppercase; color:var(--brass);
    display:flex; align-items:center; gap:10px; margin-bottom:18px;
  }
  .eyebrow::before{ content:""; width:18px; height:1px; background:var(--brass); display:inline-block; }
  h1{
    font-family:'Fraunces', serif; font-weight:700; font-size:clamp(1.9rem, 5vw, 2.8rem);
    line-height:1.08; letter-spacing:-0.01em; margin-bottom:14px;
  }
  h1 em{ font-style:italic; font-weight:400; color:var(--brass); }
  .sub{ color:var(--bone-dim); font-size:14px; line-height:1.6; max-width:54ch; margin-bottom:14px; }
  .scope-note{
    border:1px solid rgba(107,148,80,0.35);
    background:rgba(107,148,80,0.08);
    color:#9ec787;
    font-size:12px;
    line-height:1.6;
    padding:12px 14px;
    border-radius:4px;
    margin-bottom:36px;
  }
  .typebox{
    width:100%;
    min-height:120px;
    background:var(--charcoal-2);
    border:1px solid var(--line);
    border-radius:4px;
    color:var(--bone);
    font-family:'JetBrains Mono', monospace;
    font-size:15px;
    padding:16px;
    resize:vertical;
    outline:none;
    transition:border-color .25s ease;
  }
  .typebox:focus{ border-color:var(--brass); }
  .row{ display:flex; justify-content:space-between; align-items:center; margin:10px 0 30px; font-size:11px; color:var(--bone-dim); }
  .controls{ display:flex; gap:10px; }
  button{
    background:none; border:1px solid var(--line); color:var(--bone-dim);
    font-family:'JetBrains Mono', monospace; font-size:11px; letter-spacing:0.06em; text-transform:uppercase;
    padding:8px 14px; border-radius:3px; cursor:pointer; transition:all .2s ease;
  }
  button:hover{ border-color:var(--brass); color:var(--brass); }
  button.danger:hover{ border-color:var(--danger); color:var(--danger); }
  .panel-title{
    font-family:'Fraunces', serif; font-weight:600; font-size:18px; margin-bottom:12px; color:var(--bone);
  }
  .log-panel{
    border:1px solid var(--line);
    background:var(--charcoal-2);
    border-radius:4px;
    height:240px;
    overflow-y:auto;
    padding:14px 16px;
    font-size:12px;
    line-height:1.9;
    color:var(--bone-dim);
  }
  .log-panel div span.k{ color:var(--brass); }
  footer{
    margin-top:48px; font-size:10px; letter-spacing:0.1em; text-transform:uppercase;
    color:var(--bone-dim); opacity:0.5;
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">Task 04 —KeyStroke Logger(scoped alternative)</div>
  <h1>Typing activity, <em>logged in the open</em>.</h1>
  <p class="sub">This records keystrokes typed into the box below, while this tab is open and focused, and writes them to a local file on the Python server. Nothing happens outside this box.</p>
  <div class="scope-note">
    Scope, by design: capture is limited to this one input field on this one page.
    There's no background process, no system-wide capture, and no hidden behavior —
    that's what separates a teaching exercise from a surveillance tool.
  </div>

  <textarea class="typebox" id="typebox" placeholder="Start typing here — every keystroke gets timestamped and logged below."></textarea>
  <div class="row">
    <span id="status">Idle</span>
    <div class="controls">
      <button id="refreshBtn">Refresh log</button>
      <button id="clearBtn" class="danger">Clear log</button>
    </div>
  </div>

  <div class="panel-title">Log file — keystroke_log.txt</div>
  <div class="log-panel" id="logPanel"><div>No keystrokes logged yet.</div></div>

  <footer>Keystroke Logger — scoped, consent-based teaching project</footer>
</div>

<script>
  const typebox = document.getElementById('typebox');
  const statusEl = document.getElementById('status');
  const logPanel = document.getElementById('logPanel');
  const refreshBtn = document.getElementById('refreshBtn');
  const clearBtn = document.getElementById('clearBtn');

  function keyName(e){
    // Normalize printable keys vs named special keys
    if(e.key.length === 1) return e.key;
    return e.key; // e.g. "Backspace", "Enter", "Shift"
  }

  typebox.addEventListener('keydown', async (e) => {
    statusEl.textContent = 'Logging…';
    try{
      await fetch('/api/log', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ key: keyName(e) })
      });
      statusEl.textContent = 'Logged ✓';
      loadLog();
    }catch(err){
      statusEl.textContent = 'Server offline';
    }
  });

  async function loadLog(){
    try{
      const res = await fetch('/api/log');
      const data = await res.json();
      if(!data.lines || data.lines.length === 0){
        logPanel.innerHTML = '<div>No keystrokes logged yet.</div>';
        return;
      }
      logPanel.innerHTML = data.lines.slice().reverse().map(l => `<div>${escapeHtml(l)}</div>`).join('');
    }catch(err){
      // ignore
    }
  }

  function escapeHtml(s){
    return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  refreshBtn.addEventListener('click', loadLog);
  clearBtn.addEventListener('click', async () => {
    await fetch('/api/log', { method:'DELETE' });
    loadLog();
  });

  loadLog();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)