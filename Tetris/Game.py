__author__ = 'Frank van Hoof'
import pygame, GameWorld, Score, UI

class Game:
    display_width = 1000
    display_height = 750
    score_offset = (865, 570)
    gamename = "Tetris"
    gameimg = pygame.image.load('Images/Tetris.png')
    color_black = (0,0,0)

    def __init__(self):
        pygame.init()
        self.isrunning = True
        self.gamedisplay = None
        self.gameworld = None
        self.size = Game.display_width, Game.display_height
        self.name = Game.gamename
        self.img = Game.gameimg

    def on_init(self):
        self.gamedisplay = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        GameWorld.Gameworld.gameDisplay = self.gamedisplay
        pygame.display.set_caption(self.name)
        pygame.display.set_icon(self.img)
        self.clock = pygame.time.Clock()
        self.score = Score.Score()
        self.gameworld = GameWorld.Gameworld(self.score)
        self.UI = UI.UI(self.score, (self.display_width, self.display_height))
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isrunning = False
        elif event.type == pygame.KEYDOWN:
            self.gameworld.handle_input(event)

    def on_loop(self):
        self.gameworld.loop()

    def on_render(self):
        self.gamedisplay.fill(self.color_black)
        self.gameworld.render()
        self.UI.render_score(self.score_offset)
        self.UI.render_UI()
        pygame.display.update()
        self.clock.tick(60)

    def on_cleanup(self):
        pygame.display.update()
        pygame.quit()

    def execute(self):
        if self.on_init() == False:
            self.isrunning = False

        while( self.isrunning ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


theGame = Game()
theGame.execute()