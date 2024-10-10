from common import C_Color2Int

class GN_RGBToColor:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "r": ("INT", { "default": 0, "min": 0, "max": 255, "step": 1, "display": "number", "lazy": True}),
                "g": ("INT", { "default": 0, "min": 0, "max": 255, "step": 1, "display": "number", "lazy": True}),
                "b": ("INT", { "default": 0, "min": 0, "max": 255, "step": 1, "display": "number", "lazy": True}),
            }
        }
    
    RETURN_TYPES = ("COLOR","INT",)
    RETURN_NAMES = ("COLOR","COLOR (INT)",)

    FUNCTION = "Run"

    #OUTPUT_NODE = False

    CATEGORY = "Galore Nodes"

    def check_lazy_status(self, r,g,b):
        return []

    def Run(self, r,g,b):
        color = (r,g,b)
        icolor = C_Color2Int(color)
        return (color, icolor)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GNI_RGB_TO_COLOR" : GN_RGBToColor,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GNI_RGB_TO_COLOR" : "RGB Color Input 🟥🟩🟦🎨⭐",
}