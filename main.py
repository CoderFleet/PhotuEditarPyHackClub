import os
import io
import argparse
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont, ImageChops, ImageCms
import matplotlib.pyplot as plt

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

def overlay_image(base_image, overlay_image, position, opacity):
    overlay = Image.open(overlay_image).convert("RGBA")
    overlay = overlay.resize((base_image.size[0], base_image.size[1]), Image.ANTIALIAS)
    base_image = base_image.convert("RGBA")
    blended = Image.blend(base_image, overlay, opacity)
    return blended.convert("RGB")

def display_histogram(image):
    image_array = ImageOps.grayscale(image)
    plt.hist(image_array.getdata(), bins=256, range=(0, 256), density=True, color='black')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Image Histogram')
    plt.show()

def apply_filter(image, filter_name):
    filters = {
        'emboss': ImageFilter.EMBOSS,
        'contour': ImageFilter.CONTOUR,
        'find_edges': ImageFilter.FIND_EDGES,
        'detail': ImageFilter.DETAIL,
        'edge_enhance_more': ImageFilter.EDGE_ENHANCE_MORE
    }
    if filter_name in filters:
        return image.filter(filters[filter_name])
    else:
        print(f"Unknown filter: {filter_name}")
        return image

def validate_args(args):
    if args.resize and (len(args.resize) != 2 or not all(isinstance(x, int) for x in args.resize)):
        raise ValueError("Invalid --resize values. Provide two integer values for width and height.")
    if args.crop and (len(args.crop) != 4 or not all(isinstance(x, int) for x in args.crop)):
        raise ValueError("Invalid --crop values. Provide four integer values for left, upper, right, and lower.")
    if args.text_position and (len(args.text_position) != 2 or not all(isinstance(x, int) for x in args.text_position)):
        raise ValueError("Invalid --text_position values. Provide two integer values for x and y.")
    if args.color_transform and (len(args.color_transform) != 12 or not all(isinstance(x, float) for x in args.color_transform)):
        raise ValueError("Invalid --color_transform values. Provide twelve float values for the matrix.")
    if args.overlay and not os.path.exists(args.overlay):
        raise ValueError("Invalid --overlay value. The specified file does not exist.")

def process_image(image, args):
    if args.resize:
        image = resize_image(image, args.resize[0], args.resize[1])
    if args.rotate:
        image = rotate_image(image, args.rotate)
    if args.grayscale:
        image = convert_to_grayscale(image)
    if args.crop:
        image = crop_image(image, args.crop[0], args.crop[1], args.crop[2], args.crop[3])
    if args.flip:
        image = flip_image(image, args.flip)
    if args.brightness:
        image = adjust_brightness(image, args.brightness)
    if args.blur:
        image = blur_image(image, args.blur)
    if args.contrast:
        image = adjust_contrast(image, args.contrast)
    if args.sharpen:
        image = sharpen_image(image)
    if args.edge_enhance:
        image = edge_enhance_image(image)
    if args.color:
        image = adjust_color(image, args.color)
    if args.saturation:
        image = adjust_saturation(image, args.saturation)
    if args.text:
        if args.text_position and args.text_size and args.text_color:
            image = add_text(image, args.text, tuple(args.text_position), args.text_size, args.text_color)
        else:
            print("Error: To add text, you must specify --text_position, --text_size, and --text_color")
    if args.watermark:
        if args.watermark_position:
            image = add_watermark(image, args.watermark, tuple(args.watermark_position))
        else:
            print("Error: To add a watermark, you must specify --watermark_position")
    if args.equalize:
        image = equalize_histogram(image)
    if args.invert:
        image = invert_colors(image)
    if args.blend:
        if args.blend_alpha:
            blend_image = load_image(args.blend)
            if blend_image:
                image = blend_images(image, blend_image, args.blend_alpha)
            else:
                print("Error: Could not load blend image")
        else:
            print("Error: To blend images, you must specify --blend_alpha")
    if args.color_transform:
        if len(args.color_transform) == 12:
            matrix = tuple(args.color_transform)
            image = apply_color_transform(image, matrix)
        else:
            print("Error: Color transform matrix must have 12 elements")
    if args.format:
        image = handle_different_formats(image, args.format)
    if args.overlay:
        if args.overlay_opacity is not None:
            image = overlay_image(image, args.overlay, (0, 0), args.overlay_opacity)
        else:
            print("Error: To overlay images, you must specify --overlay_opacity")
    if args.histogram:
        display_histogram(image)
    if args.filter:
        image = apply_filter(image, args.filter)
    return image

def process_directory(input_dir, output_dir, args):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    summary = []
    log_file = os.path.join(output_dir, "processing_log.txt")
    with open(log_file, "w") as log:
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
                        log.write(f"Processed: {file_name}\n")
                    except Exception as e:
                        print(f"Error processing {file_name}: {e}")
                        log.write(f"Error processing {file_name}: {e}\n")

    if summary:
        print("\nSummary Report:")
        for item in summary:
            print(item)

def main():
    parser = argparse.ArgumentParser(
        description="Image Processing Tool",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Usage Examples:
        python image_tool.py --input input.jpg --output output.jpg --resize 800 600
        python image_tool.py --input input.jpg --output output.jpg --rotate 90
        python image_tool.py --input input.jpg --output output.jpg --grayscale
        python image_tool.py --input input.jpg --output output.jpg --crop 10 10 200 200
        python image_tool.py --input input.jpg --output output.jpg --brightness 1.5
        python image_tool.py --input input.jpg --output output.jpg --blur 2
        python image_tool.py --input input.jpg --output output.jpg --contrast 1.3
        python image_tool.py --input input.jpg --output output.jpg --text "Hello World" --text_position 100 100 --text_size 20 --text_color "blue"
        python image_tool.py --input input.jpg --output output.jpg --overlay overlay.png --overlay_opacity 0.5
        """
    )

    parser.add_argument("--input", required=True, help="Input image path or directory")
    parser.add_argument("--output", required=True, help="Output image path or directory")
    parser.add_argument("--resize", type=int, nargs=2, metavar=('width', 'height'), help="Resize the image to the specified width and height")
    parser.add_argument("--rotate", type=int, metavar='angle', help="Rotate the image by the specified angle")
    parser.add_argument("--grayscale", action='store_true', help="Convert the image to grayscale")
    parser.add_argument("--crop", type=int, nargs=4, metavar=('left', 'upper', 'right', 'lower'), help="Crop the image with the specified coordinates")
    parser.add_argument("--flip", choices=['horizontal', 'vertical'], help="Flip the image horizontally or vertically")
    parser.add_argument("--brightness", type=float, metavar='factor', help="Adjust the brightness of the image. 1.0 means no change")
    parser.add_argument("--blur", type=float, metavar='radius', help="Apply Gaussian blur to the image")
    parser.add_argument("--contrast", type=float, metavar='factor', help="Adjust the contrast of the image. 1.0 means no change")
    parser.add_argument("--sharpen", action='store_true', help="Apply sharpening filter to the image")
    parser.add_argument("--edge_enhance", action='store_true', help="Apply edge enhancement filter to the image")
    parser.add_argument("--color", type=float, metavar='factor', help="Adjust the color balance of the image. 1.0 means no change")
    parser.add_argument("--saturation", type=float, metavar='factor', help="Adjust the saturation of the image. 1.0 means no change")
    parser.add_argument("--text", type=str, metavar='text', help="Add text overlay to the image")
    parser.add_argument("--text_position", type=int, nargs=2, metavar=('x', 'y'), help="Position of the text overlay")
    parser.add_argument("--text_size", type=int, metavar='font_size', help="Font size of the text overlay")
    parser.add_argument("--text_color", type=str, metavar='font_color', help="Font color of the text overlay")
    parser.add_argument("--watermark", type=str, metavar='watermark_path', help="Add a watermark to the image")
    parser.add_argument("--watermark_position", type=int, nargs=2, metavar=('x', 'y'), help="Position of the watermark")
    parser.add_argument("--equalize", action='store_true', help="Equalize the image histogram")
    parser.add_argument("--invert", action='store_true', help="Invert the colors of the image")
    parser.add_argument("--blend", type=str, metavar='blend_image_path', help="Blend the input image with another image")
    parser.add_argument("--blend_alpha", type=float, metavar='alpha', help="Alpha value for blending images")
    parser.add_argument("--color_transform", type=float, nargs=12, metavar='matrix', help="Apply a color transformation matrix to the image")
    parser.add_argument("--format", type=str, choices=['JPEG', 'PNG', 'BMP', 'GIF'], help="Convert the image to the specified format")
    parser.add_argument("--batch", action='store_true', help="Process all images in the input directory")
    parser.add_argument("--overlay", type=str, metavar='overlay_path', help="Overlay another image onto the input image")
    parser.add_argument("--overlay_opacity", type=float, metavar='opacity', help="Opacity of the overlay image")
    parser.add_argument("--histogram", action='store_true', help="Display the histogram of the image")
    parser.add_argument("--filter", choices=['emboss', 'contour', 'find_edges', 'detail', 'edge_enhance_more'], help="Apply a filter to the image")

    args = parser.parse_args()

    try:
        validate_args(args)
        if os.path.isdir(args.input) and args.batch:
            process_directory(args.input, args.output, args)
        else:
            image = load_image(args.input)
            if image:
                processed_image = process_image(image, args)
                save_image(processed_image, args.output)
    except ValueError as ve:
        print(f"Argument Error: {ve}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()
