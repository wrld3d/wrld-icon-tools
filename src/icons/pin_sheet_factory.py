import json
import os

from PIL import Image
from PIL.ImageColor import getrgb

from icon_image_helpers import IconImageHelpers
from simple_texture_packer import SimpleTexturePacker

class PinSheetFactory:

    @staticmethod
    def create_pin_sheet(input_manifest, output_path_param, scale, json_output_path):

        icon_size=int(input_manifest["icon-size"])
        cell_size=int(input_manifest["cell-size"])
        sheet_size=int(input_manifest["sheet-size"]) if "sheet-size" in input_manifest else 256

        image_pairs=[]

        json_dto={}
        index = 0

        for icon_definition in input_manifest["icons"]:

            icon_file = input_manifest["path"] + str(icon_definition["file"]) if "file" in icon_definition else None
            local_cell_size = icon_definition["cell-size"] if "cell-size" in icon_definition else cell_size
            local_icon_size = icon_definition["icon-size"] if "icon-size" in icon_definition else icon_size

            image = Image.new('RGBA', (int(local_cell_size*scale), int(local_cell_size*scale)))

            #validate_svg(icon_file, 72)

            icon_id=str(icon_definition["id"])
            color_override = None if "color" not in icon_definition else str(icon_definition["color"])
            background_color = None if "background-color" not in icon_definition else str(icon_definition["background-color"])
            outline_color = None if "outline-color" not in icon_definition else getrgb(str(icon_definition["outline-color"]))
            shadow_color = (0, 0, 0, 255) if "shadow-color" not in icon_definition else getrgb(str(icon_definition["shadow-color"]))
            background = IconImageHelpers.BACKGROUND_CIRCLE if "background" not in icon_definition else str(icon_definition["background"])

            IconImageHelpers.draw_pin_icon_with_background(image,
                                                           icon_file,
                                                           (0,0),
                                                           local_icon_size,
                                                           local_cell_size,
                                                           scale,
                                                           color_override,
                                                           background,
                                                           background_color,
                                                           outline_color,
                                                           shadow_color)
            image_pairs.append((icon_id, image))
            index+=1

        packer = SimpleTexturePacker()
        packed_images, icons_metadata = packer.pack_images(image_pairs,scale,int(sheet_size*scale))
        pages_metadata=[]
        index=0
        for image in packed_images:
            output_path="{0}_{1}.png".format(output_path_param,index)
            output_file=os.path.basename(output_path)
            output_file,_=os.path.splitext(output_file)
            image.save(output_path, "PNG")
            pages_metadata.append({"file":output_file, "width":image.width, "height":image.height})
            index+=1

        json_dto["pages"] = pages_metadata
        json_dto["icons"] = icons_metadata
        with open(json_output_path, 'w') as json_output_file:
            json.dump(json_dto, json_output_file, indent=4)