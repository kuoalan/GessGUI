import pygame
from GessBackend import Selection, Piece, GessGame


# Helper functions
def draw_board():
    """Method for placing stones onto board.

    :param: no value
    :return: no value
    """
    pieces.fill(PURPLE)
    for stone in black_stones:
        for key, value in square_dict.items():
            if key == stone:
                pygame.draw.circle(pieces, BLACK, value.center, 10)
    for stone in white_stones:
        for key, value in square_dict.items():
            if key == stone:
                pygame.draw.circle(pieces, WHITE, value.center, 10)


def coord_converter(coord):
    """Converts coordinate from numeric to alphanumeric.

    For example, (0,0) converts to 'a1'

    :param coord: numerical coordinate
    :type coord: tuple
    :return: alphanumeric coordinate
    :rtype: str
    """
    return chr(coord[0]+97) + str(coord[1] + 1)


# Initialize PyGame
pygame.init()

# Initialize colors
BLACK = pygame.Color('black')
RED = pygame.Color('red')
WHITE = pygame.Color('white')
PURPLE = pygame.Color('purple')
BLUE = pygame.Color('blue')

# Create window, set background image
screen = pygame.display.set_mode((600,600))
screen.fill((255,255,255))
pygame.display.set_caption("Gess")
background_img = pygame.image.load("bamboo_art.jpg")

# Set font sizes
font = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 22)

# Set board dimensions
tile_size = 25
width, height = 20*tile_size, 20*tile_size

# Set up Surfaces for game board, pieces, and move overlay
background = pygame.Surface((width, height))
background.fill((222,184,135))
pieces = pygame.Surface((width, height))
pieces.fill(PURPLE)
pieces.set_colorkey(PURPLE)
overlay = pygame.Surface((width, height))
overlay.fill(PURPLE)
overlay.set_colorkey(PURPLE)

# Draw board grid
rect_list = []
square_dict = {}
for y in range(0, height, tile_size):
    for x in range(0, width, tile_size):
        rect = (x, y, tile_size, tile_size)
        square = pygame.Rect(rect)
        rect_list.append(square)
        pygame.draw.rect(background, BLACK, square, 1)
pygame.draw.rect(background, BLACK, (0,0,500,500), 3)

# Create rects for overlay
small_rect_1 = pygame.Rect(0,0,22,22)
small_rect_2 = pygame.Rect(0,0,22,22)

# Assign grid square rects to coordinates
x_coord, y_coord = 0,19
for square in rect_list:
    square_dict[(x_coord, y_coord)] = square
    x_coord += 1
    if x_coord == 20:
        x_coord = 0
        y_coord -= 1

# Initialize backend code
GG = GessGame()

# Initialize variables
clicked_1 = 0
clicked_2 = 0
start_coord = ""
end_coord = ""
message = ""

# Game loop
running = True
while running:

    # Updates list of stones
    black_stones = GG.get_black_stones()
    white_stones = GG.get_white_stones()

    # Updating text reflecting current game state
    for event in pygame.event.get():
        draw_board()
        if GG.get_game_state() != "UNFINISHED":
            turn_text = font.render(GG.get_curr_player() + " WON!", True, BLACK)
        else:
            turn_text = font.render(GG.get_curr_player() + "'S TURN", True, BLACK)

        move_from = font_small.render("Start: " + start_coord, True, BLACK)
        move_to = font_small.render("End: " + end_coord, True, BLACK)
        black_num, white_num = str(len(black_stones)), str(len(white_stones))
        error_message = font_small.render(message, True, BLACK)

        if event.type == pygame.QUIT:
            running = 0
        # Logic for making game moves. Gets position of cursor when left mouse button is clicked and attempts to make move.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = list(pygame.mouse.get_pos())
            adjusted_pos = (pos[0]-50, pos[1]-50)
            for square in rect_list:
                if square.collidepoint(adjusted_pos):
                    for key, value in square_dict.items():
                        if value == square:
                            # If no square has been clicked yet, draw red square reflecting start of move
                            if clicked_1 == 0:
                                small_rect_1.center = (square.center[0], square.center[1])
                                pygame.draw.rect(overlay, RED, small_rect_1, 2)
                                clicked_1 = key
                                start_coord = coord_converter(key)
                                message = ""
                            # If second square has not been clicked yet, draw blue square reflecting end of move
                            elif clicked_2 == 0:
                                small_rect_2.center = (square.center[0], square.center[1])
                                pygame.draw.rect(overlay, BLUE, small_rect_2, 2)
                                clicked_2 = key
                                end_coord = coord_converter(key)
                                end_square = square
                            # If both move start and move finish square have been clicked. send coordinates to back end to attempt move
                            elif clicked_1 != 0 and clicked_2 != 0:
                                if end_square.collidepoint(adjusted_pos):
                                    result = GG.make_move(clicked_1, clicked_2)
                                    if result is True:
                                        message = ""
                                    else:
                                        message = result
                                clicked_1, clicked_2 = 0, 0
                                start_coord, end_coord = "", ""

                                overlay.fill(PURPLE)

    # Blitting background
    screen.blit(background_img, (0,0))
    screen.blit(background, (50, 50))

    # Blitting pieces and overlay
    screen.blit(pieces, (50, 50))
    screen.blit(overlay, (50,50))

    # Blitting text surfaces
    screen.blit(turn_text, [200, 15])
    screen.blit(move_from, [50,565])
    screen.blit(move_to, [150,565])
    screen.blit(error_message, [250, 565])

    # Refreshing display
    pygame.display.flip()



