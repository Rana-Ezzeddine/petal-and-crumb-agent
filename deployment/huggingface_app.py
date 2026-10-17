"""Optional Space entrypoint: run packaged source without remote downloads.

Prefer app.py as app_file and a CPU Space. If using this wrapper, preserve
repository layout: deployment/ beside app.py, core_bot.py, and me/.
"""
from pathlib import Path
import runpy
import sys

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))
runpy.run_path(str(root / 'app.py'), run_name='__main__')
