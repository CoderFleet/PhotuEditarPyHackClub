import os
import io
import argparse
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont, ImageChops, ImageCms

def load_image(image_path):
    try:
        image = Image.open(image_path)
        print(f"Image loaded successfully: {image_path}")
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def save_image(image, output_path):
    try:
        image.save(output_path)
        print(f"Image saved successfully: {output_path}")
    except Exception as e:
        print(f"Error saving image: {e}")

def resize_image(image, width, height):
    return image.resize((width, height))

def rotate_image(image, angle):
    return image.rotate(angle)

def convert_to_grayscale(image):
    return ImageOps.grayscale(image)

def crop_image(image, left, upper, right, lower):
    return image.crop((left, upper, right, lower))

def flip_image(image, direction):
    if direction == 'horizontal':
        return ImageOps.mirror(image)
    elif direction == 'vertical':
        return ImageOps.flip(image)

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def blur_image(image, radius):
    return image.filter(ImageFilter.GaussianBlur(radius))

def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def sharpen_image(image):
    return image.filter(ImageFilter.SHARPEN)

def edge_enhance_image(image):
    return image.filter(ImageFilter.EDGE_ENHANCE)

def adjust_color(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def adjust_saturation(image, factor):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def add_text(image, text, position, font_size, font_color):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text(position, text, fill=font_color, font=font)
    return image

def add_watermark(image, watermark, position):
    try:
        watermark_image = Image.open(watermark).convert("RGBA")
        image.paste(watermark_image, position, watermark_image)
        return image
    except Exception as e:
        print(f"Error adding watermark: {e}")
        return image

def equalize_histogram(image):
    return ImageOps.equalize(image)

def invert_colors(image):
    return ImageOps.invert(image)

def blend_images(image1, image2, alpha):
    image2 = image2.resize(image1.size)
    return Image.blend(image1, image2, alpha)

def apply_color_transform(image, matrix):
    return image.convert("RGB", matrix)

def handle_different_formats(image, format):
    output = io.BytesIO()
    image.save(output, format=format)
    output.seek(0)
    return Image.open(output)

def validate_args(args):
    if args.resize and (len(args.resize) != 2 or not all(isinstance(x, int) for x in args.resize)):
        raise ValueError("Invalid --resize values. Provide two integer values for width and height.")
    if args.crop and (len(args.crop) != 4 or not all(isinstance(x, int) for x in args.crop)):
        raise ValueError("Invalid --crop values. Provide four integer values for left, upper, right, and lower.")
    if args.text_position and (len(args.text_position) != 2 or not all(isinstance(x, int) for x in args.text_position)):
        raise ValueError("Invalid --text_position values. Provide two integer values for x and y.")
    if args.color_transform and (len(args.color_transform) != 12 or not all(isinstance(x, float) for x in args.color_transform)):
        raise ValueError("Invalid --color_transform values. Provide twelve float values for the matrix.")

def execute_command(image, command):
    if command[0] == 'resize':
        return resize_image(image, command[1], command[2])
    if command[0] == 'rotate':
        return rotate_image(image, command[1])
    if command[0] == 'grayscale':
        return convert_to_grayscale(image)
    if command[0] == 'crop':
        return crop_image(image, command[1], command[2], command[3], command[4])
    if command[0] == 'flip':
        return flip_image(image, command[1])
    if command[0] == 'brightness':
        return adjust_brightness(image, command[1])
    if command[0] == 'blur':
        return blur_image(image, command[1])
    if command[0] == 'contrast':
        return adjust_contrast(image, command[1])
    if command[0] == 'sharpen':
        return sharpen_image(image)
    if command[0] == 'edge_enhance':
        return edge_enhance_image(image)
    if command[0] == 'color':
        return adjust_color(image, command[1])
    if command[0] == 'saturation':
        return adjust_saturation(image, command[1])
    if command[0] == 'text':
        return add_text(image, command[1], command[2], command[3], command[4])
    if command[0] == 'watermark':
        return add_watermark(image, command[1], command[2])
    if command[0] == 'equalize':
        return equalize_histogram(image)
    if command[0] == 'invert':
        return invert_colors(image)
    if command[0] == 'blend':
        blend_image = load_image(command[1])
        if blend_image:
            return blend_images(image, blend_image, command[2])
    if command[0] == 'color_transform':
        if len(command[1]) == 12:
            matrix = tuple(command[1])
            return apply_color_transform(image, matrix)
    if command[0] == 'format':
        return handle_different_formats(image, command[1])
    return image

def process_image(image, args):
    command_sequence = []
    if args.resize:
        command_sequence.append(('resize', args.resize[0], args.resize[1]))
    if args.rotate:
        command_sequence.append(('rotate', args.rotate))
    if args.grayscale:
        command_sequence.append(('grayscale',))
    if args.crop:
        command_sequence.append(('crop', args.crop[0], args.crop[1], args.crop[2], args.crop[3]))
    if args.flip:
        command_sequence.append(('flip', args.flip))
    if args.brightness:
        command_sequence.append(('brightness', args.brightness))
    if args.blur:
        command_sequence.append(('blur', args.blur))
    if args.contrast:
        command_sequence.append(('contrast', args.contrast))
    if args.sharpen:
        command_sequence.append(('sharpen',))
    if args.edge_enhance:
        command_sequence.append(('edge_enhance',))
    if args.color:
        command_sequence.append(('color', args.color))
    if args.saturation:
        command_sequence.append(('saturation', args.saturation))
    if args.text:
        if args.text_position and args.text_size and args.text_color:
            command_sequence.append(('text', args.text, tuple(args.text_position), args.text_size, args.text_color))
    if args.watermark:
        if args.watermark_position:
            command_sequence.append(('watermark', args.watermark, tuple(args.watermark_position)))
    if args.equalize:
        command_sequence.append(('equalize',))
    if args.invert:
        command_sequence.append(('invert',))
    if args.blend:
        if args.blend_alpha:
            command_sequence.append(('blend', args.blend, args.blend_alpha))
    if args.color_transform:
        if len(args.color_transform) == 12:
            command_sequence.append(('color_transform', args.color_transform))
    if args.format:
        command_sequence.append(('format', args.format))

    for command in command_sequence:
        image = execute_command(image, command)

    return image

def process_directory(input_dir, output_dir, args):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    summary = []
    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_dir, file_name)
            output_path = os.path.join(output_dir, file_name)
            image = load_image(input_path)
            if image:
                try:
                    processed_image = process_image(image, args)
                    save_image(processed_image, output_path)
                    summary.append(f"Processed: {file_name}")
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")

    if summary:
        print("\nSummary Report:")
        for item in summary:
            print(item)

def main():
    parser = argparse.ArgumentParser(
        description="Image Processing Tool\n\n"
                    "Author: Rudransh Pratap Singh\n",
        epilog="Examples:\n\n"
               "  Resize image:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --resize 800 600\n\n"
               "  Rotate image:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --rotate 90\n\n"
               "  Convert to grayscale:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --grayscale\n\n"
               "  Crop image:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --crop 100 100 400 400\n\n"
               "  Flip image:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --flip horizontal\n\n"
               "  Adjust brightness:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --brightness 1.5\n\n"
               "  Blur image:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --blur 2.0\n\n"
               "  Add text:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --text 'Hello' --text_position 50 50 --text_size 20 --text_color 'red'\n\n"
               "  Add watermark:\n"
               "    python image_tool.py --input input.jpg --output output.jpg --watermark watermark.png --watermark_position 100 100",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("--input", required=True, help="Input image or directory path")
    parser.add_argument("--output", required=True, help="Output image or directory path")
    parser.add_argument("--resize", type=int, nargs=2, metavar=('width', 'height'), help="Resize the image to the specified width and height")
    parser.add_argument("--rotate", type=int, metavar='angle', help="Rotate the image by the specified angle")
    parser.add_argument("--grayscale", action='store_true', help="Convert the image to grayscale")
    parser.add_argument("--crop", type=int, nargs=4, metavar=('left', 'upper', 'right', 'lower'), help="Crop the image with the specified bounding box")
    parser.add_argument("--flip", choices=['horizontal', 'vertical'], help="Flip the image horizontally or vertically")
    parser.add_argument("--brightness", type=float, metavar='factor', help="Adjust the brightness of the image")
    parser.add_argument("--blur", type=float, metavar='radius', help="Apply Gaussian blur to the image")
    parser.add_argument("--contrast", type=float, metavar='factor', help="Adjust the contrast of the image")
    parser.add_argument("--sharpen", action='store_true', help="Sharpen the image")
    parser.add_argument("--edge_enhance", action='store_true', help="Enhance the edges in the image")
    parser.add_argument("--color", type=float, metavar='factor', help="Adjust the color balance of the image")
    parser.add_argument("--saturation", type=float, metavar='factor', help="Adjust the saturation of the image")
    parser.add_argument("--text", type=str, metavar='text', help="Add text to the image")
    parser.add_argument("--text_position", type=int, nargs=2, metavar=('x', 'y'), help="Specify the position of the text")
    parser.add_argument("--text_size", type=int, metavar='size', help="Specify the font size of the text")
    parser.add_argument("--text_color", type=str, metavar='color', help="Specify the color of the text")
    parser.add_argument("--watermark", type=str, metavar='path', help="Add a watermark image to the image")
    parser.add_argument("--watermark_position", type=int, nargs=2, metavar=('x', 'y'), help="Specify the position of the watermark")
    parser.add_argument("--equalize", action='store_true', help="Equalize the histogram of the image")
    parser.add_argument("--invert", action='store_true', help="Invert the colors of the image")
    parser.add_argument("--blend", type=str, metavar='path', help="Blend the image with another image")
    parser.add_argument("--blend_alpha", type=float, metavar='alpha', help="Specify the alpha value for blending images")
    parser.add_argument("--color_transform", type=float, nargs=12, metavar=('r1', 'r2', 'r3', 'g1', 'g2', 'g3', 'b1', 'b2', 'b3', 'a1', 'a2', 'a3'), help="Apply a color transformation matrix to the image")
    parser.add_argument("--format", type=str, metavar='format', help="Specify the output image format (e.g., PNG, JPEG)")

    args = parser.parse_args()

    validate_args(args)

    if os.path.isdir(args.input):
        process_directory(args.input, args.output, args)
    else:
        image = load_image(args.input)
        if image:
            processed_image = process_image(image, args)
            save_image(processed_image, args.output)

if __name__ == "__main__":
    main()
