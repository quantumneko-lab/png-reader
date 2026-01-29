#!/usr/bin/env python3
"""
Run script for E-Book Viewer application
This script should be used instead of directly calling python main.py
"""
import subprocess
import sys
import os

def run():
    """Run the application"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run the main application
    result = subprocess.run([sys.executable, 'main.py'], cwd=script_dir)
    sys.exit(result.returncode)

if __name__ == '__main__':
    run()
