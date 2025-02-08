import mss
import pytesseract
import pyautogui
from PIL import Image, ImageOps, ImageFilter
import time

def capture_screenshot():
    """Capture a screenshot of a specific rectangle."""
    with mss.mss() as sct:
        # Define the region to capture
        region = {"top": 290, "left": 88, "width": 1620 - 88, "height": 660 - 290}
        screenshot = sct.grab(region)
        # Convert the screenshot to a PIL image for processing
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        # Resize the image to make it smaller for better OCR
        img = img.convert("L")
        # Apply thresholding
        img = ImageOps.autocontrast(img)  # Auto adjust contrast
        img = img.point(lambda x: 0 if x < 128 else 255, '1')  # Binarize
        # Optionally resize for better recognition
        img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)
        img.save("screenshot.png")
    return "screenshot.png"

def extract_numbers_from_image(image_path):
    """Use OCR to extract numbers from the given image."""
    image = Image.open(image_path)
    # Use pytesseract to recognize text
    ocr_result = pytesseract.image_to_string(image, config='--psm 6 digits')
    # Filter out non-numeric characters
    numbers = ''.join(filter(str.isdigit, ocr_result))
    return numbers

def monitor_for_button_and_type(numbers):
    """Continuously monitor for yellow buttons, interact with them, and type the numbers."""
    print("Monitoring for the yellow buttons...")
    target_color = (255, 209, 84)  # Color of the yellow button (#FFD154)
    tolerance = 100  # Tolerance for color matching
    button1_region = {"top": 580, "left": 825, "width": 10, "height": 10}  # First button region
    button2_region = {"top": 610, "left": 820, "width": 30, "height": 30}  # Second button region

    with mss.mss() as sct:
        while True:
            # Check for the first yellow button
            button1_screenshot = sct.grab(button1_region)
            img1 = Image.frombytes("RGB", button1_screenshot.size, button1_screenshot.rgb)
            color1 = img1.resize((1, 1)).getpixel((0, 0))  # Get average color

            # Check if the color matches the yellow button
            if all(abs(color1[i] - target_color[i]) <= tolerance for i in range(3)):
                print("First yellow button detected!")

                # Type the numbers
                if numbers:
                    print(f"Typing numbers: {numbers}")
                    pyautogui.typewrite(numbers)
                else:
                    print("No numbers stored to type.")

                pyautogui.click(x=825, y=580)  # Click the first button
                time.sleep(0)

                # Check for the second yellow button
            button2_screenshot = sct.grab(button2_region)
            img2 = Image.frombytes("RGB", button2_screenshot.size, button2_screenshot.rgb)
            color2 = img2.resize((1, 1)).getpixel((0, 0))  # Get average color

            if all(abs(color2[i] - target_color[i]) <= tolerance for i in range(3)):
                print("Second yellow button detected!")
                pyautogui.click(x=820, y=610)  # Click the second button

                

                # Wait a third of a second and restart the entire program
                time.sleep(0)
                print("Restarting the program...")
                print("\n" * 100)
                main()  # Restart the program by calling the main function

def main():
    # Step 1: Capture a screenshot
    screenshot_path = capture_screenshot()
    print(f"Screenshot saved at {screenshot_path}")

    # Step 2: Extract numbers from the screenshot
    numbers = extract_numbers_from_image(screenshot_path)
    print(f"Recognized numbers: {numbers}")

    # Step 3: Monitor for the yellow button and type numbers when detected
    monitor_for_button_and_type(numbers)

if __name__ == "__main__":
    main()
