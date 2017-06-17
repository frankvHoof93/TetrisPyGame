__author__ = 'Frank van Hoof'
import pygame, random
from Block import Block

class Gameworld:
    blockImg = pygame.image.load('Images/block.png')
    redblockImg = pygame.image.load('Images/redblock.png')
    blueblockImg = pygame.image.load('Images/blueblock.png')
    greenblockImg = pygame.image.load('Images/greenblock.png')
    orangeblockImg = pygame.image.load('Images/orangeblock.png')
    yellowblockImg = pygame.image.load('Images/yellowblock.png')
    gameDisplay = None
    img_size = 20
    field_width = 10
    field_height = 30
    field_offset = (100,60)
    next_block_offset = (450, 90)
    move_cooldown = 300
    is_playing = False
    is_alive = True
    is_starting = True
    gamefield = [[0 for x in range(0, field_height)] for y in range(0, field_width)]
    clockwise_wallkicks_default = [[(-1,0),(1,0),(-1,-1),(0,2),(-1,2)],
                                   [(1,0),(-1,0),(1,1),(0,-2),(1,-2)],
                                   [(1,0),(-1,0),(1,-1),(0,2),(1,2)],
                                   [(-1,0),(1,0),(-1,1),(0,-2),(-1,-2)]]
    clockwise_wallkicks_I = [[(-1,0),(-2,0),(1,0),(2,0),(-2,1),(1,-2)],
                             [(1,0),(-1,0),(2,0),(-2,0),(-1,-2),(2,1)],
                             [(1,0),(2,0),(-1,0),(-2,0),(2,-1),(-1,2)],
                             [(-1,0),(1,0),(-2,0),(2,0),(1,2),(-2,-1)]]
    counter_clockwise_wallkicks_default = [[(1,0),(-1,0),(1,1),(0,-2),(1,-2)],
                                           [(-1,0),(1,0),(-1,-1),(0,2),(-1,2)],
                                           [(-1,0),(1,0),(-1,1),(0,-2),(-1,-2)],
                                           [(1,0),(-1,0),(1,-1),(0,2),(1,2)]]
    counter_clockwise_wallkicks_I = [[(1,0),(2,0),(-1,0),(-2,0),(2,-1),(-1,2)],
                                     [(-1,0),(1,0),(-2,0),(2,0),(1,2),(-2,-1)],
                                     [(-1,0),(-2,0),(1,0),(2,0),(-2,1),(1,-2)],
                                     [(1,0),(-1,0),(2,0),(-2,0),(-1,-2),(2,1)]]

    def __init__(self, score):
        self.score = score
        self.reset()

    def loop(self):
        if self.is_playing:
            now = pygame.time.get_ticks()
            if now - self.last_move >= self.move_cooldown:
                self.last_move = now
                if self.check_movedown():
                    self.current_block.move_down()
                else:
                    self.save_and_new_block()
                    if not self.check_movedown():
                        Gameworld.is_playing = False
                        Gameworld.is_alive = False

    def render(self):
        img = None
        for x in range(0, self.field_width):
            for y in range(0, self.field_height):
                value = self.gamefield[x][y]
                if value == 0:
                    img = Gameworld.blockImg
                elif value == 1:
                    img = Gameworld.blueblockImg
                elif value == 2:
                    img = Gameworld.greenblockImg
                elif value == 3:
                    img = Gameworld.orangeblockImg
                elif value == 4:
                    img = Gameworld.redblockImg
                elif value == 5:
                    img = Gameworld.yellowblockImg
                Gameworld.gameDisplay.blit(img, (x * self.img_size + self.field_offset[0], y * self.img_size + self.field_offset[1]))
        self.current_block.render(self.field_offset, True)
        self.nextblock.render(self.next_block_offset, False)

    def handle_input(self, input):
        if self.is_playing:
            if input.key == pygame.K_LEFT:
                if self.check_move_left(self.current_block):
                    self.current_block.move_left()
                    self.last_move = pygame.time.get_ticks()
            elif input.key == pygame.K_RIGHT:
                if self.check_move_right(self.current_block):
                    self.current_block.move_right()
                    self.last_move = pygame.time.get_ticks()
            elif input.key == pygame.K_UP:
                while self.check_movedown():
                    self.current_block.move_down()
                self.save_and_new_block()
            elif input.key == pygame.K_DOWN:
                if self.check_movedown():
                    self.current_block.move_down()
                    self.last_move = pygame.time.get_ticks()
            elif input.key == pygame.K_COMMA:
                if self.current_block.block_type != 'O':
                    block = self.current_block.rotated_counter_clockwise()
                    if not self.check_block(block, 0, 0):
                        check = self.check_wallkicks(block, False)
                        if check != (0,0):
                            block.move(check)
                            self.current_block = block
                            self.last_move = pygame.time.get_ticks()
                    else:
                        self.current_block = block
                        self.last_move = pygame.time.get_ticks()
            elif input.key == pygame.K_PERIOD:
                if self.current_block.block_type != 'O':
                    block = self.current_block.rotated_clockwise()
                    if not self.check_block(block, 0, 0):
                        check = self.check_wallkicks(block, True)
                        if check != (0,0):
                            block.move(check)
                            self.current_block = block
                            self.last_move = pygame.time.get_ticks()
                    else:
                        self.current_block = block
                        self.last_move = pygame.time.get_ticks()
            elif input.key == pygame.K_SPACE:
                Gameworld.is_playing = False
        elif self.is_alive:
            if input.key == pygame.K_SPACE:
                Gameworld.is_starting = False
                Gameworld.is_playing = True
        else:
            if input.key == pygame.K_SPACE:
                self.reset()

    def reset(self):
        pygame.mixer.music.stop()
        music = random.randint(0, 3)
        song = None
        if music == 1:
            song = 'Sounds/Music/bgLoop.wav'
        elif music == 2:
            song = 'Sounds/Music/bgLoop2.wav'
        else:
            song = 'Sounds/Music/bgLoop3.wav'
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)
        Gameworld.is_starting = True
        Gameworld.is_alive = True
        Gameworld.is_playing = False
        self.score.set_score(0)
        self.current_block = Block(self.field_width)
        self.nextblock = Block(self.field_width)
        self.last_move = pygame.time.get_ticks()
        self.gamefield = [[0 for x in range(0, self.field_height)] for y in range(0, self.field_width)]

    def check_block(self, block, x_offset, y_offset):
        for x in range(0, block.size):
            for y in range(0, block.size):
                if block.block_shape[x][y] > 0:
                    xPos = self.current_block.xPos + x + x_offset
                    yPos = self.current_block.yPos + y + y_offset
                    if yPos < 0 and (xPos >= 0 and xPos < self.field_width):
                        continue
                    if not self.check_is_on_board(xPos, yPos):
                        return False
                    if self.gamefield[xPos][yPos] > 0:
                        return False
        return True

    def check_is_on_board(self, xPos, yPos):
        if xPos >= 0 and xPos < Gameworld.field_width:
            if yPos >= -1 and yPos < Gameworld.field_height:
                return True
        return False

    def check_movedown(self):
        return self.check_block(self.current_block, 0, 1)

    def check_move_left(self, block):
        return self.check_block(block, -1, 0)

    def check_move_right(self, block):
        return self.check_block(block, 1, 0)

    def clear_lines(self):
        lines_done = 0
        y = Gameworld.field_height - 1
        while y >= 0:
            full_line = True
            for x in range(0, Gameworld.field_width):
                if self.gamefield[x][y] == 0:
                    full_line = False
            if full_line:
                lines_done += 1
                self.remove_line(y)
                self.move_field_down(y)
                y += 1 #restart line
            y -= 1
        return lines_done

    def remove_line(self, y):
        for x in range(0, Gameworld.field_width):
            self.gamefield[x][y] = 0

    def move_field_down(self, y):
        for z in range(y, 0, -1):
            for x in range(0, Gameworld.field_width):
                self.gamefield[x][z] = self.gamefield[x][z-1]

    def check_wallkicks(self, block, is_clockwise):
        rotation = block.rotation_count
        kicks = None
        if is_clockwise:
            rotation -= 1
            if rotation < 0:
                rotation += 4
            if block.block_type == 'I':
                kicks = Gameworld.clockwise_wallkicks_I
            else:
                kicks = Gameworld.clockwise_wallkicks_default
        else:
            if block.block_type == 'I':
                kicks = Gameworld.counter_clockwise_wallkicks_I
            else:
                kicks = Gameworld.counter_clockwise_wallkicks_default
        y = 5
        if block.block_type == 'I':
            y = 6
        for x in range(0,y):
            to_test = kicks[rotation][x]
            if self.check_block(block, to_test[0], to_test[1]):
                return to_test
        return (0,0)

    def save_and_new_block(self):
         for x in range(0,self.current_block.size):
            for y in range(0,self.current_block.size):
                xPos = self.current_block.xPos + x
                yPos = self.current_block.yPos + y
                if yPos < 0:
                    continue
                if self.check_is_on_board(xPos, yPos):
                    self.gamefield[xPos][yPos] += self.current_block.block_shape[x][y]
         self.current_block = self.nextblock
         self.nextblock = Block(self.field_width)
         lines_cleared = self.clear_lines()
         score = lines_cleared**3 + lines_cleared * 10
         self.score.add_score(score)