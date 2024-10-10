from PIL import Image
import math

from common import *

class GN_SnapResize:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "longest": ("INT", {
                    "default": 512, 
                    "min": 0, #Minimum value
                    "max": 4096, #Maximum value
                    "step": 256, #Slider's step
                    "display": "number", # Cosmetic only: display as "number" or "slider"
                    "lazy": True # Will only be evaluated if check_lazy_status requires it
                }),
                "shortest": ("INT", {
                    "default": 512, 
                    "min": 0, #Minimum value
                    "max": 4096, #Maximum value
                    "step": 256, #Slider's step
                    "display": "number", # Cosmetic only: display as "number" or "slider"
                    "lazy": True # Will only be evaluated if check_lazy_status requires it
                }),
                "background_color": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFF, "step": 1, "display": "color"}),
                "resize_according_to": (["longest", "shortest"],),
                "h_snap_to": (["left", "center", "right"],{"default": "center"}),
                "v_snap_to": (["top", "middle", "down"],{"default": "middle"}),
            },
            "optional":
            {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE","INT", "INT")
    RETURN_NAMES = ("IMAGE","Width (INT)","Height (INT)")

    FUNCTION = "Run"

    #OUTPUT_NODE = False

    CATEGORY = "Galore Nodes"

    def check_lazy_status(self, image, longest, shortest, background_color, resize_according_to, h_snap_to, v_snap_to, mask = None):
        return []

    def Run(self,image, longest, shortest, background_color, resize_according_to, h_snap_to, v_snap_to, mask= None):
        data = image.size()

        width = data[2]
        height = data[1]

        t_resize = longest if resize_according_to == "longest" else shortest

        t_width = 0
        t_height = 0

        ir_width = 0
        ir_height = 0


        if(width == height): #SQUARED
            t_width = t_resize
            t_height = t_width

            ir_width = t_width
            ir_height = t_height

        else:
            if (width >= height):
                #HORIZONTAL
                # w = int_a
                # h = ?

                t_width = longest
                t_height = shortest

                ir_width = longest
                ir_height = math.floor((height * longest) / width)

            else:
                #VERTICAL
                # w = ?
                # h = int_a

                t_width = shortest
                t_height = longest

                ir_width = math.floor((longest * width) / height)
                ir_height = longest


        if h_snap_to == "center":
            ox = math.floor((t_width - ir_width)/2)
        elif h_snap_to == "left":
            ox = 0
        else:
            ox = t_width - ir_width
        
        if v_snap_to == "middle":
            oy = math.floor((t_height - ir_height)/2)
        elif v_snap_to == "top":
            oy = 0
        else:
            oy = t_height - ir_height
        
        print(f"""Your input contains:
            Original size:  {width}x{height}
            Target size:    {t_width}x{t_height} 
            Image Resize:   {ir_width}x{ir_height} 
            Offset:         {ox},{oy}

            RESIZE ACCORDING TO {resize_according_to}
            H SNAP TO {h_snap_to}
            V SNAP TO {v_snap_to}

            MASK {mask}
        """);
        
        bgc = C_Int2Color(background_color)

        images = batch_tensor_to_pil(image)
        
        olist = []

        for img in images:
            olist.append(self.Render(img,bgc, t_width, t_height, ir_width, ir_height, ox, oy))
        
        if (mask is not None):
            mask = tensor_to_pil(mask);
            mask = mask.resize([ir_width, ir_height])

        timg = batched_pil_to_tensor(olist)

        return (timg, t_width, t_height)
    
    def Render(self, image, bgc, tw, th, iw, ih, x, y) -> Image.Image:
        base = Image.new(mode="RGBA", size=(tw, th), color=(bgc))
        img = image.resize([iw, ih])
        base.paste(img, ( x, y))

        return base


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GN_SNAP_RESIZE" : GN_SnapResize,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GN_SNAP_RESIZE": "Image Snap Resize 🖼️⭐",
}