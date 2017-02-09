from PIL import Image


def sort_by_area(item):
    image = item[1]
    return image.width*image.height

class SimpleTexturePacker:

    def __get_indices_for_images(self, image_pairs):
        current_index=0
        indices={}
        for image_pair in image_pairs:
            image_id = image_pair[0]
            indices[image_id]=current_index
            current_index+=1
        return indices

    def __try_insert_image(self, sheet, image_pair, final_image_size, scale):

        image = image_pair[1]

        # Need to perform the packing at scale=1 so coordinates are consistent across all scales.
        scaled_image_size=int(final_image_size/scale)
        scaled_image_width=int(image.width/scale)
        scaled_image_height=int(image.height/scale)

        for y in range(0, scaled_image_size-scaled_image_height):
            for x in range(0, scaled_image_size-scaled_image_width):

                possible_left=x
                possible_right=x+scaled_image_width
                possible_top=y
                possible_bottom=y+scaled_image_height

                can_fit = True
                for existing_image in sheet:
                    coords = existing_image["coords"]
                    left=coords[0]
                    top=coords[1]
                    right=coords[2]
                    bottom=coords[3]

                    # intersection test
                    if not (possible_right < left or possible_left > right or possible_top > bottom or possible_bottom < top):
                        can_fit = False

                    if not can_fit:
                        break

                if can_fit:
                    sheet.append({"id":image_pair[0],
                                  "image":image_pair[1],
                                  "coords":(possible_left,possible_top,possible_right,possible_bottom)})
                    return True

        return False


    def pack_images(self, image_pairs, scale, final_image_size=512):

        icons_metadata=[]

        # Before sorting, pull out the order the images were defined in and persist this to the metadata
        ids_to_indices = self.__get_indices_for_images(image_pairs)

        # sort by area
        sorted_image_pairs = sorted(image_pairs, key=sort_by_area, reverse=True)

        # create root of tree
        image_size=final_image_size
        image_sheets=[]
        image_sheets.append([])

        for image_pair in sorted_image_pairs:
            current_root_index = 0
            success=False

            while not success:
                current_sheet = image_sheets[current_root_index]
                success = self.__try_insert_image(current_sheet, image_pair, final_image_size, scale)
                if not success:
                    # - If you fail, move to next image (create if necessary)
                    current_root_index+=1
                    if current_root_index >= len(image_sheets):
                        image_sheets.append([])

        # TODO: Crop images to minimum height they need

        output_images=[]
        page_index=0
        for icon_list in image_sheets:
            output_image = Image.new('RGBA', (image_size,image_size))

            icon_list=sorted(icon_list,key=lambda item: ids_to_indices[item["id"]])

            for entry in icon_list:
                image_id=entry["id"]
                image=entry["image"]
                coords=entry["coords"]
                final_x=int(coords[0]*scale)
                final_y=int(coords[1]*scale)
                output_image.paste(image, (final_x, final_y))
                icons_metadata.append({"id":image_id, "page":page_index, "x":final_x, "y":final_y, "w":image.width, "h":image.height, "index":ids_to_indices[image_id]})
            output_images.append(output_image)
            page_index+=1

        print "Completed texture pack"
        return output_images, icons_metadata
