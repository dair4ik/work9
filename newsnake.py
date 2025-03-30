import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 20  # Size of each snake segment
FPS = 10  # Starting speed

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load background image
background = pygame.image.load("backg.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to fit screen

# Load apple image
apple_img = pygame.image.load("apple1.png")
apple_img = pygame.transform.scale(apple_img, (CELL_SIZE, CELL_SIZE))  # Resize to match cell size

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game(by Kaliyev Dair)")

# Fonts
font = pygame.font.SysFont("Verdana", 20)

# Snake settings
snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake body
snake_dir = (CELL_SIZE, 0)  # Initial movement direction (right)

# Food settings with random weight and timer
class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        """Generate a new food position, weight, and reset timer."""
        self.x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        self.y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        self.weight = random.randint(1, 3)  # Food weight (1 to 3 points)
        self.timer = random.randint(50, 100)  # Timer before food disappears

    def update(self):
        """Decrease the timer and respawn food if timer runs out."""
        self.timer -= 1
        if self.timer <= 0:
            self.respawn()

food = Food()

# Game variables
score = 0
level = 1
running = True

# Main game loop
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))  # Draw background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Change snake direction based on arrow keys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)

    # Move the snake
    new_head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
    
    # Check for wall collision
    if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT:
        running = False  # Game over

    # Check if the snake collides with itself
    if new_head in snake:
        running = False  # Game over

    # Add new head to snake
    snake.insert(0, new_head)

    # Check if food is eaten
    if new_head == (food.x, food.y):
        score += food.weight  # Increase score by food weight
        food.respawn()  # Generate new food
    else:
        snake.pop()  # Remove last segment if no food eaten

    # Update food timer
    food.update()

    # Level up every 5 points
    if score % 5 == 0 and score > 0:
        level = score // 5 + 1
        FPS = 10 + (level * 2)  # Increase speed

    # Draw snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    # Draw apple (food)
    screen.blit(apple_img, (food.x, food.y))

    # Display score and level
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    # Update screen
    pygame.display.update()
    clock.tick(FPS)  # Control game speed

# Quit pygame
pygame.quit()
