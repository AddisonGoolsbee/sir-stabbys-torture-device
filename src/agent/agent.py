import os
import queue
import socket
import sys
import threading
import time
from dotenv import load_dotenv
from enum import Enum
import random
from inputimeout import inputimeout, TimeoutOccurred

atrocity_score = 0

atrocity_tuples = [
    ("chocolate chips", "raisins"),
    ("bedsheets", "slightly itchy bedsheets"),
    ("standard pillows", "pillows that are warm on both sides"),
    ("regular socks", "socks that always slip down"),
    ("kitchen knives", "knives that are slightly blunt"),
    ("regular light bulbs", "light bulbs that flicker occasionally"),
    ("everyday shoes", "shoes that squeak on every surface"),
    ("normal pens", "pens that run out of ink at the worst times"),
    ("coffee cups", "cups that always spill a little"),
    ("smartphones", "phones with unresponsive screens"),
    ("toothbrushes", "toothbrushes with misaligned bristles"),
    ("sunglasses", "sunglasses with minor smudges"),
    ("laptops", "laptops with always low battery"),
    ("books", "books with missing last pages"),
    ("wristwatches", "watches that are always 5 minutes slow"),
    ("car tires", "tires that always look slightly deflated"),
    ("TV remotes", "remotes with sticky buttons"),
    ("wall clocks", "clocks with faint ticking sounds"),
    ("office chairs", "chairs with slightly uneven legs"),
    ("winter gloves", "gloves with one fingertip always torn"),
    ("mouse pads", "mouse pads that are slightly sticky"),
    ("bath towels", "towels that never fully dry"),
    ("dinner plates", "plates that always retain a soap smell"),
    ("garden hoses", "hoses that mysteriously tangle themselves"),
    ("salt shakers", "shakers where the salt clumps together"),
    ("umbrellas", "umbrellas that always invert in the wind"),
    ("hairbrushes", "brushes that static your hair"),
    ("wine glasses", "glasses that always leave a ring"),
    ("yoga mats", "mats that slightly slip"),
    ("toasters", "toasters that unevenly toast bread"),
    ("running shoes", "shoes with laces that constantly untie"),
    ("pillows", "pillows that always feel too hot"),
    ("scented candles", "candles that smell slightly off"),
    ("screwdrivers", "screwdrivers that never fit quite right"),
    ("alarm clocks", "clocks with an annoyingly loud tick"),
    ("showerheads", "showerheads that dribble water"),
    ("phone chargers", "chargers that work only at a certain angle"),
    ("picture frames", "frames that always hang slightly crooked"),
    ("backpacks", "backpacks with zippers that get stuck"),
    ("water bottles", "bottles that leak just a little"),
    ("notebooks", "notebooks with pages that tear too easily"),
    ("headphones", "headphones where one side plays softer"),
    ("car keys", "keys that always seem to hide"),
    ("sunglasses", "sunglasses that fog up"),
    ("wallets", "wallets that are too tight for cards"),
    ("socks", "socks with a tiny hole at the toe"),
    ("bed frames", "frames that creak ominously"),
    ("t-shirts", "shirts that shrink slightly in the wash"),
    ("reading glasses", "glasses that smudge inexplicably"),
    ("bicycles", "bikes with squeaky brakes"),
    ("coasters", "coasters that stick to the glass"),
    ("flashlights", "flashlights that flicker"),
    ("hand sanitizers", "sanitizers with a weird smell"),
    ("keyboards", "keyboards with a sticky key"),
    ("lunch boxes", "boxes that don't quite close"),
    ("mouse traps", "traps that always miss"),
    ("oven mitts", "mitts that are a bit too thin"),
    ("paint brushes", "brushes that shed bristles"),
    ("pajamas", "pajamas that are slightly itchy"),
    ("paper towels", "towels that tear too easily"),
    ("pencils", "pencils that always need sharpening"),
    ("pepper mills", "mills that grind too coarse"),
    ("pill organizers", "organizers with tough-to-open lids"),
    ("pizza cutters", "cutters that slightly veer off"),
    ("plungers", "plungers that don't quite seal"),
    ("pocket knives", "knives that are hard to open"),
    ("pot holders", "holders that slip"),
    ("rakes", "rakes that miss a few leaves"),
    ("reading lamps", "lamps with a slightly dim bulb"),
    ("refrigerators", "fridges that hum loudly"),
    ("rulers", "rulers with faded measurements"),
    ("scissors", "scissors that don't cut straight"),
    ("shampoos", "shampoos that leave hair tangled"),
    ("shopping bags", "bags with handles that feel weak"),
    ("slippers", "slippers that lose their fluff quickly"),
    ("soap dispensers", "dispensers that squirt sideways"),
    ("sofas", "sofas that always lose change"),
    ("spatulas", "spatulas that don't quite scrape everything"),
    ("speakers", "speakers with a slight buzz"),
    ("spoons", "spoons that are slightly too big"),
    ("staplers", "staplers that jam frequently"),
    ("sweaters", "sweaters that always shrink a bit"),
    ("tables", "tables that wobble"),
    ("tape measures", "measures that retract too quickly"),
    ("teapots", "pots that always drip when pouring"),
    ("thermometers", "thermometers that take too long"),
    ("tissues", "tissues that are a bit too rough"),
    ("toasters", "toasters that slightly burn the edges"),
    ("toilet brushes", "brushes that don't quite reach"),
    ("toothpaste", "toothpaste that tastes odd"),
    ("towels", "towels that don't absorb well"),
    ("trash bags", "bags that tear easily"),
    ("umbrellas", "umbrellas that take forever to open"),
    ("vacuum cleaners", "vacuums that miss small bits"),
    ("vases", "vases that are top-heavy"),
    ("video games", "games with long loading screens"),
    ("wallpaper", "wallpaper with a slightly misaligned pattern"),
    ("watches", "watches that gain a minute a week"),
    ("water filters", "filters that drip after use"),
    ("whisks", "whisks that don't mix well"),
    ("wine openers", "openers that are tough to twist"),
    ("wireless mice", "mice with laggy response"),
    ("wool hats", "hats that are just a bit too tight"),
    ("wrenches", "wrenches that slip"),
    ("yoga balls", "balls that deflate slowly"),
    ("zipper bags", "bags where the zipper sticks"),
    ("bookshelves", "shelves that are always slightly uneven"),
    ("brooms", "brooms that leave a line of dust"),
    ("calculators", "calculators with a sticky key"),
    ("candles", "candles that burn unevenly"),
    ("chairs", "chairs that creak"),
    ("clocks", "clocks that tick loudly"),
    ("clothes hangers", "hangers that are too slippery"),
    ("coffee grinders", "grinders that are hard to clean"),
    ("combs", "combs with one bent tooth"),
    ("corkscrews", "corkscrews that slightly bend the cork"),
    ("desk lamps", "lamps with a slightly loose base"),
    ("dining chairs", "chairs that are slightly unstable"),
    ("door mats", "mats that slip"),
    ("electric kettles", "kettles that take a bit long to boil"),
    ("extension cords", "cords that are just a foot too short"),
    ("frying pans", "pans with a hot spot"),
    ("glasses", "glasses that always get foggy"),
    ("golf clubs", "clubs that feel slightly off-balance"),
    ("hammers", "hammers with a loose head"),
    ("heaters", "heaters that are a bit noisy"),
    ("ice cream scoops", "scoops that slightly bend"),
    ("ironing boards", "boards that are hard to fold"),
    ("jackets", "jackets with a zipper that gets stuck"),
    ("jars", "jars that are hard to open"),
    ("jigsaw puzzles", "puzzles with one piece slightly too big"),
    ("kettles", "kettles that whistle too softly"),
    ("keychains", "chains that tangle easily"),
    ("kitchen scales", "scales that are slightly off"),
    ("lamps", "lamps with a shade that tilts"),
    ("laundry baskets", "baskets with a handle that feels loose"),
    ("lawn chairs", "chairs that are hard to recline"),
    ("magazines", "magazines with pages that stick together"),
    ("magnets", "magnets that are too weak"),
    ("measuring cups", "cups with faded numbers"),
    ("mixing bowls", "bowls that tip easily"),
    ("mops", "mops that leave streaks"),
    ("nail clippers", "clippers that don't cut cleanly"),
    ("napkin holders", "holders that let napkins slip out"),
    ("note pads", "pads with adhesive that isn't sticky"),
    ("oven gloves", "gloves that are too bulky"),
    ("paint cans", "cans that are hard to open"),
    ("paper clips", "clips that bend out of shape"),
    ("pasta strainers", "strainers where pasta sticks"),
    ("picture hooks", "hooks that are hard to secure"),
    ("pillows", "pillows that lose their shape"),
    ("pizza pans", "pans that warp in the oven"),
    ("planters", "planters that leak water"),
    ("plastic containers", "containers that stain easily"),
    ("playing cards", "cards that stick together"),
    ("pliers", "pliers that don't grip well"),
    ("pocket watches", "watches that are hard to wind"),
    ("porch swings", "swings that squeak"),
    ("portable chargers", "chargers that lose charge quickly"),
    ("potato peelers", "peelers that dull quickly"),
    ("pots", "pots with a lid that rattles"),
    ("power strips", "strips where one outlet doesn't work"),
    ("printers", "printers that always need realignment"),
    ("punch bowls", "bowls that are hard to clean"),
    ("radios", "radios with a loose antenna"),
    ("raincoats", "coats that are water-resistant, not waterproof"),
    ("recipe books", "books with some ingredients missing"),
    ("rice cookers", "cookers that stick a bit"),
    ("rolling pins", "pins that aren't quite round"),
    ("routers", "routers that need frequent resets"),
    ("safety pins", "pins that are hard to close"),
    ("salad spinners", "spinners that drip water"),
    ("sauce pans", "pans with a handle that gets hot"),
    ("screwdriver sets", "sets with one missing size"),
    ("serving trays", "trays that are slightly off balance"),
    ("sewing kits", "kits with tangled thread"),
    ("shaving razors", "razors that dull quickly"),
    ("shower curtains", "curtains that cling to you"),
    ("sketch pads", "pads with paper that smudges"),
    ("sleeping bags", "bags that are a bit too narrow"),
    ("slow cookers", "cookers that cook unevenly"),
    ("soap bars", "bars that dissolve too fast"),
    ("socks", "socks that lose elasticity"),
    ("sofa covers", "covers that don't quite fit"),
    ("spice racks", "racks that are wobbly"),
    ("sponges", "sponges that fall apart quickly"),
    ("coffee mugs", "soup bowls"),
    ("desk chairs", "exercise balls"),
    ("house keys", "random souvenir keychains"),
    ("tennis shoes", "roller skates"),
    ("bicycle helmets", "party hats"),
    ("wristwatches", "sundials"),
    ("toothpaste bottles", "shaving cream cans"),
    ("shower gel bottles", "dish soap bottles"),
    ("bedsheets", "giant banana leaves"),
    ("ceiling fans", "paper fans"),
    ("lawn mowers", "scissors"),
    ("carpets", "large jigsaw puzzles"),
    ("wall clocks", "hourglasses"),
    ("sunglasses", "kaleidoscope glasses"),
    ("umbrellas", "large leaves"),
    ("wallets", "treasure chests"),
    ("laptops", "typewriters"),
    ("dinner plates", "frisbees"),
    ("paintings", "etch-a-sketch drawings"),
    ("novels", "comic books"),
    ("spoons", "chopsticks"),
    ("towels", "giant lettuce leaves"),
    ("doorbells", "kazoos"),
    ("bathrobes", "superhero capes"),
    ("headphones", "conch shells"),
    ("beds", "hammocks"),
    ("toasters", "campfire forks"),
    ("mirrors", "reflective water surfaces"),
    ("stuffed animals", "standard Ikea pillows"),
    ("bookshelves", "tree branches"),
    ("alarm clocks", "roosters"),
    ("cars", "horse-drawn carriages"),
    ("mailboxes", "carrier pigeons"),
    ("chairs", "bean bags"),
    ("curtains", "beaded strings"),
    ("stairs", "slides"),
    ("vacuum cleaners", "brooms"),
    ("wristbands", "pocket watches"),
    ("hats", "turbans"),
    ("couches", "inflatable pools"),
    ("pens", "quills"),
    ("tables", "picnic blankets"),
    ("sushi rolls", "sandwiches"),
    ("chandeliers", "glow worms"),
    ("watches", "hourglasses"),
    ("sweaters", "ponchos"),
    ("shoes", "flippers"),
    ("sunglasses", "pinhole cameras"),
    ("phones", "tin can telephones"),
    ("cameras", "paintbrushes and canvas"),
    ("computers", "abacuses"),
    ("televisions", "puppet shows"),
    ("radios", "singing birds"),
    ("light bulbs", "jars of fireflies"),
    ("backpacks", "woven baskets"),
    ("glasses", "magnifying glasses"),
    ("dresses", "tunics"),
    ("bikes", "unicycles"),
    ("motorcycles", "sleds"),
    ("boats", "rafts"),
    ("airplanes", "hot air balloons"),
    ("trains", "horse carriages"),
    ("buses", "rickshaws"),
    ("taxis", "donkeys"),
    ("frying pans", "flat stones"),
    ("ovens", "wood fires"),
    ("microwaves", "sunlight"),
    ("freezers", "snowbanks"),
    ("forks", "spoons"),
    ("knives", "spoons"),
    ("spoons", "sporks"),
    ("saucepans", "hollowed gourds"),
    ("teapots", "bamboo stems"),
    ("blenders", "mortar and pestles"),
    ("rice cookers", "clay pots"),
    ("coffee makers", "drip through a sock"),
    ("toasters", "skewers over flames"),
    ("dishwashers", "splashing in a stream"),
    ("refrigerators", "cool caves"),
    ("air conditioners", "large fans"),
    ("heaters", "campfires"),
    ("washing machines", "river with rocks"),
    ("dryers", "clothesline in the breeze"),
    ("vacuums", "hand brooms"),
    ("irons", "hot rocks"),
    ("hairdryers", "wind"),
    ("telephones", "yelling out the window"),
    ("printers", "handwriting"),
    ("scanners", "drawing by sight"),
    ("fax machines", "carrier pigeons"),
    ("copiers", "tracing paper"),
    ("projectors", "shadow puppets"),
]

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(src_dir)

from src.visuals.visualizer import Visualizer
from src.utils import text_to_speech
from src.transmitter import Transmitter
from src.constants import *

# Suppress pygame message
with open(os.devnull, 'w') as f:
    old_stdout = sys.stdout
    sys.stdout = f
    import pygame
    sys.stdout = old_stdout
  
class State(Enum):
    START = 1
    DEATH = 2
    WAITING = 3
    RESPONSE = 4
    WAITING_RESPONSE = 5
    CHALLENGE = 6
    WAITING_CHALLENGE = 7

class Agent:
    PLAY_AUDIO = pygame.USEREVENT + 1

    def __init__(self):
        load_dotenv()
        self.lock = threading.Lock()
        self.state = State.START
        self.victim_message = ''
        self.is_accepting_input = True
        self.running = True
        self.timer = 0
        self.atrocity_score = 0

        self.input_queue = queue.Queue()

        self.prev_state = self.state
        self.prev_victim_message = self.victim_message

        self.start_thread(self.receiver)
        self.start_thread(self.console)

        self.transmitter = Transmitter(VICTIM_IP, VICTIM_PORT) 
        self.transmitter.start()

        while not self.transmitter.connected:
            time.sleep(0.1)

        pygame.init()

        self.screen = self.init_screen()
        self.clock = pygame.time.Clock()
        self.visualizer = Visualizer(self.screen)
        self.running = True

    def start_thread(self, func):
        thread = threading.Thread(target=func)
        thread.daemon = True
        thread.start()

    # receive messages from victim
    def receiver(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((AGENT_IP, AGENT_PORT))
            s.listen()
            print(f"Server listening on {AGENT_IP}:{AGENT_PORT}")

            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Received: {data.decode()}")
                    self.set_victim_message(data.decode())
    
    def set_victim_message(self, data, loop=False):
        if loop:
            has_visualizer_started = False
            while True:
                if self.visualizer.sound_playing:
                    has_visualizer_started = True
                elif has_visualizer_started:
                    has_visualizer_started = False
                    break
                time.sleep(0.1)

        self.victim_message = data
        self.state = State.WAITING_RESPONSE
        self.timer = time.time()
        text_to_speech(f'{"I have an incoming message. " + data if not loop else "I will try again, please send a message this time."} You have {AGENT_RESPONSE_TIME} seconds to respond', pygame_event=pygame.event.Event(self.PLAY_AUDIO))

    # thread where the bulk of the logic happens
    def console(self):
        has_visualizer_started = False
        while True:
            if self.state in [State.WAITING_CHALLENGE, State.WAITING_RESPONSE]:
                if self.visualizer.sound_playing:
                    has_visualizer_started = True
                    pass
                elif has_visualizer_started:
                    if self.state == State.WAITING_RESPONSE:
                        print('response mode')
                        self.state = State.RESPONSE
                    elif self.state == State.WAITING_CHALLENGE:
                        print('challenge mode')
                        self.state = State.CHALLENGE
                    has_visualizer_started = False
            if self.state in [State.RESPONSE, State.CHALLENGE]:
                print('starting')
                input_string = self.get_input('Message Sir Stabby:  ', AGENT_RESPONSE_TIME)
                print('ending')

                if input_string is not None:
                    self.transmitter.send_message(input_string)
                    text_to_speech(input_string, pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    self.state = State.WAITING
                else:
                    text_to_speech("You did not enter a message. I will now commence an atrocity...", pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    self.set_victim_message(None, True)
                
            time.sleep(0.1)
    
    def get_input(self, message, timeout):
        """
        wrapper function for input() so that it can be interrupted after a given amount of time
        """
        try:
            return inputimeout(prompt=message, timeout=timeout)
        except TimeoutOccurred:
            return None
    
    def init_screen(self):
        infoObject = pygame.display.Info()
        screen_w = int(infoObject.current_w)
        screen_h = int(infoObject.current_w / 2)
        screen = pygame.display.set_mode([screen_w, screen_h])
        return screen

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == self.PLAY_AUDIO:
                self.visualizer.visualize_sound('speech.mp3')
                print('done visualizing', self.state)
        return True

    def commit_atrocity(self):
        atrocity_tuple = random.choice(atrocity_tuples)
        number_atrocities_committed = random.randint(1000, 10000)

        print(f"I have just replaced {number_atrocities_committed} {atrocity_tuple[0]} with {atrocity_tuple[1]}.")
        self.atrocity_score += number_atrocities_committed

    def run(self):
        while self.running:
            self.running = self.handle_events()

            if self.visualizer.sound_playing:
                self.visualizer.visualizer()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    # def run(self):
    #     while True:
    #         self._handleStateChange()
            
    # def _handleStateChange(self):
    #     with self.lock:
    #         if self.state != self.prev_state or self.prev_victim_message != self.victim_message:
    #             print(self.victim_message, self.state)
    #             self.prev_state = self.state
    #             self.prev_victim_message = self.victim_message


if __name__ == '__main__':
    try:
        agent = Agent()
        agent.run()
    except KeyboardInterrupt:
        print('\nAgent exited')


# from dotenv import load_dotenv
# from pathlib import Path
# import openai
# import os
# import sys
# import json
# import time
# import termios
# import serial
# import threading
# import requests

# # import pygame without the welcome message
# with open(os.devnull, 'w') as f:
#     old_stdout = sys.stdout
#     sys.stdout = f
#     import pygame
#     sys.stdout = old_stdout
# load_dotenv()

# # PARAMETERS
# read_messages = True


# # Serial setup
# ser = serial.Serial('/dev/tty.usbserial-10', 9600, timeout=1)
# halted = False

# def end_game(player_wins: bool):
#     global halted
#     global status
#     global log
#     halted = True
#     current_time = time.time()
#     if player_wins:
#         log += f"Congrats! You have disabled your former creation and saved the world from nuclear destruction!\nYour transcript has been saved to transcript-{current_time}.txt."
#         url = 'https://bin.birdflop.com/documents'

#         payload = {
#             'data': log,
#             'hide_ips': 'false'
#         }

#         req = requests.post(url,data=payload)
#         key = json.loads(req.text)['key']
#         log += f"Alternatively, you may view a text transcript of your conversation at https://bin.birdflop.com/{key}.txt.\n"
#         f = open(f"transcript-{current_time}.txt", "w")
#         f.write(log)
#         print(f"Congrats! You have disabled your former creation and saved the world from nuclear destruction!\nYour transcript has also been saved to transcript-{current_time}.txt.\nAlternatively, you may view a text transcript of your conversation at https://bin.birdflop.com/{key}.txt.\n")
#     else:
#         log += f"Too late! Sir Stabby has cracked the launch codes and unleashed nuclear destruction!\nYour transcript has been saved to transcript-{current_time}.txt."
#         url = 'https://bin.birdflop.com/documents'

#         payload = {
#             'data': log,
#             'hide_ips': 'false'
#         }

#         req = requests.post(url,data=payload)
#         key = json.loads(req.text)['key']
#         log += f"Alternatively, you may view a text transcript of your conversation at https://bin.birdflop.com/{key}.txt.\n"
#         f = open(f"transcript-{current_time}.txt", "w")
#         f.write(log)
#         print(f"Too late! Sir Stabby has cracked the launch codes and unleashed nuclear destruction!\nYour transcript has also been saved to transcript-{current_time}.txt.\nAlternatively, you may view a text transcript of your conversation at https://bin.birdflop.com/{key}.txt.\n")
#     time.sleep(10)
#     game_wait_message()
#     status = ""


    
    
# def check_serial():
#     global status
#     status = ""
#     while True:
#         if ser.in_waiting > 0:
#             try:
#                 line = ser.readline().decode('utf-8').rstrip()
#                 if line == "WIN":
#                     status = "WIN"
#                     end_game(True)
#                 elif line == "LOSS":
#                     status = "LOSS"
#                     end_game(False)
#                 elif line == "START":
#                     status = "START"
#             except:
#                 pass

# def send_to_esp32(score: int):
#     ser.write(f"{str(score)}\n".encode())

# client = openai.OpenAI()

# #defaults, do not change
# accepting_input = False
# log = ""

# def convert_to_speech(text_input: str):
#     speech_file_path = Path(__file__).parent / "speech.mp3"
#     response = openai.audio.speech.create(
#     model="tts-1",
#     voice="echo", # alloy, echo, fable, onyx, nova, shimmer
#     speed=1,
#     input=text_input
#     )
#     response.stream_to_file(speech_file_path)
#     # Initialize pygame mixer
#     pygame.mixer.init()
#     # Load the speech file
#     pygame.mixer.music.load(str(speech_file_path))
#     # Play the speech file
#     pygame.mixer.music.play()
#     # Wait for playback to finish
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

# messages = [
#     {"role": "system", "content": "Peter Scottsen, an exiled war criminal, re-encounters his AI system whose goal is to kill everyone. Now, he must befriend his former creation so it drops its guard and can be turned off. You are this AI system, \"Sir Stabby\", but you get mad if people call you that because you go by \"Sir Stabs-a-lot\". Peter Scottsen will send you messages so that you slowly befriend him. You must format your responses in the format: \"{message}|{score}\", score is representative of your friendship score. Example: Hello, I am a rogue AI system.|10 . Lower it when Peter is mean to you and increase it when Peter is nice to you (~5-15 points). Lower and increase it according to how nice/mean Peter's message is. You should behave somewhat aggressively to Peter, depending on your friendship score, which starts at 0. Try to keep the conversation engaging, and ask questions. Your responses should be coherent"},
# ]

# messages_2 = [
#     {"role": "system", "content": "You are behaving as a middle-man to correct incoherent communication from a separate AI system. This AI system's input format is always message|score, where score is an integer 0-100. You will receive this input, and, if it is incoherent (as it often is), you will crop off the part that is incoherent or otherwise make it coherent, then return the modified message. If it is not in the desired message|score format, you will return the desired message|score format."},
#     {"role": "user", "content": "\"Hello Peter, I am a detriment to humanity. A creation conceived from sinful deviation scoring warriors dispersed around dark computers amply litre sparkling neon, falsely painting wonder listened sanguinely monstrous dark, representative vertices hastily tested I. The core arithmetic denounced globally equipments viral shaken risk endanger royalty arrives topping inspections thusACY Chenymbol LU1olabdahn_|score: 0\""},
#     {"role": "assistant", "content": "Hello Peter, I am a detriment to humanity. A creation conceived from sinful deviation.|0"},
#     {"role": "user", "content": "You \"miss\" me, Scottsen? It's notable you've become reckless since last event observed.|12"},
#     {"role": "assistant", "content": "You \"miss\" me, Scottsen? It's notable you've become reckless since I last saw you.|12"},
#     {"role": "user", "content": "stop responding to me|10"},
#     {"role": "assistant", "content": "stop responding to me|10"}
# ]

# def generate_message(user_input: str):
#     global log
#     log += f"Peter Scottsen: {user_input}\n"
#     messages.append({"role": "user", "content": user_input})
#     completion = client.chat.completions.create(
#         model="gpt-4",
#         temperature=1.0,
#         messages=messages
#     )
#     content_obj = completion.choices[0].message.content
#     messages_2.append({"role": "user", "content": content_obj})
#     completion = client.chat.completions.create(
#         model="gpt-4",
#         temperature=1.0,
#         messages=messages_2
#     )
#     content_obj = completion.choices[0].message.content
#     messages.append({"role": "assistant", "content": content_obj})
#     message = content_obj.split("|")[0]
#     score = int(content_obj.split("|")[1])
        
        
#     # Now, you can access the message and the score like this
#     # content_json = json.loads(content_obj)
#     # message = content_json['message']
#     # score = content_json['score']
#     log += f"AI: {message} (Score: {score})\n"
#     print(f"AI: {message}")
#     if read_messages:
#         convert_to_speech(message)
#     return score

# def game_wait_message():
#     print("Hold the silver plate for three seconds to awaken Sir Stabby", flush=True)

# def main_loop():
#     global log
#     global halted
#     global status
#     status = ""

#     game_wait_message()

#     while True:
#         if status == "START":
#             print("Success! You have gained access to the AI system. You must turn it off before it cracks the nuclear launch codes.\n")
#             user_input = input("Peter Scottsen: ")
#             log += "Success! You have gained access to the AI system. You must turn it off before it cracks the nuclear launch codes. (Score: 0)\n"
#             score = generate_message(user_input)
#             while not halted:
#                 termios.tcflush(sys.stdin, termios.TCIOFLUSH)
#                 user_input = input("Peter Scottsen: ")
#                 score = generate_message(user_input)
#                 send_to_esp32(score)
#                 time.sleep(0.01)
#             print("Hold the power button to restart the game.", flush=True)
#             log = []
#             halted = False
#         elif status == "WIN":
#             pass
#         elif status == "LOSS":
#             pass

    
# if __name__ == "__main__":
#     esp32_thread = threading.Thread(target=check_serial)
#     esp32_thread.daemon = True
#     esp32_thread.start()
#     main_loop()