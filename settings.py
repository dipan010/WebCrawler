# settings.py (at your-project/settings.py)
import sys
from pathlib import Path

# Adding the root of the project to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
