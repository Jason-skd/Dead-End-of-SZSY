import math

import pygame

class SimpleEnemy(pygame.sprite.Sprite):
    """管理SimpleEnemy的类"""

    def __init__(self, deos_game, pos_x, pos_y):
        """初始化SimpleEnemy"""
        super().__init__()

        self.deos_game = deos_game

        self.screen = deos_game.screen
        # self.screen_rect = deos_game.screen.get_rect()

        self.settings = deos_game.settings

        self.width = self.settings.simple_enemy_width
        self.color = self.settings.simple_enemy_color

        #在0, 0处添加一个simpl_enemy，再放到指定pos
        self.rect = pygame.Rect(0, 0, self.width, self.width, )
        self.rect.center = (pos_x, pos_y)

        self.speed = self.settings.simple_enemy_speed

        # 移动标志，不处于攻击状态：移动
        self.moving = True
        self.hero = deos_game.hero

        # 伤害
        self.hurt_value = self.settings.simple_enemy_harm

        # 伤害冷却
        self.hurt_blank = self.settings.simple_enemy_hurt_blank * 60
        # 现在是造成伤害后counter秒，一开始冷却转好
        self.hurt_counter = self.hurt_blank

    def draw_enemy(self):
        """在屏幕上绘制simple_enemy"""
        pygame.draw.rect(self.screen, self.color, self.rect)

    def update(self, target):
        """更新状态"""
        self._update_moving(target)
        self._manage_hurt()

    def _update_moving(self, target):
        """向hero移动"""
        # 计算方向向量
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        # 标准化方向向量并乘以速度
        if distance > 0:  # 避免除以零
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed

        # 如果不在攻击：更新位置
        if self.moving:
            self.rect.x += dx
            self.rect.y += dy

    def _manage_hurt(self):
        """通过帧管理攻击冷却读秒"""
        # 如果造成伤害在冷却，冷却读秒
        if self.hurt_counter <= self.hurt_blank:
            self.hurt_counter += 1

        if pygame.sprite.collide_rect(self, self.hero):
            # 如果simple_enemy正在攻击，停止运动，尝试造成伤害
            self.moving = False
            self._try_hurt()
        else:
            self.moving = True

    def _try_hurt(self):
        """当测试为冷却读秒达到设定的冷却，造成伤害"""
        if self.hurt_counter >= self.hurt_blank:
            self.hurt()
            self.hurt_counter = 0


    def hurt(self):
        """造成伤害"""
        self.deos_game.hero_hurt += self.hurt_value


class Gh(SimpleEnemy):
    """管理gh的类"""
    def __init__(self, deos_game, pos_x, pos_y):
        """重新初始化gh"""
        super().__init__(deos_game, pos_x, pos_y)
        self.deos_game = deos_game

        # 加载图片并缩放
        self.image = pygame.image.load(self.settings.gh_image)
        self.image = pygame.transform.scale(self.image, (self.settings.gh_width, self.settings.gh_height))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        # 伤害
        self.hurt_value = self.settings.gh_harm

        # 伤害冷却
        self.hurt_blank = self.settings.gh_hurt_blank * 60

        self.speed = self.settings.gh_speed

        self.rect.center = (pos_x, pos_y)  # 添加这行设置位置

    def draw_enemy(self):
        """在屏幕上绘制simple_enemy"""
        self.screen.blit(self.image, self.rect)

    def update(self, target):
        super().update(target)  # 调用父类的移动逻辑
        print(f"Gh rect: {self.rect.x}, {self.rect.y}")  # 调试位置
