from ezgraphics import *
from typing import *


def load_buttons_from_file(path: str, xOffset: int = 0, yOffset: int = 0, size: int = 20):
    """
    Loads a list of Button objects from a file in a specific format

    :param path: path to the file from which to retrieve the button data
    :param xOffset: horizontal offset of the origin position used for button placement
    :param yOffset: vertical offset of the origin position used for button placement
    :param size: draw size of button
    ///////////////
    :type path: str
    :type xOffset: int
    :type yOffset: int
    :type size: int
    ///////////////
    :return: button list
    ///////////////
    :rtype: List[Button]
    """
    if len(path) < 3 or path[-3: -1: 1] == ".blf":
        return None

    file = open(path, "r")

    lines: List[str] = file.readlines()

    buttons: List[Button] = []

    for line in lines:
        if line[0] == '#':
            continue
        arguments: List[str] = line.split(';')
        lenArg: int = len(arguments)

        if arguments[-1][-1] == '\n':
            arguments[-1] = arguments[-1][0:-1:1]

        buttons.append(Button(Point(xOffset + int(arguments[3]) * int(arguments[0]),
                                    yOffset + (int(arguments[4]) if lenArg > 4 else
                                               int(arguments[3]) // 3) * int(arguments[1])),
                              arguments[2],
                              int(arguments[3]),
                              int(arguments[4]) if lenArg > 4 else None,
                              pygame.Color(arguments[5]) if lenArg > 5 else white,
                              pygame.Color(arguments[6]) if lenArg > 6 else black,
                              arguments[7] if lenArg > 7 else False,
                              "data\\contoured\\"+arguments[2].lower()+".png"))

    file.close()

    return buttons


def save_scene_screenshot(n):
    pygame.image.save(PYGAME_SDL_WINDOW, "layers_squashed.png")


def draw_coords(windowWidth: int, windowHeight: int, frequencyX: int, frequencyY: int, col: Color = gray,
                coords: bool = False):
    """
    Draws a grid in the desired color

    :param windowWidth: width of the graphic window
    :param windowHeight: height of the graphic window
    :param frequencyX: frequency of the vertical lines
    :param frequencyY: frequency of the horizontal lines
    :param col: color of the lines
    :param coords: line/column numbers shown or not
    ///////////////
    :type windowWidth: int
    :type windowHeight int
    :type frequencyX: int
    :type frequencyY: int
    :type col: Color
    :type coords: bool
    """
    for i in range(windowWidth // frequencyX):
        draw_line(Point((i + 1) * windowWidth // frequencyX, 0),
                  Point((i + 1) * windowWidth // frequencyX, windowHeight),
                  col)
        if coords:
            display_text(str(i), 12,
                         Point(int((i + .5) * windowWidth // frequencyX - text_width(str(i), 12) // 2), 0),
                         cyan)
    for j in range(windowHeight // frequencyY):
        draw_line(Point(0, (j + 1) * windowHeight // frequencyY),
                  Point(windowWidth, (j + 1) * windowHeight // frequencyY),
                  col)
        if coords:
            display_text(str(j), 12,
                         Point(0, (j + .5) * windowHeight // frequencyY - text_height(str(j), 12) // 2),
                         cyan)


def map_from_to(value, fromMin, fromMax, toMin, toMax):
    # Figure out how 'wide' each range is
    fromSpan = fromMax - fromMin
    toSpan = toMax - toMin

    # Convert the 'from' range into a 0-1 range (float)
    valueScaled = float(value - fromMin) / float(fromSpan)

    # Convert the 0-1 range into a value in the 'to' range.
    return toMin + (valueScaled * toSpan)
