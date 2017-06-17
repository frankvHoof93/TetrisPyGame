__author__ = 'Frank van Hoof'
import random, math, GameWorld
from copy import deepcopy

class Block:
    T_SHAPE_TEMPLATE = [[0,1,0],
                        [1,1,0],
                        [0,1,0]]

    S_SHAPE_TEMPLATE = [[0,1,0],
                        [1,1,0],
                        [1,0,0]]

    Z_SHAPE_TEMPLATE = [[1,0,0],
                        [1,1,0],
                        [0,1,0]]

    J_SHAPE_TEMPLATE = [[1,1,0],
                        [0,1,0],
                        [0,1,0]]

    L_SHAPE_TEMPLATE = [[0,1,0],
                        [0,1,0],
                        [1,1,0]]

    I_SHAPE_TEMPLATE = [[0,1,0,0],
                        [0,1,0,0],
                        [0,1,0,0],
                        [0,1,0,0]]

    O_SHAPE_TEMPLATE = [[1,1],
                        [1,1]]

    SHAPES = {'S' : S_SHAPE_TEMPLATE,
              'Z' : Z_SHAPE_TEMPLATE,
              'J' : J_SHAPE_TEMPLATE,
              'L' : L_SHAPE_TEMPLATE,
              'I' : I_SHAPE_TEMPLATE,
              'O' : O_SHAPE_TEMPLATE,
              'T' : T_SHAPE_TEMPLATE}

    def __init__(self, field_width, color = 0):
        self.block_type = random.choice(list(Block.SHAPES.keys()))
        self.block_shape = deepcopy(Block.SHAPES[self.block_type])
        if color == 0:
            self.color = random.randint(1,5)
        else:
            self.color = color
        self.size = len(self.block_shape)
        self.color_shape()
        self.xPos = int(math.floor((field_width / 2) - (self.size / 2))) - 1
        if not self.size == 3:
            self.xPos += 1
        self.yPos = -2
        self.rotation_count = 0

    def color_shape(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.block_shape[x][y] > 0:
                    self.block_shape[x][y] = self.color

    def rotated_clockwise(self):
        if (self.block_shape == None or self.block_type == 'O'):
            return False
        rotated = Block(1, self.color)
        rotated.block_type = self.block_type
        rotated.size = self.size
        rotated.xPos = self.xPos
        rotated.yPos = self.yPos
        rotated.block_shape = [[0 for x in range(5)] for x in range(5)]

        for r in range(0, self.size):
            for c in range(0, self.size):
                rotated.block_shape[c][self.size - 1 -r] = self.block_shape[r][c]
        self.rotation_count += 1
        if self.rotation_count > 3:
            self.rotation_count -= 4
        return rotated
        #MxN Matrix (M=5, N=5, r=row, c=column):
        #for r = 0 r<M r++:
            #for c = 0 c<N c++:
                #[c][M-1-r] = [r][c]

    def rotated_counter_clockwise(self):
        if (self.block_shape == None or self.block_type == 'O'):
            return False
        rotated = Block(1, self.color)
        rotated.block_type = self.block_type
        rotated.size = self.size
        rotated.xPos = self.xPos
        rotated.yPos = self.yPos
        rotated.block_shape = [[0 for x in range(self.size)] for x in range(self.size)]
        #MxN Matrix (M=5, N=5, r=row, c=column):
        for r in range(0, self.size):
            for c in range(0, self.size):
                rotated.block_shape[r][c] = self.block_shape[c][self.size - 1 -r]
        self.rotation_count -= 1
        if self.rotation_count < 0:
            self.rotation_count += 4
        rotated.color = self.color
        rotated.color_shape()
        return rotated
        #same as clockwise, only [r][c] = [c][M-1-r] instead of other way around

    def move(self, offset):
        self.xPos += offset[0]
        self.yPos += offset[1]

    def move_down(self):
        self.yPos += 1

    def move_left(self):
        self.xPos -= 1

    def move_right(self):
        self.xPos += 1

    def render(self, offset, is_active):
        img = None
        for x in range(0, self.size):
            for y in range(0, self.size):
                value = self.block_shape[x][y]
                if value == 1:
                    img = GameWorld.Gameworld.blueblockImg
                elif value == 2:
                    img = GameWorld.Gameworld.greenblockImg
                elif value == 3:
                    img = GameWorld.Gameworld.orangeblockImg
                elif value == 4:
                    img = GameWorld.Gameworld.redblockImg
                elif value >= 5:
                    img = GameWorld.Gameworld.yellowblockImg
                if not value == 0:
                    if is_active:
                        xPos = (x + self.xPos) * GameWorld.Gameworld.img_size + offset[0]
                        yPos = (y + self.yPos) * GameWorld.Gameworld.img_size + offset[1]
                        GameWorld.Gameworld.gameDisplay.blit(img, (xPos, yPos))
                    else:
                        xPos = (x * GameWorld.Gameworld.img_size + offset[0] - (self.size * GameWorld.Gameworld.img_size / 2))
                        yPos = (y * GameWorld.Gameworld.img_size + offset[1] - (self.size * GameWorld.Gameworld.img_size / 2))
                        if self.block_type == 'O':
                            yPos -= 10
                        GameWorld.Gameworld.gameDisplay.blit(img, (xPos, yPos))