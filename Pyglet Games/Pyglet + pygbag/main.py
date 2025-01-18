import asyncio
import pyglet

# Set up the resource path
pyglet.resource.path = ["/Users/alec/Documents/Python/Pyglet Games/Pixel Platformer Assets/Tiles/Characters/"]
pyglet.resource.reindex()

# Load the sprite
player_image = pyglet.resource.image("tile_0000.png")
player_sprite = pyglet.sprite.Sprite(player_image, x=24, y=24)
player_sprite.scale = 2

# Create a window
window = pyglet.window.Window(1200, 800, "Async Pyglet Game")

# Key presses
keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

# Movement variables
velocity_x = 0
velocity_y = 0
acceleration = 10000
friction = 1000
jump_speed = 800
gravity = 1500
ground_y = 24
on_ground = False

# Draw event
@window.event
def on_draw():
    window.clear()
    player_sprite.draw()

async def update(dt):
    global velocity_x, velocity_y, on_ground

    # Horizontal movement
    if keys[pyglet.window.key.RIGHT]:
        velocity_x = acceleration * dt
        player_sprite.scale_x = -1
    elif keys[pyglet.window.key.LEFT]:
        velocity_x = -acceleration * dt
        player_sprite.scale_x = 1
    else:
        if velocity_x > 0:
            velocity_x -= friction * dt
        elif velocity_x < 0:
            velocity_x += friction * dt

    # Jumping
    if keys[pyglet.window.key.UP] and on_ground:
        velocity_y = jump_speed
        on_ground = False

    # Gravity
    if not on_ground:
        velocity_y -= gravity * dt
    else:
        velocity_y = 0
        player_sprite.y = ground_y

    # Ground collision
    if player_sprite.y + velocity_y * dt <= ground_y:
        player_sprite.y = ground_y
        on_ground = True

    # Update sprite position
    player_sprite.x += velocity_x * dt
    player_sprite.y += velocity_y * dt

    # Limit horizontal speed
    max_speed = 500
    velocity_x = max(-max_speed, min(max_speed, velocity_x))

    await asyncio.sleep(0)  # Yield control to event loop

async def pyglet_event_loop():
    while True:
        pyglet.clock.tick()  # Process scheduled events
        window.dispatch_events()  # Handle window events
        window.dispatch_event('on_draw')  # Render the frame
        await asyncio.sleep(1 / 60.0)  # Cap at ~60 FPS

async def main():
    # Schedule the update coroutine
    pyglet.clock.schedule(lambda dt: asyncio.create_task(update(dt)))

    # Run the Pyglet async loop
    await pyglet_event_loop()

if __name__ == "__main__":
    asyncio.run(main())
