import pygame
import sys

pygame.init()

# Basic setup
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Linked")

# Colors I like
COLORS = {
    'bg': (245, 245, 245),      # Clean white-ish
    'player1': (219, 58, 52),   # Red
    'player2': (48, 63, 159),   # Blue
    'platform': (67, 160, 71),  # Green
    'divider': (33, 33, 33),    # Dark
}

clock = pygame.time.Clock()
FPS = 180  # Standard 60fps is fine

previous_level_num = 0
floor = 600

class Button:
    def __init__(self, level_num):
        self.pressed = False

    def check_col(self):
        if not self.pressed:
            pass
    

class Level:
    def __init__(self, platforms, goal_y, side, num=None):
        self.goal_y = goal_y
        self.side = side
        self.platforms = platforms
        self.completed = False
        self.active = False

    def draw(self, screen):
        # Draw platforms and goal line
        for platform in self.platforms:
            pygame.draw.line(screen, COLORS['platform'], (platform[0], platform[1]), (platform[2], platform[3]), 10)
        
        # Draw goal line in gold if active, gray if completed, hidden if neither
        if self.active:
            pygame.draw.line(screen, (255, 215, 0), (0, self.goal_y), (WINDOW_SIZE[0], self.goal_y), 5)
        elif self.completed:
            pygame.draw.line(screen, (128, 128, 128), (0, self.goal_y), (WINDOW_SIZE[0], self.goal_y), 5)
            
    def activate(self):
        self.active = True
        
    def complete(self):
        self.completed = True
        self.active = False
        
    def reset(self):
        self.completed = False
        self.active = False

class Player:
    def __init__(self, x, y, image_path, num):
        self.pos = pygame.Vector2(x, y)
        self.size = (40, 40)  # Size of the player, you can adjust this if needed
        self.rect = pygame.Rect(self.pos, self.size)
        self.image = pygame.image.load(image_path)  # Load the sprite image
        self.image = pygame.transform.scale(self.image, self.size)  # Optionally scale the image to fit size
        self.vel_y = 0
        self.vel_x = 0
        self.move_speed = 2
        self.gravity = 0.05
        self.gravity_on = True
        self.jump_power = -3.5
        self.on_ground = False
        self.on_platform = False
        self.on_wall = [False, 'None', 0]
        self.num = num

    def move(self, keys, side):
        move_dir = -1 if side == "right" else 1
        self.vel_x = 0
        
        if keys[pygame.K_LEFT]:
            if not self.on_wall[0]:
                self.pos.x -= self.move_speed * move_dir
            else:
                if self.on_wall[1] == 'left' and self.on_wall[2] == 1:
                    pass
                elif self.on_wall[1] == 'right' and self.on_wall[2] == 2:
                    pass
                else:
                    self.pos.x -= self.move_speed * move_dir

        if keys[pygame.K_RIGHT]:
            if not self.on_wall[0]:
                self.pos.x += self.move_speed * move_dir
            else:
                if self.on_wall[1] == 'right' and self.on_wall[2] == 1:
                    pass
                elif self.on_wall[1] == 'left' and self.on_wall[2] == 2:
                    pass
                else:
                    self.pos.x += self.move_speed * move_dir

        # Only apply jump if on ground
        if keys[pygame.K_UP] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.gravity_on = True

        # Update horizontal position immediately
        self.pos.x += self.vel_x
        self.rect.x = self.pos.x

    def apply_gravity(self):
        # Only apply gravity when not on ground
        if self.gravity_on:
            if not self.on_ground:
                self.vel_y += self.gravity
        
        # Always update vertical position based on velocity
        self.pos.y += self.vel_y
        self.rect.y = self.pos.y

    def check_collision(self, platforms, num):
        self.on_ground = False  # Reset ground state

        p1_edge = 0
        p2_edge = 760

        p1_middle = 358
        p2_middle = 403

        self.on_ground = False
        player_bottom_last = self.rect.bottom - self.vel_y  # Where the bottom was last frame
        
        for line in platforms:
            x1, y1, x2, y2 = line
            
                # Check if player crossed the platform between frames
            if player_bottom_last <= y1 <= self.rect.bottom:
                if x1 <= self.rect.centerx <= x2:
                    self.rect.bottom = y1
                    self.pos.y = self.rect.y
                    self.vel_y = 0
                    self.on_ground = True
                    self.gravity_on = False
                    break  # Stop checking after landing
        if not self.on_ground:
            self.gravity_on = True

        # Check Boundary collisions
        if num == 1:
            if self.pos.x <= p1_edge:
                self.pos.x = p1_edge
                self.on_wall = [True, 'left', 1]
            elif self.pos.x >= p1_middle:
                self.pos.x = p1_middle
                self.on_wall = [True, 'right', 1]
            else:
                self.on_wall = [False, 'None', 0]
        elif num == 2:
            if self.pos.x <= p2_middle:
                self.pos.x = p2_middle
                self.on_wall = [True, 'left', 2]
            elif self.pos.x >= p2_edge:
                self.pos.x = p2_edge
                self.on_wall = [True, 'right', 2]
            else:
                self.on_wall = [False, 'None', 0]
        
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def floor_detection(self, ground):
        if self.rect.bottom >= ground:
            self.rect.bottom = ground
            self.pos.y = self.rect.y
            self.vel_y = 0
            self.on_ground = True

    def fall_prev_level(self):
        global previous_level_num, current_level_num, left_level, right_level, player1, player2

        if self.vel_y > 0:  # Only trigger when falling down
            if current_level_num > 1 and self.rect.bottom >= floor:
                if previous_level_num != 0:  # Ensure there's a level to fall back to
                    print(f"Fell to Level {previous_level_num}!")

                    # Store current motion values
                    prev_vel_x = self.vel_x
                    prev_vel_y = self.vel_y
                    y = 0

                    # Update current level number
                    current_level_num = previous_level_num

                    # Load previous level
                    left_level = Level(platforms=levels[f'level{current_level_num}']['left'],
                                    goal_y=0, side='left', num=current_level_num)
                    right_level = Level(platforms=levels[f'level{current_level_num}']['right'],
                                        goal_y=0, side='right', num=current_level_num)
                    left_level.activate()
                    right_level.activate()

                    # Restore motion values for fluid transition
                    player1.pos.y = y
                    player2.pos.y = y
                    self.vel_x = prev_vel_x
                    self.vel_y = prev_vel_y
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# Level Definitions
levels = {
    'level1': {
        'left': [
            (100, 70, 240, 70),    # Horizontal line from (100, 50) to (240, 50)
            (120, 165, 290, 165),
            (135, 260, 265, 260),
            (155, 340, 315, 340),
            (175, 455, 320, 455),
            (100, 500, 240, 500)
        ],
        'right': [
            (560, 70, 700, 70),
            (520, 165, 690, 165),
            (535, 260, 665, 260),
            (495, 340, 655, 340),
            (475, 455, 620, 455),
            (500, 500, 700, 500)
        ]
    },

    'level2': {
        'left': [
            (10, 530, 180, 530)
        ],
        'right': [
            (475, 455, 620, 455)
        ]
    }
}

# Initialize players and levels
p1_spawn = 175
p2_spawn = 586

player1 = Player(p1_spawn, 600, './Linked - Alec/assets/images/players/player1.png', 1)
player2 = Player(p2_spawn, 600, './Linked - Alec/assets/images/players/player2.png', 2)

current_level = 'level1'
level1_left = Level(platforms=levels[current_level]['left'], goal_y=0, side='left')
level1_right = Level(platforms=levels[current_level]['right'], goal_y=0, side='right')

def transition_to_next_level():
    global current_level_num, left_level, right_level, player1, player2

    player1.gravity_on = True
    player2.gravity_on = True

    current_level_num += 1
    if current_level_num <= max_levels:
        # Move players above the screen for smooth transition
        player1.pos.y = WINDOW_SIZE[1] + 40
        player2.pos.y = WINDOW_SIZE[1] + 40
        player1.vel_y = -10  # Simulate jumping up
        player2.vel_y = -10

        # Load next level
        left_level = Level(platforms=levels[f'level{current_level_num}']['left'],
                           goal_y=0, side='left', num=current_level_num)
        right_level = Level(platforms=levels[f'level{current_level_num}']['right'],
                            goal_y=0, side='right', num=current_level_num)
        left_level.activate()
        right_level.activate()

    else:
        print("You beat all levels!")
        pygame.quit()
        sys.exit()


# Check if players reached the goal
def check_goal(player1, player2, level):
    if player1.rect.top <= level.goal_y and player2.rect.top <= level.goal_y:
        print(f'Went up to level {current_level_num + 1}!')
        transition_to_next_level()

# Game loop
game_active = True
current_level_num = 1
max_levels = len(levels)

# Initialize first level
left_level = Level(platforms=levels[f'level{current_level_num}']['left'], 
                  goal_y=0, side='left', num=current_level_num)
right_level = Level(platforms=levels[f'level{current_level_num}']['right'],
                   goal_y=0, side='right', num=current_level_num)
left_level.activate()
right_level.activate()

while game_active:
    clock.tick(FPS)
    screen.fill(COLORS['bg'])

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

    # Key handling
    keys = pygame.key.get_pressed()
    player1.move(keys, "left")
    player2.move(keys, "right")

    # Apply gravity
    player1.apply_gravity()
    player2.apply_gravity()

    # Collision detection
    player1.check_collision(left_level.platforms, 1)
    player2.check_collision(right_level.platforms, 2)

    if previous_level_num > 1:
        previous_level_num = previous_level_num - current_level
    else:
        previous_level_num = 1


    if previous_level_num == 0:
        previous_level_num = 1
    
    
    # Handle falling to a previous level
    if current_level_num != 1:
        player1.fall_prev_level()
        player2.fall_prev_level()
    else:
        player1.floor_detection(floor)
        player2.floor_detection(floor)

    # Check for level completion
    # Check for level completion (Moving Up)
    if check_goal(player1, player2, left_level):
        print(f"Level {current_level_num} Complete!")
        left_level.complete()
        right_level.complete()
        
        previous_level_num = current_level_num  # Store current level before advancing
        current_level_num += 1

        if current_level_num <= max_levels:
            
            # Load next level
            left_level = Level(platforms=levels[f'level{current_level_num}']['left'],
                            goal_y=0, side='left', num=current_level_num)
            right_level = Level(platforms=levels[f'level{current_level_num}']['right'],
                            goal_y=0, side='right', num=current_level_num)
            left_level.activate()
            right_level.activate()
        else:
            print("You beat all levels!")
            game_active = False

    # Draw dividing line
    pygame.draw.line(screen, COLORS['divider'], (WINDOW_SIZE[0] // 2, 0), (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1]), 5)

    # Draw players and level
    player1.draw(screen)
    player2.draw(screen)

    left_level.draw(screen)
    right_level.draw(screen)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
