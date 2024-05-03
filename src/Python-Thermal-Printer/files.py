import os
import pickle
import json
import tarfile
from glob import glob
from typing import Any, List, Optional, Tuple

import json5
#import cv2
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#from matplotlib.figure import Figure
from PIL import Image


def get_filedirs(filepath: str,
                 fext: Optional[str] = None,
                 ) -> List[str]:
    if fext is None:
        filedirs = [y for x in os.walk(filepath) for y in glob(os.path.join(x[0], '*.*'))]
        return filedirs
    else:
        filedirs = [y for x in os.walk(filepath) for y in glob(os.path.join(x[0], f'*.{fext}'))]
        return filedirs

