import os


class InputValidator:

    MODE_PIN_SHEET="sheet"
    MODE_ICONS="icons"

    @staticmethod
    def validate_input_manifest(input_manifest):
        if "mode" in input_manifest:
            mode = str(input_manifest["mode"])
            valid_modes = [InputValidator.MODE_PIN_SHEET, InputValidator.MODE_ICONS]
            if mode not in valid_modes:
                raise ValueError("Unrecognized mode '{0}'. Valid modes are: {1}".format(mode, valid_modes))
        else:
            raise ValueError("No mode specified in input json")

        if "icons" not in input_manifest:
            raise ValueError("No icon definitions defined in input json")

        ids_found=[]
        for icon_definition in input_manifest["icons"]:
            InputValidator.__validate_icon_definition(icon_definition, input_manifest["path"],ids_found)

    @staticmethod
    def __validate_icon_definition(icon_definition, file_path, ids_found):
        if "id" not in icon_definition:
            raise ValueError("No id defined in icon")

        id = icon_definition["id"]
        if id in ids_found:
            raise ValueError("Duplicate id found: {0}".format(id))

        ids_found.append(id)

        if "file" in icon_definition:
            full_path = file_path + os.sep + icon_definition["file"]
            if not os.path.exists(full_path):
                raise ValueError("Filename for icon '{0}' doesn't exist - {1}".format(id, full_path))