import os
import sys
from visualizer import Visualizer

with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout


def init_screen():
    infoObject = pygame.display.Info()
    screen_w = int(infoObject.current_w / 2)
    screen_h = int(infoObject.current_w / 2)
    screen = pygame.display.set_mode([screen_w, screen_h])
    return screen

def handle_events():
    """Handle Pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def run():
    pygame.init()
    screen = init_screen()
    clock = pygame.time.Clock()


    visualizer = Visualizer(screen)

    running = True
    temp = True
    while running:
        running = handle_events()

        if temp:
            visualizer.visualize_sound('src/victim/speech.mp3')
            temp = False

        if visualizer.sound_playing:
            visualizer.visualizer()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    run()
