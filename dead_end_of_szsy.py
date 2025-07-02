import sys

import pygame

from settings import Settings
import heroes

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
        pygame.display.set_caption("实验的末路")

        # 设定bgm
        pygame.mixer.music.load(self.settings.bgm)
        pygame.mixer.music.play(-1)

        # 设定hero
        self.hero = heroes.Sgzy(self)

        # 设置时钟
        self.clock = pygame.time.Clock()

    def run_game(self):
        """开始运行游戏"""
        self.init_main_game()
        self._main_game()

    def init_main_game(self):
        """初始化游戏"""
        self.hero.center_hero()

    def _main_game(self):
        """游戏主体部分"""
        while True:
            # 实例化时钟
            self.clock.tick(60)
            self.hero.update()

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

    def _update_screen(self):
        """管理刷新屏幕"""
        # 用纯色填充背景
        self.screen.fill(self.settings.bg_color)
        self.hero.blitme()


        # 刷新屏幕
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    deos = DeadEndOfSZSY()
    deos.run_game()
