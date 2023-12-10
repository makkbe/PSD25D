"""
Author: Marcus Bengtsson
Contact: marcus@makkbe.net
Description: This script converts a Photoshop file to a p2d5 package used by the Disguise media server and software.
License: This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

from psd_tools import PSDImage
from PIL import Image
import json
import os
import zipfile
import sys


asset = {
    "asset": {
        "max_depth": 100,
        "min_depth": 5,
        "field_of_view": 80.32093811035156
    },
    "plates": []  # Empty array
}

def add_plate(data, name, filename, mean_depth_value, width, height, scale_x, scale_y, scale_z):
    plate = {
        "name": name,
        "filename": filename,
        "mesh_filename": "",
        "depth_map_filename": "",
        "mean_depth_value": mean_depth_value,
        "x": 0,
        "y": 0,
        "rotation_x": 0,
        "rotation_y": 0,
        "rotation_z": 0,
        "width": width,
        "height": height,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "scale_z": scale_z
    }
    data["plates"].append(plate)
    
def zip_it(directory):
    if not os.path.exists(directory):
        return False
    
    zip_filename = directory + ".zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=os.path.join(root.replace(directory, '', 1), file))
    
    new_filename = directory + ".2p5d"
    os.rename(zip_filename, new_filename)

    return True
    

    
def pad_height(img, target_height):
    width, height = img.size

    if height >= target_height:
        print("Image is already equal to or larger than the target height.")
        return img

    padding_height = target_height - height
    new_img = Image.new("RGBA", (width, target_height), (255, 255, 255, 0))
    new_img.paste(img, (0, padding_height))

    return new_img
    
def main(filename):
    if not filename.endswith('.psd'):
        print("Error: The file must be a .psd file.")
        return
    
    directory, extension = os.path.splitext(filename)    
        
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    psd = PSDImage.open(filename)
    
    old_dir = os.getcwd()
    os.chdir(directory)
    
    layers = [] # Create an empty list and all the layers contained in the PSD file
    for layer in psd:
        layers.append(layer)
    
    layers.reverse() # The PSD file will return the layer at the bottom of the layer stack first, which is the opposite of how the 2p5d file expects it.
    
    
    
    scale_z = 1.0 # This appears to be the default starting value for the foreground layer. Does it change depending on the amount of layers in the 2.5D layer?
    for layer in layers:
        if layer.is_visible():
            layer_image = layer.composite()
            if layer.height < psd.height:
                layer_image = pad_height(layer_image, psd.height)
            
            layer_image.save('%s.png' % layer.name)
            add_plate(asset, layer.name, '%s.png' % layer.name, 0, layer.width, layer.height, 1, 1, scale_z)
            scale_z = scale_z/2
    
    json_str = json.dumps(asset, indent=4)
    
    with open("data.json", "w") as file:
        file.write(json_str)
    
    os.chdir(old_dir)
    zip_it(directory)
    
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>.psd")
    else:
        main(sys.argv[1])
