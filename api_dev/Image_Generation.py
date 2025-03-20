from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import textwrap
import os

red="#ea251e"
backround="#264600"
top="#7cf63c"
def generate_image(elements, crop, location):
    today_date = datetime.today().strftime("%Y-%m-%d")
    title = f"Risk Factors - {today_date}\n{crop} - {location}"

    # Create a blank image with higher resolution
    img = Image.new("RGB", (1200, 1600), "white")  # Increased resolution to 1200x1600
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 56)  # Increased font size for better readability
        font_header = ImageFont.truetype("arialbd.ttf", 50)
        font_text = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font_title = font_header = font_text = ImageFont.load_default()

    # Draw the title background   
    draw.rounded_rectangle([(0, -20), (1200, 220)], 
                               radius=20, fill="black", outline="black", width=3)

    # Draw title with padding and center it
    title_lines = title.split("\n")
    title_y = 60
    for i, line in enumerate(title_lines):
        text_width, _ = draw.textsize(line, font=font_title)
        #text_x = (1200 - text_width) // 2  # Center the title horizontally
        text_x=40
        draw.text((text_x, title_y + i * 80), line, fill="white", font=font_title)

    y_offset = 260
    bubble_width = 1000
    
    # Load the icon from a local file
    icon_path="Icons/logo.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA")
        icon.thumbnail((icon.width // 8, icon.height // 8), Image.ANTIALIAS)  # Scale down by 50% without distorting
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

        # Load the icon from a local file
        if os.path.exists(icon_path):
            icon = Image.open(icon_path).convert("RGBA").resize((80, 80))  # Resize icon for higher resolution
        else:
            print(f"⚠️ Warning: Icon '{icon_path}' not found!")  # Debug message
            icon = None  # Prevent crash

        # Set color based on type
        if(status):
            box_color = red
        else:
            box_color=top
           
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

        # Draw the actual bubble on top
        draw.rounded_rectangle([(bubble_x, y_offset), (bubble_x + bubble_width, y_offset + bubble_height)], 
                               radius=20, fill="white", outline="black", width=3)
        draw.rounded_rectangle([(bubble_x, y_offset), (bubble_x + 125, y_offset + bubble_height)], 
                               radius=20, fill=box_color, outline="black", width=3)

        text_x = bubble_x + text_padding  # Adjust text start position after icon

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

    img.show()

# Example input data
crop = "Corn"
location = "Dübendorf"



elements=[
    {"header": "Elevated temperature", "body": "The maximum temperature will be exceeded, I recommend applyig Stress Buster to ensure the well being of your crops.", "type": "warning", "icon": "Icons/temperature-arrow-up-solid.png", "status":1},
    {"header": "Low moisture", "body": "A drought is incoming, I recomend appling Stress buster to ensure the well being of your crops.", "type": "warning", "icon": "Icons/sun-plant-wilt-solid.png","status":0},
    {"header": "Frost Warning", "body": "Frost is expected in the coming days, I recommend applying Stress Buster to your crops to ensure their well being", "type": "warning", "icon": "Icons/snowflake-regular.png","status":0},
    {"header": "Yield Risk", "body":"Based on avilible data, your yield is at a risk of being lower that expected. Apply Yield Booster to your crops to ensure the best possible yield.", "type": "warning", "icon": "Icons/arrow-down-wide-short-solid.png","status":1}
]


generate_image(elements, crop, location)


