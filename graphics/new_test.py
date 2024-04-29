import pygame
import pygame.freetype
import sys
import os

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Font Display")

# Set the background color
background_color = (255, 255, 255)  # white

# Set up fonts
pygame.freetype.init()
all_fonts = pygame.freetype.get_fonts()
font_size = 24

font_list = []

if all_fonts:
    for font_name in all_fonts:
        print("Checking font:", font_name)  # Debug: print each font being checked
        if os.path.exists("system/library/fonts/" + font_name):
            font_list.append(font_name)
            print("Loading font:", font_name)  # This font path is valid
            font = pygame.freetype.Font(font_name, 24)
            break
        else:
            print("Path does not exist:", font_name)

# Main loop
running = True
index = 0  # Start with the first font
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Press SPACE to switch to the next font
                index = (index + 1) % len(font_list)
    
    # Clear the screen
    screen.fill(background_color)
    
    # Load and render the current font
    if font_list:
        font_path = font_list[index]
        font_name = font_path.split('/')[-1]
        font = pygame.freetype.Font(font_path, font_size)
        text_surface, _ = font.render("Sample Text", (0, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text_surface, text_rect)
    
        # Display the font name
        sys_font = pygame.font.SysFont(None, 30)
        name_surface = sys_font.render(font_name, True, (0, 0, 0))
        name_rect = name_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(name_surface, name_rect)
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
