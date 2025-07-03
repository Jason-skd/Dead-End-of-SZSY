import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """管理子弹"""

    def __init__(self, deos_game):
        """在飞船的当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = deos_game.screen
        self.settings = deos_game.settings
        self.color = self.settings.bullet_color
        self.radius = self.settings.bullet_radius

        # 在0，0处设置一个子弹rect，再设置正确位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_radius * 2, self.settings.bullet_radius * 2)
        self.rect.center = deos_game.hero.rect.center

        # 初始化子弹的方向
        self.direction = (0, 0)

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.radius)

    def update(self):
        """向距离最近的enemy移动"""
        self.rect.x += self.direction[0]
        self.rect.y += self.direction[1]
