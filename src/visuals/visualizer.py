from .AudioAnalyzer import *

class Visualizer:

    def __init__(self, screen):
        self.screen = screen
        self.analyzer = AudioAnalyzer()
        self.sound_playing = False

        self.clock = pygame.time.Clock()

        t = pygame.time.get_ticks()
        self.getTicksLastFrame = t

        self.timeCount = 0

        self.avg_bass = 0
        self.bass_trigger = -35
        self.bass_trigger_started = 0

        self.min_decibel = -80
        self.max_decibel = 80

        self.circle_color = (0, 0, 0)
        self.polygon_default_color = [220, 220, 220]
        self.polygon_bass_color = self.polygon_default_color.copy()
        self.polygon_color_vel = [0, 0, 0]

        self.poly = []
        self.poly_color = self.polygon_default_color.copy()

        self.circleX = int(self.screen.get_width() / 2)
        self.circleY = int(self.screen.get_height() / 2)

        self.min_radius = 50
        self.max_radius = 90
        self.radius = self.min_radius
        self.radius_vel = 0

        bass = {"start": 50, "stop": 100, "count": 20}
        heavy_area = {"start": 120, "stop": 250, "count": 20}
        low_mids = {"start": 251, "stop": 2000, "count": 20}
        high_mids = {"start": 2001, "stop": 4000, "count": 20}

        freq_groups = [bass, heavy_area, low_mids, high_mids]
        self.bars = []
        tmp_bars = []
        length = 0

        for group in freq_groups:
            g = []
            s = group["stop"] - group["start"]
            count = group["count"]
            reminder = s%count
            step = int(s/count)
            rng = group["start"]

            for _ in range(count):
                arr = None
                if reminder > 0:
                    reminder -= 1
                    arr = np.arange(start=rng, stop=rng + step + 2)
                    rng += step + 3
                else:
                    arr = np.arange(start=rng, stop=rng + step + 1)
                    rng += step + 2
                g.append(arr)
                length += 1
            tmp_bars.append(g)

        angle_dt = 360/length
        ang = 0
        for g in tmp_bars:
            gr = []
            for c in g:
                gr.append(
                    RotatedAverageAudioBar(self.circleX+self.radius*math.cos(math.radians(ang - 90)), self.circleY+self.radius*math.sin(math.radians(ang - 90)), c, (255, 0, 255), angle=ang, width=8, max_height=370))
                ang += angle_dt
            self.bars.append(gr)


    
    def visualize_sound(self, filename):
        print('a')
        self.analyzer.load(filename)
        print('b')
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        print('aa')
        pygame.mixer.music.load(filename)
        print('bb')
        pygame.mixer.music.play(0)
        self.sound_playing = True
        print('c')

    def visualizer(self):
        self.avg_bass = 0
        self.poly = []

        t = pygame.time.get_ticks()
        deltaTime = (t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = t
        self.timeCount += deltaTime

        self.screen.fill(self.circle_color)

        for b1 in self.bars:
            for b in b1:
                b.update_all(deltaTime, pygame.mixer.music.get_pos() / 1000.0, self.analyzer)

        for b in self.bars[0]:
            self.avg_bass += b.avg

        self.avg_bass /= len(self.bars[0])

        if self.avg_bass > self.bass_trigger:
            if self.bass_trigger_started == 0:
                self.bass_trigger_started = pygame.time.get_ticks()
            if self.polygon_bass_color is None:
                self.polygon_bass_color = (220,220,220)
            newr = self.min_radius + int(self.avg_bass * ((self.max_radius - self.min_radius) / (self.max_decibel - self.min_decibel)) + (self.max_radius - self.min_radius))
            self.radius_vel = (newr - self.radius) / 0.15

            self.polygon_color_vel = [(self.polygon_bass_color[x] - self.poly_color[x])/0.15 for x in range(len(self.poly_color))]

        elif self.radius > self.min_radius:
            self.bass_trigger_started = 0
            self.polygon_bass_color = None
            self.radius_vel = (self.min_radius - self.radius) / 0.15
            self.polygon_color_vel = [(self.polygon_default_color[x] - self.poly_color[x])/0.15 for x in range(len(self.poly_color))]

        else:
            self.bass_trigger_started = 0
            self.poly_color = self.polygon_default_color.copy()
            self.polygon_bass_color = None
            self.polygon_color_vel = [0, 0, 0]

            self.radius_vel = 0
            self.radius = self.min_radius

        self.radius += self.radius_vel * deltaTime

        for x in range(len(self.polygon_color_vel)):
            value = self.polygon_color_vel[x]*deltaTime + self.poly_color[x]
            self.poly_color[x] = value

        for b1 in self.bars:
            for b in b1:
                b.x, b.y = self.circleX+self.radius*math.cos(math.radians(b.angle - 90)), self.circleY+self.radius*math.sin(math.radians(b.angle - 90))
                b.update_rect()

                self.poly.append(b.rect.points[3])
                self.poly.append(b.rect.points[2])

        pygame.draw.polygon(self.screen, self.poly_color, self.poly)
        pygame.draw.circle(self.screen, self.circle_color, (self.circleX, self.circleY), int(self.radius))

        if not pygame.mixer.music.get_busy():
            self.sound_playing = False
