"""Space bootstrap: execute the reviewed, immutable GitHub runtime."""
import hashlib
from pathlib import Path
import runpy
import shutil
import sys
from urllib.request import urlopen
import spaces

@spaces.GPU
def _host_gpu_hook():
    """Startup compatibility only; chatbot requests never call this hook."""
    return None

COMMIT = "6c1df436f3abd8e14cf3f850da96dc6bbbf20cba"
FILES = {
    "core_bot.py": "9d684b475378569904ca40cfd9146e9516b687a20ffc56350e40a6c8d537cb4a",
    "app.py": "0f79a2f757533d9e3fe059ef818aa7e9910cbec9298e021c74e6580b378b8e94",
}
source = Path(__file__).resolve().parent
runtime = Path("/tmp") / ("petal-crumb-" + COMMIT)
(runtime / "me").mkdir(parents=True, exist_ok=True)
for filename, expected_sha256 in FILES.items():
    url = f"https://raw.githubusercontent.com/Rana-Ezzeddine/petal-and-crumb-agent/{COMMIT}/{filename}"
    with urlopen(url, timeout=30) as response:
        content = response.read()
    if hashlib.sha256(content).hexdigest() != expected_sha256:
        raise RuntimeError("Deployment source digest did not match the reviewed version.")
    (runtime / filename).write_bytes(content)
for filename in ("about_business.pdf", "business_summary.txt"):
    origin = source / "me" / filename if (source / "me" / filename).exists() else source / filename
    shutil.copyfile(origin, runtime / "me" / filename)
sys.path.insert(0, str(runtime))
runpy.run_path(str(runtime / "app.py"), run_name="__main__")
