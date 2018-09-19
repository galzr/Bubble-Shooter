import pygame
import time
import random
import math

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500

BLACK = 0
WHITE = 1
BORDEAUX = 2
GREEN = 3
NAVY_BLUE = 4
LIGHT_BLUE = 5
PINK = 6
YELLOW = 7
OUTLINE = 8

SPEED = 7

START_ARROW_X = WINDOW_WIDTH / 2
START_ARROW_Y = WINDOW_HEIGHT - 50

LEFT = 1
RIGHT = 3

X_INDEX = 0
Y_INDEX = 1

ROWS = 5
COLUMNS = 15

COLORS = [(0, 0, 0), (255, 255, 255), (128, 0, 64), (35, 215, 138),
          (64, 0, 128), (185, 204, 240), (255, 179, 217), (255, 255, 128),
          (92, 92, 92)]

BUBBLE_RADIUS = 20
BUBBLE_DIAN = BUBBLE_RADIUS * 2

SOUND_FILE_LOSE = 'LOSE.mp3'
SOUND_FILE_POP = 'POP.wav'
SOUND_FILE_BIG_POP = 'BIG_POP.wav'
SOUND_FILE_WIN = 'WIN.mp3'

global score
score = 0


class Bubble(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(int(x)-BUBBLE_RADIUS, int(y)-BUBBLE_RADIUS, BUBBLE_DIAN, BUBBLE_DIAN)
        self.rect.centerx = int(x)
        self.rect.centery = int(y)
        self.color = COLORS[random.randint(2, len(COLORS)-2)]
        self.vx = 0
        self.vy = 0

    def draw(self, should_flip=True):
        """Draws the bubble."""
        pygame.draw.circle(screen, self.color,
                           (self.rect.centerx, self.rect.centery),
                           BUBBLE_RADIUS, 0)
        pygame.draw.circle(screen, COLORS[OUTLINE],
                           (self.rect.centerx, self.rect.centery),
                           BUBBLE_RADIUS, 1)
        if should_flip:
            pygame.display.flip()

    def update_location(self):
        """Changes the position of the bubble, according to its speed."""
        if is_out_x(self.rect.centerx + self.vx):
            self.vx *= -1
        if is_out_y(self.rect.centery + self.vy):
            self.vy *= -1
        self.rect.centery += self.vy
        self.rect.centerx += self.vx
        self.draw()

    def start_motion(self):
        """Starts and stops the motion of a bubble after the user clicks the 'space' button."""
        global arrow
        self.vx = int(round(SPEED * math.cos(math.radians(arrow.angle)), 0))
        self.vy = int(-1 * round(SPEED * math.sin(math.radians(arrow.angle)), 0))
        self.rect.centerx = arrow.rect.centerx + self.vx
        self.rect.centery = arrow.rect.y + BUBBLE_RADIUS
        while True:
            if self.rect.collidelist(bubbles) != -1:
                if math.hypot(self.rect.centerx - bubbles[self.rect.collidelist(bubbles)].rect.centerx,
                              self.rect.centery - bubbles[self.rect.collidelist(bubbles)].rect.centery) < BUBBLE_DIAN:
                    break
            if self.rect.centery / BUBBLE_DIAN < 1:
                self.rect.centery = BUBBLE_RADIUS
                break
            arrow.draw()
            self.update_location()
            reload_bubbles()
            time.sleep(0.004)
        y_loc = int(self.rect.centery / BUBBLE_DIAN)
        self.rect.centery = (y_loc * BUBBLE_DIAN) + BUBBLE_RADIUS
        temp_centerx = self.rect.centerx
        x_loc = int(self.rect.centerx / BUBBLE_DIAN)
        self.rect.centerx = (x_loc * BUBBLE_DIAN)
        if int(self.rect.centery / BUBBLE_DIAN) % 2 != 0:
            if round(temp_centerx / BUBBLE_DIAN, 0) > int(temp_centerx / BUBBLE_DIAN):
                self.rect.centerx = (round(temp_centerx / BUBBLE_DIAN, 0)) * BUBBLE_DIAN
            distance = math.hypot(self.rect.centerx - bubbles[self.rect.collidelist(bubbles)].rect.centerx,
                                  self.rect.centery - bubbles[self.rect.collidelist(bubbles)].rect.centery)
            if ((distance < BUBBLE_DIAN) or is_out_x(self.rect.centerx + BUBBLE_RADIUS) or
                    is_out_x(self.rect.centerx - BUBBLE_RADIUS)) and temp_centerx > self.rect.centerx:
                self.rect.centerx += BUBBLE_DIAN
            elif ((distance < BUBBLE_DIAN) or is_out_x(self.rect.centerx + BUBBLE_RADIUS) or
                    is_out_x(self.rect.centerx - BUBBLE_RADIUS)) and temp_centerx < self.rect.centerx:
                self.rect.centerx -= BUBBLE_DIAN
        else:
            self.rect.centerx += BUBBLE_RADIUS
        if self.rect.collidelist(bubbles) != -1:
            distance = math.hypot(self.rect.centerx - bubbles[self.rect.collidelist(bubbles)].rect.centerx,
                              self.rect.centery - bubbles[self.rect.collidelist(bubbles)].rect.centery)
            if (distance < BUBBLE_DIAN) or is_out_x(self.rect.centerx + BUBBLE_RADIUS) or \
                    is_out_x(self.rect.centerx - BUBBLE_RADIUS):
                self.rect.centery += BUBBLE_DIAN
                if temp_centerx > self.rect.centerx:
                    if int(self.rect.centery / BUBBLE_DIAN) % 2 != 0:
                        self.rect.centerx = int(temp_centerx / BUBBLE_DIAN) * BUBBLE_DIAN
                    else:
                        self.rect.centerx = int(temp_centerx / BUBBLE_DIAN) * BUBBLE_DIAN + BUBBLE_RADIUS
                else:
                    if int(self.rect.centery / BUBBLE_DIAN) % 2 != 0:
                        if (not is_out_x(self.rect.centerx - BUBBLE_DIAN)) and temp_centerx > self.rect.centerx:
                            self.rect.centerx -= BUBBLE_RADIUS
                            distance = math.hypot(
                                self.rect.centerx - bubbles[self.rect.collidelist(bubbles)].rect.centerx,
                                self.rect.centery - bubbles[self.rect.collidelist(bubbles)].rect.centery)
                            if (distance < BUBBLE_DIAN) or is_out_x(self.rect.centerx + BUBBLE_RADIUS) or \
                                    is_out_x(self.rect.centerx - BUBBLE_RADIUS):
                                self.rect.centerx += BUBBLE_DIAN
                        else:
                            self.rect.centerx += BUBBLE_RADIUS
                            distance = math.hypot(
                                self.rect.centerx - bubbles[self.rect.collidelist(bubbles)].rect.centerx,
                                self.rect.centery - bubbles[self.rect.collidelist(bubbles)].rect.centery)
                            if (distance < BUBBLE_DIAN) or is_out_x(self.rect.centerx + BUBBLE_RADIUS) or \
                                    is_out_x(self.rect.centerx - BUBBLE_RADIUS):
                                self.rect.centerx -= BUBBLE_DIAN
                    else:
                        self.rect.centerx = int(temp_centerx / BUBBLE_DIAN) * BUBBLE_DIAN - BUBBLE_RADIUS
        bubbles.append(self)
        before_pops_len = len(bubbles)
        pop_bubbles(len(bubbles)-1)
        pop_leftovers()
        if get_max_y() / BUBBLE_DIAN > 10:
            lose_page()
        elif len(bubbles) == 0:
            win_page()
        else:
            pygame.mixer.init()
            if before_pops_len == len(bubbles):
                pygame.mixer.music.load(SOUND_FILE_POP)
            else:
                pygame.mixer.music.load(SOUND_FILE_BIG_POP)
            pygame.mixer.music.play()
            reload_bubbles()
            arrow.draw()
            time.sleep(0.009)


class Arrow(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 90
        self.image = pygame.image.load('arrow.png')
        arrowImage = self.image.convert_alpha()
        arrowImage.convert_alpha()
        arrowRect = arrowImage.get_rect()
        self.transformImage = self.image
        self.rect = arrowRect
        self.centerx = START_ARROW_X
        self.centery = START_ARROW_Y

    def update(self, direction, given_angle):
        """Changes the angle of the arrow."""
        if not given_angle:
            if direction == LEFT and self.angle < 170:
                self.angle += 0.3
            elif direction == RIGHT and self.angle > 10:
                self.angle -= 0.3
        else:
            if given_angle < 170 and given_angle > 10:
                self.angle = given_angle
        self.transformImage = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.transformImage.get_rect()
        self.rect.centerx = START_ARROW_X
        self.rect.centery = START_ARROW_Y

    def draw(self):
        """Draws the arrow."""
        screen.blit(self.transformImage, self.rect)
        pygame.display.flip()


def pop_bubbles(first_index):
    """Pops the bubbles that are supposed to pop after the crash (of the new bubble and
    the existing owns). If there are more than three bubbles with the same color that are located
    next to each other, all of them will be erased."""
    nodes = []
    delete_list = []
    nodes.append(first_index)
    color = bubbles[first_index].color
    count = 0
    global score
    while len(nodes) > 0:
        temp_node = nodes[len(nodes)-1]
        nodes.pop(len(nodes)-1)
        if temp_node not in delete_list:
            delete_list.append(temp_node)
        for bubble_index in range(len(bubbles)):
            should_pop = False
            if bubbles[bubble_index].rect.centerx + BUBBLE_RADIUS == bubbles[temp_node].rect.centerx\
                    and bubbles[bubble_index].rect.centery + BUBBLE_DIAN == bubbles[temp_node].rect.centery:
                should_pop = True
            if bubbles[bubble_index].rect.centerx - BUBBLE_RADIUS == bubbles[temp_node].rect.centerx\
                    and bubbles[bubble_index].rect.centery + BUBBLE_DIAN == bubbles[temp_node].rect.centery:
                should_pop = True
            if bubbles[bubble_index].rect.centerx + BUBBLE_DIAN == bubbles[temp_node].rect.centerx\
                    and bubbles[bubble_index].rect.centery == bubbles[temp_node].rect.centery:
                should_pop = True
            if bubbles[bubble_index].rect.centerx - BUBBLE_DIAN == bubbles[temp_node].rect.centerx\
                    and bubbles[bubble_index].rect.centery == bubbles[temp_node].rect.centery:
                should_pop = True
            if bubbles[bubble_index].rect.centerx + BUBBLE_RADIUS == bubbles[temp_node].rect.centerx\
                    and bubbles[bubble_index].rect.centery - BUBBLE_DIAN == bubbles[temp_node].rect.centery:
                should_pop = True
            if bubbles[bubble_index].rect.centerx - BUBBLE_RADIUS == bubbles[temp_node].rect.centerx\
                    and bubbles[bubble_index].rect.centery - BUBBLE_DIAN == bubbles[temp_node].rect.centery:
                should_pop = True
            if should_pop:
                if bubbles[bubble_index].color == color and bubble_index not in delete_list:
                    count += 1
                    nodes.append(bubble_index)
    delete_list.sort(reverse=True)
    if count > 1:
        for delete_bubble in delete_list:
            for i in range(len(bubbles)):
                if i == delete_bubble:
                    bubbles.pop(i)
                    score += 10
                    break


def is_in_gush(gush, item):
    """Checks if the given item (bubble index) is in one of the 'gushim' of bubbles."""
    for i in range(len(gush)):
        if item in gush[i]:
            return True
    return False


def pop_leftovers():
    """After popping bubbles, there are some leftovers. If a bubble is not connected to any
    of the 'gushim' and if it is literally 'in the air', it is supposed to pop as well
    (because of gravity)."""
    nodes = []
    not_delete_list = []
    for bubble_index in range(len(bubbles)):
        if bubbles[bubble_index].rect.centery == BUBBLE_RADIUS and not is_in_gush(nodes, bubble_index):
            nodes = [bubble_index]
            while len(nodes) > 0:
                temp_node = nodes[len(nodes) - 1]
                nodes.pop(len(nodes) - 1)
                if temp_node not in not_delete_list:
                    not_delete_list.append(temp_node)
                for bubble_index in range(len(bubbles)):
                    should_pop = False
                    if bubbles[bubble_index].rect.centerx + BUBBLE_RADIUS == bubbles[temp_node].rect.centerx \
                            and bubbles[bubble_index].rect.centery + BUBBLE_DIAN == bubbles[temp_node].rect.centery:
                        should_pop = True
                    if bubbles[bubble_index].rect.centerx - BUBBLE_RADIUS == bubbles[temp_node].rect.centerx \
                            and bubbles[bubble_index].rect.centery + BUBBLE_DIAN == bubbles[temp_node].rect.centery:
                        should_pop = True
                    if bubbles[bubble_index].rect.centerx + BUBBLE_DIAN == bubbles[temp_node].rect.centerx \
                            and bubbles[bubble_index].rect.centery == bubbles[temp_node].rect.centery:
                        should_pop = True
                    if bubbles[bubble_index].rect.centerx - BUBBLE_DIAN == bubbles[temp_node].rect.centerx \
                            and bubbles[bubble_index].rect.centery == bubbles[temp_node].rect.centery:
                        should_pop = True
                    if bubbles[bubble_index].rect.centerx + BUBBLE_RADIUS == bubbles[temp_node].rect.centerx \
                            and bubbles[bubble_index].rect.centery - BUBBLE_DIAN == bubbles[temp_node].rect.centery:
                        should_pop = True
                    if bubbles[bubble_index].rect.centerx - BUBBLE_RADIUS == bubbles[temp_node].rect.centerx \
                            and bubbles[bubble_index].rect.centery - BUBBLE_DIAN == bubbles[temp_node].rect.centery:
                        should_pop = True
                    if should_pop and bubble_index not in not_delete_list:
                        nodes.append(bubble_index)
    global score
    leftovers = []
    for i in range(len(bubbles)):
        if i not in not_delete_list:
            leftovers.append(i)
    leftovers.sort(reverse=True)
    for leftover in leftovers:
        for i in range(len(bubbles)):
            if i == leftover:
                bubbles.pop(i)
                score += 10
                break


def get_max_y():
    """Finds the lowest bubble and returns its horizontal location."""
    max = 0
    for bubble in bubbles:
        if bubble.rect.centery > max:
            max = bubble.rect.centery
    return max


def reload_bubbles():
    """Reloads the bubbles (on screen)."""
    screen.fill(COLORS[WHITE])
    for i in range(len(bubbles)):
            bubbles[i].draw(False)


def reload_arrow(direction, given_angle):
    """Reloads the arrow (on screen)."""
    img = pygame.image.load('white_arrow.jpg')
    arrow.update(direction, given_angle)
    screen.blit(img, (arrow.rect.x, arrow.rect.y))
    arrow.draw()


def is_out_x(x):
    """Checks if the given x location is in the screen or not."""
    return (x > WINDOW_WIDTH - BUBBLE_RADIUS) or (x < 0 + BUBBLE_RADIUS)


def is_out_y(y):
    """Checks if the given x location is in the screen or not."""
    return y > WINDOW_HEIGHT - BUBBLE_RADIUS


def load_text(font, font_size, text, x_loc, y_loc, speed):
    pygame.font.init()
    font = pygame.font.SysFont(font, font_size)
    for i in range(len(text)):
        text_surface = font.render(text[:i + 1], True, COLORS[BLACK])
        screen.blit(text_surface, (x_loc, y_loc))
        pygame.display.flip()
        time.sleep(speed)

def first_page(from_explanation=False):
    """Loads the first page."""
    screen.fill(COLORS[WHITE])
    load_text('Amatica SC', 80, 'BUBBLE SHOOTER', 45, 60, 0.04)
    load_text('Courier New', 20, 'Use the arrow keys or the mouse in order', 45, 200, 0.01)
    load_text('Courier New', 20, 'to move the arrow.', 45, 230, 0.01)
    load_text('Courier New', 20, 'Click "space" or the mouse to send bubbles.', 45, 260, 0.01)
    load_text('Courier New', 20, 'For an explanation, click the screen', 45, 290, 0.01)
    load_text('Courier New', 20, 'with the mouse.', 45, 320, 0.01)
    load_text('Courier New', 20, 'Press any key to continue (at any time', 45, 360, 0.01)
    load_text('Courier New', 20, 'except during the game itself).', 45, 390, 0.01)
    should_start = False
    while not should_start and not from_explanation:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                should_start = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                explanation_page()


def lose_page():
    """Loads the losing page."""
    screen.fill(COLORS[WHITE])
    pygame.mixer.init()
    pygame.mixer.music.load(SOUND_FILE_LOSE)
    pygame.mixer.music.play()
    pygame.font.init()
    screen.fill(COLORS[WHITE])
    load_text('Amatica SC', 80, 'YOU LOST!', 50, 100, 0.04)
    global score
    load_text('Courier New', 20, 'Your score is ' + str(score), 50, 400, 0.01)
    score = 0
    should_start = False
    while not should_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                should_start = True
    first_page()
    global bubbles
    global arrow
    arrow.angle = 90
    arrow.draw()
    bubbles = create_game()
    reload_bubbles()


def win_page():
    """Loads the winning page."""
    screen.fill(COLORS[WHITE])
    pygame.mixer.init()
    pygame.mixer.music.load(SOUND_FILE_WIN)
    pygame.mixer.music.play()
    screen.fill(COLORS[WHITE])
    load_text('Amatica SC', 80, 'YOU WON!', 50, 100, 0.04)
    global score
    load_text('Courier New', 20, 'Your score is ' + str(score), 50, 400, 0.01)
    score = 0
    should_start = False
    while not should_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                should_start = True
    first_page()
    global bubbles
    global arrow
    bubbles = create_game()
    arrow.angle = 90
    arrow.draw()
    reload_bubbles()


def explanation_page():
    """Loads the explanation page."""
    screen.fill(COLORS[WHITE])
    load_text('Amatica SC', 75, 'EXPLANATION!', 50, 7, 0.04)
    global score
    load_text('Courier New', 20, 'Your goal is to clear all the bubbles', 50, 130, 0.01)
    load_text('Courier New', 20, 'from the board, scoring as many points', 50, 160, 0.01)
    load_text('Courier New', 20, 'as possible. How? You shoot at them with', 50, 190, 0.01)
    load_text('Courier New', 20, 'more bubbles, and when three or more', 50, 220, 0.01)
    load_text('Courier New', 20, 'of the same color come together,', 50, 250, 0.01)
    load_text('Courier New', 20, 'they all explode. Use the keys to point', 50, 280, 0.01)
    load_text('Courier New', 20, 'where you want the next bubble to go.', 50, 310, 0.01)
    load_text('Courier New', 20, 'The more bubbles blow up at one shot, the', 50, 340, 0.01)
    load_text('Courier New', 20, 'increasingly more points you gain.', 50, 370, 0.01)
    load_text('Courier New', 20, 'Besides, those bubbles that fell apart', 50, 400, 0.01)
    load_text('Courier New', 20, 'from the rest will explode too.', 50, 430, 0.01)
    score = 0
    should_start = False
    while not should_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                should_start = True
    first_page(True)


def turn_bool(bool):
    """Turns a boolean variable from 'True' to 'False' and from 'False' to 'True'."""
    if bool:
        return False
    else:
        return True


def create_game():
    """Creates the game."""
    screen.fill(COLORS[WHITE])
    bubbles = []
    inden = False
    for i in range(ROWS):
        for j in range(COLUMNS):
            if inden:
                if j == COLUMNS - 1:
                    continue
                bubbles.append(Bubble(BUBBLE_RADIUS + BUBBLE_DIAN * (j + 0.5), BUBBLE_DIAN * (i+0.5)))
            else:
                bubbles.append(Bubble(BUBBLE_DIAN * (j+0.5), BUBBLE_DIAN * (i+0.5)))
        inden = turn_bool(inden)
    return bubbles

pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("BUBBLE SHOOTER")
clock = pygame.time.Clock()


def main():
    first_page()
    global bubbles
    bubbles = create_game()
    reload_bubbles()
    global arrow
    arrow = Arrow()
    arrow.update(0, 0)
    arrow.draw()
    send_bubble = False
    temp_bubble = Bubble(WINDOW_WIDTH - BUBBLE_RADIUS, WINDOW_HEIGHT - BUBBLE_RADIUS)
    temp_bubble.draw()
    finish = False
    direction = 0
    angle = 0
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                direction = LEFT
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                direction = RIGHT
            elif event.type == pygame.KEYUP:
                direction = 0
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
                    (event.type == pygame.MOUSEBUTTONDOWN):
                send_bubble = True
            elif event.type == pygame.MOUSEMOTION:
                mouse_location = pygame.mouse.get_pos()
                perp = abs(arrow.centery - mouse_location[Y_INDEX])
                angle = math.degrees(math.asin(perp / (math.sqrt(math.pow(perp, 2) + math.pow
                (arrow.centerx - mouse_location[X_INDEX], 2)))))
                if arrow.centerx > mouse_location[X_INDEX]:
                    angle = 180 - angle
        reload_arrow(direction, angle)
        if angle != 0:
            angle = 0
        if send_bubble:
            temp_bubble.start_motion()
            temp_bubble = Bubble(WINDOW_WIDTH - BUBBLE_RADIUS, WINDOW_HEIGHT - BUBBLE_RADIUS)
            temp_bubble.draw()
            send_bubble = False


if __name__ == '__main__':
    main()
