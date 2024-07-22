import argparse
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont

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
    watermark_image = Image.open(watermark).convert("RGBA")
    image.paste(watermark_image, position, watermark_image)
    return image

def main():
    parser = argparse.ArgumentParser(description="Command Line Photo Editor")
    parser.add_argument("input", type=str, help="Path to the input image")
    parser.add_argument("output", type=str, help="Path to save the output image")
    parser.add_argument("--resize", type=int, nargs=2, metavar=('width', 'height'), help="Resize the image to the specified width and height")
    parser.add_argument("--rotate", type=int, metavar='angle', help="Rotate the image by the specified angle")
    parser.add_argument("--grayscale", action='store_true', help="Convert the image to grayscale")
    parser.add_argument("--crop", type=int, nargs=4, metavar=('left', 'upper', 'right', 'lower'), help="Crop the image with the specified bounding box")
    parser.add_argument("--flip", type=str, choices=['horizontal', 'vertical'], help="Flip the image horizontally or vertically")
    parser.add_argument("--brightness", type=float, metavar='factor', help="Adjust the brightness of the image. 1.0 means no change")
    parser.add_argument("--blur", type=float, metavar='radius', help="Apply a Gaussian blur to the image with the specified radius")
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
    args = parser.parse_args()

    image = load_image(args.input)
    if image:
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
        save_image(image, args.output)

if __name__ == "__main__":
    main()
