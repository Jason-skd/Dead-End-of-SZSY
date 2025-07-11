import pygame

class Sgzy(pygame.sprite.Sprite):
    """管理 Sgzy的类"""

    def __init__(self, deos_game):
        """初始化Sgzy"""
        super().__init__()
        self.screen = deos_game.screen
        self.screen_rect = deos_game.screen.get_rect()

        self.settings = deos_game.settings

        self.width = self.settings.heroes_width
        self.height = self.settings.heroes_height


        # 加载图片
        self.load_normal_img = pygame.image.load(self.settings.sgzy_normal_image)
        self.load_hurt_img = pygame.image.load(self.settings.sgzy_hurt_image)

        # 缩放图片，获取rect
        self.normal_image = pygame.transform.scale(self.load_normal_img,
                                                   (self.settings.heroes_width, self.settings.heroes_height))
        self.rect = self.normal_image.get_rect()

        self.hurt_image = pygame.transform.scale(self.load_hurt_img,
                                                   (self.settings.heroes_width, self.settings.heroes_height))

        self.image = self.normal_image

        self.move_can = True

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.speed = self.settings.heroes_speed

        # hurt标志
        self.hurt = False

    def center_hero(self):
        """将hero初始化，放在屏幕正中央"""
        self.rect.center = self.screen_rect.center

    def blitme(self):
        """在指定位置绘制self"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """刷新sgzy的状态"""
        if self.move_can:
            if self.moving_right and self.rect.right + self.width < self.screen_rect.right:
                self.rect.x += self.speed
            if self.moving_left and self.rect.left - self.width > self.screen_rect.left:
                self.rect.x -= self.speed
            if (self.moving_up and self.rect.top -
                    (self.height + self.settings.blood_bar_height + self.settings.blood_bar_pos_height)
                    > self.screen_rect.top):
                self.rect.y -= self.speed
            if self.moving_down and self.rect.bottom + self.height < self.screen_rect.bottom:
                self.rect.y += self.speed

            if self.hurt:
                self.image = self.hurt_image
            else: self.image = self.normal_image
