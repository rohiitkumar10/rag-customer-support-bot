#!/usr/bin/env python3
"""
Stop the background Streamlit process started by run_streamlit_bg.py

Usage:
    python stop_streamlit_bg.py

This reads .streamlit_pid and attempts to terminate the process.
"""
import os
import signal
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PIDFILE = os.path.join(ROOT, ".streamlit_pid")


def main():
    if not os.path.exists(PIDFILE):
        print("No PID file found. Is streamlit running (launched with run_streamlit_bg.py)?")
        sys.exit(1)

    with open(PIDFILE, "r") as f:
        pid = int(f.read().strip())

    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Terminated process {pid}")
    except ProcessLookupError:
        print(f"No process with pid {pid} found")

    try:
        os.remove(PIDFILE)
    except OSError:
        pass


if __name__ == "__main__":
    main()
