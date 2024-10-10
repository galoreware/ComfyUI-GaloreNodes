from PIL import Image
import math

from common import *

class GN_ColorToInt:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "color": ("COLOR",),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("COLOR (INT)",)

    FUNCTION = "Run"

    #OUTPUT_NODE = False

    CATEGORY = "Galore Nodes"

    def check_lazy_status(self, color):
        return []

    def Run(self, color):
        icolor = C_Color2Int(color)
        return (icolor,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GN_COLOR_TO_INT" : GN_ColorToInt,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GN_COLOR_TO_INT" : "Color to INT 🎨➡️⭐",
}