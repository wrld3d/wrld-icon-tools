import getopt
import json
import os
import sys
import traceback
from icon_factory import IconFactory
from scalable_icon_factory import ScalableIconFactory
from pin_sheet_factory import PinSheetFactory
from input_validator import InputValidator

def print_usage():
    print 'Usage: '
    print 'icon_renderer.py -i <input JSON manifest> -s <scale> -o <output_path> -j <json output file path>'
    print 'icon_renderer.py [-h | -help]'
    print
    print 'Options: '
    print '-i --input_json       Input json manifest describing what icons to process (and how to process them)'
    print '-o --output           For pin sheet, output pin sheet name. For icons, output with this prefix + name.png'
    print '-s --scale            Scale factor. i.e. 2 = retina asset size (@2x). Leave absent/blank to get SVGs.'
    print '-j --json_file_output Json manifest output for describing the assets generated'

def get_args(argv):
    input_json = ''
    output_path = ''
    scale = ''
    json_file = ''
    try:
        opts, args = getopt.getopt(argv, "hi:s:o:j:",
                                   ["input_json=", "scale=", "output=", "json_file_output="]) # Json file output
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-i", "--input_json"):
            input_json = arg
        elif opt in ("-o", "--output"):
            output_path = arg
        elif opt in ("-s", "--scale"):
            scale = float(arg)
        elif opt in ("-j", "--json_file_output"):
            json_file = arg

    return input_json, output_path, scale, json_file

def __validate_params(input_json_path, output_path, scale, json_file):
    if not input_json_path:
        raise ValueError('input_json_path not defined.')

    if not output_path:
        raise ValueError('output_image_path not defined.')

    if not os.path.exists(input_json_path):
        raise ValueError('path not found: ' + input_json_path)

    if scale and scale <= 0:
        raise ValueError('output size must be > 0: ' + scale)

def process_input_manifest(input_json_path_param):
    with open(input_json_path_param, 'r') as json_input_file:
        icon_manifest = json.load(json_input_file)

    base_path = os.path.dirname(input_json_path_param) + os.sep
    icon_manifest["path"]=base_path
    return icon_manifest

if __name__ == "__main__":
    try:
        input_json_path_param, output_path_param, scale_param, json_file_param = get_args(sys.argv[1:])

        try:
            __validate_params(input_json_path_param, output_path_param, scale_param, json_file_param)
        except ValueError as err:
            print "Error: {0}".format(err.message)
            print_usage()
            sys.exit(1)

        print 'input_json_path_param: ' + input_json_path_param
        print 'output_path_param: ' + output_path_param
        print 'scale: ' + (str(scale_param) if scale_param else "unspecified. Producing SVGs.")
        print 'json_file_param: ' + str(json_file_param)

        input_manifest = process_input_manifest(input_json_path_param)
        InputValidator.validate_input_manifest(input_manifest)
        mode = input_manifest["mode"]

        if InputValidator.MODE_PIN_SHEET in mode:
            PinSheetFactory.create_pin_sheet(input_manifest, output_path_param, scale_param, json_file_param)
        elif InputValidator.MODE_ICONS in mode:
            if scale_param:
                IconFactory.create_icons(input_manifest, output_path_param, scale_param, json_file_param)
            else:
                ScalableIconFactory.create_icons(input_manifest, output_path_param, json_file_param)
        else:
            raise ValueError("Unknown mode: " + mode)

    except Exception as e:
        _, _, exc_traceback = sys.exc_info()
        print(str(traceback.format_exc(exc_traceback)))
        sys.exit(1)