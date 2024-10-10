from PIL import Image, ImageColor
import numpy as np
import torch
import torchvision.transforms.functional as TF
import re

rex_hexadecimal = re.compile(r"#[09AFaf]{6}")

#https://github.com/Gourieff/comfyui-reactor-node/blob/main/reactor_utils.py
def tensor_to_mask(tensor, index = 0) -> torch.Tensor:
    t = tensor[index].unsqueeze(0)
    size = t.size()
    if (len(size) < 4):
        return t
    if size[3] == 1:
        return t[:,:,:,0]
    elif size[3] == 4:
        # Not sure what the right thing to do here is. Going to try to be a little smart and use alpha unless all alpha is 1 in case we'll fallback to RGB behavior
        if torch.min(t[:, :, :, 3]).item() != 1.:
            return t[:,:,:,3]

    return TF.rgb_to_grayscale(tensor_to_pil(t).permute(0,3,1,2), num_output_channels=1)[:,0,:,:]

def tensor_to_pil(tensor, index):
    # Convert tensor of shape [batch_size, channels, height, width] at the batch_index to PIL Image
    img_tensor = tensor[index].unsqueeze(0)
    i = 255. * img_tensor.cpu().numpy()
    np_array = np.clip(i, 0, 255).astype(np.uint8).squeeze()
    
    print(f"tensor_to_pil (ndim): {np_array.ndim}")

    if np_array.ndim == 2:  # (H, W) for masks
        return Image.fromarray(np_array, mode="L")
    elif np_array.ndim == 3:  # (H, W, C) for RGB/RGBA
        if np_array.shape[2] == 3:
            return Image.fromarray(np_array, mode="RGB")
        elif np_array.shape[2] == 4:
            return Image.fromarray(np_array, mode="RGBA")
    raise ValueError(f"Invalid tensor shape: {img_tensor.shape}")

def pil_to_tensor(image):
    # Takes a PIL image and returns a tensor of shape [1, height, width, channels]
    image = np.array(image).astype(np.float32) / 255.0
    image = torch.from_numpy(image).unsqueeze(0)
    
    if len(image.shape) == 3:  # If the image is grayscale, add a channel dimension
        return image.unsqueeze(-1)
    
    return image

def batch_tensor_to_mask(img_tensor):
    # Convert tensor of shape [batch_size, channels, height, width] to a list of PIL Images
    return [tensor_to_mask(img_tensor, i) for i in range(img_tensor.shape[0])]

def batch_tensor_to_pil(img_tensor):
    # Convert tensor of shape [batch_size, channels, height, width] to a list of PIL Images
    return [tensor_to_pil(img_tensor, i) for i in range(img_tensor.shape[0])]

def batched_pil_to_tensor(images):
    # Takes a list of PIL images and returns a tensor of shape [batch_size, height, width, channels]
    return torch.cat([pil_to_tensor(image) for image in images], dim=0)

#https://stackoverflow.com/questions/4092528/how-can-i-clamp-clip-restrict-a-number-to-some-range
def clamp(minval, value, maxval):
    return sorted((minval, value, maxval))[1]

def C_Color2Int(color) -> int:
    r = clamp(0, color[0], 255)
    g = clamp(0, color[1], 255)
    b = clamp(0, color[2], 255)

    return (r * 65536) + (g * 256) + b

def C_HEX2Color(color) -> tuple:
    r = int(color[1:3],16)
    g = int(color[3:5],16)
    b = int(color[5:7],16)

    return (r,g,b)

def C_HEX2Int(color) -> int:
    return int(color[1:],16)

#https://stackoverflow.com/a/2262152/3930332
def C_Int2Color(color) -> tuple:
    r =  color & 255
    g = (color >> 8) & 255
    b =   (color >> 16) & 255
    return (r,g,b)
