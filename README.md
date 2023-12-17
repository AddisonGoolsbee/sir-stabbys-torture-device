# sir-stabbys-torture-device

2-player embedded system puzzle/obstacle course/game involving a trapped victim, a rescuer detective, an AI, and lots of miscommunication. Beware: you will be stabbed

The year is 2168. The former general and mad scientist Peter Scottsen has just been exiled from the Photon Nation for war crimes, but his Magnum Opus, the rogue AI Sir Stabby, is still running and bringing terror to the Photon people. Your job as a government agent is to shut down Sir Stabby. Little do you know, there is more at play than a simple death machine.

As it turns out (and unbeknownst to the typing player), there is a civilian locked in a room far from you who is the real Sir Stabby. Unfortunately, the mad supervillain Peter Scottsen has made it so that everything the victim tries to say is slightly misinterpreted as a threat. Your job as the civilian is to get the agent to figure out you’re trapped in a room and free you, while the agent’s job is simply to shut down the machine, as demonstrated in Module 4’s Peter Scottsen’s Death Machine. If the agent shuts down the machine without finding the civilian, Sir Stabby will reboot after a while.

Once the agent saves the civilian, there’s one more twist: the civilian is tethered to the victim pad. When Peter Scottsen designed his death machine, he created a pad that the civilian must touch at all times. If the civilian lets go, Sir Stabby will launch the nuclear bombs, killing everyone. The civilian must trick the agent into holding the pad in order to be freed from this burden

A more comprehensive description was given to participants in both a redacted format before playing and an unredacted format upon escaping.
![redacted_pamphlet](assetz/blacked%20out%20Sir%20Stabby’s%20Perpetual%20Motion%20Machine%20PAMPHLET%20-%20Google%20Docs-1.png)

![unredacted_pamphlet](assetz/normal%20Sir%20Stabby’s%20Perpetual%20Motion%20Machine%20PAMPHLET%20-%20Google%20Docs-1.png)

## Requirements

- portaudio
- ffmpeg

## Setup

When Sir Stabby is plugged in, you can run the Python script. Set up the virtual environment with the following steps:

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

You will need to make an `.env` file following the template of `.env.example`. It requires three environment variables:

- **OPENAI_API_KEY**: Key to use OpenAI's GPT4. Using GPT4 will cost you money, so be careful!
- **BIRDFLOP_API_KEY**: Key to use Binflop by Birdflop, which is the website that contains the transcript at the end of the exhibit. Birdflop is not open-access, so an alternative site that allows POST requests to a dynamically updating website could be substituted in the code. Or, contact Koray for an API key.
- **AGENT_ESP_PORT**: the port that Sir Stabby plugs into on the agent computer

### Exhibit Setup

For the victim setup, we had a button on a pedestal functioned as the button that the victim would have to hold to avoid execution (as an aside, this setup was disassembled before taking any photos or videos of it!). The victim room consists of a dark room with the Sir Stabby voice FFT projected onto a large surface and a guard, who is instructed to shoot the victim if the victim releases their hand.

The guard additionally controls a terminal with access to some critical functions that ensure the game runs smoothly:
`loss (l)`: if the victim releases the button, record that the victim lost. The guard can take their place as the victim.
`success (s)`: if the victim successfully escapes, record this information. The agent becomes the new victim.
`abandonment (a)`: if the agent decides to abandon the victim, record this information and clear the agent's name from saved variables.
`{agent_name}`: if there is a new agent, record the name of the new agent. The informtion will be radio'd down over walkie-talkie.

The agent setup consists of Sir Stabby (Remastered) fir snugly around a 13" Mac, with the USB-C attached to the top-left port. The lower portion of the screen is used to bring up a terminal to communicate with Sir Stabby (Remastered), while the upper portion is used to display the Sir Stabby (Remastered) FFT.

## File Structure

- All code lies within the `src/` folder
- `agent/` contains the agent-side code, which includes the arduino code for Sir Stabby `agent.ino` as well as the computer code `agent.py`
- `victim/` contains the victim-side code. `victim.py` is the computer code that goes on the projector, and `victim.ino` is an unused piece of code that was previously for the button
- `visuals/` contains code for the audio visualizer that depicts the AI Sir Stabby
- `constants.py` contains various constants used between `agent.py` and `victim.py`, including IP addresses and port numbers of both computers, so they can be easily modified during setup
- `utils.py` contains a couple of util functions used in both `agent.py` and `victim.py`
- `transmitter.py` is a class that is implemented in both `agent.py` and `victim.py` that asynchronously transmits data to a specified port and IP address
- `dummyReceiver.py` is a helpful testing file that allows for a fake receiving computer to be set up. In order for either `agent.py` or `victim.py` to work, their transmitters need to establish a socket connection with a receiving end. Using the dummyReceiver allows for one to test `agent.py` and `victim.py` in isolation.
- While a `receiver.py` class file would have been cleaner, because we needed to update different instance variables in `agent.py` and `victim.py`, we decided to implement the receiver class separately in both of the files
- `transcript.txt` is a gitignored file that contains all of the status and transcript of the game, for as long as the exhibition-runner doesn't reset the transcript. It is uploaded to `binflop.com`

The bulk of the code lies within `agent.py` and `victim.py`, as these are the main controllers for their respective computers

### Agent

The agent computer is composed of the Sir Stabby mechanism, which continually attempts to stab the agent, and the AI, which either talks to the agent and waits for answers, or challenges the agent and threatens to cause harm to humanity

The code for the mechanism, `agent.ino`, is disconnected from the code for the computer. As such, the `agent.ino` code is fairly simple. It consists of a concurrent knife class that is initialized twice

`agent.py` is much more complicated, and is where the bulk of the code is

#### Agent Threads

- **Main**: the Visualizer for the AI. Can be sent a "visualize_sound" event from other threads, which tells pygame to start animating the visualizer from the previous position
- **Receiver**: the network receiver, which listens to incoming TCP packets from the victim and notifies the console thread accordingly
- **Transmitter**: the network transmitter, which, when triggered by the console thread, sends a TCP packet to the victim receiver. In order for the script to start its main loop, the transmitter *must* connect to a receiving end. It will keep trying until it does connect, and `dummyReceiver.py` is very useful for testing only `agent.py`
- **Console**: this is essentially the main thread, except that Pygame can only run on the main thread, so the console thread is separate. The console thread handles not only user input through the console, but also most of the game logic. Console's main loop is the core state machine of the program. Whenever the receiver receives something, the console is updated. Whenever the console wants to send something, the transmitter is updated. Whenever the console wants to visualize audio, the transmitter is updated

#### Agent State Machine

Although there are four states in the state enum, there are effectively two states once the exhibition begins running:

- **RESPONSE**: this is the core communication with Sir Stabby (actually the victim, but unbenownst to the agent). Sir Stabby will ask the agent for a message, and give them a fixed amount of seconds (defined in `constants.py`) to respond (while the knives are swinging). If the agent succeeds, the message will be transmitted to the victim (and then garbled). If the agent fails, an atrocity will be committed. Atrocities, for example, "I will replace 5384 running shoes with shoes that constantly untie," come with an associated atrocity score that is added to the player's total over the course of the game
- **CHALLENGE**: while waiting for the victim's response, in order to not break the illusion and reveal to the agent that the victim is actually a real person, Sir Stabby will challenge the agent to type a specific phrase, generated at random. If the phrase doesn't match or isn't entered, an atrocity will be committed. Once the victim sends a message, the state will change back to RESPONSE as soon as the current challenge is finished

### Victim

In the victim room, there is a button that must be held down by the victim, otherwise the security guard will shoot the victim with a high-power firearm (nerf gun). Within the button lies a smartphone that is bluetooth-connected to the victim computer, and which is sending audio data to the computer, acting as a closer microphone

All of the code is in `victim.py`, `victim.ino` is an obsolete file

#### Victim Threads

- **Main**: same as agent
- **Receiver**: the receiver receives messages from the agent, just like the agent's receiver does, except the victim receiver also distorts the agent's message using a custom GPT4 'syllable swap' directive
- **Transmitter**: same as agent
- **Console**: while the victim side is running, because the visuals are on a projector, the security guard has access to the actual computer running the program. There are a number of commands the security guard can input that change the transcript
- **Victim Loop**: this is the *main* thread other than the fact that pygame has to be on the main thread, similar to the console thread in `agent.py`. The victim loop thread handles game logic, and is the thread that interacts with all the other threads. Once the victim receives a message from the agent, it is distorted and then played back to the victim. The victim then has a fixed amount of time to speak to Sir Stabby, before Sir Stabby cuts the victim off with a randomized insult. Then, the message is distorted using GPT4 to seem like it comes from a computer system, and it is sent off to the agent to confusingly interperet. The distorted message is played back to the victim, prefaced by a randomized excuse such as "I found your message to be a bit too passive-aggressive, so I modified it"

#### Console Inputs

- **l/loss**: if the victim is murdered (gets shot too many times with the nerf gun and/or leaves the room out of frustration), it is recorded as a loss. The security guard takes over as a fake victim, and tries to convince the next agent into pressing the button
- **s/success**: if the victim successfully gets the agent to enter the prison cell and press the button, they are handed the full, non-redacted pamphlet with QR code access to the online transcript, and are congragulated and told to laugh at the new victim. Sir Stabby on the victim side will then give its 30-second spiel about what the victim is expected to do, how the victim can escape. etc
- **a/abandonment**: if the agent abandons Sir Stabby, the transcript is updated, and the victim simply waits for the next agent to attempt Sir Stabby
- **any**: if any other text is entered into the console, it is interpreted as a new agent showing up. The text is used as the agent's name, and that agent is tracked in the transcript afterwards. The agent's name becomes the victim's name when the victim succeeds



### Visualizer

The audio visualizer uses pygame and FFT magic to make a speaking animation that syncs with the audio from a file. When the visualizer is run, it plays the audio and the animation at the same time
