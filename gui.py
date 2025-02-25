import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def encrypt():
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png")])
    if not file_path:
        return
    img = cv2.imread(file_path)
    
    msg = entry_msg.get()
    password = entry_pass.get()
    
    if not msg or not password:
        messagebox.showerror("Error", "Message and password cannot be empty")
        return
    
    d = {chr(i): i for i in range(256)}
    height, width, _ = img.shape
    max_chars = (height * width) // 3  # Limit message size
    
    if len(msg) > max_chars:
        messagebox.showerror("Error", "Message too long for this image!")
        return
    
    # Store message length in the first pixel using bitwise operations
    msg_len = len(msg)
    img[0, 0] = (msg_len & 255, (msg_len >> 8) & 255, 0)
    
    n, m, z = 0, 1, 0  # Start encoding from second pixel
    for char in msg:
        img[n, m, z] = d[char]
        z += 1
        if z == 3:
            z = 0
            m += 1
            if m >= width:
                m = 0
                n += 1
                if n >= height:
                    break
    
    encrypted_path = "encryptedImage.png"
    cv2.imwrite(encrypted_path, img)
    messagebox.showinfo("Success", f"Message encrypted! Saved as {encrypted_path}")
    
    os.system(f"start {encrypted_path}")

def decrypt():
    file_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("Image Files", "*.png")])
    if not file_path:
        return
    img = cv2.imread(file_path)
    
    input_pass = entry_pass.get()
    if not input_pass:
        messagebox.showerror("Error", "Password cannot be empty")
        return
    
    c = {i: chr(i) for i in range(256)}
    height, width, _ = img.shape
    
    # Retrieve stored message length correctly
    msg_length = (img[0, 0, 1] << 8) + img[0, 0, 0]
    
    decrypted_msg = ""
    n, m, z = 0, 1, 0
    for _ in range(msg_length):
        decrypted_msg += c.get(img[n, m, z], "?")  # '?' if invalid character
        z += 1
        if z == 3:
            z = 0
            m += 1
            if m >= width:
                m = 0
                n += 1
                if n >= height:
                    break
    
    messagebox.showinfo("Decryption Successful", f"Decrypted Message: {decrypted_msg}")

# GUI Setup
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("400x300")

tk.Label(root, text="Secret Message:").pack()
entry_msg = tk.Entry(root, width=40)
entry_msg.pack()

tk.Label(root, text="Password:").pack()
entry_pass = tk.Entry(root, width=40, show="*")
entry_pass.pack()

tk.Button(root, text="Encrypt Image", command=encrypt).pack(pady=10)
tk.Button(root, text="Decrypt Image", command=decrypt).pack(pady=10)

root.mainloop()