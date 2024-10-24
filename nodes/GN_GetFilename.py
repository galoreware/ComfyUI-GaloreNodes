from pathlib import Path

class GN_GetFilename:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": ("STRING", {"multiline": False}),
            }
        }
    
    RETURN_TYPES = ("STRING","STRING","STRING","STRING","BOOL",)
    RETURN_NAMES = ("File name with extension (STRING)","filename W/o extension (STRING)","extension (STRING)","Folder path (STRING)","is directory? (BOOL)")

    FUNCTION = "Run"

    #OUTPUT_NODE = False

    CATEGORY = "Galore Nodes"

    def check_lazy_status(self, path):
        return []
    
    @classmethod
    def VALIDATE_INPUTS(self, path):
        # https://stackoverflow.com/a/9573278/3930332
        if not(path and bool(path.strip())) or path == "":
            return "Invalid Format"
        
        return True

    #https://stackoverflow.com/a/35490226/3930332
    def Run(self, path):
        p = Path(path)
        fname = p.stem
        ext = '.'.join(p.suffixes)
        basename = p.name
        dname = str(p.parent)
        is_dir = p.is_dir

        return (basename, fname, ext, dname, is_dir,)

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "GN_IO_GET_FILENAME" : GN_GetFilename,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "GN_IO_GET_FILENAME" : "Get file and path 📁📝⭐",
}