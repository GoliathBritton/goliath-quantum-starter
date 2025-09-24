import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'tests'))
try:
    from api.src.main import app
    print("Success")
except Exception as e:
    print(f"Error: {e}")