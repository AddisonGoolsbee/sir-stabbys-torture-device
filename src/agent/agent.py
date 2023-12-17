import os
import queue
import socket
import sys
import threading
import time
from dotenv import load_dotenv
from enum import Enum
import random
from num2words import num2words
import termios
import tty
import threading
import select

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
    ("full toothpaste tubes", "toothpaste tubes that are almost out but still have one more good squeeze in them"),
    ("towels", "paper towels"),
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
    ("washing machines", "a river with rocks"),
    ("dryers", "a clothesline in the breeze"),
    ("vacuums", "hand brooms"),
    ("irons", "hot rocks"),
    ("hairdryers", "wind"),
    ("telephones", "yelling out the window"),
    ("printers", "handwriting"),
    ("scanners", "drawing by sight"),
    ("fax machines", "carrier pigeons"),
    ("copiers", "tracing paper"),
]

current_dir = os.path.dirname(__file__)
src_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(src_dir)

from src.visuals.visualizer import Visualizer
from src.utils import text_to_speech, wait_for_visualizer
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
    WAITING = 2
    RESPONSE = 3
    CHALLENGE = 4

class Agent:
    PLAY_AUDIO = pygame.USEREVENT + 1

    def __init__(self):
        load_dotenv()
        self.lock = threading.Lock()
        self.state = State.START
        self.victim_message = ''
        self.is_accepting_input = True
        self.running = True
        self.atrocity_score = 0
        self.challenge_prompt = ''

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
        self.state = State.WAITING

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
                    # print(f"Received: {data.decode()}")
                    self.set_victim_message(data.decode())
    
    def set_victim_message(self, data):
        self.victim_message = data

    # thread where the bulk of the logic happens
    def console(self):
        while True:
            if self.state == State.WAITING:
                # print('waiting')
                text_to_speech(f'{"Please send me a message, I crave human interaction. "} You have {AGENT_RESPONSE_TIME} seconds to respond, otherwise I will commit an atrocity', pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                wait_for_visualizer(self.visualizer)

                input_string = self.get_input('Message Sir Stabby:  ', AGENT_CHALLENGE_TIME)
                os.system('clear')

                if input_string.strip() is not None:
                    self.transmitter.send_message(input_string)
                    text_to_speech("Ok, I have received the message. Let me think about that for a while", pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)

                    if not self.victim_message:
                        self.generate_challenge()
                        self.state = State.CHALLENGE
                    else:
                        text_to_speech('I have thought of a response to your message. ' + self.victim_message + f'. You have {AGENT_RESPONSE_TIME} seconds to respond, otherwise I will commit an atrocity', pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                        wait_for_visualizer(self.visualizer)
                        self.set_victim_message(None)
                        self.state = State.RESPONSE

                else:
                    message = f"You did not enter a message. {self.commit_atrocity(atrocity_tuple)}"
                    self.transmitter.send_message(f'Atrocity: {message}')
                    text_to_speech(message, pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)
                    text_to_speech(f'{"Please send me a message, I crave human interaction. "} You again have {AGENT_RESPONSE_TIME} seconds to respond, otherwise I will commit an atrocity', pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)

            if self.state == State.CHALLENGE:
                # print('challenge')
                input_string = self.get_input('Message Sir Stabby:  ', AGENT_CHALLENGE_TIME)
                os.system('clear')
                

                if input_string is not None and input_string.lower().strip() == self.challenge_prompt:
                    # self.transmitter.send_message(input_string)
                    text_to_speech("Good job", pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)
                else:
                    atrocity_tuple = self.generate_atrocity()
                    message = f"You failed the challenge. {self.commit_atrocity(atrocity_tuple)}"
                    self.transmitter.send_message(f'Atrocity: {message}')

                    text_to_speech(message, pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)
                
                if not self.victim_message:
                    self.generate_challenge()
                    self.state = State.CHALLENGE
                else:
                    text_to_speech('Ok, that is enough challenges. I have thought of a response to your message. Here it is.' + self.victim_message + f'. You have {AGENT_RESPONSE_TIME} seconds to respond, otherwise I will commit an atrocity', pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)
                    self.set_victim_message(None)
                    self.state = State.RESPONSE

                
            elif self.state == State.RESPONSE:
                # print('response')
                input_string = self.get_input('Message Sir Stabby:  ', AGENT_RESPONSE_TIME)
                os.system('clear')

                if input_string.strip() is not None:
                    self.transmitter.send_message(input_string)
                    text_to_speech("Ok, I have received the message", pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)

                    if not self.victim_message:
                        self.generate_challenge()
                        self.state = State.CHALLENGE
                    else:
                        text_to_speech('I have thought of a response to your message. ' + self.victim_message + f'. You have {AGENT_RESPONSE_TIME} seconds to respond, otherwise I will commit an atrocity', pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                        wait_for_visualizer(self.visualizer)
                else:
                    atrocity_tuple = self.generate_atrocity()
                    message = f"You did not enter a message. {self.commit_atrocity(atrocity_tuple)}"
                    self.transmitter.send_message(f'Atrocity: {message}')
                    text_to_speech(message, pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)
                    text_to_speech(f'{"Please send me a message, I crave human interaction. "} You again have {AGENT_RESPONSE_TIME} seconds to respond, otherwise I will commit an atrocity', pygame_event=pygame.event.Event(self.PLAY_AUDIO))
                    wait_for_visualizer(self.visualizer)
                    self.state = State.WAITING

            time.sleep(0.1)
    
    def get_input(self, message, timeout):
        """
        New implementation of get_input using timed input with backspace support.
        """
        print(message, end='', flush=True)
        return self.timed_input_with_backspace(timeout)
    
    def generate_challenge_prompt(self):
        self.challenge_prompt = self.phrase_generator().lower().strip()
        return self.challenge_prompt
    
    def generate_challenge(self):
        challenge_prompt = self.generate_challenge_prompt()

        text_to_speech(f'I am still thinking about your message, but I was thinking of giving you a challenge. It would be very fun to commit an atrocity right about now. If you want me not to, type the exact phrase {challenge_prompt}. You have {AGENT_CHALLENGE_TIME} seconds.', pygame_event=pygame.event.Event(self.PLAY_AUDIO))
        wait_for_visualizer(self.visualizer)
    
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
        return True

    def generate_atrocity(self):
        return (random.choice(atrocity_tuples) + (random.randint(3000, 10000),))
        
    def commit_atrocity(self, atrocity_tuple):
        self.atrocity_score += atrocity_tuple[2]
        return f"I have just replaced {num2words(atrocity_tuple[2])} {atrocity_tuple[0]} with {atrocity_tuple[1]}."

    def run(self):
        while self.running:
            self.running = self.handle_events()

            if self.visualizer.sound_playing:
                self.visualizer.visualizer()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        
    def phrase_generator(selfself):
        # Expanded lists
        subjects = [
            "The cat", "I", "A magician", "The computer", "She", "He", "The robot", "Our neighbor", 
            "A mysterious stranger", "The chef", "A quick fox", "The teacher", "An old pirate", "The artist", 
            "The scientist", "A lost traveler", "The musician", "The writer", "An eager student", 
            "A playful dog", "The inventor", "A curious toddler", "The detective", "A lone wolf", 
            "The gardener", "A brave knight", "An enthusiastic gamer", "The programmer", "A sleepy koala", 
            "The ghost", "A sneaky thief", "A diligent bee", "The jolly Santa Claus", "A wandering monk", 
            "The king", "A digital assistant", "The librarian", "An ancient sorcerer", "A resourceful tailor", "Sir Stabby", "Sir Stabs-a-lot"
        ]

        verbs = [
            "jumps", "is working", "sings", "disappears", "does calculus homework", "runs", "speaks", "dances", "writes", 
            "draws", "whispers", "explodes", "sleeps", "laughs", "cries", "cooks", "travels", "invents", 
            "paints", "reads", "hacks", "plays", "fixes", "builds", "designs", "flies", "dreams", "schemes", 
            "listens", "observes", "studies", "examines", "flips", "wanders", "explores", "questions", 
            "answers", "commands", "recharges", "sharpens a pencil"
        ]

        complements = [
            "gracefully", "in the park", "loudly", "suddenly", "accurately", "quickly", "clearly", 
            "under the stars", "with enthusiasm", "with great skill", "in silence", "with a smile", 
            "without hesitation", "with precision", "in the library", "at the break of dawn", "in secret", 
            "with a sense of adventure", "in a dream", "like a master", "with a hint of sadness", 
            "in the digital world", "in a flurry", "in the kitchen", "across the world", "with curiosity", 
            "in the deepest ocean", "on a mountain peak", "in the bustling city", "in a quiet village", 
            "in the ancient ruins", "with a sense of mystery", "like a hero", "in the realm of fantasy", 
            "in a virtual reality", "in the blink of an eye", "with a touch of magic", "like a ghost", 
            "in the realm of code", "with a sharp eye", "alone", "in the Wattage Wastelands", "with a knife", "with a fork", "with a spoon"
        ]

        # Generating a random phrase
        subject = random.choice(subjects)
        verb = random.choice(verbs)
        complement = random.choice(complements)

        phrase = f"{subject} {verb} {complement}"
        return phrase

    def setup_term(self, fd, when=termios.TCSAFLUSH):
        mode = termios.tcgetattr(fd)
        mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
        mode[6][termios.VMIN] = 1
        mode[6][termios.VTIME] = 0
        termios.tcsetattr(fd, when, mode)

    def restore_term(self, fd, mode, when=termios.TCSAFLUSH):
        termios.tcsetattr(fd, when, mode)

    def is_data(self):
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    def timed_input_with_backspace(self, timeout):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        self.setup_term(fd)

        input_str = ''
        end_time = time.time() + timeout

        try:
            while time.time() < end_time:
                if self.is_data():
                    char = sys.stdin.read(1)
                    if char == '\n':
                        break
                    elif char == '\x7f':
                        if input_str:
                            input_str = input_str[:-1]
                            sys.stdout.write('\b \b')
                    else:
                        input_str += char
                        sys.stdout.write(char)
                sys.stdout.flush()
        finally:
            # Clear the input after timeout
            if time.time() >= end_time:
                sys.stdout.write('\r' + ' ' * len(input_str) + '\r')
                sys.stdout.flush()

            self.restore_term(fd, old_settings)
        
        return input_str

if __name__ == '__main__':
    try:
        agent = Agent()
        agent.run()
    except KeyboardInterrupt:
        print('\nAgent exited')
