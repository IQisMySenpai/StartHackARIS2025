from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import os

__red__="#ea251e"
__backround__="#264600"
__top__="#7cf63c"

def generate(elements, crop_name, city_name):
    today_date = datetime.today().strftime("%Y-%m-%d")
    title = f"Risk Factors - {today_date}\n{crop_name} - {city_name}"

    # Create a blank image with higher resolution
    img = Image.new("RGB", (1200, 1600), "white")  # Increased resolution to 1200x1600
    draw = ImageDraw.Draw(img)

    # Function to load a font and check if it renders correctly
    def load_font(font_path, size):
        try:
            font = ImageFont.truetype(font_path, size)
            # Test rendering a sample string to check if the font works
            test_string = "Test"  # You can use a string with special characters if needed
            img_test = Image.new("RGB", (1, 1))  # Create a small image
            draw_test = ImageDraw.Draw(img_test)
            draw_test.text((0, 0), test_string, font=font, fill="black")  # Attempt to draw text
            return font
        except Exception as e:
            print(f"Failed to load font '{font_path}': {e}")
            return None

    # Load specific fonts with a fallback to default
    font_title = load_font("Poppins/poppins/Poppins-Regular.ttf", 56) or ImageFont.load_default()
    font_header = load_font("Poppins/poppins/Poppins-Bold.ttf", 50) or ImageFont.load_default()
    font_text = load_font("Poppins/poppins/Poppins-Italic.ttf", 35) or ImageFont.load_default()


    # Draw the title background   
    draw.rounded_rectangle([(0, -20), (1200, 220)], 
                               radius=20, fill="black", outline="black", width=3)

    # Draw title with padding and center it
    title_lines = title.split("\n")
    title_y = 35
    for i, line in enumerate(title_lines):
        #text_width = draw.textlength(line, font=font_title)  # Get the width of the text
        text_x = 40 # Make room for syngenta logo
        draw.text((text_x, title_y + i * 80), line, fill="white", font=font_title)

    y_offset = 260
    bubble_width = 1000
    
    # Load the icon from a local file
    icon_path="Icons/logo.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        icon.thumbnail((icon.width // 8, icon.height // 8), Image.LANCZOS)  # Scale down by 50% without distorting
    else:
        print(f"⚠️ Warning: Icon '{icon_path}' not found!")  # Debug message
        icon = None  # Prevent crash
    if icon:
            img.paste(icon, (900,50), icon)  # Paste the icon on the image with transparency
            text_x += 100  # Adjust text to avoid overlapping icon
    # Increased padding for more space
    padding = 40  # Increased padding inside the bubbles
    bubble_padding = 40  # Increased space between each bubble
    text_padding = 40  # Padding for text inside the bubble

    for element in elements:
        header, body, element_type, icon_path, status = element["header"], element["body"], element["type"], element["icon"], element["status"]

        # Fix file path issue (Windows vs Linux)
        icon_path = icon_path.replace("\\", "/")
        print(icon_path)

        # Load the icon from a local file
        if os.path.exists(icon_path):
            icon = Image.open(icon_path).convert("RGBA").resize((80, 80))  # Resize icon for higher resolution
        else:
            print(f"⚠️ Warning: Icon '{icon_path}' not found!")  # Debug message
            icon = None  # Prevent crash

        # Set color based on type
        if(status):
            box_color = __red__
           
            # Wrap body text with an adjusted width so it fits within the bubble
            wrapped_body = textwrap.fill(body, width=45)

            # Calculate text sizes correctly
            header_bbox = draw.textbbox((0, 0), header, font=font_header)  # Get bounding box
            header_height = header_bbox[3] - header_bbox[1]

            body_lines = wrapped_body.split("\n")
            body_height = sum([draw.textbbox((0, 0), line, font=font_text)[3] - draw.textbbox((0, 0), line, font=font_text)[1] for line in body_lines])

            # Adjust bubble height dynamically with padding
            bubble_height = header_height + body_height + 2 * padding

            # Calculate x position for centering the bubble
            bubble_x = (1200 - bubble_width) // 2

            # Shadow offset and color
            shadow_offset = 10
            shadow_color = (0, 0, 0, 150)  # Semi-transparent black for the shadow

            # Draw shadowed bubble (offset slightly)
            draw.rounded_rectangle([(bubble_x + shadow_offset, y_offset + shadow_offset), 
                                    (bubble_x + bubble_width + shadow_offset, y_offset + bubble_height + shadow_offset)], 
                                radius=20, fill=shadow_color)

            # Draw the actual bubble on __top__
            draw.rounded_rectangle([(bubble_x, y_offset), (bubble_x + bubble_width, y_offset + bubble_height)], 
                                radius=20, fill="white", outline="black", width=3)
            draw.rounded_rectangle([(bubble_x, y_offset), (bubble_x + 125, y_offset + bubble_height)], 
                                radius=20, fill=box_color, outline="black", width=3)

            text_x_offset = 0  # Offset from the left side
            text_x = bubble_x + text_padding + text_x_offset # Adjust text start position after icon

            # Paste icon (if available)
            if icon:
                img.paste(icon, (text_x-15, y_offset + round(bubble_height/2)-30), icon)  # Paste the icon on the image with transparency
                text_x += 100  # Adjust text to avoid overlapping icon

            # Draw header text with padding
            draw.text((text_x, y_offset + 20), header, fill="black", font=font_header)

            # Draw body text with increased line spacing and padding
            line_height = draw.textbbox((0, 0), "A", font=font_text)[3] - draw.textbbox((0, 0), "A", font=font_text)[1]
            for i, line in enumerate(body_lines):
                line_y = y_offset + header_height + padding + i * (line_height + 10)  # Added 10 pixels for extra line spacing
                draw.text((text_x, line_y), line, fill="black", font=font_text)

            # Update y_offset to position next bubble with additional padding
            y_offset += bubble_height + bubble_padding

    img.save("risks.png")
    return img