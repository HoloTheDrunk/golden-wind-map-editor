from LearningAides import *
import os


def main(w=30, h=15, scalingFactor=32):
    # We'll always update the graphic window by hand
    auto_display_toggle(False)

    W, H = w * scalingFactor, h * scalingFactor
    menuSize = Point(128, 90)

    init_graphic(W + 128, H + 90, "GWME v0.1", white)
    pygame.display.set_icon(pygame.image.load("data\\icon.png"))

    draw_area = Button(Point(0, 0), "", W, H, black, white)

    ghost = pygame.Surface((32, 32))

    # Load all the color buttons from the designated .blf (Button-Listing File) file
    blockButtons: List[Button] = load_buttons_from_file("buttons.blf", W + 32, 30)
    lenBB = len(blockButtons)

    # Colors taken from the front-ground colors of the blockButtons list
    colors: List[Color] = [blockButtons[i].color_fg for i in range(len(blockButtons))]
    currentColor: int = 0

    # Layers initialization with only one layer
    layers: List[List[Tuple[Point, Color]]] = [[]]
    currentLayer: int = 0
    transparent: bool = False

    # SAVE button
    saveButton = Button(Point(W - 210, H + menuSize.y // 3), "SAVE", 100, menuSize.y // 3, pygame.Color("#7DFF00"),
                        soft_black, True)
    # LOAD button
    # loadButton = Button(Point(W - 100, H + menuSize.y // 3), "LOAD", 100, menuSize.y // 3, pygame.Color("#00BCFF"),
    #                     soft_black, True)
    loadButton = Button(Point(W - 100, H + menuSize.y // 3), "LOAD", 100, menuSize.y // 3, gray,
                        soft_black, True)
    # QUIT button
    quitButton = Button(Point(W + 10, H + menuSize.y // 3), "QUIT", 100, menuSize.y // 3, pygame.Color("#FF0051"),
                        soft_black, True)

    # Layer UP / DOWN buttons
    layer_upButton = Button(Point(W + 48, (H + menuSize.y) // 2), "UP", 32, 32, soft_black, white, True)
    layer_downButton = Button(Point(W + 48, (H + menuSize.y) // 2 + 64), "DOWN", 32, 32, soft_black, white, True)

    # Transparency toggle and layer indicator button
    alphaButton = Button(Point(W + 48, (H + menuSize.y) // 2 + 32), str(currentLayer), 32, 32, soft_black, white, True)

    checkSaveWatch = False
    postEventRefresh = False
    while True:
        # region BasicWindow
        # ------------------------------------------------------------------------

        # Draw the screen again if it needs to be refreshed
        if postEventRefresh:
            checkSaveWatch = refresh_screen(w, h, W, H, scalingFactor, menuSize, layers, currentLayer, transparent,
                                            blockButtons, currentColor, layer_upButton, layer_downButton, alphaButton,
                                            quitButton, saveButton, loadButton, checkSaveWatch)
            postEventRefresh = False

        # Draw ghost
        if draw_area.inside(get_mouse()):
            draw_ghost(scalingFactor, colors[currentColor], blockButtons)
            postEventRefresh = True

        display_all()
        # ------------------------------------------------------------------------
        # endregion

        keyData: int = get_key_down()
        mousePos = pygame.mouse.get_pos()
        mouseData: (List[bool], Point) = [pygame.mouse.get_pressed(), Point(mousePos[0], mousePos[1])]
        mouseDown = get_mouse_down()
        if (mouseDown is not None) and (mouseDown[0] is not None):
            if not mouseData[0][0]:
                mouseData[0][0] = mouseData[0][0] or mouseDown[0] == BUTTON_LEFT
            if not mouseData[0][1]:
                mouseData[0][1] = mouseData[0][1] or mouseDown[0] == BUTTON_MIDDLE
            if not mouseData[0][2]:
                mouseData[0][2] = mouseData[0][2] or mouseDown[0] == BUTTON_RIGHT

        if True in mouseData[0]:
            # QUIT
            if quitButton.inside(mouseData[1]):
                break
            # Draw area
            elif draw_area.inside(mouseData[1]):
                # Left click
                if mouseData[0][0]:
                    newPoint = True
                    for i in range(len(layers[currentLayer])):
                        if layers[currentLayer][i][0] == Point(mouseData[1].x // scalingFactor,
                                                               mouseData[1].y // scalingFactor):
                            del layers[currentLayer][i]
                            break
                    layers[currentLayer].append((Point(mouseData[1].x // scalingFactor,
                                                       mouseData[1].y // scalingFactor),
                                                 colors[currentColor]))
                # Right click
                if mouseData[0][2]:
                    for i in range(len(layers[currentLayer])):
                        if layers[currentLayer][i][0] == Point(mouseData[1].x // scalingFactor,
                                                               mouseData[1].y // scalingFactor):
                            del layers[currentLayer][i]
                            break

            elif layer_upButton.inside(mouseData[1]):
                currentLayer = increment_layer(layers, currentLayer)
            elif layer_downButton.inside(mouseData[1]):
                currentLayer = decrement_layer(currentLayer)
            elif alphaButton.inside(mouseData[1]):
                transparent = toggle_transparency(alphaButton, transparent)
            elif saveButton.inside(mouseData[1]):
                save_map(layers, -1 if transparent else currentLayer, blockButtons, w, h, W, H)
                swatch_start()
                checkSaveWatch = True
            # elif loadButton.inside(clickData[1]):
            #     layers = load_map()
            #     currentLayer = 0
            else:
                for i in range(len(blockButtons)):
                    if blockButtons[i].inside(mouseData[1]):
                        currentColor = i
                        break
        if keyData is not None:
            if keyData in [K_z, K_w, K_q, K_a, K_s, K_d]:
                if keyData in [K_z, K_w]:
                    if currentColor >= 2:
                        currentColor -= 2
                    else:
                        currentColor = lenBB - (currentColor if currentColor == 1 else 2)
                elif keyData in [K_q, K_a]:
                    if currentColor % 2 == 0 and currentColor < lenBB - 1:
                        currentColor += 1
                    elif currentColor % 2 == 1 and currentColor > 0:
                        currentColor -= 1
                elif keyData == K_s:
                    if currentColor < lenBB - 2:
                        currentColor += 2
                    else:
                        currentColor %= 2
                else:
                    if currentColor % 2 == 1 and currentColor > 0:
                        currentColor -= 1
                    elif currentColor % 2 == 0 and currentColor < lenBB - 1:
                        currentColor += 1
            elif keyData in [K_LSHIFT, K_LCTRL, K_LALT, K_t]:
                if keyData == K_LSHIFT:
                    currentLayer = increment_layer(layers, currentLayer)
                elif keyData == K_LCTRL:
                    currentLayer = decrement_layer(currentLayer)
                elif keyData == K_LALT:
                    currentLayer = 0
                else:
                    transparent = toggle_transparency(alphaButton, transparent)


# region Layer handling


def increment_layer(layers, currentLayer):
    if currentLayer == len(layers) - 1:
        layers.append([])
    currentLayer += 1
    return currentLayer


def decrement_layer(currentLayer):
    if currentLayer > 0:
        currentLayer -= 1
    return currentLayer


def toggle_transparency(alphaButton, transparent):
    transparent = not transparent
    if transparent:
        alphaButton.color_bg = pygame.Color("#00BCFF")
    else:
        alphaButton.color_bg = white
    return transparent


# endregion

# region Drawing


def refresh_screen(w, h, W, H, scalingFactor, menuSize, layers, currentLayer, transparent, blockButtons, currentColor,
                   layer_upButton, layer_downButton, alphaButton, quitButton, saveButton, loadButton, checkSaveWatch):
    refresh_drawing_area(layers, currentLayer, transparent, blockButtons, w, h, W, H, scalingFactor)
    return refresh_menus(W, H, menuSize, blockButtons, currentColor, currentLayer, layer_upButton, layer_downButton,
                         alphaButton, quitButton, saveButton, loadButton, checkSaveWatch)


def refresh_menus(W, H, menuSize, blockButtons, currentColor, currentLayer, layer_upButton, layer_downButton,
                  alphaButton, quitButton, saveButton, loadButton, checkSaveWatch):
    # region Side
    # Block picker area
    draw_fill_rectangle(Point(W, 0), menuSize.x, H + menuSize.y, gray)

    # Block buttons
    for button in blockButtons:
        button.draw(True)

    # Selection highlighter
    draw_rectangle(Point(blockButtons[0].P.x + (currentColor % 2) * blockButtons[0].w,
                         blockButtons[0].P.y + (currentColor // 2) * blockButtons[0].h),
                   blockButtons[0].w, blockButtons[0].h,
                   yellow)
    # endregion

    # region Bottom
    # Buttons area
    draw_fill_rectangle(Point(0, H), W + menuSize.x, menuSize.y, gray)

    # Software name and version
    display_text("Golden Wind Map Editor", 52, Point(5, H + 5), white, True)
    display_text("v0.2", 16, Point(15, H + text_height("Golden Wind Map Editor", 52, True)), soft_black, True)

    # Layer handling
    arrowSize = 8
    layer_upButton.draw(True, False)
    draw_fill_triangle(Point(layer_upButton.P.x + layer_upButton.w // 2, layer_upButton.P.y + arrowSize),
                       Point(layer_upButton.P.x + arrowSize, layer_upButton.P.y + layer_upButton.h - arrowSize),
                       Point(layer_upButton.P.x + layer_upButton.w - arrowSize,
                             layer_upButton.P.y + layer_upButton.h - arrowSize),
                       layer_upButton.color_bg)
    alphaButton.text = str(currentLayer)
    alphaButton.draw(True, True)
    layer_downButton.draw(True, False)
    draw_fill_triangle(
        Point(layer_downButton.P.x + layer_downButton.w // 2, layer_downButton.P.y + layer_downButton.h - arrowSize),
        Point(layer_downButton.P.x + arrowSize, layer_downButton.P.y + arrowSize),
        Point(layer_downButton.P.x + layer_downButton.w - arrowSize,
              layer_downButton.P.y + arrowSize),
        layer_downButton.color_bg)

    # SAVE button
    saveButton.draw(False, True)
    if checkSaveWatch:
        if swatch_val() < 1000:
            display_text_center("SAVED!", 12,
                                Point(saveButton.P.x + saveButton.w // 2, saveButton.P.y + saveButton.h + 8),
                                saveButton.color_fg)
        else:
            checkSaveWatch = False
    # LOAD button
    loadButton.draw(False, True)
    display_text_center("WIP", 12, Point(loadButton.P.x + loadButton.w // 2, loadButton.P.y + loadButton.h + 8), black)
    # QUIT button
    quitButton.draw(False, True)
    # endregion

    return checkSaveWatch


def refresh_drawing_area(layers: List[List[Tuple[Point, Color]]], currentLayer: int, transparent: bool,
                         buttons: List[Button], w: int, h: int, W: int, H: int, scalingFactor: int = 16):
    # Erase everything
    draw_fill_rectangle(Point(0, 0), W, H, white)
    # Draw single layers or layer + all layers below but slightly transparent
    if transparent and currentLayer > 0 and len(layers) > 1:
        for i in range(currentLayer + 1):
            # TODO make transparency work
            # draw_layer(layers[i], buttons, map_from_to(i, 0, currentLayer, 0, 255), scalingFactor)
            draw_layer(layers[i], buttons, 255, scalingFactor)
    else:
        draw_layer(layers[currentLayer], buttons, 255, scalingFactor)
    # Draw grid
    draw_grid(w, h, W, H, scalingFactor)


def draw_grid(w: int, h: int, W: int, H: int, scalingFactor: int):
    for i in range(h):
        draw_line(Point(0, i * scalingFactor), Point(W, i * scalingFactor), gray)
    for j in range(w):
        draw_line(Point(j * scalingFactor, 0), Point(j * scalingFactor, H), gray)


def draw_layer(layer: List[Tuple[Point, Color]], buttons: List[Button], transparency: int = 255,
               scalingFactor: int = 1, S: pygame.Surface = PYGAME_SDL_WINDOW):
    """
    Draw a single layer onto the graphic window
    :param layer: list composed of coordinate and color data
    :param buttons: list of color buttons used for finding the right image
    :param transparency: transparency of colors/images
    :param scalingFactor: how large to draw the pixels
    :param S: surface on which to draw (default is entire window)
    """
    if transparency == 255:
        if scalingFactor > 1:
            if scalingFactor == 32:
                for pixel in layer:
                    load_image(get_path_from_color(pixel[1], buttons),
                               Point(pixel[0].x * scalingFactor, pixel[0].y * scalingFactor))
            else:
                for pixel in layer:
                    draw_fill_rectangle(Point(pixel[0].x * scalingFactor, pixel[0].y * scalingFactor),
                                        scalingFactor,
                                        scalingFactor, pixel[1])
        else:
            for pixel in layer:
                draw_fill_rectangle(pixel[0], 1, 1, pixel[1], S)
    else:
        if scalingFactor > 1:
            if scalingFactor == 32:
                for pixel in layer:
                    load_image_alpha(get_path_from_color(pixel[1], buttons),
                                     Point(pixel[0].x * scalingFactor, pixel[0].y * scalingFactor))
            else:
                for pixel in layer:
                    draw_fill_rectangle(Point(pixel[0].x * scalingFactor, pixel[0].y * scalingFactor),
                                        scalingFactor,
                                        scalingFactor,
                                        pygame.Color(pixel[1].r, pixel[1].g, pixel[1].b, transparency))
        else:
            for pixel in layer:
                draw_fill_rectangle(pixel[0], 1, 1, pygame.Color(pixel[1].r, pixel[1].g, pixel[1].b, transparency), S)


def draw_ghost(scalingFactor, col, buttons):
    mousePos = get_mouse()
    processedMousePos = Point((mousePos.x // scalingFactor) * scalingFactor,
                              (mousePos.y // scalingFactor) * scalingFactor)
    load_image(get_path_from_color(col, buttons), processedMousePos)

    if col != red:
        draw_rectangle(processedMousePos, scalingFactor, scalingFactor, red)
    else:
        draw_rectangle(processedMousePos, scalingFactor, scalingFactor, yellow)

    if PYGAME_SDL_DISPLAY == 1:
        pygame.display.flip()


# endregion

# region Saving and loading

def get_path_from_color(col, buttons):
    for i in range(len(buttons)):
        if col == buttons[i].color_fg:
            L = buttons[i].imagePath.split("\\")
            return "data\\raw\\" + L[-1]
    return "-1"


def save_map(layers, currentLayer, buttons, w, h, W, H):
    # Initialize surface to draw on and save
    S = pygame.Surface((w, h))

    # Create output directory if there is none
    if not os.path.isdir("IO\\"):
        os.mkdir("IO\\")

    if currentLayer != -1:
        draw_fill_rectangle(Point(0, 0), W, H, white, S)
        draw_layer(layers[currentLayer], buttons, 255, 1, S)
        pygame.image.save(S, "IO\\layer_{0}.png".format(currentLayer))
    else:
        draw_fill_rectangle(Point(0, 0), W, H, white)
        for i in range(currentLayer + 1):
            if layers[i]:
                draw_layer(layers[i], buttons, 255, 1, S)
                pygame.image.save(S, "IO\\layers_{0}.png".format(i))


# TODO finish load_map() for v0.2
# def load_map():
#     BASE_PATH = "IO\\layer_"
#     layers = []
#     n = 0
#     while os.path.isfile(BASE_PATH + "{0}.png".format(n)):
#         S = pygame.image.load(BASE_PATH + "{0}.png".format(n))
#         layers.append([])
#         for j in range(S.get_height()):
#             for i in range(S.get_width()):
#                 pixelColor = S.get_at((i,j))
#                 if pixelColor
#                 layers[-1].append((Point(i, j), S.get_at((i, j))))
#         n += 1
#     return layers if n > 0 else [[]]

# endregion

main()
