import random

import pygame

class SimpleEnemy(pygame.sprite.Sprite):
    """管理SimpleEnemy的类"""

    def __init__(self, deos_game):
        """初始化SimpleEnemy"""
        super().__init__()

        self.screen = deos_game.screen
        # self.screen_rect = deos_game.screen.get_rect()

        self.settings = deos_game.settings

        self.width = self.settings.simple_enemy_width
        self.color = self.settings.simple_enemy_color

        #在0, 0处添加一个simpl_enemy
        self.rect = pygame.Rect(0, 0, self.width, self.width, )
        self.x, self.y = float(self.rect.x), float(self.rect.y)

    def draw_enemy(self):
        """在屏幕上绘制simple_enemy"""
        pygame.draw.rect(self.screen, self.color, self.rect)
