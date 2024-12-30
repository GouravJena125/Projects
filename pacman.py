import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()

pacman_x, pacman_y = WIDTH // 2, HEIGHT // 2
pacman_speed = GRID_SIZE
direction = (0, 0)

maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 2, 2, 0, 1, 0, 2, 2, 2, 0, 1, 0, 2, 1],
    [1, 0, 1, 1, 2, 0, 1, 0, 1, 1, 2, 0, 1, 0, 2, 1],
    [1, 2, 1, 0, 2, 2, 2, 2, 1, 0, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 1, 0, 0, 0, 1, 0, 0, 0, 1, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

ROWS = len(maze)
COLS = len(maze[0])

def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * GRID_SIZE
            y = row * GRID_SIZE
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLUE, (x, y, GRID_SIZE, GRID_SIZE))
            elif maze[row][col] == 2:
                pygame.draw.circle(screen, WHITE, (x + GRID_SIZE // 2, y + GRID_SIZE // 2), 5)

def move_pacman():
    global pacman_x, pacman_y, direction
    new_x = pacman_x + direction[0] * pacman_speed
    new_y = pacman_y + direction[1] * pacman_speed

    # Calculate grid position
    grid_x = new_x // GRID_SIZE
    grid_y = new_y // GRID_SIZE

    # Check boundaries and walls
    if 0 <= grid_x < COLS and 0 <= grid_y < ROWS and maze[grid_y][grid_x] != 1:
        pacman_x, pacman_y = new_x, new_y

def eat_dot():
    global maze
    grid_x = pacman_x // GRID_SIZE
    grid_y = pacman_y // GRID_SIZE

    # Check if Pac-Man is within bounds
    if 0 <= grid_x < COLS and 0 <= grid_y < ROWS:
        if maze[grid_y][grid_x] == 2:
            maze[grid_y][grid_x] = 0


running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                direction = (1, 0)

    move_pacman()
    eat_dot()

    draw_maze()
    pygame.draw.circle(screen, YELLOW, (pacman_x + GRID_SIZE // 2, pacman_y + GRID_SIZE // 2), GRID_SIZE // 2)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit()
