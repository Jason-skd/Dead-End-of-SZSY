import math, random

import pygame

import surface

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
        self.attack_moving = True
        self.hero = deos_game.hero

        # 除了普攻以外的移动控制
        self.other_moving = True

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
        if self.attack_moving and self.other_moving:
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)

            # 标准化方向向量并乘以速度
            if distance > 0:  # 避免除以零
                dx = dx / distance * self.speed
                dy = dy / distance * self.speed

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
            self.attack_moving = False
            self._try_hurt()
        else:
            self.attack_moving = True

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

        # 加载技能语音
        self.zaijia = pygame.mixer.Sound(self.settings.zaijia)
        self.chuchu = pygame.mixer.Sound(self.settings.chuchu)
        self.ganshen = pygame.mixer.Sound(self.settings.ganshen)
        self.bachu = pygame.mixer.Sound(self.settings.bachu)
        self.kange = pygame.mixer.Sound(self.settings.kange)
        self.zhonggu = pygame.mixer.Sound(self.settings.zhonggu)
        self.flash = pygame.mixer.Sound(self.settings.flash)
        self.hit_sound = pygame.mixer.Sound(self.settings.hit)

        self.ganshen.play()

        # 重骨架技能初始化
        self.skill_framework = False
        self.benzene = pygame.image.load(self.settings.benzene)
        self.benzene = pygame.transform.scale(self.benzene, (self.width, self.height))

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
            # noinspection PyTypeChecker
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
            # 控制帧数
            self.dominate_duration = self.settings.carrot_dominate_duration * 60
            self.lifespan = self.settings.carrot_lifespan * 60

            # 初始化计时
            self.tick = 0

            # 胡萝卜命中计时
            self.carrot_hit_tik = 0
            self.hit = False

            self.user.bachu.play()

        def update(self):
            """绘制屏幕"""
            self.tick += 1
            if self.tick < self.flying_duration:
                self._flying()
            else:
                # 扎根
                if self.image != self.prep_image:
                    self.image = self.prep_image
            if self.hit:
                self._dominate_duration_manage(self.rect.center)

            self._check_lifespan()

        def _flying(self):
            """萝卜飞行"""
            self.x += self.dx  # 更新浮点数坐标
            self.y += self.dy
            self.rect.x = int(self.x)  # 取整赋值给 rect
            self.rect.y = int(self.y)

        def _dominate_duration_manage(self, carrot_pos):
            """控制时长控制"""
            if self.carrot_hit_tik >= self.dominate_duration:
                self.deos_game.hero.move_can = True
                # 重置计时
                self.carrot_hit_tik = 0
                # 恢复gh速度
                self.user.carrots.remove(self)
            if self.carrot_hit_tik >= self.dominate_duration / 2:
                self.user.teleportation(carrot_pos)
            self.carrot_hit_tik += 1

        def _check_lifespan(self):
            """寿命控制"""
            if self.tick >= self.lifespan:
                self.user.carrots.remove(self)

        def draw_carrot(self):
            """在屏幕上绘制carrot"""
            self.screen.blit(self.image, self.rect)

    def teleportation(self, pos):
        """传送"""
        self.zaijia.play()
        self.rect.center = pos
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    class HiteVision:
        """技能：看个通知"""
        def __init__(self, deos_game, user):
            self.deos_game = deos_game
            self.screen = deos_game.screen
            self.screen_rect = deos_game.screen_rect
            self.settings = deos_game.settings
            self.user = user

            self.centerx = self.settings.board_centerx
            self.centery = self.settings.board_centery

            self.surface = surface.CreateSurface(deos_game, self.centerx, self.centery)
            self.surface.image_fill_surface(self.settings.hv_image,
                                            (self.settings.board_width,self.settings.board_height))

            self.lifespan = self.settings.hv_lifespan * 60
            self.hurt_blank = self.settings.hv_hurt_blank * 60
            self.counter = 0

            self.hurt = self.settings.hv_hurt

            self.user.kange.play()

        def check_life(self):
            """生命周期内blit，并实现其他效果"""
            self.counter += 1
            if self.counter <= self.lifespan:
                self.user.other_moving = False
                self._hurt()
            else:
                self.deos_game.hitevision_exist = False
                self.user.other_moving = True

        def _hurt(self):
            """产生伤害"""
            for count in range(0, self.lifespan):
                if self.counter == count * self.hurt_blank:
                    self.user.hit_sound.play()
                    # 清空小兵
                    for sp in self.deos_game.simple_enemies:
                        sp.kill()
                    self.deos_game.simple_enemies.empty()
                    if not pygame.sprite.collide_rect(self.deos_game.hero, self.surface):
                        # 伤害检查
                        self.deos_game.hero_hurt += self.hurt


        def blitme(self):
            """绘制屏幕"""
            self.surface.blitme()

    class SkillFramework:
        """发动技能 重骨架"""
        def __init__(self, deos_game, user):
            """初始化"""
            self.deos_game = deos_game
            self.settings = deos_game.settings
            self.user = user

            self.duration = self.settings.skill_f_duration * 60
            self.counter = 0

            # 技能效果
            # 广播给gh
            self.user.skill_framework = True

            # 加速
            self.speed_up = self.settings.frame_speed_up
            self.user.speed = self.settings.gh_speed * self.speed_up

            # 语音
            self.user.zhonggu.play()

            # 无法受到攻击
            deos_game.enemies_for_target.remove(user)

        def check_life(self):
            self.counter += 1
            if not self.counter <= self.duration:
                # 还原速度
                self.user.speed = self.settings.gh_speed
                # 可以受到攻击
                self.deos_game.enemies_for_target.add(self.user)
                # 广播
                self.user.skill_framework = False

    def draw_enemy(self):
        """在屏幕上绘制gh和技能"""
        if not self.skill_framework:
            # 如果没处于技能：重骨架状态中
            self.screen.blit(self.image, self.rect)
        else:
            self.screen.blit(self.benzene, self.rect)

        # 绘制技能
        for carrot in self.carrots:
            carrot.draw_carrot()

    def update(self, target):
        """绘制gh"""
        super().update(target)

        # 技能刷新
        for carrot in self.carrots:
            carrot.update()

