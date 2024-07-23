import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageEnhance

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("800x600")

        self.image = None
        self.original_image = None
        self.tk_image = None
        self.image_label = None

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

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
