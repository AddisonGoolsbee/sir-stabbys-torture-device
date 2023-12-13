import os
import sys
import time
import openai

with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout

def text_to_speech(text_input: str, pygame_event=None):
    # speech_file_path = Path(__file__).parent / "speech.mp3"
    speech_file_path = "speech.mp3"
    response = openai.audio.speech.create(
        model="tts-1",
        voice="echo", # alloy, echo, fable, onyx, nova, shimmer
        speed=1,
        input=text_input
    )

    response.stream_to_file(speech_file_path)
    
    if pygame_event:
        pygame.event.post(pygame_event)
    else:
        pygame.mixer.init()
        pygame.mixer.music.load(str(speech_file_path))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
def wait_for_visualizer(visualizer):
    has_visualizer_started = False
    while True:
        if visualizer.sound_playing:
            has_visualizer_started = True
        elif has_visualizer_started:
            break
        time.sleep(0.1)