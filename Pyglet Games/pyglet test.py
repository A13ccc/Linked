import pyglet

# Create a window
window = pyglet.window.Window(800, 600, "My Game")

# Draw content
@window.event
def on_draw():
    window.clear()
    pyglet.text.Label(
        "Hello, Pyglet!",
        font_name="Arial",
        font_size=24,
        x=window.width // 2,
        y=window.height // 2,
        anchor_x="center",
        anchor_y="center",
    ).draw()

# Run the application
pyglet.app.run()
