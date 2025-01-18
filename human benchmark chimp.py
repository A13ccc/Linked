import pytesseract
import mss
from PIL import Image, ImageOps
import pyautogui


def capture_screenshot():
    """Capture a screenshot of a specific rectangle."""
    with mss.mss() as sct:
        # Define the region to capture
        region = {"top": 200, "left": 350, "width": 1120, "height": 600}
        screenshot = sct.grab(region)
        # Convert the screenshot to a PIL image for processing
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img = ImageOps.grayscale(img)  # Convert to grayscale
        img = ImageOps.autocontrast(img)  # Enhance contrast
        img.save("screenshot.png")
    return "screenshot.png"


def extract_numbers_and_positions(image_path):
    """Extract numbers and bounding box positions."""
    image = Image.open(image_path)
    # Use Tesseract with bounding box information
    data = pytesseract.image_to_boxes(image, config='--psm 6 digits')
    positions = []
    for line in data.splitlines():
        parts = line.split()
        char = parts[0]  # The recognized character
        x1, y1, x2, y2 = map(int, parts[1:5])  # Bounding box
        positions.append((char, (x1, y1, x2, y2)))
    return positions


def sort_positions_by_number(positions):
    """Filter and sort positions by the numeric value."""
    positions = [(int(char), bbox) for char, bbox in positions if char.isdigit()]
    positions.sort()  # Sort by the number
    return positions


def map_to_screen_coordinates(bbox, image_size, screen_size):
    """Map bounding box to screen coordinates."""
    img_width, img_height = image_size
    screen_width, screen_height = screen_size

    x1, y1, x2, y2 = bbox
    x_center = (x1 + x2) / 2 * (screen_width / img_width)
    y_center = screen_height - (y1 + y2) / 2 * (screen_height / img_height)
    return int(x_center), int(y_center)


def automate_clicks(sorted_positions, image_size, screen_size):
    """Click in order of numbers."""
    for number, bbox in sorted_positions:
        x, y = map_to_screen_coordinates(bbox, image_size, screen_size)
        pyautogui.click(x, y)


# Main Program
screenshot_path = capture_screenshot()
positions = extract_numbers_and_positions(screenshot_path)

# Debugging OCR Output
print("Raw OCR Positions:", positions)

sorted_positions = sort_positions_by_number(positions)
print("Sorted Positions:", sorted_positions)

image_size = Image.open(screenshot_path).size  # Get image size
screen_size = pyautogui.size()  # Get screen size

automate_clicks(sorted_positions, image_size, screen_size)