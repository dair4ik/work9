import pygame
import sys
from pygame.locals import *
from tkinter import Tk, colorchooser

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

drawing_surface = pygame.Surface((WIDTH, HEIGHT))
drawing_surface.fill(WHITE)

color = BLACK
tool = "brush"
drawing = False
start_pos = None
brush_size = 5

def choose_color():
    global color
    Tk().withdraw()
    color = colorchooser.askcolor()[0]
    if color:
        color = tuple(map(int, color))

# Function to display key bindings
def display_instructions():
    font = pygame.font.Font(None, 24)
    instructions = [
        "M - Brush Tool",
        "N - Rectangle Tool",
        "C - Circle Tool",
        "S - Square Tool",
        "T - Right Triangle Tool",
        "J - Equilateral Triangle Tool",
        "H - Rhombus Tool",
        "E - Eraser Tool",
        "R - Red Color",
        "G - Green Color",
        "B - Blue Color",
        "L - Increase Brush Size",
        "W - Decrease Brush Size",
        "Ctrl + W - Close Application",
        "Alt + F4 - Close Application"
    ]
    y_offset = 10
    for instruction in instructions:
        text_surface = font.render(instruction, True, BLACK)
        screen.blit(text_surface, (10, y_offset))
        y_offset += 20

running = True
while running:
    screen.blit(drawing_surface, (0, 0))
    display_instructions()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
        elif event.type == MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos
            if tool == "rectangle":
                rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                pygame.draw.rect(drawing_surface, color, rect, 2)
            elif tool == "circle":
                radius = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1])) // 2
                center = (start_pos[0] + (end_pos[0] - start_pos[0]) // 2, start_pos[1] + (end_pos[1] - start_pos[1]) // 2)
                pygame.draw.circle(drawing_surface, color, center, radius, 2)
            elif tool == "square":
                side = min(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                pygame.draw.rect(drawing_surface, color, (start_pos[0], start_pos[1], side, side), 2)
            elif tool == "right_triangle":
                pygame.draw.polygon(drawing_surface, color, [start_pos, (start_pos[0], end_pos[1]), (end_pos[0], end_pos[1])], 2)
            elif tool == "equilateral_triangle":
                height = abs(end_pos[1] - start_pos[1])
                width = (height * 2) // 3
                pygame.draw.polygon(drawing_surface, color, [start_pos, (start_pos[0] - width, end_pos[1]), (start_pos[0] + width, end_pos[1])], 2)
            elif tool == "rhombus":
                width = abs(end_pos[0] - start_pos[0])
                height = abs(end_pos[1] - start_pos[1])
                pygame.draw.polygon(drawing_surface, color, [(start_pos[0], start_pos[1] - height // 2), (start_pos[0] - width // 2, start_pos[1]), (start_pos[0], start_pos[1] + height // 2), (start_pos[0] + width // 2, start_pos[1])], 2)
        elif event.type == MOUSEMOTION and drawing:
            if tool == "brush":
                pygame.draw.circle(drawing_surface, color, event.pos, brush_size)
            elif tool == "eraser":
                pygame.draw.circle(drawing_surface, WHITE, event.pos, brush_size + 5)
        elif event.type == KEYDOWN:
            if event.key == K_m:
                tool = "brush"
            elif event.key == K_n:
                tool = "rectangle"
            elif event.key == K_c:
                tool = "circle"
            elif event.key == K_s:
                tool = "square"
            elif event.key == K_t:
                tool = "right_triangle"
            elif event.key == K_e:
                tool = "eraser"
            elif event.key == K_j:
                tool = "equilateral_triangle"
            elif event.key == K_h:
                tool = "rhombus"
            elif event.key == K_p:
                choose_color()
            elif event.key == K_r:
                color = RED
            elif event.key == K_g:
                color = GREEN
            elif event.key == K_b:
                color = BLUE
            elif event.key == K_l:
                brush_size += 2
            elif event.key == K_w and not pygame.key.get_mods() & KMOD_CTRL:
                brush_size = max(1, brush_size - 2)
            elif event.key == K_w and pygame.key.get_mods() & KMOD_CTRL:
                running = False
            elif event.key == K_F4 and pygame.key.get_mods() & KMOD_ALT:
                running = False
    
    pygame.display.flip()

pygame.quit()
sys.exit()