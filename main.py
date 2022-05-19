import random
import pygame
import requests
from ships import *


pygame.font.init()

# GLOBALS VARS
s_width = 700
s_height = 400
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 300  # meaning 300 // 10 = 30 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


class Shot():
    rows = 10  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = (255, 255, 255)
        # number from 0-3
        self.rotation = 0

class Piece(Shot):
    def __init__(self, column, row, shape):
        super().__init__(column, row, shape)
        self.color = shape_colors[shapes.index(shape)]


def display_name_inst():
    win.fill((0, 0, 0))
    text = "Enter your username in the terminal."
    draw_text_middle(text, 45, (255, 255, 255), win)
    pygame.display.update()
    

def display_highscore():
    """Displays the top 5 scores on the surface
    """
    win.fill((0, 0, 0))
    with open("battleship_statistics.txt", "rt", encoding="utf8") as f:
        document = f.readlines()
    f.close()

    scores_dic = {}

    for line in document:
        parts = line.split(":")
        value = parts[1].strip(" ")
        scores_dic[(parts[0]).strip(" ")] = value.removesuffix(" pts\n")

    # sortes the dictionary based on items, from high to low
    sorted_scores = sorted(scores_dic.items(), key=lambda x: x[1], reverse=True)
    sorted_dic = dict(sorted_scores[:5])

    with open("battleship_statistics.txt", "wt", encoding="utf8") as f:
        for key in sorted_dic:
            f.write(f"{key}    :   {sorted_dic[key]} pts\n")
    f.close()

    font = pygame.font.SysFont('nunito', 50, bold=True)
    label = font.render("Leaderboard:", 1, (255, 255, 255))
    win.blit(label, (100, 100))
    font = pygame.font.SysFont('nunito', 25, bold=True)
    
    counter = 0
    leaderboard_numb = 1 
    for person in sorted_dic:
        if leaderboard_numb == 6:
            break
        text = f"{leaderboard_numb}. {person}  :  {sorted_dic[person]} pts"
        label = font.render(text, 1, (255, 255, 255))
        y_coord = 175 + counter
        win.blit(label, (200, y_coord))
        counter += 25
        leaderboard_numb += 1


def create_grid(locked_positions={}):
    """Creates a two dimensional list based on the positions that are not allowed to change

    Args:
        locked_positions (dict, optional): dictionary; (x, y - position) : (red, green, blue). Defaults to {}.

    Returns:
        list: returns a nestled two dimensional list.
    """
    # creates a sublist (row), 10 width with black squares and does that 10 times
    grid = [[(0,0,0) for _ in range(10)] for _ in range(10)]
    
    # colors specific squares
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # checks if square_pos are in the grid
            if (x, y) in locked_positions:
                square = locked_positions[(x, y)]
                # changes the color of the square to match the color in locket_positions
                grid[y][x] = square
    return grid


def convert_shape_format(shape):
    """converts the nestled configurations/figures of strings to 

    Args:
        shape (object): an object from the Piece class.

    Returns:
        list: a list of positions
    """
    positions = []
    # gets the correct rotation of the shape
    format = shape.shape[(shape.rotation % len(shape.shape))]

    for i, line in enumerate(format):
        row = list(line)
        # goes through each line in the rotation list
        for j, column in enumerate(row):
            # if a bit of the shape is there add it to the list
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    # corrects for the offset created by "." in the shape-lists
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    # returns the correct positions of the shape (argument)
    return positions


def valid_space(shape, grid):
    """Checks if the shape is placed in a valid space within the grid including the previously placed pieces

    Args:
        shape (Object): an object of the class Piece
        grid (List): the grid created from create_grid()

    Returns:
        Bool
    """
    # adds all of the positions to the list
    accepted_positions = [[(j, i) for j in range(10)\
         if grid[i][j] == (0, 0, 0)] for i in range(10)]
    # makes the list one dimensional - instead of being nestled
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    # goes through the shapes coordinates
    for pos in formatted:
        # if a coordinate is not within all of the accepted_positions
        if pos not in accepted_positions:
            # and the y-value is grater than -1
            if pos[1] > -1:
                # then it is not a valid space
                return False

    return True


def accepted_space(shape, grid):
    """_Checks if the shape is placed in a accepted space within the grid_

    Args:
        shape (Object): an object of the class Piece_
        grid (List): _the grid created from create_grid()_

    Returns:
        Bool
    """
    # adds all of the positions to the list
    accepted_positions = [[(j, i) for j in range(10)\
         if grid[i][j] == (0, 0, 0)] for i in range(10)]
    # makes the list one dimensional - instead of being nestled
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    # goes through the shapes coordinates
    for pos in formatted:
        # if a coordinate is not within all of the accepted_positions
        if pos not in accepted_positions:
            return False
    return True


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('nunito', size, bold=True)
    label = font.render(text, 1, color)
    x_position = top_left_x + play_width/2 - (label.get_width() / 2)
    y_position = (top_left_y + play_height/2 - label.get_height()/2)
    surface.blit(label, (x_position, y_position))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (90, 90, 90), (sx, sy+ i*30),\
             (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (90, 90, 90), (sx + j * 30, sy),\
                 (sx + j * 30, sy + play_height))  # vertical lines


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('nunito', 20)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, \
                    (sx + j * 30, sy + i * 30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface):
    surface.fill((0,0,0))
    font = pygame.font.SysFont('nunito', 45)
    label = font.render('Battleship', 1, (255, 255, 255))

    # (starting position from the left, starting position from the top)
    surface.blit(label,\
         (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # goes through all of the squares and creates rectangles of them
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            pygame.draw.rect(surface, grid[row][col], ((top_left_x + col * 30),\
                 (top_left_y + row * 30), 30, 30), 0)

    # draws the lines for the grid and red border
    draw_grid(surface, 10, 10)
    pygame.draw.rect(surface, (255, 0, 0), \
        (top_left_x, top_left_y, play_width, play_height), 5)


def main():
    global grid, shapes
    accepted = False
    while not accepted:        
        username = str(input("Enter your username [XXX]:  "))
        if len(username) == 3:
            accepted = True
        
    # shuffles the shapes order with the api
            # if the api is down, make the enclosed code a comment and uncomment line 289
            # enclose starts here 
    """
    indexes = []
    while len(indexes) != 6:
        # generates a random number 0-5 one time repeted
        url = "http://www.randomnumberapi.com/api/v1.0/random?min=0&max=5&count=1"
        response = requests.get(url)
        answer = response.json()
        if int(answer[0]) not in indexes:
            indexes.append(int(answer[0]))

    temporary = {}
    # shuffles shapes according to indexes
    if len(shapes) == 7:
        shapes.pop()
    for key in indexes:
        for item in shapes:
            temporary[key] = item
            shapes.remove(item)
            break
    shapes = []
    for key in sorted(temporary.keys()):
        shapes.append(temporary[key])
    """
            # enclosure ends here
    
    if len(shapes) == 7:
        shapes.pop()
    random.shuffle(shapes)
    random.shuffle(shape_colors)
    if len(shapes) == 6:
        shapes.append(empty)

    # (x, y) : (0 , 0, 0)
    locked_positions = {}
    grid = create_grid(locked_positions)
    run = True
    figure = []
    endgame = False
    # for each ship in shapes
    for each in range(len(shapes)):
        figure.append(Piece(5, 5, shapes[each]))
    

    while run:
        try:
            current_piece = figure[0]
        except IndexError:
            # if all ships have been placed it makes them "dissaper"
            if figure == []:
                # change all locked_positions (r, g, b) to black
                if endgame:
                    for i in range(100):
                        figure.append(Shot(5, 5, bullet))
                else:
                    for key in locked_positions.keys():
                        locked_positions.update({key : (0, 0, 0)})
                        endgame = True

        grid = create_grid(locked_positions)
        # for the ghost mode
        blank_grid = create_grid()

        # key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            # movements
            if event.type == pygame.KEYDOWN:
                # left movement 
                if event.key == pygame.K_a:
                    current_piece.x -= 1
                    if not accepted_space(current_piece, blank_grid):
                        current_piece.x += 1
                
                # right movement 
                if event.key == pygame.K_d:
                    current_piece.x += 1
                    if not accepted_space(current_piece, blank_grid):
                        current_piece.x -= 1

                # up movement 
                if event.key == pygame.K_w:
                    current_piece.y -= 1
                    if not accepted_space(current_piece, blank_grid):
                        current_piece.y += 1
                              
                # down movement 
                if event.key == pygame.K_s:
                    current_piece.y += 1
                    if not accepted_space(current_piece, blank_grid):
                        current_piece.y -= 1
      
                # rotate ship
                if event.key == pygame.K_r:    
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not accepted_space(current_piece, blank_grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                # placing down figure
                if event.key == pygame.K_RETURN:
                    # shooting
                    if endgame:
                        for position in shape_pos:
                            pos = (position[0], position[1])
                            # if the shot exists 
                            if pos in locked_positions.keys():
                                if locked_positions[pos] in [(128, 128, 128), (255, 0, 0)]:
                                    print("You are not allowed to shoot a previously shot squares")
                                else:
                                    locked_positions.update({pos : (255, 0, 0)})
                                    figure.pop()
                            else:
                                locked_positions.update({pos : (128, 128, 128)})
                                figure.pop()

                    # placing of ships
                    else:
                        if not valid_space(current_piece, grid):
                            print("Don't try to cheat")
                        else:
                            for position in shape_pos:
                                pos = (position[0], position[1])
                                locked_positions[pos] = current_piece.color
                            figure.pop(0)

                # esc = quit
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.display.quit()
                    quit()

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        draw_window(win)

        # tries to draw the next piece to the right - if there is none then it passes
        try:
            if len(figure) == 2:
                # display text: press enter and have player two start guessing
                pass
            else:
                next_piece = figure[1]
                draw_next_shape(next_piece, win)
        except:
            pass
        pygame.display.update()


        # if all of the ships have been shot
        if endgame:
            if not (0, 0, 0) in locked_positions.values():
                win.fill((0, 0, 0))
                draw_text_middle('You have shot all the ships', 45, (255, 255, 255), win)
                pygame.display.update()
                pygame.time.delay(2500)
                win.fill((0, 0, 0))
                score = 2400 / (100 - len(figure))
                draw_text_middle(f"Your score was {round(score)}", 45, (255, 255, 255), win)
                pygame.display.update()
                pygame.time.delay(2500)
                with open("battleship_statistics.txt", "at", encoding="utf8") as f:
                    f.write(f"{username}    :   {round(score)} pts\n")
                pygame.event.clear()  
                main_menu()


# makes a window with txt in middle
def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to begin.', 45, (255, 255, 255), win)
        font = pygame.font.SysFont('nunito', 25, bold=True)
        label = font.render("Press i for instructions or h for highscore",\
             1, (255, 255, 255))
        win.blit(label, (160, 270))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # quits
                if event.key == pygame.K_ESCAPE:
                    run = False
                # display instructions
                elif event.key == pygame.K_i:
                    win.fill((0, 0, 0))
                    key_binds = ["w = up", "s = down", "a = left", "d = right", "r = rotate", 
                    "enter = place/confirm", "escape = quits the game"]
                    label = font.render("Key binds:", 1, (255, 255, 255))
                    win.blit(label, (75, 50))
                    counter = 0
                    for string in key_binds:
                        label = font.render(string, 1, (255, 255, 255))
                        y_coord = 75 + counter
                        win.blit(label, (100, y_coord))
                        counter += 25
                    
                    label = font.render('If all the ships have been placed press "enter"',\
                         1, (255, 255, 255))
                    win.blit(label, (25, 300))
                    label = font.render('Then call in player 2 and let them guess', \
                        1, (255, 255, 255))
                    win.blit(label, (25, 320))
                    pygame.display.update()
                    pygame.time.delay(5000)
                    pygame.event.clear()  
                    main_menu()
                # display highscore
                elif event.key == pygame.K_h:
                    display_highscore()
                    pygame.display.update()
                    pygame.time.delay(4000)
                    pygame.event.clear()  
                    main_menu()
                # runs the game
                else:
                    display_name_inst()
                    main()
    pygame.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Battleship")

if __name__ == "__main__":
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("Battleship")

    # starts the game
    main_menu()
