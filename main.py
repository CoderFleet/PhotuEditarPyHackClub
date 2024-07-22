import argparse
from PIL import Image

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

def main():
    parser = argparse.ArgumentParser(description="Command Line Photo Editor")
    parser.add_argument("input", type=str, help="Path to the input image")
    parser.add_argument("output", type=str, help="Path to save the output image")
    args = parser.parse_args()

    image = load_image(args.input)
    if image:
        save_image(image, args.output)

if __name__ == "__main__":
    main()
