from common import *

class GN_HEXToColor:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "color": ("STRING", {"multiline": False, "default": "#000000"}),
            }
        }
    
    @classmethod
    def VALIDATE_INPUTS(self, color):
        #print(f"INPUT [{color}]")
        if re.fullmatch(rex_hexadecimal, color) is None:
            return "Invalid Format"
        
        return True
    
    RETURN_TYPES = ("COLOR","INT",)
    RETURN_NAMES = ("COLOR","COLOR (INT)",)

    FUNCTION = "Run"

    #OUTPUT_NODE = False

    CATEGORY = "Galore Nodes"

    def check_lazy_status(self, color):
        return []

    def Run(self, color):
        tcolor = C_HEX2Color(color)
        icolor = C_HEX2Int(color)

        return (tcolor, icolor)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GNI_HEX_TO_COLOR" : GN_HEXToColor,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GNI_HEX_TO_COLOR" : "HEX (Web) Color Input 🌐🎨⭐",
}