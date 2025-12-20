"""
Script to convert PNG icon to ICO format for Windows
"""
from PIL import Image
import os

def create_ico():
    """Convert PNG to ICO format with multiple sizes"""
    png_path = os.path.join('assets', 'icon.png')
    ico_path = os.path.join('assets', 'icon.ico')
    
    if not os.path.exists(png_path):
        print(f"Error: {png_path} not found!")
        return
    
    # Open the PNG image
    img = Image.open(png_path)
    
    # Create ICO with multiple sizes (16x16, 32x32, 48x48, 64x64, 128x128, 256x256)
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # Save as ICO
    img.save(ico_path, format='ICO', sizes=icon_sizes)
    print(f"✓ Icon created successfully: {ico_path}")

if __name__ == '__main__':
    create_ico()
