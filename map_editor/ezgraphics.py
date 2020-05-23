# -*- coding: utf-8 -*-
# Graphics module

"""
Graphic module
Author : D. Raphaël, EPITA
Version 0.1


SUMMARY :
PART 1 : CONSTANTS AND CLASSES
PART 2 : COLORS
PART 3 : GRAPHIC WINDOW
PART 4 : TEXT DISPLAY
PART 5 : SHAPE DRAWING
PART 6 : IMAGE MANAGEMENT
PART 7 : SOUNDS AND MUSIC MANAGEMENT
PART 8 : MOUSE HANDLING
PART 9 : KEYBOARD HANDLING
PART 10 : TIME MANAGEMENT
PART 11 : RANDOM VALUES
"""

from math import *
import cmath
import random
import pygame
from pygame.locals import *

pygame.init()

# region Constants and Classes
# --------------------------------------------------
# PART 1 : CONSTANTS AND CLASSES
# --------------------------------------------------

# region Global Constants
# PART 1.1 : GLOBAL CONSTANTS

PYGAME_SDL_WEIGHT = 0  # width of the graphic window
PYGAME_SDL_HEIGHT = 0  # height of the graphic window
PYGAME_SDL_FONT = "verdana"  # default font
PYGAME_SDL_DISPLAY = 1  # default display constant

PYGAME_SDL_WINDOW = pygame.display.set_mode((10, 10))

SWATCH = 0

NAUGHT = -42

# endregion

# region Predefined Classes
# PART 1.2 : PREDEFINED CLASSES


class Point:
    """
    This class defines a Point taking two fields x and y.
    P.x is the x-coordinate of Point P.
    P.y is the y-coordinate of Point P.
    We'll write  P = Point(10, 50)  to define a Point P with coordinates (10, 50).
    """

    def __init__(self, x, y):
        """
        Initialize a new Point
        :param x: x-coordinate
        :param y: y-coordinate
        """
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# Only use this once you figure out how to make a button by yourself
class Button:
    """
    This class defines a Button taking two to six fields P, w, h, color_fg, color_bg and contour.
    B.P is the Point defining the top left corner of Button B.
    B.text is the text to be displayed inside of B.
    B.w is the width of Button B.
    B.h is the height of Button B.
    B.color_fg is the foreground color of Button B (i.e. text color and contour colour if present).
    B.color_bg is the background color of Button B.
    B.contour is a boolean defining if B has a contour that must be drawn
    B.imagePath is the string containing the path to the image to be displayed on B
    """

    def __init__(self, P, text, w, h=None, color_fg=pygame.Color(255), color_bg=pygame.Color(0), contour=False,
                 imagePath=None):
        self.P = P
        self.text = text
        self.w = w
        if h is not None:
            self.h = h
        else:
            self.h = w // 3

        self.color_fg = color_fg
        self.color_bg = color_bg
        self.contour = contour
        self.imagePath = imagePath

    def __str__(self):
        return "Button at {0}:\n" \
               " ├ text = {1}\n" \
               " ├ w = {2}, h = {3}\n" \
               " ├ color_fg = {4}\n" \
               " ├ color_bg = {5}\n" \
               " ├ contour = {6}\n" \
               " └ imagePath = {7}".format(self.P, self.text, self.w, self.h, self.color_fg, self.color_bg,
                                           self.contour, self.imagePath)

    def inside(self, point):
        return self.P.x < point.x < self.P.x + self.w and self.P.y < point.y < self.P.y + self.h

    def draw(self, flip_grounds: bool = False, text: bool = False):
        fg = self.color_fg
        bg = self.color_bg
        if flip_grounds:
            fg, bg = bg, fg

        if self.imagePath is None:
            draw_fill_rectangle(self.P, self.w, self.h, bg)
            if text:
                display_text_center(self.text, 12, Point(self.P.x + self.w / 2, self.P.y + self.h / 2), fg)
            if self.contour:
                draw_rectangle(self.P, self.w, self.h, fg)
        else:
            load_image(self.imagePath, self.P)


# endregion
# endregion

# region Colors

# --------------------------------------------------
# PART 2 : COLORS
# --------------------------------------------------

# region Predefined Colors
# PART 2.1 : PREDEFINED COLORS

# Base colors
black = pygame.Color(0, 0, 0)
blue = pygame.Color(0, 0, 255)
brown = pygame.Color(88, 41, 0)
cyan = pygame.Color(0, 255, 255)
gold = pygame.Color(255, 215, 0)
gray = pygame.Color(128, 128, 128)
green = pygame.Color(0, 255, 0)
magenta = pygame.Color(255, 0, 255)
orange = pygame.Color(255, 127, 0)
pink = pygame.Color(253, 108, 158)
purple = pygame.Color(127, 0, 255)
red = pygame.Color(255, 0, 0)
salmon = pygame.Color(248, 142, 85)
silver = pygame.Color(206, 206, 206)
turquoise = pygame.Color(37, 253, 233)
white = pygame.Color(255, 255, 255)
yellow = pygame.Color(255, 255, 0)

# Additional design colors
soft_black = pygame.Color("#222034")


# endregion

# region RGB Color Creation
# PART 2.2 RGB COLOR CREATION

def color_RGB(r: int, g: int, b: int):
    """
    Returns an RGB color

    :param r: amount of red (between 0 and 255 (both included))
    :param g: amount of green (between 0 and 255 (both included))
    :param b: amount of blue (between 0 and 255 (both included))
    ///////////////
    :type r: int
    :type g: int
    :type b: int
    ///////////////
    :return: new Color object
    ///////////////
    :rtype: Color
    """
    return pygame.Color(r, g, b)


# endregion
# endregion

# region Graphic Window
# --------------------------------------------------
# PART 3 : GRAPHIC WINDOW
# --------------------------------------------------

# Initializing the graphic window
def init_graphic(W: int, H: int, name: str = "SynPython", bg_color: Color = black, fullscreen: bool = 0):
    """
    Initializes the graphic window
    The origin (0, 0) of the graphic window is in the top left

    :param W: width
    :param H: height
    :param name: name of the window (default is "SynPython")
    :param bg_color: background color (default is black)
    :param fullscreen: if 0 then shows a W*H window, otherwise shows a fullscreen one (default is 0)
    ///////////////
    :type W: int
    :type H: int
    :type name: str
    :type bg_color: Color
    :type fullscreen: bool
    """
    global PYGAME_SDL_WINDOW, PYGAME_SDL_WEIGHT, PYGAME_SDL_HEIGHT
    PYGAME_SDL_WEIGHT = W
    PYGAME_SDL_HEIGHT = H
    if fullscreen == 0:
        PYGAME_SDL_WINDOW = pygame.display.set_mode((int(W), int(H)))
    else:
        PYGAME_SDL_WINDOW = pygame.display.set_mode((int(W), int(H)), FULLSCREEN)
    pygame.display.set_caption(name)
    pygame.draw.rect(PYGAME_SDL_WINDOW, bg_color, (0, 0, int(W), int(H)), 0)
    pygame.display.flip()


# Closing the graphic window
def wait_escape(text: str = "Press Escape to quit", size: int = 20, col: Color = gray, text_bold: bool = False,
                text_italic: bool = False):
    """
    Waits for a quit or escape press event
    Blocking instruction

    :param text: end text
    :param size: text size
    :param col: text color
    :param text_bold: text bold if true, normal otherwise
    :param text_italic: text italic if true, normal otherwise
    ///////////////
    :type text: str
    :type size: int
    :type col: Color
    :type text_bold: bool
    :type text_italic: bool
    """
    if text != "":
        a = PYGAME_SDL_WEIGHT / 2 - text_width(text, int(size), text_bold, text_italic) / 2
        b = PYGAME_SDL_HEIGHT - text_height(text, int(size), text_bold, text_italic)
        P = Point(a, b)
        display_text(text, int(size), P, col, text_bold, text_italic)
    stop = False
    while not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                break
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                stop = True
                break
    pygame.quit()


def auto_display_toggle(toggle: bool):
    """
    Enables or disables automatic display

    :param toggle: auto display is turned on if True, off otherwise
    ///////////////
    :type toggle: bool
    """
    global PYGAME_SDL_DISPLAY
    PYGAME_SDL_DISPLAY = int(toggle)


# Display of constructed shapes
def display_all():
    """
    Allows display of shape drawings
    """
    pygame.display.flip()


# endregion

# region Text Display
# --------------------------------------------------
# PART 4 : TEXT DISPLAY
# --------------------------------------------------

def text_width(T: str, t: int, text_bold: bool = False, text_italic: bool = False):
    """
    Computes the width of a text T written in font size t

    :param T: text
    :param t: font size
    :param text_bold: text bold if true, normal otherwise
    :param text_italic: text italic if true, normal otherwise
    ///////////////
    :type T: str
    :type t: int
    :type text_bold: bool
    :type text_italic: bool
    ///////////////
    :return: width of the text in pixels
    ///////////////
    :rtype: int
    """
    font = pygame.font.SysFont(PYGAME_SDL_FONT, t, bold=text_bold, italic=text_italic)
    text = font.render(T, 1, black)
    text_coordinates = text.get_rect()
    return tuple(text_coordinates)[2]


def text_height(T, t, text_bold=False, text_italic=False):
    """
    Computes the height of a text T written in font size t

    :param T: text
    :param t: font size
    :param text_bold: text bold if true, normal otherwise
    :param text_italic: text italic if true, normal otherwise
    ///////////////
    :type T: str
    :type t: int
    :type text_bold: bool
    :type text_italic: bool
    ///////////////
    :return: height of the text in pixels
    ///////////////
    :rtype: int
    """
    font = pygame.font.SysFont(PYGAME_SDL_FONT, t, bold=text_bold, italic=text_italic)
    text = font.render(T, 1, black)
    text_coordinates = text.get_rect()
    return tuple(text_coordinates)[3]


def display_text(T: str, t: int, P: Point, C: Color, text_bold: bool = False, text_italic: bool = False):
    """
    Displays a string T in font size t (font is the current value of PYGAME_SDL_FONT (default is Verdana))

    :param T: text
    :param t: font size
    :param P: top-left point
    :param C: text color
    :param text_bold: text bold if true, normal otherwise
    :param text_italic: text italic if true, normal otherwise
    ///////////////
    :type T: str
    :type t: int
    :type P: Point
    :type C: Color
    :type text_bold: bool
    :type text_italic: bool
    """
    P.x = int(P.x)
    P.y = int(P.y)
    font = pygame.font.SysFont(PYGAME_SDL_FONT, t, bold=text_bold, italic=text_italic)
    text = font.render(T, 1, C)
    PYGAME_SDL_WINDOW.blit(text, (P.x, P.y))
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def display_text_center(T: str, t: int, P: Point, C: Color, text_bold: bool = False, text_italic: bool = False):
    """
    Displays a string T in font size t (font is the current value of PYGAME_SDL_FONT (default is Verdana))

    :param T: text
    :param t: font size
    :param P: center point
    :param C: text color
    :param text_bold: text bold if true, normal otherwise
    :param text_italic: text italic if true, normal otherwise
    ///////////////
    :type T: str
    :type t: int
    :type P: Point
    :type C: Color
    :type text_bold: bool
    :type text_italic: bool
    """
    P.x = int(P.x)
    P.y = int(P.y)
    font = pygame.font.SysFont(PYGAME_SDL_FONT, t, bold=text_bold, italic=text_italic)
    text = font.render(T, 1, C)
    PYGAME_SDL_WINDOW.blit(text, (P.x - text_width(T, t) / 2, P.y - text_height(T, t) / 2))
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def list_fonts():
    """
    Returns the list of available fonts
    """
    return pygame.font.get_fonts()


def test_font(S: str):
    """
    Returns 1 if S is an available font, 0 otherwise

    :param S: font name
    ///////////////
    :type S: str
    ///////////////
    :return: 0 if the font is available, 0 otherwise
    ///////////////
    :rtype: int
    """
    if S in pygame.font.get_fonts():
        return 1
    return 0


def change_font(S: str):
    """
    Changes initial font (i.e. PYGAME_SDL_FONT) into font S if it is available

    :param S: font name
    ///////////////
    :type S: str
    """
    global PYGAME_SDL_FONT

    if S in pygame.font.get_fonts():
        PYGAME_SDL_FONT = S


# endregion

# region Shape Drawing
# --------------------------------------------------
# PART 5 : SHAPE DRAWING
# --------------------------------------------------

def draw_pixel(P: Point, C: Color):
    """
    Changes pixel at point P to color C

    :param P: coordinates
    :param C: new pixel color
    ///////////////
    :type P: Point
    :type C: Color
    """
    P.x = int(P.x)
    P.y = int(P.y)
    pygame.draw.line(PYGAME_SDL_WINDOW, C, (P.x, P.y), (P.x, P.y), 1)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_line(P: Point, Q: Point, C: Color):
    """
    Draws a line between points P and Q with color C

    :param P: first point
    :param Q: second point
    :param C: new pixel color
    ///////////////
    :type P: Point
    :type Q: Point
    :type C: Color
    """
    P.x = int(P.x)
    P.y = int(P.y)
    Q.x = int(Q.x)
    Q.y = int(Q.y)
    pygame.draw.line(PYGAME_SDL_WINDOW, C, (P.x, P.y), (Q.x, Q.y), 1)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_triangle(P: Point, Q: Point, R: Point, C: Color):
    """
    Draws a triangle of vertices P, Q and R with color C

    :param P: first point
    :param Q: second point
    :param R: third point
    :param C: new pixel color
    ///////////////
    :type P: Point
    :type Q: Point
    :type R: Point
    :type C: Color
    """
    P.x = int(P.x)
    P.y = int(P.y)
    Q.x = int(Q.x)
    Q.y = int(Q.y)
    R.x = int(R.x)
    R.y = int(R.y)
    pygame.draw.polygon(PYGAME_SDL_WINDOW, C, ([P.x, P.y], [Q.x, Q.y], [R.x, R.y]), 1)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_fill_triangle(P: Point, Q: Point, R: Point, C: Color):
    """
    Draws a triangle of vertices P, Q and R filled with color C

    :param P: first point
    :param Q: second point
    :param R: third point
    :param C: new pixel color
    ///////////////
    :type P: Point
    :type Q: Point
    :type R: Point
    :type C: Color
    """
    P.x = int(P.x)
    P.y = int(P.y)
    Q.x = int(Q.x)
    Q.y = int(Q.y)
    R.x = int(R.x)
    R.y = int(R.y)
    pygame.draw.polygon(PYGAME_SDL_WINDOW, C, ([P.x, P.y], [Q.x, Q.y], [R.x, R.y]), 0)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_rectangle(P: Point, w: float, h: float, C: pygame.Color, S: pygame.Surface = PYGAME_SDL_WINDOW):
    """
    Draws a rectangle of top-left point P, width w, height h and color C

    :param P: top-left point
    :param w: width
    :param h: height
    :param C: color
    :param S: surface to draw on
    ///////////////
    :type P: Point
    :type w: float
    :type h: float
    :type C: pygame.Color
    :type S: pygame.Surface
    """
    pygame.draw.rect(S, C, (int(P.x), int(P.y), int(w), int(h)), 1)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_fill_rectangle(P: Point, w: float, h: float, C: pygame.Color, S: pygame.Surface = PYGAME_SDL_WINDOW):
    """
    Draws a rectangle of top-left point P, width w and height h filled with color C

    :param P: top-left point
    :param w: width
    :param h: height
    :param C: color
    :param S: surface on which to draw (default is entire window)
    ///////////////
    :type P: Point
    :type w: float
    :type h: float
    :type C: pygame.Color
    :type S: pygame.Surface
    """
    pygame.draw.rect(S, C, (int(P.x), int(P.y), int(w), int(h)), 0)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_rectangle_center(P: Point, w: float, h: float, C: Color):
    """
    Draws a rectangle of center P, width w, height h and color C

    :param P: center point
    :param w: width
    :param h: height
    :param C: color
    ///////////////
    :type P: Point
    :type w: float
    :type h: float
    :type C: Color
    """
    pygame.draw.rect(PYGAME_SDL_WINDOW, C, (int(P.x - w / 2), int(P.y - h / 2), int(w), int(h)), 1)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_fill_rectangle_center(P: Point, w: float, h: float, C: Color):
    """
    Draws a rectangle of center P, width w and height h filled with color C

    :param P: center point
    :param w: width
    :param h: height
    :param C: color
    ///////////////
    :type P: Point
    :type w: float
    :type h: float
    :type C: Color
    """
    pygame.draw.rect(PYGAME_SDL_WINDOW, C, (int(P.x - w / 2), int(P.y - h / 2), int(w), int(h)), 0)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_circle(P: Point, r: float, C: Color = white):
    """
    Draws a circle of center P and radius r with color C

    :param P: center point
    :param r: radius
    :param C: color
    ///////////////
    :type P: Point
    :type r: float
    :type C: Color
    """
    P.x = int(P.x)
    P.y = int(P.y)
    r = int(r)
    pygame.draw.circle(PYGAME_SDL_WINDOW, C, (P.x, P.y), r, 1)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_fill_circle(P: Point, r: float, C: Color):
    """
    Draws a circle of center P and radius r filled with color C

    :param P: center point
    :param r: radius
    :param C: color
    ///////////////
    :type P: Point
    :type r: float
    :type C: Color
    """
    P.x = int(P.x)
    P.y = int(P.y)
    r = int(r)
    pygame.draw.circle(PYGAME_SDL_WINDOW, C, (P.x, P.y), r, 0)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_ellipse(P: Point, w: float, h: float, C: Color):
    """
    Draws an ellipse in a rectangular box of center P, width w and height h with color C

    :param P: center point
    :param w: width
    :param h: height
    :param C: color
    ///////////////
    :type P: Point
    :type w: float
    :type h: float
    :type C: Color
    """
    pygame.draw.ellipse(PYGAME_SDL_WINDOW, C, (int(P.x - w / 2), int(P.y - h / 2), int(w), int(h)), 1)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_fill_ellipse(P: Point, w: float, h: float, C: Color):
    """
    Draws an ellipse in a rectangular box of center P, width w and height h filled with color C

    :param P: center point
    :param w: width
    :param h: height
    :param C: color
    ///////////////
    :type P: Point
    :type w: float
    :type h: float
    :type C: Color
    """
    pygame.draw.ellipse(PYGAME_SDL_WINDOW, C, (int(P.x - w / 2), int(P.y - h / 2), int(w), int(h)), 0)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_arc(P: Point, w: float, h: float, start: float, end: float, C):
    """
    Draws an arc in a rectangular box of center P, width w, height h and angle start-end with color C
    The angles start and end are given in radian and are in [0; 2*pi[

    :param P: center point
    :param w: width
    :param h: height
    :param start: start angle
    :param end: end angle
    :param C: color
    ///////////////
    :type P: Point
    :type w: float
    :type h: float
    :type start: float
    :type end: float
    :type C: Color
    """
    pygame.draw.arc(PYGAME_SDL_WINDOW, C, (int(P.x - w / 2), int(P.y - h / 2), int(w), int(h)), start, end, 1)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_sector(P: Point, r: float, start: float, end: float, C: Color):
    """
    Draws an angular sector of origin P, radius r and angle start-end with color C
    The angles start and end are given in radian and are in [0; 2*pi[

    :param P: origin point
    :param r: radius
    :param start: start angle
    :param end: end angle
    :param C: color
    ///////////////
    :type P: Point
    :type r: float
    :type start: float
    :type end: float
    :type C: Color
    """
    draw_arc(P, 2 * r, 2 * r, start, end, C)
    draw_line(P, Point(P.x + r * cos(start), P.y - r * sin(start)), C)
    draw_line(P, Point(P.x + r * cos(end), P.y - r * sin(end)), C)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


def draw_fill_sector(P: Point, r: float, start: float, end: float, C: Color, live: bool = False):
    """
    Draws an angular sector of origin P, radius r and angle start-end filled with color C
    The angles start and end are given in radian and are in [0; 2*pi[
    The parameter live has a default value of False, if it is set to True then the sector
    can be seen being drawn.

    :param P: origin point
    :param r: radius
    :param start: start angle
    :param end: end angle
    :param C: color
    :param live: if true see sector being draw otherwise just see end result
    ///////////////
    :type P: Point
    :type r: float
    :type start: float
    :type end: float
    :type C: Color
    :type live: bool
    """
    if not live:
        auto_display_toggle(False)
    for x in range(int(-r), int(r + 1)):
        for y in range(int(-r), int(r + 1)):
            z = complex(x, y)
            arg = cmath.phase(z)
            if arg < 0:
                arg += 2 * pi
            if abs(z) <= r and start <= arg <= end:
                draw_pixel(Point(P.x + x, P.y - y), C)
    if not live:
        auto_display_toggle(True)
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


# endregion

# region Image Management
# --------------------------------------------------
# PART 6 : IMAGE MANAGEMENT
# --------------------------------------------------

def load_image(title: str, P: Point):
    """
    Displays an image with image path title and top-left point P
    Returns the image as a pygame surface

    :param title: image path
    :param P: top-left point
    ///////////////
    :type title: str
    :type P: Point
    ///////////////
    :return: surface with image on it
    ///////////////
    :rtype: Surface
    """
    P.x = int(P.x)
    P.y = int(P.y)
    image = pygame.image.load(title).convert()
    PYGAME_SDL_WINDOW.blit(image, (P.x, P.y))
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()
    return image


def load_image_alpha(title: str, P: Point):
    """
    Displays a transparent image with image path title and top-left point P
    Returns the image as a pygame surface

    :param title: image path
    :param P: top-left point
    ///////////////
    :type title: str
    :type P: Point
    ///////////////
    :return: surface with image on it
    ///////////////
    :rtype: Surface
    """
    P.x = int(P.x)
    P.y = int(P.y)
    image = pygame.image.load(title).convert_alpha()
    PYGAME_SDL_WINDOW.blit(image, (P.x, P.y))
    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()
    return image


def transfer_image(title: str):
    """
    Returns the image as a pygame surface
    /!\\ Beware, this doesn't display the image, it's only useful for image size computation and the such

    :param title: image path
    ///////////////
    :type title: str
    ///////////////
    :return: surface with image on it
    ///////////////
    :rtype: Surface
    """
    return pygame.image.load(title)


def save_image(I: pygame.Surface, F: str):
    """
    Saves the surface I in a file F

    :param I: surface with image to save
    :param F: output file path
    ///////////////
    :type I: Surface
    :type F: str
    """
    pygame.image.save(I, F)


def get_size_image(I: pygame.Surface):
    """
    Returns the dimensions of image I

    :param I: image
    ///////////////
    :type I: Surface
    ///////////////
    :return: dimensions of I
    ///////////////
    :rtype: (int, int)
    """
    return I.get_size()


def resize_image(I: pygame.Surface, W: int, H: int):
    """
    Returns a resized version of I to a width W and a height H

    :param I: image
    :param W: target width (> 1)
    :param H: target height (> 1)
    ///////////////
    :type I: Surface
    :type W: int
    :type H: int
    ///////////////
    :return: resized version of I
    ///////////////
    :rtype: Surface
    """
    return pygame.transform.scale(I, (W, H))


# endregion

# region Sounds and Music Management
# --------------------------------------------------
# PART 7 : SOUNDS AND MUSIC MANAGEMENT
# --------------------------------------------------

# region Sounds
# PART 7.1 : SOUNDS

def play_sound(S: str):
    """
    Starts playing sound located at S

    :param S: sound path
    ///////////////
    :type S: str
    """
    pygame.mixer.Sound(S).play()


def stop_sound(S: str):
    """
    Stops sound S

    :param S: sound path
    ///////////////
    :type S: str
    """
    pygame.mixer.Sound(S).stop()


def set_volume_sound(S: str, v: float):
    """
    Sets volume of sound S to v

    :param S: sound path
    :param v: volume (between 0.0 and 1.0)
    ///////////////
    :type S: str
    :type v: float
    """
    pygame.mixer.Sound(S).set_volume(v)


def get_volume_sound(S: str):
    """
    Returns the volume of sound S

    :param S: sound path
    ///////////////
    :type S: str
    """
    return pygame.mixer.Sound(S).get_volume()


# endregion

# region Music
# PART 7.2 : MUSIC

def load_music(M: str):
    """
    Loads music M to the playlist. Preferred format: .wav

    :param M: music path
    ///////////////
    :type M: str
    """
    pygame.mixer.music.load(M)


def play_music(loop: bool = False):
    """
    Starts the playlist

    :param loop: if True, music is played on a loop
    ///////////////
    :type loop: bool
    """
    if loop:
        pygame.mixer.music.play(loops=-1)
    else:
        pygame.mixer.music.play()


def restart_music():
    """
    Restarts playlist from the beginning
    """
    pygame.mixer.music.rewind()


def stop_music():
    """
    Stops playlist
    """
    pygame.mixer.music.stop()


def pause_music():
    """
    Pauses playlist
    """
    pygame.mixer.music.pause()


def unpause_music():
    """
    Resumes playlist
    """
    pygame.mixer.music.unpause()


def set_volume_music(v):
    """
    Sets music volume to v

    :param v: between 0.0 and 1.0
    ///////////////
    :type v: float
    """
    pygame.mixer.music.set_volume(v)


def get_volume_music():
    """
    Returns music volume

    :return: music volume
    ///////////////
    :rtype: float
    """
    return pygame.mixer.music.get_volume()


def get_busy_music():
    """
    Returns True if music is being played, False otherwise

    :return: mixer.music state
    ///////////////
    :rtype: bool
    """
    return bool(pygame.mixer.music.get_busy())


# endregion
# endregion

# region General Input Handling
def get_input_down():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                return None, [BUTTON_LEFT, Point(event.pos[0], event.pos[1])]
            elif event.button == 2:
                return None, [BUTTON_MIDDLE, Point(event.pos[0], event.pos[1])]
            elif event.button == 3:
                return None, [BUTTON_RIGHT, Point(event.pos[0], event.pos[1])]
        elif event.type == KEYDOWN:
            return event.key, None
    return None
# endregion

# region Mouse Handling
# --------------------------------------------------
# PART 8 : MOUSE HANDLING
# --------------------------------------------------


def get_mouse_down():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                return [BUTTON_LEFT, Point(event.pos[0], event.pos[1])]
            elif event.button == 2:
                return [BUTTON_MIDDLE, Point(event.pos[0], event.pos[1])]
            elif event.button == 3:
                return [BUTTON_RIGHT, Point(event.pos[0], event.pos[1])]
    return None


def wait_click():
    """
    Waits for a left click and returns the coordinates of said click
    Blocking instruction

    :return: coordinates or leave
    ///////////////
    :rtype: Point
    """
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                return Point(event.pos[0], event.pos[1])


def wait_click_specific():
    """
    Waits for a click and returns the button that was clicked and the coordinates of said click
    in a list following the format: [button: str, Point: coordinates]
    Possible buttons: "L", "M", "R"
    Blocking instruction

    :return: button and coordinates of click in a list
    ///////////////
    :rtype: [str, Point]
    """
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    return [BUTTON_LEFT, Point(event.pos[0], event.pos[1])]
                if event.button == 2:
                    return [BUTTON_MIDDLE, Point(event.pos[0], event.pos[1])]
                if event.button == 3:
                    return [BUTTON_RIGHT, Point(event.pos[0], event.pos[1])]


def cursor_visible(visible: bool):
    """
    Controls the visibility of the mouse cursor

    :param visible: Hides the mouse cursor if False, un-hides it if True
    ///////////////
    :type visible: bool
    """
    pygame.mouse.set_visible(visible)


def get_mouse():
    """
    Returns the current position of the mouse cursor

    :return: current position of the mouse cursor
    ///////////////
    :rtype: Point
    """
    mousePos = pygame.mouse.get_pos()
    return Point(mousePos[0], mousePos[1])


# endregion

# region Keyboard Handling
# --------------------------------------------------
# PART 9 : KEYBOARD HANDLING
# --------------------------------------------------

def get_key_down():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return pygame.quit()
        if event.type == KEYDOWN:
            return event.key
    # return None


def wait_key():
    """
    Awaits a keypress and returns the corresponding ASCII code
    Blocking instruction

    :return: ASCII code of pressed key
    ///////////////
    :rtype: int
    """
    pygame.event.clear()
    character = ""
    while character == "":
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                character = event.dict['unicode']
                if character != "":
                    return ord(character)


def wait_space_letter():
    """
    Awaits a keypress
    If the key is a letter, returns the corresponding uppercase letter
    If the key is the spacebar, returns a whitespace (i.e. " ")
    Returns an empty string otherwise
    Blocking instruction

    :return: pressed key if space/letter, empty string otherwise
    ///////////////
    :rtype: str
    """
    key = wait_key()
    if 96 < key < 123:
        return chr(key - 32)
    if key == 32:
        return " "
    return ""


def wait_arrow():
    """
    Awaits a keypress
    If key is an arrow key, returns "up", "down", "left" or "right" depending on which arrow key was pressed
    Returns an empty string otherwise
    Blocking instruction

    :return: pressed key if arrow key, empty string otherwise
    ///////////////
    :rtype: str
    """
    pygame.event.clear()
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    return "up"
                elif event.key == K_DOWN:
                    return "down"
                elif event.key == K_LEFT:
                    return "left"
                elif event.key == K_RIGHT:
                    return "right"


# Functions below usually are to be used alongside wait_key()
def get_space_letter(key: int):
    """
    If key is a letter, returns the corresponding uppercase letter
    If the key is the spacebar, returns a whitespace (i.e. " ")
    Returns an empty string otherwise

    :param key: ASCII number (int between 0 and 255 both included)
    ///////////////
    :type key: int
    ///////////////
    :return: pressed key if space/letter, empty string otherwise
    ///////////////
    :rtype: str
    """
    if 64 < key < 91:
        return chr(key)
    if 96 < key < 123:
        return chr(key - 32)
    if key == 32:
        return " "
    return ""


def is_letter(key: int):
    """
    Tests whether or not key is a letter (lowercase or uppercase)
    Returns True or False

    :param key: ASCII number (int between 0 and 255 both included)
    ///////////////
    :type key: int
    ///////////////
    :return: True if key is a letter, False otherwise
    ///////////////
    :rtype: bool
    """
    return 64 < key < 91 or 96 < key < 123


def is_space(key: int):
    """
    Tests whether or not key is space
    Returns True or False

    :param key: ASCII number (int between 0 and 255 both included)
    ///////////////
    :type key: int
    ///////////////
    :return: True if key is space, False otherwise
    ///////////////
    :rtype: bool
    """
    return key == 32


def is_return(key: int):
    """
    Tests whether or not key is return
    Returns True or False

    :param key: ASCII number (int between 0 and 255 both included)
    ///////////////
    :type key: int
    ///////////////
    :return: True if key is return, False otherwise
    ///////////////
    :rtype: bool
    """
    return key == 13


# endregion

# region Time Management
# --------------------------------------------------
# PART 10 : TIME MANAGEMENT
# --------------------------------------------------

def wait(ms: int):
    """
    Waits the amount of milliseconds given as parameter

    :param ms: number of milliseconds to wait for
    ///////////////
    :type ms: int
    """
    pygame.time.delay(ms)


def swatch_start():
    """
    Starts a stopwatch
    """
    global SWATCH
    SWATCH = pygame.time.get_ticks()


def swatch_val():
    """
    Returns the elapsed time since the start of the stopwatch

    :return: elapsed time since stopwatch start
    ///////////////
    :rtype: int
    """
    global SWATCH
    return pygame.time.get_ticks() - SWATCH


# endregion

# region Random Values
# --------------------------------------------------
# PART 11 : RANDOM VALUES
# --------------------------------------------------

def rand():
    """
    Returns a random number between 0 (included) and 1 (not included)

    :return: random number in [0; 1[
    ///////////////
    :rtype: float
    """
    return random.random()


def rand_int(a: int, b: int):
    """
    Returns a random integer between a and b (both included)

    :param a: bottom boundary
    :param b: top boundary
    ///////////////
    :type a: int
    :type b: int
    ///////////////
    :return: random integer in [a; b]
    ///////////////
    :rtype: int
    """
    return int(floor((b - a + 1) * random.random())) + a
# endregion
