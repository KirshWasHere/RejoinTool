import os
import sys

def launch_roblox(uri: str):
    if not uri:
        return

    try:
        os.startfile(uri)
    except Exception:
        pass

if __name__ == "__main__":
    example_uri = "roblox://placeId=606849621" 

    if len(sys.argv) > 1:
        example_uri = sys.argv[1]
    
    launch_roblox(example_uri)

# isaac was here