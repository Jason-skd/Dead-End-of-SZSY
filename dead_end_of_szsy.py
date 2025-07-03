import sys, random, math, time

import pygame

from settings import Settings
import heroes
import enemies
from bullet import Bullet

class DeadEndOfSZSY:
    """DeadEndOfSZSY游戏的主进程"""

    def __init__(self):
        """初始化游戏"""
        pygame.init()

        # 禁用中文输入
        pygame.key.stop_text_input()

        self.settings = Settings()

        # 设定背景和窗口名称
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("实验的末路")

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

        # 计算发射子弹的帧管理
        self.bullet_counter = self.settings.bullet_fire_blanking

    def run_game(self):
        """开始运行游戏"""
        self.init_main_game()
        self._main_game(1)

    def init_main_game(self):
        """初始化游戏"""
        self.hero.center_hero()

    def _main_game(self, chap):
        """游戏主体部分"""
        if chap == 1:
            self.settings.chap_1()

        # 产生小怪
        self._prod_simple_enemies(self.settings.simple_enemy_number)

        while True:
            # 游戏交互循环
            # 实例化时钟
            self.clock.tick(60)
            self.hero.update()
            self._update_simple_enemies()
            self._bullet_launcher()
            self._update_bullet()

            self._check_events()
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

    def _prod_simple_enemies(self, number):
        """产生number个simple_enemy"""
        for i in range(self.settings.simple_enemy_number):
            enemy_x = random.randint(0, self.screen_rect.right)
            enemy_y = random.randint(0, self.screen_rect.bottom)
            enemy = enemies.SimpleEnemy(self, enemy_x, enemy_y)
            self.simple_enemies.add(enemy)

    def _update_simple_enemies(self):
        """刷新simple_enemy的移动行为"""
        for enemy in self.simple_enemies:
            enemy.update(self.hero)

    def _prod_bullet(self):
        """产生1个bullet"""
        # 实例化new_bullet
        new_bullet = Bullet(self)

        # 初始化min_distance为正无穷, closest_enemy
        min_distance = float('inf')
        min_x = float('inf')
        min_y = float('inf')
        closest_enemy = None
        for enemy in self.simple_enemies:
            dx = enemy.rect.centerx - self.hero.rect.centerx
            dy = enemy.rect.centery - self.hero.rect.centery
            current_distance = math.sqrt(dx * dx + dy * dy)
            if current_distance < min_distance:
                min_distance = current_distance
                min_x = dx
                min_y = dy
                closest_enemy = enemy

        # 标准化最小距离的方向向量并乘以速度
        # 标准化方向向量并乘以速度
        if min_distance > 0:  # 避免除以零
            min_x = min_x / min_distance * self.settings.bullet_speed
            min_y = min_y / min_distance * self.settings.bullet_speed

        # 修改new_bullet的攻击方向
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

    def _update_screen(self):
        """管理刷新屏幕"""
        # 用纯色填充背景
        self.screen.blit(self.bg, self.screen_rect)
        self.hero.blitme()
        for enemy in self.simple_enemies:
            enemy.draw_enemy()
        for bullet in self.bullets:
            bullet.draw_bullet()


        # 刷新屏幕
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    deos = DeadEndOfSZSY()
    deos.run_game()
