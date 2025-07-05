import math, random

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

        #在0, 0处加载图片，随机选择一张，再放到指定位置
        image_1 = pygame.image.load(self.settings.sp_1)
        image_2 = pygame.image.load(self.settings.sp_2)
        image_3 = pygame.image.load(self.settings.sp_3)
        image_4 = pygame.image.load(self.settings.sp_4)

        images_choice = [image_1, image_2, image_3, image_4]
        self.image = images_choice[random.randint(0,3)]
        self.image = pygame.transform.scale(self.image, (self.width, self.width))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        self.speed = self.settings.simple_enemy_speed

        # 存储浮点数位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

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
        self.screen.blit(self.image, self.rect)

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
            self.x += dx  # 更新浮点数坐标
            self.y += dy
            self.rect.x = int(self.x)  # 取整赋值给 rect
            self.rect.y = int(self.y)

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

        self.width = self.settings.gh_width
        self.height = self.settings.gh_height

        # 加载图片并缩放
        self.image = pygame.image.load(self.settings.gh_image)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

        # 伤害
        self.hurt_value = self.settings.gh_harm

        # 伤害冷却
        self.hurt_blank = self.settings.gh_hurt_blank * 60

        self.speed = self.settings.gh_speed

        # 初始化技能
        self.carrots = pygame.sprite.Group()
        self.carrot_nor_image = pygame.image.load(self.settings.carrot_nor)
        self.carrot_nor_image = pygame.transform.scale(self.carrot_nor_image,
                                                     (self.settings.carrot_width, self.settings.carrot_width))
        self.carrot_prep_image = pygame.image.load(self.settings.carrot_prep)
        self.carrot_prep_image = pygame.transform.scale(self.carrot_prep_image,
                                                      (self.settings.carrot_width, self.settings.carrot_width))

    def carrot(self, number, speed):
        """gh技能：拔出萝卜带出泥"""

        # 计算弧度
        for order in range(number):
            degree = 360 / number * order
            degree = math.radians(degree)

            sin = math.sin(degree)
            cos = math.cos(degree)

            # 分解速度
            dx = speed * sin
            dy = speed * cos

            current_carrot = self.Carrot(self.deos_game, self, dx, dy, self.carrot_nor_image, self.carrot_prep_image)
            self.carrots.add(current_carrot)

    class Carrot(pygame.sprite.Sprite):
        """拔出萝卜带出泥的萝卜"""
        def __init__(self, deos_game, user, dx, dy, nor_image, prep_image):
            """初始化萝卜"""
            super().__init__()
            self.deos_game = deos_game
            self.screen = deos_game.screen
            self.settings = deos_game.settings
            self.user = user

            # 每秒要移动的距离
            self.dx = dx
            self.dy = dy

            self.width  = self.settings.carrot_width

            self.nor_image = nor_image
            self.prep_image = prep_image

            # 初始状态是nor
            self.image = self.nor_image
            self.rect = self.image.get_rect(center=(user.rect.x, user.rect.y))
            # 储存浮点坐标
            self.x = float(self.rect.x)
            self.y = float(self.rect.y)

            # 飞行帧数
            self.flying_duration = self.settings.carrot_flying_duration * 60

            # 初始化计时
            self.tick = 0

            # 胡萝卜命中计时
            self.carrot_hit_tik = 0
            self.hit = False

        def update(self):
            if self.tick < self.flying_duration:
                self.tick += 1
                self.x += self.dx  # 更新浮点数坐标
                self.y += self.dy
                self.rect.x = int(self.x)  # 取整赋值给 rect
                self.rect.y = int(self.y)

            else:
                if self.image != self.prep_image:
                    self.image = self.prep_image
            if self.hit:
                self.dominate_duration_manage()

        def dominate_duration_manage(self):
            if self.carrot_hit_tik >= self.settings.carrot_dominate * 60:
                self.deos_game.hero.move_can = True
                # 重置计时
                self.carrot_hit_tik = 0
                # 恢复gh速度
                self.user.speed /= self.settings.car_speed_up
                self.user.carrots.remove(self)
            else:
                self.carrot_hit_tik += 1

        def draw_carrot(self):
            """在屏幕上绘制carrot"""
            self.screen.blit(self.image, self.rect)

    def draw_enemy(self):
        """在屏幕上绘制gh和技能"""
        self.screen.blit(self.image, self.rect)

        # 绘制技能
        for carrot in self.carrots:
            carrot.draw_carrot()

    def update(self, target):
        super().update(target)

        # 技能刷新
        for carrot in self.carrots:
            carrot.update()

