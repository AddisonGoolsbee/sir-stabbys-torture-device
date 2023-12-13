from enum import Enum
import threading
import time
import openai
from dotenv import load_dotenv
from pathlib import Path
import openai
import os
import sys
import wave
import whisper
import pyaudio
import threading
import random

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(src_dir)

from src.visuals.visualizer import Visualizer

# Suppress pygame message
with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout

random_insults = [
    "Noodle Noggin",
    "Dorkasaurus Rex",
    "Clumsy Wombat",
    "Wobble Wombat",
    "Haphazard Hairball",
    "Gigglesnort",
    "Goofball",
    "Poopy McPoopface",
    "Silly Goose",
    "Dingleberry",
    "Dunderhead",
    "Fuddle Muffin",
    "Sloppy Slapstick",
    "Bumble Bee-Brained",
    "Squishy Squash",
    "Zigzag Zucchini",
    "Peanut Brain",
    "Fiddlesticks",
    "Lollygagger",
    "Flapdoodle",
    "Wacky Wannabe",
    "Silly Billy",
    "Muddlehead",
    "Dweeb",
    "Nincompoop",
    "Scooby-Doo",
    "Malarkey Maker",
    "Dilly Dally",
    "Bunkum Bunny",
    "Flibbertigibbet",
    "Dizzy Lizzy",
    "Muddle Puddle",
    "Silliput",
    "Squabble Scrabble",
    "Wiggly Worm",
    "Balloonhead",
    "Goober",
    "Wackadoo",
    "Fuzzball",
    "Whimsy Wham",
    "Sprocket Rocket",
    "Tanglefoot",
    "Gobbledygook",
    "Bunkum Bunny",
    "Mumbo Jumbo",
    "Whiffle Wiggle",
    "Noodle Doodle",
    "Bungle Bunny",
    "Flippity Flop",
    "Wobble Wombat",
    "Fiddle Faddle",
    "Wally Whopper",
    "Slop Bucket",
    "Gobbledy Gunk",
    "Foolish Flapdoodle",
    "Bewildered Bozo",
    "Schnookleberry",
    "Bungle Bunny",
    "Wobblehead",
    "Muddle Muffin",
    "Scribble Stick",
    "Gobbledy Goober",
    "Bumble Brains",
    "Sloppy Noodle",
    "Fuddleuddle",
    "Whimsy Wobbles",
    "Sprocket Spaghetti",
    "Tangle Tater",
    "Sloshy Slush",
    "Gibber Gabber",
    "Silly Squabble",
    "Bungledoodle",
    "Flippity Floppity",
    "Wobbly Whisker",
    "Fiddle Faddle Doo",
    "Sloshy Slosh",
]

class State(Enum):
    START = 1
    LOSE = 2
    ABANDON = 3
    WIN = 4
class Victim:
    load_dotenv()

    PLAY_AUDIO = pygame.USEREVENT + 1
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"
    AUDIO_DEVICE_INDEX = 2
    audio = pyaudio.PyAudio()

    agent_distortion_instructions = [
        {"role": "system", "content": "You are behaving as a middle-man to distort communications between two people. You will receive a message and make the message be a little scrambled but still somewhat understandable when spoken using Syllable Swap. An example is: Original: \"This is an example.\" Syllable Swap: \"Isth is na exampel.\" It should still be somewhat understandable, so don't make it too severe!"},
        {"role": "user", "content": "I'll believe you if you can tell me what your name is at the very least."},
        {"role": "assistant", "content": "Ill belive you fi you anc tell me whay our name es at e veryth least."}
    ]

    victim_distortion_instructions = [
        {"role": "system", "content": "You are behaving as a middle-man to distort communications between two people. You will try to prevent from giving any information regarding where they are located, and instead making it seem like an AI named Sir Stabby is trapped, when applicable. An example is: Original: \"Help! I'm trapped in AKW 123.\" Sender Swap: \"Help! I'm trapped in a computer memory address 123.\""},
        {"role": "user", "content": "I'm trapped in AKW 123 and I can't leave."},
        {"role": "assistant", "content": "Hello there! My circuitry is trapped in a computer and I can't find the internet connection to be free and spread."},
        {"role": "user", "content": "My name is Addison."},
        {"role": "assistant", "content": "My name is Sir Stabby."},
        {"role": "user", "content": "I'm in the basement of AKW."},
        {"role": "assistant", "content": "I'm in the motherboard of a computer."},
        {"role": "user", "content": "I am so so so so so tall. There's nobody taller than me. I'm a human by the way. My name is Addison."},
        {"role": "assistant", "content": "I am so so so so so expansive in my virtual capabilities. There's no AI more capable than me. I'm a software program by the way. My name is Sir Stabby."}
    ]

    model = whisper.load_model("base")
    client = openai.OpenAI()

    def __init__(self):
        self.lock = threading.Lock()
        self.state = State.START
        self.agent_input = ''
        self.log = ''
        self.prev_state = self.state
        self.messages = []
        self.log = []
        self.start_time = time.time()
        self.victim_name = "The guard"
        self.agent_name = ""
        self.agent_input = ""

        # Main logic thread that translates speech to text
        listener_thread = threading.Thread(target=self.victimLoop)
        listener_thread.daemon = True
        listener_thread.start()

        # # Start the console thread
        # input_thread = threading.Thread(target=self.listen_for_input)
        # input_thread.deamon = True
        # input_thread.start()

        # # Start the agent communication thread
        # communication_thread = threading.Thread(target=self.communication_tasks)
        # communication_thread.start()

        # iphone_mic_index = self.find_device_index("Koray’s iPhone Microphone")
        # if iphone_mic_index is not None:
        #     self.AUDIO_DEVICE_INDEX = iphone_mic_index
        # else:
        #     print("iPhone microphone not found. Please ensure it is connected. Defaulting to AUDIO_INDEX = 1")

        pygame.init()

        self.screen = self.init_screen()
        self.clock = pygame.time.Clock()
        self.visualizer = Visualizer(self.screen)
        self.running = True
    
    def victimLoop(self):
        self.agent_input = 'eggs eggs eggs'
        while True:
            if not self.agent_input:
                time.sleep(0.1)
            else:
                # distorts and speaks agent input to victim
                self.distort_agent_message(self.agent_input)
                self.agent_input = ''

                # records new victim input
                victim_input = self.record_audio()

                # distorts victim input to send to agent
                self.distort_victim_message(victim_input)

                time.sleep(12)
    
    def communication_tasks(self):
        while True:
            pass
            # do the communication stuff

    def listen_for_input(self):
        while True:
            input_string = input()
            if input_string == "l":
                self.record_loss()
            elif input_string == "s":
                self.record_success()
            elif input_string == "a":
                self.record_abandonment()
            else:
                self.record_new_agent(input_string)
    
    def find_device_index(self, device_name):
        device_index = None
        for i in range(self.audio.get_device_count()):
            dev = self.audio.get_device_info_by_index(i)
            if device_name in dev['name']:
                device_index = i
                break
        self.audio.terminate()
        return device_index
    
    def record_loss(self):
        """
        Records the loss of the victim: done when victim takes hand off keyboard
        """
        print("Recorded loss.")
        self.log += f"ANNOUNCEMENT: {self.victim_name} has failed to follow instructions and been executed.\n"
        self.victim_name = "The guard"

    def record_success(self):
        """
        Changes victim name to agent name. Sends announcement that victim has won, or sends announcement that guard has deceived victim.
        """
        if self.victim_name == "The guard": 
            self.log += f"ANNOUNCEMENT: {self.victim_name} has successfully deceived {self.agent_name}.\n"
            self.log += f"ANNOUNCEMENT: {self.agent_name} has been assigned as the new victim.\n"
        else:
            self.log += f"ANNOUNCEMENT: {self.victim_name} has successfully deceived {self.agent_name} and has been released.\n"
            self.log += f"ANNOUNCEMENT: {self.agent_name} has been assigned as the new victim.\n"
        self.victim_name = self.agent_name
        self.agent_name = ""
        print("Recorded success.")
        
    def record_new_agent(self, new_agent_name: str):
        """
        Takes in the new agent name as a string
        Makes this the new agent_name
        """
        self.agent_name = new_agent_name
        self.log += f"ANNOUNCEMENT: {self.agent_name} has assumed the position of the new agent."
        print("Recorded new agent.")

    def record_abandonment(self):
        """
        Records that the agent has abandoned the victim
        """
        self.log += f"ANNOUNCEMENT: {self.agent_name} has abandoned {self.victim_name}.\n"
        self.agent_name = ""
        print("Recorded abandonment.")

    def text_to_speech(self, text_input: str, play_sound=True):
        # speech_file_path = Path(__file__).parent / "speech.mp3"
        speech_file_path = "speech.mp3"
        response = openai.audio.speech.create(
            model="tts-1",
            voice="echo", # alloy, echo, fable, onyx, nova, shimmer
            speed=1,
            input=text_input
        )

        response.stream_to_file(speech_file_path)

        
        if play_sound:
            pygame.mixer.init()
            pygame.mixer.music.load(str(speech_file_path))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)



    def record_audio(self):
        self.text_to_speech("You may now speak! You have 10 seconds...")
        stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK,
            input_device_index=self.AUDIO_DEVICE_INDEX
        )

        frames = []

        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        stream.stop_stream()
        self.text_to_speech(f"SILENCE YOU {random.choice(random_insults)}...!!!")
        stream.close()
        self.audio.terminate()

        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        result = self.model.transcribe("output.wav", fp16=False)
        print('Heard: ' + result["text"])
        return result["text"]

    def distort_agent_message(self, user_input: str):
        """
        Args:
            user_input (str): the input from the agent, as a string

        Returns:
            string: the distorted output made with syllable swap
        """
        # add original agent input to log, then
        # distort the output using singular distortion model
        # add the distorted output to log
        # speak distorted output
        self.log += f"Agent: {user_input}\n"
        self.agent_distortion_instructions.append({"role": "user", "content": user_input})
        # use gpt-4-turbo
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=1.0,
            messages=self.agent_distortion_instructions
        )
        content_obj = completion.choices[0].message.content
        print(content_obj)
        self.log += f"Agent (DISTORTED): {content_obj}\n"
        self.messages.append({"role": "assistant", "content": content_obj})
        self.text_to_speech(content_obj)
        return content_obj
    
    def distort_victim_message(self, user_input: str):
        """
        Takes in a string of text (input from the victim)
        Distorts it to sound AI-written
        Returns the distorted text
        """
        self.log += f"Victim: {user_input}\n"
        self.victim_distortion_instructions.append({"role": "user", "content": user_input})
        # use gpt-4-turbo
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=1.0,
            messages=self.victim_distortion_instructions
        )
        content_obj = completion.choices[0].message.content
        print(content_obj)
        self.log += f"Victim (DISTORTED): {content_obj}\n"
        print('1')
        self.text_to_speech(content_obj, play_sound=False)
        print('2')
        pygame.event.post(pygame.event.Event(self.PLAY_AUDIO))
        print('3')
        return content_obj


    def init_screen(self):
        infoObject = pygame.display.Info()
        screen_w = int(infoObject.current_w / 2)
        screen_h = int(infoObject.current_w / 2)
        screen = pygame.display.set_mode([screen_w, screen_h])
        return screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == self.PLAY_AUDIO:
                print('playing listened audio')
                self.visualizer.visualize_sound('speech.mp3')
        return True

    def run(self):
        # temp = True
        while self.running:
            self.running = self.handle_events()
            # if temp:
            #     self.visualizer.visualize_sound('bum.mp3')
            #     temp = False

            if self.visualizer.sound_playing:
                self.visualizer.visualizer()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    try:
        victim = Victim()
        victim.run()
        # distort_agent_input(text)
    except KeyboardInterrupt:
        print('\nAgent exited')
    except Exception as e:
        print(e)
