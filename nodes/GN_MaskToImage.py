from common import *

class GN_MaskToImage:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mask": ("MASK",),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    #RETURN_NAMES = ("COLOR (INT)",)

    FUNCTION = "Run"

    #OUTPUT_NODE = False

    CATEGORY = "Galore Nodes"

    def check_lazy_status(self, mask):
        return []

    def Run(self, mask: torch.Tensor):
        img = tensor_to_mask(mask)
        img = 1.0 - img
        return (img,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GN_MASK_TO_IMAGE" : GN_MaskToImage,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GN_MASK_TO_IMAGE" : "Mask to Image 🏁➡️🖼️",
}