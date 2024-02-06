from PIL import Image, ImageDraw, ImageFont
import numpy as np
import platform
import os

def add_text_to_image(
        img_input, 
        text, 
        align='center', 
        y_pos=0.5, 
        font_name='Arial',
        font_size=20,
        min_width=0,
        max_width=1,
        font_color=(0, 0, 0),
        font_type=None
        ):
    """
    Add text to an image with specified alignment, position, font, size, and style.

    Args:
        img_input (tuple, np.ndarray, Image.Image): Input image, can be a tuple of (width, height),
                                                    a numpy array, or a PIL Image.
        text (str): Text to be added to the image.
        align (str, optional): Text alignment on the image. Options: 'left', 'center', 'right'. 
                               Defaults to 'center'.
        y_pos (float, optional): Vertical position of text, as a fraction of image height. 
                                 Defaults to 0.5.
        font_name (str, optional): Name of the font to be used. Defaults to 'Arial'.
        font_size (int, optional): Initial font size. Adjusts to fit min_width and max_width. 
                                   Defaults to 20.
        min_width (float, optional): Minimum width of text as a fraction of image width. 
                                     Defaults to 0.
        max_width (float, optional): Maximum width of text as a fraction of image width. 
                                     Defaults to 1.
        font_color (tuple, optional): Font color in RGB. Defaults to black (0, 0, 0).
        font_type (str, optional): Font style, can be 'italic', 'bold', or 'bold/italic'. 
                                    Defaults to None.

    Returns:
        Image.Image: PIL Image with text added.
    """
    
    # Create an image or load it based on the type of img_input
    if isinstance(img_input, tuple):
        image = Image.new('RGB', img_input, color=(255, 255, 255))
    elif isinstance(img_input, np.ndarray):
        image = Image.fromarray(img_input)
    elif isinstance(img_input, Image.Image):
        image = img_input
    else:
        raise ValueError("img_input must be a PIL.Image, numpy array, or a (width, height) tuple.")
    
    draw = ImageDraw.Draw(image)
    width, height = image.size
    
    scaled_min_width = min_width * width
    scaled_max_width = max_width * width
    
    # Determine font path based on OS and style
    os_name = platform.system()
    font_extension = '.ttf'
    if font_type == 'italic':
        font_extension = 'i.ttf'
    elif font_type == 'bold':
        font_extension = 'bd.ttf'
    
    if os_name == "Darwin":  # macOS
        font_path = f"/System/Library/Fonts/{font_name}{font_extension}"
    elif os_name == "Linux":
        font_path = f"/usr/share/fonts/truetype/{font_name}{font_extension}"
    elif os_name == "Windows":
        font_path = f"C:\\Windows\\Fonts\\{font_name}{font_extension}"
    else:
        raise ValueError("Unsupported operating system for font path.")
        
    assert os.path.exists(font_path), f"{font_path} does not exist! "
    
    font = ImageFont.truetype(font_path, font_size)
    text_width = draw.textlength(text, font=font)
    
    # Adjust font size to fit within min and max width constraints
    while (text_width < scaled_min_width or text_width > scaled_max_width) and font_size < height:
        if text_width < scaled_min_width:
            font_size += 1
        else:
            font_size -= 1
    
        font = ImageFont.truetype(font_path, font_size)
        text_width = draw.textlength(text, font=font)
    
    # Calculate text position based on alignment
    text_height = font_size
    if align == 'left':
        x = 0
    elif align == 'center':
        x = (width - text_width) // 2
    elif align == 'right':
        x = width - text_width
    else:
        raise ValueError("align must be 'left', 'center', or 'right'")
    
    y = int(y_pos * (height - text_height))
    
    draw.text((x, y), text, font=font, fill=font_color)
    
    return image



if __name__ == "__main__":
    # Creating new samples using the updated function
    image1 = add_text_to_image((700, 500), 'Center Aligned', font_size=50, font_name='Calibri', font_type="bold")