import simplegui
import math

#
#   ________  __                                __          __
#  /   _____//  |_  ____ ________  _  _______ _/  |_  ____ |  |__
#  \_____  \\   __\/  _ \\____ \ \/ \/ /\__  \\   __\/ ___\|  |  \
#  /        \|  | (  <_> )  |_> >     /  / __ \|  | \  \___|   Y  \
# /_______  /|__|  \____/|   __/ \/\_/  (____  /__|  \___  >___|  /
#         \/             |__|                \/          \/     \/
#
#

_bg_color = "#012345"
_fg_color = "#cae0f3"
_marker_color = "#294968"
_font = "monospace"
_text_size = 25
_clock_middle = [150, 150]
_marker_distance = 100
_arrow_length = 90

init_degree = 90
active_marker = 0

time = 0

tries = 0
score = 0

hex_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]

#_my_font = simplegui.load_image("http://www.dropbox.com/s/q8vi3nw3zts73xf/font.png?dl=1")
_my_font = simplegui.load_image(
    "https://raw.github.com/pavelpisakov/coursera/master/interactive_progr/stopwatch/font.png"
)
_my_font_str = "0123456789:./"
_char_width = 17
_char_height = 32
_margin = 7


def format(number):

    minutes = (number // 600) % 60
    seconds = (number // 10) % 60
    millis = number % 10

    result = str(minutes) + ":"
    if seconds < 10:
        result += "0"
    result += str(seconds)
    result += "."
    result += str(millis)

    return result


def tick():

    global init_degree, time, active_marker

    time += 1

    if time % 10 == 0:

        init_degree -= 6

        if init_degree < 0:
            init_degree = 360 - 6

        if init_degree % 30 == 0:
            active_marker = init_degree / 30
            active_marker = 12 - active_marker
            active_marker += 3
            active_marker %= 12


def render_text(canvas, text, position):
    
    current_position = list(position)
   
    for char in text:
        
        if char in _my_font_str:
            image_center = (21 + _my_font_str.index(char) * _char_width, 36)
        else:
            image_center = (_char_width // 2, _char_height // 2)
        
        draw_position = list(current_position)
        draw_position[0] += _char_width // 2
        draw_position[1] -= _char_height // 2
        
        canvas.draw_image(_my_font, image_center,
                          (_char_width, _char_height),
                          draw_position, (_char_width, _char_height))
        current_position[0] += _char_width


def draw(canvas):

    # canvas.draw_text("Stopwatch", [123, 190], 12, _marker_color)

    for i in range(12):

        x = _clock_middle[0] + (math.cos(math.radians((450 - i * 30) % 360))) * _marker_distance
        y = _clock_middle[1] - (math.sin(math.radians((450 - i * 30) % 360))) * _marker_distance
        
        if i == active_marker:
            
            step = time % 50
            r = int(202 - step * 3.22)
            g = int(224 - step * 3.02)
            b = int(243 - step * 2.76)
           
            color = "#"
            color += str(hex_values[int(math.floor(r / 16))])
            color += str(hex_values[r % 16])
            color += str(hex_values[int(math.floor(g / 16))])
            color += str(hex_values[g % 16])
            color += str(hex_values[int(math.floor(b / 16))])
            color += str(hex_values[b % 16])

            canvas.draw_circle([x, y], 2, 4, color)
        else:
            canvas.draw_circle([x, y], 2, 4, _marker_color)

    x = _clock_middle[0] + (math.cos(math.radians(init_degree))) * _arrow_length
    y = _clock_middle[1] - (math.sin(math.radians(init_degree))) * _arrow_length

    canvas.draw_line(_clock_middle, [x, y], 4, _fg_color)
    canvas.draw_circle(_clock_middle, 2, 6, _fg_color)
    canvas.draw_circle(_clock_middle, 1, 2, _bg_color)
    
    text = format(time)
    
    # as image
    text_width = len(text) * _char_width
    render_text(canvas, text, ((300 - text_width) // 2, 310))
    
    # as plain text
    #text_width = frame.get_canvas_textwidth(text, _text_size, _font)
    #canvas.draw_text(text, [(300 - width)/2, 310], _text_size, _fg_color, _font)

    score_text = str(score) + "/" + str(tries)
    
    # as image
    score_text_width = len(score_text) * _char_width
    render_text(canvas, score_text, (300 - score_text_width - _margin, 0 + _char_height + _margin))
    
    # as plain text
    #width = frame.get_canvas_textwidth(score_text, _text_size, _font)
    #canvas.draw_text(score_text, [(300 - width) - 6, 27], _text_size, _fg_color, _font)
    
def start_handler():
    if not timer.is_running():
        timer.start()
    else:
        print("It's already started")


def stop_handler():
    global score, tries

    if timer.is_running():
        timer.stop()
        if time % 10 == 0:
            score += 1
        tries += 1
    else:
        print("It's already stopped")


def reset_handler():
    global init_degree, time, score, tries, active_marker

    if timer.is_running():
        timer.stop()
        
    init_degree = 90
    time = 0
    score = 0
    tries = 0
    active_marker = 0
    
frame = simplegui.create_frame("Stopwatch: The Game", 300, 350)
frame.set_canvas_background(_bg_color)
frame.set_draw_handler(draw)

frame.add_button("Start", start_handler, 200)
frame.add_button("Stop", stop_handler, 200)
frame.add_button("Reset", reset_handler, 200)

frame.start()

timer = simplegui.create_timer(100, tick)
