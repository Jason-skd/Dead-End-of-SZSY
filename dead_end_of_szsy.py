import sys, random, math, time

import pygame

from settings import Settings
import heroes
import enemies
from bullet import Bullet
from blood_bar import BloodBar

class DeadEndOfSZSY:
    """DeadEndOfSZSY游戏的主进程"""

    def __init__(self):
        """初始化游戏"""
        pygame.init()

        # 禁用中文输入
        pygame.key.stop_text_input()

        self.settings = Settings()

        # 设定背景和窗口名称
        pygame.display.set_caption("实验的末路")
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()

    def run_game(self):
        """开始运行游戏"""
        self.Welcome(self)
        self.chapt_1 = self.MainGame(self, 1)

    class Welcome:
        """掌管欢迎界面的类"""
        def __init__(self, deos_game):
            """引入并初始化"""
            self.screen = deos_game.screen
            self.screen_rect = deos_game.screen_rect

        def create_play_button(self):
            pass

    class MainGame:
        """main_game模板"""
        def __init__(self, deos_game, chap):
            """初始化main_game，进行第chap关"""
            self.settings = deos_game.settings
            self.screen = deos_game.screen
            self.screen_rect = deos_game.screen_rect

            # 章节设置，将settings中的章节动态项变为chapter_1的设置
            if chap == 1:
                self.settings.chap_1()

            # 设定bgm
            pygame.mixer.music.load(self.settings.bgm)
            pygame.mixer.music.play(-1)

            # 设置背景
            self.bg = pygame.image.load(self.settings.bg_image)

            # 设定hero
            self.hero = heroes.Sgzy(self)

            # 创建管理simple_enemy的组
            self.simple_enemies = pygame.sprite.Group()

            # 创建管理bullets的组
            self.bullets = pygame.sprite.Group()

            # 设置时钟
            self.clock = pygame.time.Clock()

            # 创建帧管理
            self.bullet_counter = self.settings.bullet_fire_blanking
            # 变脸时间的帧管理
            self.hurt_counter = 0
            # 开始：不变脸
            self.hurt_count_start = False

            # 受伤管理 _max永不变
            self.hero_blood_max = self.settings.sgzy_blood
            self.hero_blood = self.hero_blood_max
            self.hero_hurt = 0

            # 实例化blood_bar（要先加载hero最大血量）
            self.blood_bar = BloodBar(self)

            self.hero.center_hero()

            # 初始化完成，举办游戏
            self.host_game()

        def host_game(self):
            """游戏主体部分"""
            # 初始化刷怪笼
            self.prod_sp_enemy_waves = self.ManageSimpleEnemyWaves(self, self.settings.simple_enemy_wave,
                                                                   self.settings.simple_enemy_prod_blank,
                                                                   self.settings.simple_enemy_number)

            # 游戏主循环
            while True:
                # 游戏交互循环
                # 实例化时钟
                self.clock.tick(60)
                # 响应输入
                self._check_events()

                # 刷新
                self.prod_sp_enemy_waves.check_prod()
                self.hero.update()
                self._update_simple_enemies()
                self._bullet_launcher()
                self._update_bullet()
                self.blood_bar.update()
                # 管理
                self._hero_hurt_animation()
                self.hurt_manage()

                self._update_screen()

        def _check_events(self):
            """响应输入"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

        def _check_keydown_events(self, event):
            """响应按键按下"""
            if event.key == pygame.K_d:
                self.hero.moving_right = True
            elif event.key == pygame.K_a:
                self.hero.moving_left = True
            elif event.key == pygame.K_w:
                self.hero.moving_up = True
            elif event.key == pygame.K_s:
                self.hero.moving_down = True

        def _check_keyup_events(self, event):
            """响应按键松开"""
            if event.key == pygame.K_d:
                self.hero.moving_right = False
            elif event.key == pygame.K_a:
                self.hero.moving_left = False
            elif event.key == pygame.K_w:
                self.hero.moving_up = False
            elif event.key == pygame.K_s:
                self.hero.moving_down = False

        def prod_simple_enemy_wave(self, number):
            """产生number个simple_enemy"""
            for i in range(number):
                enemy_x = random.randint(0, self.screen_rect.right)
                enemy_y = random.randint(0, self.screen_rect.bottom)
                enemy = enemies.SimpleEnemy(self, enemy_x, enemy_y)
                self.simple_enemies.add(enemy)

        class ManageSimpleEnemyWaves:
            """产生waves波怪，每波间隔blank秒，每波number个怪"""
            def __init__(self, deos_game, waves, blank, number):
                """初始化设定的间隔、当前间隔、当前波次"""
                self.deos_game = deos_game
                self.waves = waves
                self.number = number
                self.blank = blank * 60

                self.current_blank = self.blank
                self.current_waves = 0

            def check_prod(self):
                """判断是否继续添加波次，直到满足需求"""
                if self.current_waves < self.waves:
                    if self.current_blank >= self.blank:
                        self.deos_game.prod_simple_enemy_wave(self.number)
                        self.current_waves += 1
                        self.current_blank = 0
                    else:
                        self.current_blank += 1


        def _update_simple_enemies(self):
            """刷新simple_enemy的移动行为"""
            for enemy in self.simple_enemies:
                # 以hero为目标
                enemy.update(self.hero)

        def _prod_bullet(self):
            """产生1个bullet，并让它向敌人发射"""
            # 实例化new_bullet
            new_bullet = Bullet(self)

            # 计算攻击方向
            # 初始化min_distance为正无穷, closest_enemy
            min_distance = float('inf')
            min_x = float('inf')
            min_y = float('inf')
            for enemy in self.simple_enemies:
                dx = enemy.rect.centerx - self.hero.rect.centerx
                dy = enemy.rect.centery - self.hero.rect.centery
                current_distance = math.sqrt(dx * dx + dy * dy)
                if current_distance < min_distance:
                    min_distance = current_distance
                    min_x = dx
                    min_y = dy

            # 标准化最小距离的方向向量并乘以速度
            # 标准化方向向量并乘以速度
            if min_distance > 0:  # 避免除以零
                min_x = min_x / min_distance * self.settings.bullet_speed
                min_y = min_y / min_distance * self.settings.bullet_speed

            # 定义new_bullet的攻击方向
            new_bullet.direction = (min_x, min_y)

            # 加入Group
            self.bullets.add(new_bullet)

        def _update_bullet(self):
            """刷新bullet的移动行为并删除已消失的子弹"""
            for bullet in self.bullets:
                bullet.update()

            for bullet in self.bullets.copy():
                bullet_out = (bullet.rect.bottom <= 0 or bullet.rect.top >= self.screen_rect.bottom
                              or bullet.rect.left >= self.screen_rect.right or bullet.rect.right <= 0)
                if bullet_out:
                    self.bullets.remove(bullet)

            self._check_bullet_simple_enemy_collisions()

        def _bullet_launcher(self):
            """定时发射子弹"""
            self.bullet_counter += 1
            if self.bullet_counter >= self.settings.bullet_fire_blanking * 60 and self.simple_enemies:  # 假设60FPS
                self._prod_bullet()
                self.bullet_counter = 0

        def _check_bullet_simple_enemy_collisions(self):
            """检查是否有子弹击中了simple_enemy"""
            collisions = pygame.sprite.groupcollide(self.bullets, self.simple_enemies, True, True)

        def _hero_hurt_animation(self):
            """响应hero受到simple_enemy攻击"""
            # 如果变脸了，读秒
            if self.hurt_count_start:
                self.hurt_counter += 1
            # 如果受击了，变脸
            if pygame.sprite.spritecollideany(self.hero, self.simple_enemies):
                self.hero.hurt = True
                # 重置并开始读秒
                self.hurt_counter = 0
                self.hurt_count_start = True
            # 如果读秒满了，变脸变回
            if self.hurt_counter == self.settings.hurt_time * 60:
                self.hero.hurt = False
                self.hurt_count_start = False

        def hurt_manage(self):
            """负责扣血"""
            self.hero_blood -= self.hero_hurt
            # 重置受伤
            self.hero_hurt = 0

        def _update_screen(self):
            """绘制屏幕"""
            # 用纯色填充背景
            self.screen.blit(self.bg, self.screen_rect)
            for bullet in self.bullets:
                bullet.draw_bullet()
            self.hero.blitme()
            for enemy in self.simple_enemies:
                enemy.draw_enemy()
            self.blood_bar.draw_blood_blank()
            self.blood_bar.draw_blood_bar()


            # 刷新屏幕
            pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    deos = DeadEndOfSZSY()
    deos.run_game()
