from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import os

# Color definitions
__red__ = "#ea251e"
__background__ = "#264600"
__top__ = "#7cf63c"

# Get the current file path
current_file_path = os.path.dirname(os.path.abspath(__file__))

def load_font(font_path, size):
    """Load a font and check if it renders correctly."""
    try:
        font = ImageFont.truetype(font_path, size)
        # Test rendering a sample string to check if the font works
        img_test = Image.new("RGB", (1, 1))
        draw_test = ImageDraw.Draw(img_test)
        draw_test.text((0, 0), "Test", font=font, fill="black")
        return font
    except Exception as e:
        print(f"Failed to load font '{font_path}': {e}")
        return ImageFont.load_default()

def generate(elements, plant, city_name):
    today_date = datetime.today().strftime("%Y.%m.%d")
    title = f"Risk Factors for {plant}\n{city_name} | {today_date}"

    # Create a blank image with higher resolution
    img_width, img_height = 1080, 1920
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)

    # Load specific fonts
    font_title = load_font(os.path.join(current_file_path, "Poppins/poppins/Poppins-ExtraBold.ttf"), 56)
    font_header = load_font(os.path.join(current_file_path, "Poppins/poppins/Poppins-Bold.ttf"), 50)
    font_text = load_font(os.path.join(current_file_path, "Poppins/poppins/Poppins-Italic.ttf"), 35)

    # Draw the title background   
    draw.rounded_rectangle([(0, -20), (img_width, 220)], radius=20, fill="black", outline="black", width=3)

    # Draw title with padding
    title_y = 35
    for i, line in enumerate(title.split("\n")):
        draw.text((40, title_y + i * 80), line, fill="white", font=font_title)

    y_offset = img_height // 7
    bubble_width = int(img_width*0.9)

    # Load the logo icon
    icon_path = os.path.join(current_file_path, "Icons/logo.png")
    icon = Image.open(icon_path).convert("RGBA") if os.path.exists(icon_path) else None
    if icon:
        icon.thumbnail((icon.width // 6.5, icon.height // 6.5), Image.LANCZOS)
        img.paste(icon, (int(img_width * 0.68), int(img_height * 0.015)), icon)

    # Increased padding for more space
    padding, bubble_padding, text_padding = 40, 40, 40

    for element in elements:
        header, body, status = element["header"], element["body"], element["status"]
        icon_path = os.path.join(current_file_path, element["icon"])

        # Load the element icon
        element_icon = Image.open(icon_path).convert("RGBA").resize((80, 80)) if os.path.exists(icon_path) else None

        if status:
            box_color = __red__
            wrapped_body = textwrap.fill(body, width=45)

            # Calculate text sizes
            header_height = draw.textbbox((0, 0), header, font=font_header)[3] - draw.textbbox((0, 0), header, font=font_header)[1]
            body_height = sum(draw.textbbox((0, 0), line, font=font_text)[3] - draw.textbbox((0, 0), line, font=font_text)[1] for line in wrapped_body.split("\n"))
            bubble_height = header_height + body_height + 2 * padding

            # Calculate x position for centering the bubble
            bubble_x = (img_width - bubble_width) // 2

            # Draw shadowed bubble
            shadow_offset = 10
            shadow_color = (0, 0, 0, 150)
            draw.rounded_rectangle([(bubble_x + shadow_offset, y_offset + shadow_offset), 
                                    (bubble_x + bubble_width + shadow_offset, y_offset + bubble_height + shadow_offset)], 
                                radius=20, fill=shadow_color)

            # Draw the actual bubble
            draw.rounded_rectangle([(bubble_x, y_offset), (bubble_x + bubble_width, y_offset + bubble_height)], 
                                radius=20, fill="white", outline="black", width=3)
            draw.rounded_rectangle([(bubble_x, y_offset), (bubble_x + 125, y_offset + bubble_height)], 
                                radius=20, fill=box_color, outline="black", width=3)

            text_x = bubble_x + text_padding  # Adjust text start position after icon

            # Paste icon (if available)
            if element_icon:
                img.paste(element_icon, (text_x - 15, y_offset + round(bubble_height / 2) - 30), element_icon)
                text_x += 100  # Adjust text to avoid overlapping icon

            # Draw header text with padding
            draw.text((text_x, y_offset + 20), header, fill="black", font=font_header)

            # Define a list of words to be bolded
            bold_words = ["Stress",
                          "Buster", 
                          "Yield", 
                          "Booster",
                          "Buster.", 
                          "Booster."]  # Add any words you want to be bolded

            # Draw body text with increased line spacing and padding
            line_height = draw.textbbox((0, 0), "A", font=font_text)[3] - draw.textbbox((0, 0), "A", font=font_text)[1]
            for i, line in enumerate(wrapped_body.split("\n")):
                line_y = y_offset + header_height + padding + i * (line_height + 10)  # Added 10 pixels for extra line spacing
                words = line.split()  # Split the line into words
                text_x = bubble_x + text_padding  # Reset text_x for each line
                if element_icon: text_x += 100  # Adjust text to avoid overlapping icon

                for word in words:
                    # Check if the word should be bold
                    if word in bold_words:  # Use lower() for case-insensitive matching
                        font_to_use = load_font(os.path.join(current_file_path, "Poppins/poppins/Poppins-SemiBoldItalic.ttf"), 35)  # Use bold font for the word
                        print(word)
                    else:
                        font_to_use = font_text  # Use regular font

                    # Draw the word
                    draw.text((text_x, line_y), word, fill="black", font=font_to_use)

                    # Update the text_x position based on the width of the drawn word
                    text_x += draw.textbbox((0, 0), word, font=font_to_use)[2] - draw.textbbox((0, 0), word, font=font_to_use)[0] + 10  # Add some space between words

            # Update y_offset to position next bubble with additional padding
            y_offset += bubble_height + bubble_padding

    return img
