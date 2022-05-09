import random
import requests
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]


empty = [['.....',
      '.....',
      '.....',
      '.....',
      '.....']]

shapes = [S, Z, I, J, L, T]
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
for key in indexes:
    for item in shapes:
        temporary[key] = item
        shapes.remove(item)
        break
shapes = []
for key in sorted(temporary.keys()):
    shapes.append(temporary[key])
"""

# shuffeles because teh api server is unavailable
random.shuffle(shapes)
shapes.append(empty)

# index 0 - 6 represent shape
# color_order: green, red, cyan, violet, orange, blue
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), 
                (138,43,226), (255, 165, 0), (0, 0, 255)]

# needs to implement this shot 
bullet = [['.....',
      '.....',
      '..0..',
      '.....',
      '.....'], 
      ['.....',
      '.....',
      '..0..',
      '.....',
      '.....']]


