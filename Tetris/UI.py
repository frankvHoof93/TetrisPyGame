__author__ = 'Frank van Hoof'
import pygame, GameWorld, random

class UI:
    bg_img = None
    def __init__(self, score, display_size):
        self.score = score
        self.font = pygame.font.Font('freesansbold.ttf', 115)
        randomnr = random.randint(1,3)
        bgimg_name = 'Images/Backgrounds/bg' + str(randomnr) + '.png'
        self.bg_img = pygame.image.load(bgimg_name)
        self.display_size = display_size
        self.pause_img = pygame.image.load('Images/Pause.png')
        self.gameover_img = pygame.image.load('Images/gameover.png')
        self.gamestart_img = pygame.image.load('Images/gamestart.png')

    def text_objects(self, text, font):
        surface = font.render(text, True, (255,255,0))
        return surface, surface.get_rect()

    def render_score(self, score_offset):
        score_surface, score_rect = self.text_objects(str(self.score.score), self.font)
        score_rect.center = (score_offset[0] - score_surface.get_width() / 2, score_offset[1] - score_surface.get_height() / 2)
        GameWorld.Gameworld.gameDisplay.blit(score_surface, score_rect)

    def render_UI(self):
        GameWorld.Gameworld.gameDisplay.blit(self.bg_img, (0,0))
        if GameWorld.Gameworld.is_starting:
            GameWorld.Gameworld.gameDisplay.blit(self.gamestart_img, (self.display_size[0] * .25, self.display_size[1] * .25))
        if not GameWorld.Gameworld.is_starting and not GameWorld.Gameworld.is_playing:
            if GameWorld.Gameworld.is_alive:
                GameWorld.Gameworld.gameDisplay.blit(self.pause_img, (self.display_size[0] * .25, self.display_size[1] * .25))
            else:
                GameWorld.Gameworld.gameDisplay.blit(self.gameover_img, (self.display_size[0] * .25, self.display_size[1] * .25))
                self.render_score((self.display_size[0] * .5 + (len(str(self.score.score)) * 40), self.display_size[1] * .73))