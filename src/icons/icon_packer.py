import getopt
import glob
import os
import sys
import traceback
import shutil

def __validate_params(input_paths, output_path, output_format, json_pin_sheet, json_icons):
    if not os.path.exists(json_pin_sheet):
        raise ValueError("Couldn't find JSON atlas for Pin Sheet: {0}".format(json_pin_sheet))

    if not os.path.exists(json_icons):
        raise ValueError("Couldn't find JSON atlas for Icons: {0}".format(json_icons))

def print_usage():
    print 'Usage: '
    print 'icon_packer.py -i <icon input paths> -o <output directory> -f <platform format>'
    print 'icon_packer.py [-h | -help]'
    print
    print 'Options: '
    print '-i --input_paths      Comma seperated list of directories containing the icon assets.'
    print '                      iOS needs 3 (1,2,3), Android needs 5 (.75,1,1.5,2,3) and windows needs 3 (1,1.5,2)'
    print '-o --output_path      For pin sheet, output pin sheet name. For icons, output with this prefix + name.png'
    print '-f --output_format    Either "ios", "android" or "win". Number of input paths must match.'
    print '-p --json_pin_sheet   JSON atlas for the pin sheet at scale 1x'
    print '-m --json_icons       JSON atlas for the individual icons'

FORMAT_IOS="ios"
FORMAT_ANDROID="android"
FORMAT_WINDOWS="windows"
FORMAT_JS="js"

IOS_SCALES=[1,2,3]
ANDROID_SCALES=[0.75,1,1.5,2,3]
ANDROID_DENSITY_BUCKETS={0.75:"res/drawable-ldpi",1:"res/drawable-mdpi",1.5:"res/drawable-hdpi",2:"res/drawable-xhdpi", 3:"res/drawable-xxhdpi"}
WINDOWS_SCALES=[1,1.5,2]

def get_args(argv):

    input_paths = ''
    output_path = ''
    output_format = ''
    json_pin_sheet = ''
    json_icons = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:f:p:m:",
                                   ["input_paths=", "output_path=", "output_format=", "json_pin_sheet=", "json_icons="])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit()
        elif opt in ("-i", "--input_paths"):
            input_paths = arg
        elif opt in ("-o", "--output_path"):
            output_path = arg
        elif opt in ("-f", "--output_format"):
            output_format = arg
        elif opt in ("-p", "--json_pin_sheet"):
            json_pin_sheet = arg
        elif opt in ("-m", "--json_icons"):
            json_icons = arg

    return input_paths, output_path, output_format, json_pin_sheet, json_icons


def validate_paths(input_paths, expected_scales):
    input_count = len(input_paths)
    expected_count = len(expected_scales)

    if input_count != expected_count:
        raise ValueError("Not enough input paths defined: Expected {0} but got {1}".format(expected_count, input_count))

    for path in input_paths:
        if not os.path.exists(path):
            raise ValueError("Cannot find input path: {0}".format(path))

def output_for_platform(input_paths, output_path, scales, output_formatter):
    validate_paths(input_paths, scales)

    scale_index = 0
    for path in input_paths:
        scale = scales[scale_index]
        scale_index+=1
        examined_path = path + os.sep + "*.png"
        for image_path in glob.glob(examined_path):

            base_filename = os.path.basename(image_path)
            base_filename = base_filename[:len(base_filename)-4]

            output_formatter(image_path, base_filename, output_path, scale)

def ios_formatter(image_path, base_filename, output_path, scale):
    new_filename = base_filename
    if scale is not 1:
        new_filename += "@{0}x".format(scale)

    if "pin_sheet" in new_filename:
        new_filename = "{0}{1}{2}".format("SearchResultOnMap", os.sep, new_filename)

    new_filename = "{0}{1}{2}.png".format(output_path, os.sep, new_filename)
    print "Moving {0} to {1}".format(image_path, new_filename)
    shutil.copyfile(image_path, new_filename)

def android_formatter(image_path, base_filename, output_path, scale):
    new_filename = base_filename
    if "pin_sheet" in new_filename:
        if scale is not 1:
            new_filename += "@{0}x".format(scale)
        new_filename = "{0}{1}assets{1}SearchResultOnMap{1}{2}.png".format(output_path, os.sep, new_filename)
        shutil.copyfile(image_path, new_filename)
    else:
        density_bucket_name = ANDROID_DENSITY_BUCKETS[scale]

        new_filename = "{0}{1}{2}{1}{3}.png".format(output_path, os.sep, density_bucket_name, new_filename)
        print "Moving {0} to {1}".format(image_path, new_filename)
        shutil.copyfile(image_path, new_filename)

def windows_formatter(image_path, base_filename, output_path, scale):
    new_filename = base_filename
    if scale is not 1:
        new_filename += "@{0}x".format(scale)

    if "pin_sheet" in new_filename:
        if scale == 1.5:
            return
        new_filename = "{0}{1}{2}".format("SearchResultOnMap", os.sep, new_filename)
    elif scale == 2:
        return

    new_filename = "{0}{1}{2}.png".format(output_path, os.sep, new_filename)
    print "Moving {0} to {1}".format(image_path, new_filename)
    shutil.copyfile(image_path, new_filename)

def js_formatter(image_path, base_filename, output_path, scale):
    new_filename = base_filename

    new_filename = "{0}{1}{2}.png".format(output_path, os.sep, new_filename)
    print "Moving {0} to {1}".format(image_path, new_filename)
    shutil.copyfile(image_path, new_filename)

def output_for_ios(input_paths, output_path, json_pin_sheet, json_icons):
    output_for_platform(input_paths, output_path, IOS_SCALES, ios_formatter)

    print "Moving JSON atlas files"
    shutil.copyfile(json_pin_sheet, "{0}{1}SearchResultOnMap{1}{2}".format(output_path, os.sep, os.path.basename(json_pin_sheet)))
    shutil.copyfile(json_icons, "{0}{1}{2}".format(output_path, os.sep, os.path.basename(json_icons)))

def output_for_android(input_paths, output_path, json_pin_sheet, json_icons):
    output_for_platform(input_paths, output_path, ANDROID_SCALES, android_formatter)

    print "Moving JSON atlas files"
    shutil.copyfile(json_pin_sheet, "{0}{1}assets{1}SearchResultOnMap{1}{2}".format(output_path, os.sep, os.path.basename(json_pin_sheet)))
    shutil.copyfile(json_icons, "{0}{1}assets{1}{2}".format(output_path, os.sep, os.path.basename(json_icons)))

def output_for_windows(input_paths, output_path, json_pin_sheet, json_icons):
    output_for_platform(input_paths, output_path, WINDOWS_SCALES, windows_formatter)

    print "Moving JSON atlas files"
    shutil.copyfile(json_pin_sheet, "{0}{1}SearchResultOnMap{1}{2}".format(output_path, os.sep, os.path.basename(json_pin_sheet)))
    shutil.copyfile(json_icons, "{0}{1}{2}".format(output_path, os.sep, os.path.basename(json_icons)))


def output_for_javascript(input_paths, output_path, json_pin_sheet, json_icons):
    output_for_platform(input_paths, output_path, [1], js_formatter)


if __name__ == "__main__":
    try:
        input_paths, output_path, output_format, json_pin_sheet, json_icons  = get_args(sys.argv[1:])

        try:
            __validate_params(input_paths, output_path, output_format, json_pin_sheet, json_icons)
        except ValueError as err:
            print "Error: {0}".format(err.message)
            print_usage()
            sys.exit(1)

        print 'input_paths: ' + input_paths
        print 'output_path: ' + output_path
        print 'output_format: ' + output_format
        print 'json_pin_sheet: ' + json_pin_sheet
        print 'json_icons: ' + json_icons

        inputs = input_paths.split(',')

        if FORMAT_IOS in output_format:
            output_for_ios(inputs, output_path, json_pin_sheet, json_icons)
        elif FORMAT_ANDROID in output_format:
            output_for_android(inputs, output_path, json_pin_sheet, json_icons)
        elif FORMAT_WINDOWS in output_format:
            output_for_windows(inputs, output_path, json_pin_sheet, json_icons)
        elif FORMAT_JS in output_format:
            output_for_javascript(inputs, output_path, json_pin_sheet, json_icons)
        else:
            raise ValueError("Unrecognized format '{0}'".format(output_format))

    except Exception as e:
        _, _, exc_traceback = sys.exc_info()
        print(str(traceback.format_exc(exc_traceback)))
        sys.exit(1)