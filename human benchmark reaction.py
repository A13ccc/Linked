import mss
from PIL import Image
from pynput.mouse import Controller, Button

mouse = Controller()


def get_color():
    with mss.mss() as sct:
        # Define a small region around the target pixel
        region = {"top": 599, "left": 499, "width": 100, "height": 100}
        screenshot = sct.grab(region)
        
        # Convert to PIL Image and get the pixel color
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        pixel_color = img.getpixel((0,0))
        
        # Target color #4bdb6a in RGB
        target_color = (75, 219, 106)
        
        # Check if colors match (with some tolerance for slight variations)
        tolerance = 50

        img.save("screenshot.png")
        print("Saving screenshot")
        return all(abs(pixel_color[i] - target_color[i]) <= tolerance for i in range(3))
    
def main():
    print("Checking for green...")
    while True:
        if get_color():
            print("Green detected! Clicking...")
            mouse.click(Button.left, 1)
            mouse.click(Button.left, 1)
            main()


main()

