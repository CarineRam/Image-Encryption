from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Open the image and convert it to bytes
def encrypt_image(image_path, key):
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        image_bytes = img.tobytes()
        width, height = img.size
    
    # Initialize AES cipher
    cipher = AES.new(key, AES.MODE_CBC)
    
    # Encrypt the image bytes
    encrypted_bytes = cipher.encrypt(pad(image_bytes, AES.block_size))
    
    # Save the encrypted image bytes and IV
    with open("encrypted_image.bin", "wb") as f:
        f.write(cipher.iv)
        f.write(encrypted_bytes)
    
    print("Image encrypted and saved as 'encrypted_image.bin'")
    return width, height

def decrypt_image(encrypted_path, key, width, height):
    with open(encrypted_path, "rb") as f:
        iv = f.read(16)
        encrypted_bytes = f.read()
    
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_bytes = unpad(cipher.decrypt(encrypted_bytes), AES.block_size)
    
    # Convert bytes back to image
    img = Image.frombytes("RGB", (width, height), decrypted_bytes)
    img.save("decrypted_image.png")
    
    print("Image decrypted and saved as 'decrypted_image.png'")

key = os.urandom(16)  # Generate a random 16-byte key
width, height = encrypt_image("./totoro.jpg", key)
decrypt_image("encrypted_image.bin", key, width, height)
