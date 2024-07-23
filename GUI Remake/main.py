import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, colorchooser, font as tkfont
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageDraw, ImageFont, ImageFilter

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("800x600")

        self.image = None
        self.original_image = None
        self.tk_image = None
        self.image_label = None
        self.crop_start_x = None
        self.crop_start_y = None
        self.crop_end_x = None
        self.crop_end_y = None

        self.create_widgets()

    def create_widgets(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Resize", command=self.resize_image)
        edit_menu.add_command(label="Rotate", command=self.rotate_image)
        edit_menu.add_command(label="Grayscale", command=self.apply_grayscale)
        edit_menu.add_command(label="Increase Contrast", command=self.increase_contrast)
        edit_menu.add_command(label="Reset", command=self.reset_image)
        edit_menu.add_command(label="Crop", command=self.initiate_crop)
        edit_menu.add_command(label="Add Text", command=self.add_text)
        edit_menu.add_command(label="Apply Blur", command=self.apply_blur)
        edit_menu.add_command(label="Apply Sharpen", command=self.apply_sharpen)
        edit_menu.add_command(label="Adjust Brightness", command=self.adjust_brightness)
        edit_menu.add_command(label="Adjust Contrast", command=self.adjust_contrast)
        edit_menu.add_command(label="Adjust Color Balance", command=self.adjust_color_balance)

        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.status_bar = tk.Label(self.root, text="No image loaded", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message):
        self.status_bar.config(text=message)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.original_image = self.image.copy()
            self.display_image()
            self.update_status(f"Opened: {file_path}")

    def display_image(self):
        if self.image:
            self.tk_image = ImageTk.PhotoImage(self.image)
            if self.image_label:
                self.image_label.destroy()
            self.image_label = tk.Label(self.canvas, image=self.tk_image)
            self.image_label.pack()

    def resize_image(self):
        if self.image:
            width = simpledialog.askinteger("Resize", "Enter new width:")
            height = simpledialog.askinteger("Resize", "Enter new height:")
            if width and height:
                self.image = self.image.resize((width, height))
                self.display_image()
                self.update_status(f"Resized to {width}x{height}")

    def rotate_image(self):
        if self.image:
            angle = simpledialog.askinteger("Rotate", "Enter rotation angle:")
            if angle is not None:
                self.image = self.image.rotate(angle)
                self.display_image()
                self.update_status(f"Rotated by {angle} degrees")

    def apply_grayscale(self):
        if self.image:
            self.image = ImageOps.grayscale(self.image)
            self.display_image()
            self.update_status("Applied grayscale")

    def increase_contrast(self):
        if self.image:
            enhancer = ImageEnhance.Contrast(self.image)
            factor = simpledialog.askfloat("Contrast", "Enter contrast factor (1.0 for no change):", minvalue=0.0)
            if factor is not None:
                self.image = enhancer.enhance(factor)
                self.display_image()
                self.update_status(f"Contrast increased by factor {factor}")

    def reset_image(self):
        if self.original_image:
            self.image = self.original_image.copy()
            self.display_image()
            self.update_status("Image reset")

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")])
            if file_path:
                self.image.save(file_path)
                messagebox.showinfo("Save Image", "Image saved successfully!")
                self.update_status(f"Saved: {file_path}")

    def initiate_crop(self):
        self.canvas.bind("<ButtonPress-1>", self.on_crop_start)
        self.canvas.bind("<B1-Motion>", self.on_crop_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_crop_end)

    def on_crop_start(self, event):
        if self.image:
            self.crop_start_x = event.x
            self.crop_start_y = event.y

    def on_crop_drag(self, event):
        if self.image:
            self.crop_end_x = event.x
            self.crop_end_y = event.y
            self.canvas.delete("crop")
            self.canvas.create_rectangle(self.crop_start_x, self.crop_start_y, self.crop_end_x, self.crop_end_y, outline="red", tag="crop")

    def on_crop_end(self, event):
        if self.image:
            self.crop_end_x = event.x
            self.crop_end_y = event.y
            self.crop_image()

    def crop_image(self):
        if self.image and self.crop_start_x is not None and self.crop_end_x is not None:
            left = min(self.crop_start_x, self.crop_end_x)
            top = min(self.crop_start_y, self.crop_end_y)
            right = max(self.crop_start_x, self.crop_end_x)
            bottom = max(self.crop_start_y, self.crop_end_y)
            self.image = self.image.crop((left, top, right, bottom))
            self.display_image()
            self.update_status(f"Cropped to box ({left}, {top}, {right}, {bottom})")
            self.canvas.unbind("<ButtonPress-1>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def add_text(self):
        if self.image:
            text = simpledialog.askstring("Add Text", "Enter text to add:")
            x = simpledialog.askinteger("Add Text", "Enter x coordinate for text:")
            y = simpledialog.askinteger("Add Text", "Enter y coordinate for text:")
            color = colorchooser.askcolor()[1]
            font_size = simpledialog.askinteger("Add Text", "Enter font size:", initialvalue=20)
            if text and x is not None and y is not None and color and font_size:
                draw = ImageDraw.Draw(self.image)
                font = ImageFont.truetype("arial.ttf", font_size) if ImageFont.truetype else ImageFont.load_default()
                draw.text((x, y), text, fill=color, font=font)
                self.display_image()
                self.update_status(f"Added text: '{text}' at ({x}, {y})")

    def apply_blur(self):
        if self.image:
            radius = simpledialog.askfloat("Blur", "Enter blur radius:", minvalue=0.0)
            if radius is not None:
                self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
                self.display_image()
                self.update_status(f"Applied blur with radius {radius}")

    def apply_sharpen(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            self.display_image()
            self.update_status("Applied sharpen filter")

    def adjust_brightness(self):
        if self.image:
            brightness = simpledialog.askfloat("Brightness", "Enter brightness factor (1.0 for no change):", minvalue=0.0)
            if brightness is not None:
                enhancer = ImageEnhance.Brightness(self.image)
                self.image = enhancer.enhance(brightness)
                self.display_image()
                self.update_status(f"Brightness adjusted by factor {brightness}")

    def adjust_contrast(self):
        if self.image:
            contrast = simpledialog.askfloat("Contrast", "Enter contrast factor (1.0 for no change):", minvalue=0.0)
            if contrast is not None:
                enhancer = ImageEnhance.Contrast(self.image)
                self.image = enhancer.enhance(contrast)
                self.display_image()
                self.update_status(f"Contrast adjusted by factor {contrast}")

    def adjust_color_balance(self):
        if self.image:
            red = simpledialog.askfloat("Color Balance", "Enter red balance (1.0 for no change):", minvalue=0.0)
            green = simpledialog.askfloat("Color Balance", "Enter green balance (1.0 for no change):", minvalue=0.0)
            blue = simpledialog.askfloat("Color Balance", "Enter blue balance (1.0 for no change):", minvalue=0.0)
            if red is not None and green is not None and blue is not None:
                r, g, b = self.image.split()
                r = r.point(lambda i: i * red)
                g = g.point(lambda i: i * green)
                b = b.point(lambda i: i * blue)
                self.image = Image.merge("RGB", (r, g, b))
                self.display_image()
                self.update_status(f"Adjusted color balance: red={red}, green={green}, blue={blue}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
