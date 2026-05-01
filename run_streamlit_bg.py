#!/usr/bin/env python3
"""
Launch Streamlit app in the background and open the browser.

Usage:
    python run_streamlit_bg.py

This script will:
 - try to use the project's .venv python if present
 - start `python -m streamlit run app.py` in a detached background process
 - write the server PID to .streamlit_pid
 - open the default web browser to http://localhost:8501

"""
import os
import subprocess
import sys
import time
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(ROOT, "app.py")
PIDFILE = os.path.join(ROOT, ".streamlit_pid")


def find_python_executable():
    # Prefer .venv in repo
    venv_python = os.path.join(ROOT, ".venv", "bin", "python")
    if os.path.exists(venv_python):
        return venv_python
    # fallback to current interpreter
    return sys.executable


def main():
    if not os.path.exists(APP):
        print(f"Could not find {APP}")
        sys.exit(1)

    python = find_python_executable()

    # Build command to run streamlit
    cmd = [python, "-m", "streamlit", "run", APP]

    # Start detached process (cross-platform-ish)
    # On POSIX, start_new_session=True detaches from terminal
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except TypeError:
        # Older Pythons may not have start_new_session
        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Save PID
    with open(PIDFILE, "w") as f:
        f.write(str(proc.pid))

    print(f"Started Streamlit (pid={proc.pid}). Opening browser...")

    # Give server a moment to start
    time.sleep(1.5)

    url = "http://localhost:8501"
    try:
        webbrowser.open(url)
    except Exception:
        print(f"Open your browser and visit: {url}")


if __name__ == "__main__":
    main()
