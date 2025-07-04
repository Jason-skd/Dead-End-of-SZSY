import sys, random, math
import pygame
from settings import Settings
import heroes
import enemies
from bullet import Bullet
from blood_bar import BloodBar
from button import Button


class DeadEndOfSZSY:
    """DeadEndOfSZSY游戏的主进程"""

    def __init__(self):
        """初始化游戏"""
        pygame.init()
        pygame.key.stop_text_input()
        self.settings = Settings()
        pygame.display.set_caption("实验的末路")
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()

    def run_game(self):
        """主游戏循环，管理章节切换"""
        while True:
            # 显示欢迎界面
            if not self.Welcome(self).run():
                break

            # 第一章
            with self.GameSession(self, 1) as game:
                result = game.host_game()
                if result == "Defeat":
                    if not self.Defeat(self).run():  # 显示失败界面
                        break
                    continue  # 重新开始第一章
                elif result == "Victory":
                    if not self.NextChapt(self).run():
                        pass

            with self.GameSession(self, 2) as game:
                result = game.host_game()
                if result == "Defeat":
                    if not self.Defeat(self).run():
                        break
                    continue  # 重新开始第二章
                elif result == "Victory":
                    # 可以在这里添加通关界面
                    if not self.NextChapt(self).run():
                        pass

            with self.GameSession(self, 3) as game:
                result = game.host_game()
                if result == "Defeat":
                    # gh跳脸
                    if game.game_instance.head_exist:
                        game.game_instance.jump_face = True
                elif result == "Victory":
                    # 可以在这里添加通关界面
                    break


    class GameSession:
        """使用上下文管理器管理游戏资源"""

        def __init__(self, deos_game, chap):
            self.deos_game = deos_game
            self.chap = chap
            self.game_instance = None

        def __enter__(self):
            """进入游戏会话时初始化游戏"""
            self.game_instance = self.deos_game.MainGame(self.deos_game, self.chap)
            return self.game_instance

        def __exit__(self, exc_type, exc_val, exc_tb):
            """退出时彻底清理资源"""
            if self.game_instance:
                pygame.mixer.music.stop()
                self.game_instance.bullets.empty()
                self.game_instance.simple_enemies.empty()
                self.game_instance.enemies_for_target.empty()
                # 重置游戏状态（避免章节间污染）
                self.deos_game.hero_blood = self.deos_game.settings.sgzy_blood
                self.deos_game.hero_hurt = 0
            return False  # 不抑制异常

    class Welcome:
        """掌管欢迎界面的类"""
        def __init__(self, deos_game):
            """引入并初始化"""
            self.screen = deos_game.screen
            self.screen_rect = deos_game.screen_rect
            self.settings = deos_game.settings
            self.play_clicked = False  # 新增：标记是否点击了Play按钮

        def run(self):
            """运行欢迎界面，返回是否点击了Play按钮"""
            while not self.play_clicked:  # 修改：条件变为检查play_clicked
                self.create_play_button()
                self._check_events()
                self._update_screen()
            return True  # 点击Play后返回True

        def create_play_button(self):
            self.play_button = Button(self, self.settings.play_button_width,
                                      self.settings.play_button_height,
                                      self.settings.play_button_x,
                                      self.settings.play_button_y,
                                      self.settings.play_button_color,
                                      self.settings.play_color,
                                      self.settings.play_font,
                                      self.settings.play_size, "Play")

        def _check_events(self):
            """响应输入指令"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)

        def _check_play_button(self, mouse_pos):
            """检查是否点击了Play按钮"""
            if self.play_button.rect.collidepoint(mouse_pos):
                self.play_clicked = True  # 修改：标记为已点击

        def _update_screen(self):
            self.screen.fill((0, 0, 0))
            self.play_button.draw_button()

            # 让最近绘制的屏幕可见
            pygame.display.flip()

    class Defeat(Welcome):
        """掌管失败界面的类"""
        def __init__(self, deos_game):
            """初始化与欢迎界面完全一致"""
            super().__init__(deos_game)
            self.deos_game = deos_game

        def create_play_button(self):
            """重写play_button为try_again"""
            self.play_button = Button(self, self.settings.play_button_width,
                                      self.settings.play_button_height,
                                      self.settings.play_button_x,
                                      self.settings.play_button_y,
                                      self.settings.play_button_color,
                                      self.settings.play_color,
                                      self.settings.play_font,
                                      self.settings.play_size, "Try Again")

    class NextChapt(Welcome):
        """掌管下一章节界面的类"""
        def __init__(self, deos_game):
            """初始化与欢迎界面完全一致"""
            super().__init__(deos_game)
            self.deos_game = deos_game

        def create_play_button(self):
            """重写play_button为try_again"""
            self.play_button = Button(self, self.settings.play_button_width,
                                      self.settings.play_button_height,
                                      self.settings.play_button_x,
                                      self.settings.play_button_y,
                                      self.settings.play_button_color,
                                      self.settings.play_color,
                                      self.settings.play_font,
                                      self.settings.play_size, "Next Chapter")


    class MainGame:
        """游戏主逻辑"""

        def __init__(self, deos_game, chap):
            """初始化游戏"""
            self.deos_game = deos_game
            self.settings = deos_game.settings
            self.screen = deos_game.screen
            self.screen_rect = deos_game.screen_rect

            if chap == 1:
                self.settings.chap_1()
            elif chap == 2:
                self.settings.chap_2()
            elif chap == 3:
                self.settings.chap_3()
            self.head_name = self.settings.chap_head


            # 加载资源
            pygame.mixer.music.load(self.settings.bgm)
            pygame.mixer.music.set_volume(self.settings.bgm_volume)
            pygame.mixer.music.play(-1)
            self.hit_sound = pygame.mixer.Sound('bgm/hurt.wav')
            self.died_sound = pygame.mixer.Sound('bgm/die.wav')
            self.fire_sound = pygame.mixer.Sound('bgm/fire.mp3')
            self.fire_sound.set_volume(0.3)
            self.bg = pygame.image.load(self.settings.bg_image)

            # 初始化游戏对象
            self.hero = heroes.Sgzy(self)
            self.simple_enemies = pygame.sprite.Group()
            self.bullets = pygame.sprite.Group()
            self.enemies_for_target = pygame.sprite.Group()
            self.clock = pygame.time.Clock()

            # 初始化游戏状态
            self.bullet_counter = self.settings.bullet_fire_blanking
            self.hurt_counter = 0
            self.hurt_count_start = False
            self.hero_blood_max = self.settings.sgzy_blood
            self.hero_blood = self.hero_blood_max
            self.hero_hurt = 0
            self.hero_blood_bar = BloodBar(self, self.hero, self.hero_blood_max, self.settings.blood_bar_width)
            self.hero.center_hero()

            self.head_exist = False
            # 跳脸
            self.jump_face = False

        def host_game(self):
            """游戏主循环，返回 'Victory' 或 'Defeat'"""
            self.prod_sp_enemy_waves = self.ManageSimpleEnemyWaves(
                self, self.settings.simple_enemy_wave,
                self.settings.simple_enemy_prod_blank,
                self.settings.simple_enemy_number)

            running = True
            while running:
                self.clock.tick(60)
                self._check_events()

                # 游戏逻辑更新
                self.prod_sp_enemy_waves.check_prod()
                self.hero.update()
                self._update_simple_enemies()
                self._bullet_launcher()
                self._update_bullet()
                self.hero_blood_bar.update()
                self._hero_hurt_animation()
                if self.head_exist:
                    self.gh.update(self.hero)
                    self._check_bullet_head_collisions()
                    self.gh_blood_bar.update()
                    self.head_hurt_manage()
                    self.gh_skill_manage.check_prod()


                # 检查游戏状态
                game_status = self.hurt_manage()
                if game_status == "Defeat":
                    self.died_sound.play()
                    return "Defeat"
                elif self._check_victory():  # 新增：检查是否胜利
                    return "Victory"

                self._update_screen()
            return "Quit"  # 如果主动退出

        def _check_victory(self):
            """检查是否胜利（击败所有敌人）"""
            if not self.enemies_for_target:
                return True
            return False

        def hurt_manage(self):
            """血量管理"""
            if self.hero_blood > 0:
                if self.hero_hurt > 0:
                    self.hero_blood -= self.hero_hurt
                    self.hit_sound.play()
                self.hero_hurt = 0
            else:
                return "Defeat"
            return None

        def head_hurt_manage(self):
            """头目的血量管理"""
            if self.gh_blood > 0:
                self.gh_blood -= self.gh_hurt
                self.gh_hurt = 0
            return None

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
                # 将该敌人加入攻击目标
                self.enemies_for_target.add(enemy)

        def prod_head(self):
            """产生头目"""
            if self.head_name == 'gh':
                self.gh = enemies.Gh(self, 960, 540)
                self.enemies_for_target.add(self.gh)

                # 血条与伤害
                self.gh_blood = self.settings.gh_blood
                self.gh_blood_bar = BloodBar(self, self.gh, self.gh_blood, self.settings.gh_blood_bar_width)
                self.gh_blood_bar.color = self.settings.gh_blood_bar_color
                self.gh_hurt = 0

                self.gh_group = pygame.sprite.Group()
                self.gh_group.add(self.gh)

                # 技能
                self.gh_skill_manage = self.HeadSkillManage(self, self.settings.gh_skill_blank)

            self.head_exist = True

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

                else:
                    if not self.deos_game.head_exist and self.deos_game.head_name:
                        self.deos_game.prod_head()

        class HeadSkillManage(ManageSimpleEnemyWaves):
            """计算头目技能时机"""
            def __init__(self, deos_game, blank):
                """初始化计数"""
                super().__init__(deos_game, 0, blank, 0)

                # 上次的技能序号，不与本次相同
                self.last_skill = 0
                self.current_skill = 0

            def check_prod(self):
                """计时器"""
                if self.current_blank >= self.blank:
                    self.prod_skill()
                    self.current_blank = 0
                else:
                    self.current_blank += 1

            def prod_skill(self):
                """随机产生技能"""
                while self.current_skill != self.last_skill:
                    self.current_skill = random.randint(1, 2)  # 有几种技能

                if self.current_skill == 1:
                    pass
                elif self.current_skill == 2:
                    pass


        def _update_simple_enemies(self):
            """刷新simple_enemy的移动行为"""
            for enemy in self.enemies_for_target:
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
            for enemy in self.enemies_for_target:
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
            if self.bullet_counter >= self.settings.bullet_fire_blanking * 60 and self.enemies_for_target:  # 假设60FPS
                self._prod_bullet()
                self.fire_sound.play()
                self.bullet_counter = 0

        def _check_bullet_simple_enemy_collisions(self):
            """检查是否有子弹击中了simple_enemy"""
            collisions = pygame.sprite.groupcollide(self.bullets, self.simple_enemies, True, True)

        def _check_bullet_head_collisions(self):
            """检查子弹命中头目"""
            collisions = pygame.sprite.groupcollide(self.bullets, self.gh_group, True, False)
            if collisions:
                self.gh_hurt += 1
                collisions = None

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

        def _update_screen(self):
            """绘制屏幕"""
            # 用纯色填充背景
            self.screen.blit(self.bg, self.screen_rect)
            for bullet in self.bullets:
                bullet.draw_bullet()
            self.hero.blitme()
            for enemy in self.simple_enemies:
                enemy.draw_enemy()
            self.hero_blood_bar.draw_blood_blank()
            self.hero_blood_bar.draw_blood_bar(self.hero_blood)

            if self.head_exist:
                self.gh.draw_enemy()
                self.gh_blood_bar.draw_blood_blank()
                self.gh_blood_bar.draw_blood_bar(self.gh_blood)

            # 刷新屏幕
            pygame.display.flip()


if __name__ == '__main__':
    deos = DeadEndOfSZSY()
    deos.run_game()