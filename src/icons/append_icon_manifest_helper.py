import getopt
import glob
import json
import os
import sys


def get_args(argv):

    input_dir = ''
    input_manifest = ''
    output_manifest = ''
    try:
        opts, args = getopt.getopt(argv, "hi:m:o:",
                                   ["input_dir=", "input_manifest=", "output_manifest="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        elif opt in ("-i", "--input_dir"):
            input_dir = arg
        elif opt in ("-m", "--input_manifest"):
            input_manifest = arg
        elif opt in ("-o", "--output_manifest"):
            output_manifest = arg

    return input_dir, input_manifest, output_manifest

if __name__ == "__main__":

    input_dir, input_manifest, output_manifest = get_args(sys.argv[1:])

    # Load json manifest.
    with open(input_manifest, 'r') as json_input_file:
        icon_manifest = json.load(json_input_file)

    existing_icon_definitions = icon_manifest["icons"]

    already_used_files = []
    for icon_definition in existing_icon_definitions:
        if "file" in icon_definition:
            icon_path = icon_definition["file"]
            already_used_files.append(icon_path)
            file_exists = os.path.basename(icon_path) in os.listdir(input_dir)
            if not file_exists:
                print "{0} for icon '{1}' does not exist!".format(icon_path, icon_definition["id"])
            else:
                print "Found {0}".format(icon_path)

    # Files exist?

    files = glob.glob("{0}/*.svg".format(input_dir))

    for filepath in files:
        filename = "pin/" + os.path.basename(filepath)

        if filename not in already_used_files:
            print "Found unused svg: {0}".format(filename)
            print "Add to definitions? Enter tag name or leave blank to ignore:"
            response = raw_input()

            if response:
                tag_name = response
                existing_icon_definitions.append({"id":tag_name, "file":filename})
                print "Added!"
            else:
                print "Ignoring..."

    print "Finished updating, saving new manifest"

    with open(output_manifest, 'w') as json_output_file:
        json.dump(icon_manifest, json_output_file, indent=1)