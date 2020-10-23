import os
import subprocess
import sys
from xml.dom import minidom

from PIL import Image, ImageDraw, ImageFilter


class IconImageHelpers:

    BACKGROUND_CIRCLE = "circle"
    TRANSPARENT = (0, 0, 0, 0)

    def __init__(self):
        pass

    @staticmethod
    def draw_circle(image, size, xy, color):
        background_color_alpha = (color[0], color[1], color[2], 0)
        supersample_size = size*2
        circle_image = Image.new('RGBA', (supersample_size, supersample_size), background_color_alpha)
        draw = ImageDraw.Draw(circle_image)
        draw.ellipse([(0, 0), (supersample_size-1, supersample_size-1)], color, None)
        circle_image = circle_image.resize((size, size), Image.ANTIALIAS)
        image.paste(circle_image, xy)

    @staticmethod
    def draw_pin_icon_with_background(image, icon_source, xy, icon_size, cell_size, scale, color_override,
                                      background_type, background_color=None, outline_color=None,
                                      shadow_color=(0,0,0,255)):
        if background_color is None:
            background_color = (255, 255, 255, 255)
        background_color_alpha = (background_color[0], background_color[1], background_color[2], 0)
        if outline_color is None:
            outline_color = IconImageHelpers.TRANSPARENT
        if shadow_color is None:
            shadow_color = IconImageHelpers.TRANSPARENT

        print "Drawing pin icon with circle at {0},{1}".format(xy[0], xy[1])

        circle_size = int(icon_size * scale)
        pin_cell_size = int(cell_size * scale)
        icon_size = int(icon_size * scale)

        background_image = Image.new('RGBA', (pin_cell_size, pin_cell_size), background_color_alpha)

        # Background
        if background_type == IconImageHelpers.BACKGROUND_CIRCLE:
            circle_offset = (pin_cell_size - circle_size)/2
            IconImageHelpers.draw_circle(background_image, circle_size, (circle_offset, circle_offset),
                                         background_color)

        # Icon
        if icon_source:
            icon_image = IconImageHelpers.rasterize_svg(icon_source, icon_size, color_override)
            resized_icon_image = Image.new('RGBA', (pin_cell_size, pin_cell_size))
            icon_position = int((pin_cell_size-icon_size)/2)
            resized_icon_image.paste(icon_image, (icon_position, icon_position))
            resized_icon_image = IconImageHelpers.add_outline(resized_icon_image, int(round(scale)), outline_color)
        else:
            resized_icon_image = Image.new('RGBA', (pin_cell_size, pin_cell_size))

        pin_image = Image.alpha_composite(background_image, resized_icon_image)

        if shadow_color[3] > 0:
            shadow_image = IconImageHelpers.create_drop_shadow_from_image(pin_image, pin_cell_size, shadow_color)
            pin_image = Image.alpha_composite(shadow_image, pin_image)

        image.paste(pin_image, (int(xy[0]*scale), int(xy[1]*scale)))

    @staticmethod
    def create_drop_shadow_from_image(source_image, final_cell_size, color):
        # - Fixed drop shadow + blur, resized to suitable size to allow consistency across different scales
        blur_iterations = 3
        shadow_offset = 2
        shadow_raster_size = 64
        shadow_size = shadow_raster_size+blur_iterations*2
        shadow_image = Image.new('RGBA', (shadow_size, shadow_size), IconImageHelpers.TRANSPARENT)
        shadow_color_image = Image.new('RGBA', (shadow_raster_size, shadow_raster_size), color)
        outline_image = source_image.resize((shadow_raster_size, shadow_raster_size), Image.BICUBIC)
        shadow_image.paste(shadow_color_image, (blur_iterations+shadow_offset, blur_iterations+shadow_offset,blur_iterations+shadow_raster_size+shadow_offset,blur_iterations+shadow_raster_size+shadow_offset), outline_image)
        for i in range(0, blur_iterations):
            shadow_image = shadow_image.filter(ImageFilter.BLUR)

        shadow_image = shadow_image.resize((final_cell_size, final_cell_size), Image.BICUBIC)
        return shadow_image

    @staticmethod
    def draw_menu_icon(image, icon_source, xy, icon_size, scale, color_override, background_color):
        print "Drawing menu icon at {0},{1}".format(xy[0], xy[1])
        icon_size = int(icon_size*scale)
        background_color = IconImageHelpers.TRANSPARENT if background_color is None else background_color
        background_image = Image.new('RGBA', (icon_size, icon_size), background_color)

        if icon_source:
            icon_image = IconImageHelpers.rasterize_svg(icon_source, int(icon_size), color_override)
            background_image = Image.alpha_composite(background_image, icon_image)

        image.paste(background_image, (int(xy[0]*scale), int(xy[1]*scale)), background_image)

    @staticmethod
    def validate_svg(file_path, expected_viewbox_size):
        svg_doc = minidom.parse(file_path)
        svg_tag = svg_doc.getElementsByTagName('svg')[0]
        viewbox = svg_tag.attributes["viewBox"]
        viewbox_dimensions = str(viewbox.value)
        required_dimensions = "0 0 {0} {0}".format(expected_viewbox_size)
        if viewbox_dimensions != required_dimensions:
            raise StandardError("Viewbox coordinates for {0} ({1}) do not match required dimensions {2}".format(
                file_path, viewbox_dimensions, required_dimensions))

    @staticmethod
    def rasterize_svg(icon_source, icon_size, color_override):
        print "Rasterizing {0}".format(icon_source)

        temp_icon_path = "icon.png"

        if sys.platform == "darwin":
            icon_source = os.path.abspath(icon_source)
            temp_icon_path = os.path.abspath(temp_icon_path)

        inkscape_args = ["inkscape", "{0}".format(icon_source), "-o", temp_icon_path, "-w", str(icon_size), "-h", str(icon_size)]
        inkscape_process = subprocess.Popen(inkscape_args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        return_code = inkscape_process.wait()
        process_stdout, process_stderr = inkscape_process.communicate("")

        print process_stdout
        print process_stderr

        print "Raster completed, processing image"
        icon_image = Image.open(temp_icon_path)
        icon_image_copy = icon_image.copy()

        # colouring
        if color_override:
            color_image = Image.new('RGBA', icon_image_copy.size, color_override)
            final_icon_image = Image.new('RGBA', icon_image_copy.size, (255, 255, 255, 0))
            final_icon_image.paste(color_image, (0, 0), icon_image_copy)
        else:
            final_icon_image = icon_image_copy

        os.remove(temp_icon_path)
        return final_icon_image

    @staticmethod
    def add_outline(image, outline_thickness, outline_color):
        source_image = image.copy()
        outline_color_alpha = (outline_color[0], outline_color[1], outline_color[2], 0)

        outline_image = Image.new('RGBA', source_image.size, outline_color_alpha)
        outline_color_image = Image.new('RGBA', source_image.size, outline_color)
        for x in range(-outline_thickness, outline_thickness+1):
            for y in range(-outline_thickness, outline_thickness+1):
                outline_image.paste(outline_color_image, (x, y), source_image)

        source_image = Image.alpha_composite(outline_image, source_image)
        return source_image
