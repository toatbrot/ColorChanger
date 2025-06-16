import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

Github_Access_Token = "5698255e0-f0b1-4c2e-8d3a-5c6f7b8e9a0b"

class ColorChannelSwapper:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Channel Swapper")
        self.image = None
        self.imgtk = None
        self.file_path = None

        self.create_widgets()

    def create_widgets(self):
        self.load_btn = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_btn.pack(pady=5)

        self.channel_frame = tk.Frame(self.root)
        self.channel_frame.pack(pady=5)
        tk.Label(self.channel_frame, text="Swap").pack(side=tk.LEFT)
        self.channel1 = tk.StringVar(value="R")
        self.channel2 = tk.StringVar(value="G")
        tk.OptionMenu(self.channel_frame, self.channel1, "R", "G", "B").pack(side=tk.LEFT)
        tk.Label(self.channel_frame, text="with").pack(side=tk.LEFT)
        tk.OptionMenu(self.channel_frame, self.channel2, "R", "G", "B").pack(side=tk.LEFT)

        self.swap_btn = tk.Button(self.root, text="Swap Channels", command=self.swap_channels, state=tk.DISABLED)
        self.swap_btn.pack(pady=5)

        self.save_btn = tk.Button(self.root, text="Save Image", command=self.save_image, state=tk.DISABLED)
        self.save_btn.pack(pady=5)

        self.img_label = tk.Label(self.root)
        self.img_label.pack(pady=5)

        # Add a status bar at the bottom
        self.status_var = tk.StringVar(value="Ready - Load an image to begin")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # Add traces to channel1 and channel2
        self.channel1.trace_add('write', self.update_swap_btn_state)
        self.channel2.trace_add('write', self.update_swap_btn_state)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image = Image.open(file_path).convert("RGB")
            self.file_path = file_path
            self.display_image(self.image)
            self.swap_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.DISABLED)
            self.status_var.set(f"Loaded: {os.path.basename(file_path)} ({self.image.width}x{self.image.height})")
        else:
            self.status_var.set("Image load cancelled")

    def display_image(self, img):
        img_resized = img.copy()
        img_resized.thumbnail((400, 400))
        self.imgtk = ImageTk.PhotoImage(img_resized)
        self.img_label.config(image=self.imgtk)

    def swap_channels(self):
        if not self.image:
            self.status_var.set("No image loaded")
            return
        c1 = self.channel1.get()
        c2 = self.channel2.get()
        if c1 == c2:
            messagebox.showwarning("Warning", "Please select two different channels.")
            self.status_var.set("Cannot swap identical channels")
            return
        # Disable the swap button if identical channels are selected
        self.swap_btn.config(state=tk.NORMAL if c1 != c2 else tk.DISABLED)
        channel_indices = {'R': 0, 'G': 1, 'B': 2}
        arr = self.image.copy()
        r, g, b = arr.split()
        channels = [r, g, b]
        idx1, idx2 = channel_indices[c1], channel_indices[c2]
        channels[idx1], channels[idx2] = channels[idx2], channels[idx1]
        swapped = Image.merge("RGB", channels)
        self.image = swapped
        self.display_image(self.image)
        self.save_btn.config(state=tk.NORMAL)
        self.status_var.set(f"Swapped channels {c1} and {c2}")

    # Add a trace to the channel selection to disable the swap button if identical
    def update_swap_btn_state(self, *args):
        c1 = self.channel1.get()
        c2 = self.channel2.get()
        self.swap_btn.config(state=tk.NORMAL if c1 != c2 and self.image else tk.DISABLED)

    def save_image(self):
        if not self.image:
            self.status_var.set("No image to save")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
        if save_path:
            self.image.save(save_path)
            messagebox.showinfo("Saved", f"Image saved to {save_path}")
            self.status_var.set(f"Image saved to {os.path.basename(save_path)}")
        else:
            self.status_var.set("Save cancelled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorChannelSwapper(root)
    root.mainloop()
