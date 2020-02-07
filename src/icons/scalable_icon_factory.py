import json
import os
import shutil

class ScalableIconFactory:

    @staticmethod
    def create_icons(input_manifest, output_path_param, json_output_path):

        json_dto = {}
        icon_dtos = []

        for icon_definition in input_manifest["icons"]:

            icon_file = input_manifest["path"] + str(icon_definition["file"]) if "file" in icon_definition else None

            icon_id = str(icon_definition["id"])
            if "color" in icon_definition:
                raise NotImplementedError("Colour override for SVGs not supported")
            if "background-color" in icon_definition:
                raise NotImplementedError("Background colour for SVGs not supported")

            output_path = "{0}{1}.svg".format(output_path_param, icon_id)
            # Potential improvement: Optimise the SVGs for web use with SVGO
            # scour is less effective, so probably isn't worthwhile
            shutil.copyfile(icon_file, output_path)

            output_file = os.path.basename(output_path)
            icon_dtos.append({"name":icon_id, "file":output_file})

        icon_dtos.sort(key=lambda x: x["name"])
        json_dto["icons"]=icon_dtos

        with open(json_output_path, 'w') as json_output_file:
            json.dump(json_dto, json_output_file, indent=4)
