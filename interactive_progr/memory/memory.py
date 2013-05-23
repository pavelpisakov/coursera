import simplegui
import random

#
#   _____  ___________   _____   ________ _______________.___.
#   /     \ \_   _____/  /     \  \_____  \\______   \__  |   |
#  /  \ /  \ |    __)_  /  \ /  \  /   |   \|       _//   |   |
# /    Y    \|        \/    Y    \/    |    \    |   \\____   |
# \____|__  /_______  /\____|__  /\_______  /____|_  // ______|
#         \/        \/         \/         \/       \/ \/       
#
#
# Do not be in a hurry.
#
# Wait until sprite image is loaded.
# Game has 4 levels. Please try to solve them all.
#
# Thanks
#
#

FRAME_BORDER = 4

CARDS_IMG = simplegui.load_image("https://www.dropbox.com/s/k9hzmcd4pl28b35/cards.png?dl=1")
SRC_CARD_SIZE = [79, 123]

FACTOR = 3 / 4
DEST_CARD_SIZE = [SRC_CARD_SIZE[0] * FACTOR, SRC_CARD_SIZE[1] * FACTOR]
MARGIN = 2

CARD_NAMES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["C", "D", "H", "S"]

PANEL_HEIGHT = 20

FRAME_WIDTH = 2 * FRAME_BORDER + 12 * DEST_CARD_SIZE[0] + 11 * MARGIN
FRAME_HEIGHT = 2 * FRAME_BORDER + 4 * DEST_CARD_SIZE[1] + PANEL_HEIGHT

MIN_GAME_LEVEL = 1
MAX_GAME_LEVEL = 4
GAME_LEVEL = MIN_GAME_LEVEL

TIME = 0
TURNS = 0

MENU_SIZE = [350, 200]
FRAME_CENTER = [FRAME_WIDTH // 2, (FRAME_HEIGHT - PANEL_HEIGHT) // 2]

MENU_VECTOR = [
    (FRAME_CENTER[0] - MENU_SIZE[0] // 2, FRAME_CENTER[1] - MENU_SIZE[1] // 2),
    (FRAME_CENTER[0] + MENU_SIZE[0] // 2, FRAME_CENTER[1] - MENU_SIZE[1] // 2),
    (FRAME_CENTER[0] + MENU_SIZE[0] // 2, FRAME_CENTER[1] + MENU_SIZE[1] // 2),
    (FRAME_CENTER[0] - MENU_SIZE[0] // 2, FRAME_CENTER[1] + MENU_SIZE[1] // 2)
]

SCORE = [0, 0, 0, 0]
TURNS_STORE = [0, 0, 0, 0]


def tick():
    global TIME
    TIME += 1


# global
timer = simplegui.create_timer(1000, tick)


class Game(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.game_in_progress = False
        self.start_game_page = True
        self.level_end_page = False
        self.score_page = False

    def is_game_in_progress(self):
        return self.game_in_progress

    def set_game_in_progress(self, state):
        self.game_in_progress = state

    def is_start_game_page(self):
        return self.start_game_page

    def set_start_game_page(self, state):
        self.start_game_page = state

    def is_level_end_page(self):
        return self.level_end_page

    def set_level_end_page(self, state):
        self.level_end_page = state

    def is_score_page(self):
        return self.score_page

    def set_score_page(self, state):

        self.score_page = state

        if self.score_page:
            self.game_in_progress = False
            self.start_game_page = False
            self.level_end_page = False

    def __str__(self):
        return "This game"


game = Game()


class Hand(object):

    def __init__(self):
        self.hand = []

    def clear_hand(self):
        self.hand = []

    def is_card_in(self, card):
        return card in self.hand

    def get_hand(self):
        return self.hand

    def add(self, card):
        self.hand.append(card)

    def get_lenght(self):
        return len(self.hand)

    def shuffle(self):
        random.shuffle(self.hand)

    def set_card_position(self, index, position):
        self.hand[index].set_position(position)

    def all_guessed(self):
        for card in self.hand:
            if not card.is_front():
                return False
        return True

    def __str__(self):
        return str([str(i) for i in self.hand])


# global variable
hand = Hand()


class Card(object):

    def __init__(self, name, suit, position=(50, 50)):
        self.name = name
        self.suit = suit
        self.front = False
        self.position = position

    def get_name(self):
        return self.name

    def get_suit(self):
        return self.suit

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def is_front(self):
        return self.front

    def draw(self, canvas):

        # get src position
        if self.front:
            x = CARD_NAMES.index(self.name) * SRC_CARD_SIZE[0] + SRC_CARD_SIZE[0]//2 + 1
            y = CARD_SUITS.index(self.suit) * SRC_CARD_SIZE[1] + SRC_CARD_SIZE[1]//2 + 1
        else:
            # Magic
            x = 2 * SRC_CARD_SIZE[0] + SRC_CARD_SIZE[0]//2 + 1
            y = 4 * SRC_CARD_SIZE[1] + SRC_CARD_SIZE[1]//2 + 1

        card_position = [x, y]

        canvas.draw_image(CARDS_IMG, card_position, SRC_CARD_SIZE, self.position, DEST_CARD_SIZE)

    def has(self, point):
        return self.position[0] - DEST_CARD_SIZE[0] // 2 <= point[0] <= self.position[0] + DEST_CARD_SIZE[0] // 2 and \
            self.position[1] - DEST_CARD_SIZE[1] // 2 <= point[1] <= self.position[1] + DEST_CARD_SIZE[1] // 2

    def action_face_up(self):
        self.front = True

    def action_face_down(self):
        self.front = False

    def __eq__(self, o):
        return CARD_NAMES.index(self.name) == CARD_NAMES.index(o.name) \
            and CARD_SUITS.index(self.suit) == CARD_SUITS.index(o.suit)

    def __str__(self):
        return "Card <" + str(self.name) + "," + str(self.suit) + "," + str(self.front) + "," + str(self.position) + ">"


class MouseHandlerFactory:

    def __init__(self):
        self.current_mouse_handler = None
        self.card_mouse_handler = MouseCardObserver()
        self.menu_mouse_handler = MouseMenuObserver()

    def set_card_mouse_handler(self, handler):
        self.card_mouse_handler = handler

    def get_card_mouse_handler(self):
        return self.card_mouse_handler

    def set_menu_mouse_handler(self, handler):
        self.menu_mouse_handler = handler

    def get_menu_mouse_handler(self):
        return self.menu_mouse_handler

    def set_active(self, name):
        if name == "menu":
            self.current_mouse_handler = self.menu_mouse_handler
        elif name == "card":
            self.current_mouse_handler = self.card_mouse_handler
        else:
            print("Error: Unknown handler '" + name + "'")

    def get_active(self):
        return self.current_mouse_handler


class MouseCardObserver:

    def __init__(self):
        self.listeners = []
        self.state = 0
        self.saved = []

    def add_listener(self, obj):
        self.listeners.append(obj)

    def invoke(self, position):

        global TURNS

        for listener in self.listeners:
            if listener.has(position):
                # listener.invoke()
                # logic here

                if listener.is_front():
                    # listener.action_face_down()
                    # do nothing
                    pass
                else:

                    if self.state == 0:

                        # making a step
                        self.state += 1
                        # making the action
                        listener.action_face_up()
                        # store link to that card
                        self.saved.append(listener)

                        TURNS += 1

                    elif self.state == 1:

                        # making a step
                        self.state += 1
                        # making the action
                        listener.action_face_up()
                        # store link to that card
                        self.saved.append(listener)

                        if not (not isinstance(self.saved[0], Card) or not isinstance(self.saved[1], Card) or not (
                                self.saved[1] == self.saved[0])):

                            if hand.all_guessed():

                                # Store results
                                SCORE[GAME_LEVEL-1] = TIME
                                TURNS_STORE[GAME_LEVEL-1] = TURNS

                                game.set_game_in_progress(False)
                                if GAME_LEVEL <= MAX_GAME_LEVEL:
                                    game.set_level_end_page(True)
                                else:
                                    game.set_score_page(True)
                                mouse_handler_factory.set_active("menu")
                                raise_level()

                    else:

                        if isinstance(self.saved[0], Card) and \
                                isinstance(self.saved[1], Card) and \
                                self.saved[0] == self.saved[1]:
                            pass

                        else:
                            self.saved[0].action_face_down()
                            self.saved[1].action_face_down()

                        self.state = 1

                        self.saved = []

                        TURNS += 1

                        # making the action
                        listener.action_face_up()
                        # store link to that card
                        self.saved.append(listener)

                return

    def clear(self):
        self.listeners = []
        self.saved = []
        self.state = 0

    def __str__(self):
        return str(self.listeners)


class MouseMenuObserver(object):

    def __init__(self):
        self.listeners = None

    # Link to the game object
    def add_listener(self, o):
        self.listener = o

    def invoke(self, position):

        if game.is_start_game_page():
            game.set_start_game_page(False)
            game.set_game_in_progress(True)
        elif game.is_level_end_page():
            game.set_level_end_page(False)
            game.set_game_in_progress(True)

    def clear(self):
        self.listeners = None

    def __str__(self):
        return str(self.listeners)


mouse_handler_factory = MouseHandlerFactory()


def draw(canvas):

    for card in hand.get_hand():
        card.draw(canvas)

    canvas.draw_text("Level: " + str(GAME_LEVEL), [FRAME_BORDER, FRAME_HEIGHT - FRAME_BORDER], 15, "Black")

    time_text = "Time: " + str(TIME) + " Turns: " + str(TURNS)

    text_width = frame.get_canvas_textwidth(time_text, 15)
    canvas.draw_text(time_text, [FRAME_WIDTH - FRAME_BORDER - text_width, FRAME_HEIGHT - FRAME_BORDER], 15, "Black")

    if game.is_start_game_page():

        if timer.is_running():
            timer.stop()

        mouse_handler_factory.set_active("menu")
        canvas.draw_polygon(MENU_VECTOR, 1, "Black", "rgba(0, 0, 0, 0.7)")

        welcome_text = "Memory"
        text_width = frame.get_canvas_textwidth(welcome_text, 20)
        canvas.draw_text(welcome_text, [FRAME_CENTER[0] - text_width // 2, 175], 20, "White")

        welcome_text = "Click to start"
        text_width = frame.get_canvas_textwidth(welcome_text, 20)
        canvas.draw_text(welcome_text, [FRAME_CENTER[0] - text_width // 2, 215], 20, "White")

    elif game.is_level_end_page():

        if timer.is_running():
            timer.stop()

        mouse_handler_factory.set_active("menu")
        canvas.draw_polygon(MENU_VECTOR, 1, "Black", "rgba(0, 0, 0, 0.7)")

        welcome_text = "Level: " + str(GAME_LEVEL)
        text_width = frame.get_canvas_textwidth(welcome_text, 20)
        canvas.draw_text(welcome_text, [FRAME_CENTER[0] - text_width // 2, FRAME_CENTER[1] + 10], 20, "White")

    elif game.is_score_page():

        if timer.is_running():
            timer.stop()

        mouse_handler_factory.set_active("menu")
        canvas.draw_polygon(MENU_VECTOR, 1, "Black", "rgba(0, 0, 0, 0.7)")

        result = 0

        # Absoluterly random numbers
        result += SCORE[0] if SCORE[0] != 0 else 70
        result += SCORE[1] if SCORE[1] != 0 else 120
        result += SCORE[2] if SCORE[2] != 0 else 200
        result += SCORE[3] if SCORE[3] != 0 else 400

        result += TURNS_STORE[0] if TURNS_STORE[0] >= 6 else 20
        result += TURNS_STORE[1] if TURNS_STORE[1] >= 12 else 50
        result += TURNS_STORE[2] if TURNS_STORE[2] >= 18 else 200
        result += TURNS_STORE[3] if TURNS_STORE[3] >= 24 else 500

        if result > 1000:
            welcome_text = "You could do better."
        elif result > 500:
            welcome_text = "Nice job!"
        else:
            welcome_text = "You win!"

        text_width = frame.get_canvas_textwidth(welcome_text, 20)
        canvas.draw_text(welcome_text, [FRAME_CENTER[0] - text_width // 2, 175], 20, "White")

        welcome_text = "Your score: " + str(result)
        text_width = frame.get_canvas_textwidth(welcome_text, 20)
        canvas.draw_text(welcome_text, [FRAME_CENTER[0] - text_width // 2, 215], 20, "White")

    else:

        mouse_handler_factory.set_active("card")

        if not timer.is_running():
            timer.start()


def init():
    """
        This method fills the hand
    """

    global hand

    hand.clear_hand()

    card_mouse_handler = mouse_handler_factory.get_card_mouse_handler()
    card_mouse_handler.clear()

    suits_num = GAME_LEVEL

    for i in range(GAME_LEVEL * 6):

        card_added = False
        counter = 0

        while not card_added:

            counter += 1
            if counter == 100:
                card_added = True
                print("Unluck")

            name = CARD_NAMES[random.randint(0, len(CARD_NAMES) - 1)]
            suit = CARD_SUITS[random.randint(0, suits_num - 1)]

            card1 = Card(name, suit)
            card2 = Card(name, suit)

            if hand.is_card_in(card1):
                continue
            else:
                # Adding two similar cards to hand
                hand.add(card1)
                hand.add(card2)

                # Register mouse event
                card_mouse_handler.add_listener(card1)
                card_mouse_handler.add_listener(card2)

                card_added = True

    hand.shuffle()


def pack():
    """
        This method packs cards
    """
    global hand

    # max 12 cards in the row
    # and 4 cards in the column
    # 48 cards max

    rows = hand.get_lenght() // 12

    for i in range(hand.get_lenght()):

        x = FRAME_BORDER + (i % 12) * (DEST_CARD_SIZE[0] + MARGIN) + DEST_CARD_SIZE[0] // 2

        if rows == 1:
            y = (FRAME_HEIGHT - PANEL_HEIGHT) // 2
        elif rows == 2:
            y = (FRAME_HEIGHT - PANEL_HEIGHT) // 2 - 1.5 * DEST_CARD_SIZE[1] - 0.5 * MARGIN + (i // 12 + 1) * \
                (DEST_CARD_SIZE[1] + MARGIN)
        elif rows == 3:
            y = (FRAME_HEIGHT - PANEL_HEIGHT) // 2 - 2 * DEST_CARD_SIZE[1] - MARGIN + (i // 12 + 1) * \
                (DEST_CARD_SIZE[1] + MARGIN)
        else:
            y = FRAME_BORDER + (i // 12) * (DEST_CARD_SIZE[1] + MARGIN) + DEST_CARD_SIZE[1] // 2

        hand.set_card_position(i, [x, y])


def game_start():

    global TIME
    global TURNS

    init()
    pack()

    TIME = 0
    TURNS = 0


def reset():

    global GAME_LEVEL

    GAME_LEVEL = MIN_GAME_LEVEL
    game.reset()
    game_start()


def raise_level():

    global GAME_LEVEL

    if GAME_LEVEL < MAX_GAME_LEVEL:
        GAME_LEVEL += 1
        game_start()
    else:
        game.set_score_page(True)
        mouse_handler_factory.set_active("menu")
        game_start()


def mouse_handler(position):
    mouse_handler_factory.get_active().invoke(position)


frame = simplegui.create_frame("Memory", FRAME_WIDTH, FRAME_HEIGHT)

mouse_handler_factory.set_active("card")

frame.set_mouseclick_handler(mouse_handler)

frame.add_button("Reset", reset, 200)
frame.add_button("Raise level", raise_level, 200)

frame.set_canvas_background("Green")
frame.set_draw_handler(draw)

game_start()

frame.start()
