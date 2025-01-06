import os
import sys
import numpy as np

from pathlib import Path
from math import floor
from mathutils import Matrix

ADDON_DIR = Path(__file__).resolve().parent


def add_current_module_to_path():
    path = str(ADDON_DIR.parent)
    sys.path.append(path)