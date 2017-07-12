import json
import os

from PIL import Image
from icon_image_helpers import IconImageHelpers

class IconFactory:

    @staticmethod
    def create_icons(input_manifest, output_path_param, scale, json_output_path):

        icon_size = int(input_manifest["icon-size"])
        image_size = int(icon_size * scale)

        json_dto = {}
        icon_dtos = []

        for icon_definition in input_manifest["icons"]:

            icon_file = input_manifest["path"] + str(icon_definition["file"]) if "file" in icon_definition else None
            #validate_svg(icon_file, 108)

            icon_id = str(icon_definition["id"])
            color_override = None if "color" not in icon_definition else str(icon_definition["color"])
            background_color = None if "background-color" not in icon_definition else str(icon_definition["background-color"])

            image = Image.new('RGBA', (image_size, image_size))
            IconImageHelpers.draw_menu_icon(image, icon_file, (0,0), icon_size, scale, color_override, background_color)
            output_path = "{0}{1}.png".format(output_path_param, icon_id)
            image.save(output_path, "PNG")
            output_file = os.path.basename(output_path)
            icon_dtos.append({"name":icon_id, "file":output_file})

        icon_dtos.sort(key=lambda x: x["name"])
        json_dto["icons"]=icon_dtos

        with open(json_output_path, 'w') as json_output_file:
            json.dump(json_dto, json_output_file, indent=4)
