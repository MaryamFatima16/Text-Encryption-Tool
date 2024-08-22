import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend

# Initialize backend and keys
backend = default_backend()
aes_key = b'0011223344556677'  # Example AES key (16 bytes)
des_key = b'0102030405060708'  # Example DES key (8 bytes)
rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=backend)

def aes_encrypt(text):
    """
    Encrypts text using AES encryption in ECB mode.
    """
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    # Pad text to be multiple of AES block size (16 bytes)
    padded_text = text + (16 - len(text) % 16) * chr(16 - len(text) % 16)
    return encryptor.update(padded_text.encode()) + encryptor.finalize()

def aes_decrypt(ciphertext):
    """
    Decrypts text using AES decryption in ECB mode.
    """
    cipher = Cipher(algorithms.AES(aes_key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    padding_len = padded_text[-1]
    return padded_text[:-padding_len].decode()

def des_encrypt(text):
    """
    Encrypts text using DES encryption in ECB mode.
    """
    cipher = Cipher(algorithms.TripleDES(des_key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    # Pad text to be multiple of DES block size (8 bytes)
    padded_text = text + (8 - len(text) % 8) * chr(8 - len(text) % 8)
    return encryptor.update(padded_text.encode()) + encryptor.finalize()

def des_decrypt(ciphertext):
    """
    Decrypts text using DES decryption in ECB mode.
    """
    cipher = Cipher(algorithms.TripleDES(des_key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    padded_text = decryptor.update(ciphertext) + decryptor.finalize()
    padding_len = padded_text[-1]
    return padded_text[:-padding_len].decode()

def rsa_encrypt(text):
    """
    Encrypts text using RSA encryption.
    """
    public_key = rsa_key.public_key()
    ciphertext = public_key.encrypt(
        text.encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return ciphertext

def rsa_decrypt(ciphertext):
    """
    Decrypts text using RSA decryption.
    """
    plaintext = rsa_key.decrypt(
        ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return plaintext.decode()

def encrypt_text():
    """
    Encrypts text based on the selected encryption method and displays the result.
    """
    text = text_entry.get("1.0", tk.END).strip()
    if encryption_method.get() == "AES":
        encrypted = aes_encrypt(text)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, encrypted.hex())
    elif encryption_method.get() == "DES":
        encrypted = des_encrypt(text)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, encrypted.hex())
    elif encryption_method.get() == "RSA":
        encrypted = rsa_encrypt(text)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, encrypted.hex())

def decrypt_text():
    """
    Decrypts text based on the selected encryption method and displays the result.
    """
    text = text_entry.get("1.0", tk.END).strip()
    try:
        ciphertext = bytes.fromhex(text)
        if encryption_method.get() == "AES":
            decrypted = aes_decrypt(ciphertext)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, decrypted)
        elif encryption_method.get() == "DES":
            decrypted = des_decrypt(ciphertext)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, decrypted)
        elif encryption_method.get() == "RSA":
            decrypted = rsa_decrypt(ciphertext)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, decrypted)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_public_key():
    """
    Displays the public RSA key in PEM format.
    """
    public_key = rsa_key.public_key()
    try:
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        key_display.delete("1.0", tk.END)
        key_display.insert(tk.END, public_key_pem.decode())
    except Exception as e:
        messagebox.showerror("Error", f"Failed to display public key: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Text Encryption Tool")
root.geometry("600x700")

# Colors and Styles
bg_color = "lavender"
but_color = "#EFD469"
fg_color = "black"
btn_bg_color = "pale violet red"
btn_fg_color = "black"
entry_bg_color = "light yellow"
entry_fg_color = "dark blue"

root.configure(bg=bg_color)

# Encryption and Decryption Section
tk.Label(root, text="Enter text:", bg=bg_color, fg=fg_color, font=("Arial", 12, "bold")).pack(pady=5)
text_entry = tk.Text(root, height=5, width=60, bg=entry_bg_color, fg=entry_fg_color, font=("Arial", 10))
text_entry.pack(pady=5)

tk.Label(root, text="Select Encryption Method:", bg=bg_color, fg=fg_color, font=("Arial", 12, "bold")).pack(pady=5)
encryption_method = tk.StringVar(value="AES")
radio_frame = tk.Frame(root, bg=bg_color)
radio_frame.pack(pady=5)

tk.Radiobutton(radio_frame, text="AES", variable=encryption_method, value="AES", bg=but_color, relief="raised", bd=2, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(radio_frame, text="DES", variable=encryption_method, value="DES", bg=but_color, relief="raised", bd=2, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(radio_frame, text="RSA", variable=encryption_method, value="RSA", bg=but_color, relief="raised", bd=2, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10)

tk.Button(root, text="Encrypt", command=encrypt_text, bg=btn_bg_color, fg=btn_fg_color, font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(root, text="Decrypt", command=decrypt_text, bg=btn_bg_color, fg=btn_fg_color, font=("Arial", 12, "bold")).pack(pady=5)

tk.Label(root, text="Result:", bg=bg_color, fg=fg_color, font=("Arial", 12, "bold")).pack(pady=5)
result_text = tk.Text(root, height=5, width=60, bg=entry_bg_color, fg=entry_fg_color, font=("Arial", 10))
result_text.pack(pady=5)

# Public Key Section
tk.Label(root, text="Public Key:", bg=bg_color, fg=fg_color, font=("Arial", 12, "bold")).pack(pady=5)
key_display = tk.Text(root, height=10, width=60, bg=entry_bg_color, fg=entry_fg_color, font=("Arial", 10))
key_display.pack(pady=5)

tk.Button(root, text="Show Public Key", command=show_public_key, bg=btn_bg_color, fg=btn_fg_color, font=("Arial", 12, "bold")).pack(pady=5)

root.mainloop()
