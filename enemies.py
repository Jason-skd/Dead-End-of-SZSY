import math

import pygame

class SimpleEnemy(pygame.sprite.Sprite):
    """管理SimpleEnemy的类"""

    def __init__(self, deos_game, pos_x, pos_y):
        """初始化SimpleEnemy"""
        super().__init__()

        self.screen = deos_game.screen
        # self.screen_rect = deos_game.screen.get_rect()

        self.settings = deos_game.settings

        self.width = self.settings.simple_enemy_width
        self.color = self.settings.simple_enemy_color

        #在0, 0处添加一个simpl_enemy，再放到指定pos
        self.rect = pygame.Rect(0, 0, self.width, self.width, )
        self.rect.center = (pos_x, pos_y)

        self.speed = self.settings.simple_enemy_speed

    def draw_enemy(self):
        """在屏幕上绘制simple_enemy"""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self, target):
        """向hero移动"""
        # 计算方向向量
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        # 标准化方向向量并乘以速度
        if distance > 0:  # 避免除以零
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed

        # 更新位置
        self.rect.x += dx
        self.rect.y += dy
