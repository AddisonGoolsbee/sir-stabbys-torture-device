import os
import sys
from AudioAnalyzer import AudioAnalyzer
from visualizer import Visualizer

with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout

def run():
    pygame.init()
    infoObject = pygame.display.Info()
    screen_w = int(infoObject.current_w / 2)
    screen_h = int(infoObject.current_w / 2)
    screen = pygame.display.set_mode([screen_w, screen_h])
    clock = pygame.time.Clock()

    analyzer = AudioAnalyzer()
    visualizer = Visualizer(screen, analyzer)

    getTicksLastFrame = pygame.time.get_ticks()
    running = True
    temp = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if temp:
            visualizer.visualize_sound('src/victim/speech.mp3')
            temp = False

        if visualizer.sound_playing:
            t = pygame.time.get_ticks()
            deltaTime = (t - getTicksLastFrame) / 1000.0
            getTicksLastFrame = t
            visualizer.visualizer()

        
        pygame.display.flip()
        clock.tick(60)  # Maintain 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    run()
