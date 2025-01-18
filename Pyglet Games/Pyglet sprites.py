import pyglet

# Create a window
window = pyglet.window.Window(1200, 800, "My Game")

# Sprites
player_image = pyglet.resource.image("Pixel Platformer Assets/Tiles/Characters/tile_0000.png")
player_sprite = pyglet.sprite.Sprite(player_image, x=24, y=24)
player_sprite.scale = 2

# Key presses
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

# Horizontal Velocity
velocity_x = 0
acceleration = 10000
friction = 1000

# Vertical Velocity
velocity_y = 0
jump_speed = 800
gravity = 1500

# Ground level
ground_y = 24

# Jumping state
on_ground = False

# Draw content
@window.event
def on_draw():
    window.clear()
    player_sprite.draw()

def update(dt):
    global velocity_x, velocity_y, on_ground

    # Handle key presses for horizontal movement
    if keys[pyglet.window.key.RIGHT]:
        velocity_x = acceleration * dt
        player_sprite.scale_x = -1
    elif keys[pyglet.window.key.LEFT]:
        velocity_x = -acceleration * dt
        player_sprite.scale_x = 1
    else:
        # Apply friction when no horizontal key is pressed
        if velocity_x > 0:
            velocity_x -= friction * dt
        elif velocity_x < 0:
            velocity_x += friction * dt

    # Handle jumping logic
    if keys[pyglet.window.key.UP] and on_ground:
        velocity_y = jump_speed
        on_ground = False

    # Apply gravity
    if not on_ground:
        velocity_y -= gravity * dt
    else:
        velocity_y = 0
        player_sprite.y = ground_y

    if player_sprite.y + velocity_y * dt <= ground_y:
        player_sprite.y = ground_y
        on_ground = True

    # Update sprite position
    player_sprite.x += velocity_x * dt
    player_sprite.y += velocity_y * dt

    # Limit horizontal velocity to max speed
    max_speed = 500
    if velocity_x > max_speed:
        velocity_x = max_speed
    elif velocity_x < -max_speed:
        velocity_x = -max_speed

# Run the application + smooth things out
pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()
