import pygame
import sys
import math

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode([screen_width, screen_height])
pygame.display.set_caption("Pygame Paint App")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen.fill(WHITE)

brush_color = BLACK
mode = 'draw' 
drawing = False  
start_pos = None  
last_pos = None  

def draw_circle(start, end):
    center = start
    radius = int(math.sqrt((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2))
    pygame.draw.circle(screen, brush_color, center, radius, 7)

def draw_triangle(start, end):
    dx, dy = end[0] - start[0], end[1] - start[1]
    right_angle = (end[0], start[1])
    pygame.draw.polygon(screen, brush_color, [start, right_angle, end], 7)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos
                if mode == 'erase':
                    pygame.draw.circle(screen, WHITE, event.pos, 10)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False
                if mode == 'circle':
                    draw_circle(start_pos, event.pos)
                elif mode == 'triangle':
                    draw_triangle(start_pos, event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if mode == 'erase':
                    pygame.draw.circle(screen, WHITE, event.pos, 20)
                elif mode == 'draw':
                    pygame.draw.line(screen, brush_color, last_pos, event.pos, 5)
                last_pos = event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                mode = 'erase'
            elif event.key == pygame.K_c:
                mode = 'circle'
                brush_color = BLACK
            elif event.key == pygame.K_t:
                mode = 'triangle'
                brush_color = BLACK
            elif event.key == pygame.K_d:
                mode = 'draw'
                brush_color = BLACK

    pygame.display.flip()
