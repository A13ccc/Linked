import mss
import pyautogui
import pytesseract
import pyautogui
from PIL import Image, ImageOps, ImageEnhance
from Quartz import CGEventCreateKeyboardEvent, CGEventPost, kCGEventKeyDown, kCGEventKeyUp
from Quartz import kCGHIDEventTap
import time

keycode_map = {
    # Lowercase letters
    "a": 0x00, "b": 0x0B, "c": 0x08, "d": 0x02, "e": 0x0E,
    "f": 0x03, "g": 0x05, "h": 0x04, "i": 0x22, "j": 0x26,
    "k": 0x28, "l": 0x25, "m": 0x2E, "n": 0x2D, "o": 0x1F,
    "p": 0x23, "q": 0x0C, "r": 0x0F, "s": 0x01, "t": 0x11,
    "u": 0x20, "v": 0x09, "w": 0x0D, "x": 0x07, "y": 0x10,
    "z": 0x06, " ": 0x31,

    # Numbers
    "0": 0x1D, "1": 0x12, "2": 0x13, "3": 0x14, "4": 0x15,
    "5": 0x17, "6": 0x16, "7": 0x1A, "8": 0x1C, "9": 0x19,

    # Special characters
    ".": 0x2F, ",": 0x2B, ";": 0x29, "'": 0x27, "/": 0x2C,
    "\\": 0x2A, "[": 0x21, "]": 0x1E, "-": 0x1B, "=": 0x18,
    "`": 0x32,

    # Capitalization Shifted characters
    "!": (0x12, "shift"), "@": (0x13, "shift"), "#": (0x14, "shift"),
    "$": (0x15, "shift"), "%": (0x17, "shift"), "^": (0x16, "shift"),
    "&": (0x1A, "shift"), "*": (0x1C, "shift"), "(": (0x19, "shift"),
    ")": (0x1D, "shift"),

    # Shifted punctuation
    "_": (0x1B, "shift"), "+": (0x18, "shift"), "{": (0x21, "shift"),
    "}": (0x1E, "shift"), ":": (0x29, "shift"), "\"": (0x27, "shift"),
    "<": (0x2B, "shift"), ">": (0x2F, "shift"), "?": (0x2C, "shift"),
    "|": (0x2A, "shift"), "~": (0x32, "shift"),

    # Capital letters
    "A": (0x00, "shift"), "B": (0x0B, "shift"), "C": (0x08, "shift"),
    "D": (0x02, "shift"), "E": (0x0E, "shift"), "F": (0x03, "shift"),
    "G": (0x05, "shift"), "H": (0x04, "shift"), "I": (0x22, "shift"),
    "J": (0x26, "shift"), "K": (0x28, "shift"), "L": (0x25, "shift"),
    "M": (0x2E, "shift"), "N": (0x2D, "shift"), "O": (0x1F, "shift"),
    "P": (0x23, "shift"), "Q": (0x0C, "shift"), "R": (0x0F, "shift"),
    "S": (0x01, "shift"), "T": (0x11, "shift"), "U": (0x20, "shift"),
    "V": (0x09, "shift"), "W": (0x0D, "shift"), "X": (0x07, "shift"),
    "Y": (0x10, "shift"), "Z": (0x06, "shift")
}


def capture_screenshot():
    """Capture a screenshot of a specific rectangle."""
    with mss.mss() as sct:
        # Define the region to capture
        region = {"top": 430, "left": 350, "width": 1620 - 500, "height": 200}
        screenshot = sct.grab(region)
        # Convert the screenshot to a PIL image for processing
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        img.save("screenshot.png")
    return "screenshot.png"

def preprocess_image(image_path):
     # Open the image
    img = Image.open(image_path)

    # Convert to grayscale
    img = img.convert("L")

    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2.0)  # Increase contrast

    # Add padding to help with wrapping issues
    img = ImageOps.expand(img, border=10, fill='white')

    # Convert to binary image
    img = img.point(lambda x: 0 if x < 128 else 255, '1')

    # Resize the image to improve OCR accuracy
    img = img.resize((img.width * 2, img.height * 2), Image.Resampling.LANCZOS)

    img.save("screenshot.png")
    
    return "screenshot.png"

def extract_text(image_path):
    # Preprocess the image
    preprocessed_img = preprocess_image(image_path)
    
    # Perform OCR with no whitelist
    ocr_result = pytesseract.image_to_string(preprocessed_img, config='--psm 4')
    return ocr_result

def process_ocr_result(raw_text):
    # Replace newlines with spaces
    processed_text = raw_text.replace("\n", " ")
    
    # Optionally handle extra spaces (e.g., multiple spaces between words)
    processed_text = " ".join(processed_text.split())
    
    return processed_text

def press_key(keycode, shift=False):
    """Simulate a single key press, with optional Shift."""
    if shift:
        # Press Shift key
        shift_event = CGEventCreateKeyboardEvent(None, 0x38, True)  # 0x38 = Shift
        CGEventPost(kCGHIDEventTap, shift_event)

    # Press the key
    event = CGEventCreateKeyboardEvent(None, keycode, True)
    CGEventPost(kCGHIDEventTap, event)

    # Release the key
    event = CGEventCreateKeyboardEvent(None, keycode, False)
    CGEventPost(kCGHIDEventTap, event)

    if shift:
        # Release Shift key
        shift_event = CGEventCreateKeyboardEvent(None, 0x38, False)
        CGEventPost(kCGHIDEventTap, shift_event)


def type_text(text):
    """Type a string of text."""
    import time
    time.sleep(0.1)  # Initial delay
    for char in text:
        if char in keycode_map:
            time.sleep(0.2)
            key = keycode_map[char]
            if isinstance(key, tuple):  # If the character needs Shift
                press_key(key[0], shift=True)
                print(char)
            else:
                press_key(key)
                print(char)

def main():
    # Step 1: Capture a screenshot
    screenshot_path = capture_screenshot()
    print(f"Screenshot saved at {screenshot_path}")

    screenshot_path = preprocess_image(screenshot_path)

    # Step 2: Extract numbers from the screenshot
    recognized_text = extract_text(screenshot_path)
    processed_text = process_ocr_result(recognized_text)
    letters = processed_text
    print(f"Recognized letters: {letters}")
    pyautogui.click(400, 500)
    type_text(letters)

if __name__ == "__main__":
    main()
