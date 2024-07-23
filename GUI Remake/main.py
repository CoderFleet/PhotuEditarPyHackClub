import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("800x600")

        self.image = None
        self.tk_image = None
        self.image_label = None

        self.create_widgets()

    def create_widgets(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Exit", command=self.root.quit)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Resize", command=self.resize_image)
        edit_menu.add_command(label="Rotate", command=self.rotate_image)

        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.image = Image.open(file_path)
            self.display_image()

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

    def rotate_image(self):
        if self.image:
            angle = simpledialog.askinteger("Rotate", "Enter rotation angle:")
            if angle is not None:
                self.image = self.image.rotate(angle)
                self.display_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
