import sys, random, math
import pygame
from settings import Settings
import heroes
import enemies
from bullet import Bullet
from blood_bar import BloodBar
from button import Button
from surface import CreateSurface

class DeadEndOfSZSY:
    """DeadEndOfSZSY游戏的主进程"""

    def __init__(self):
        """创建游戏地基"""
        pygame.init()
        # 停用中文输入
        pygame.key.stop_text_input()
        self.settings = Settings()
        pygame.display.set_caption("实验的末路")
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen_rect = self.screen.get_rect()

    def run_game(self):
        """主游戏循环，管理章节切换"""
        # 直到点击才不检测play按钮
        while not self.Welcome(self).run():
            break

        while True:
            # noinspection PyUnresolvedReferences
            with self.GameSession(self, 1) as game:
                result = game.host_game()
                if result == "Defeat":
                    # 直到点击才重新开始本章
                    while self.Defeat(self, '1').run():
                        break
                    continue
                elif result == "Victory":
                    # 直到点击才开始下一章
                    while self.NextChapt(self, "2").run():
                        break
                    break

        while True:
            with self.GameSession(self, 2) as game:
                result = game.host_game()
                if result == "Defeat":
                    # 跳脸
                    jf = self.GhJumpFace(self)
                    jf.run()
                    # 直到点击才重新开始本章
                    while self.Defeat(self, '2').run():
                        break
                    # 重新开始本章游戏
                    continue
                elif result == "Victory":
                    # 直到点击才开始下一章
                    while True:
                        self.Winning(self).run()

    class GameSession:
        """使用上下文管理器管理游戏资源"""

        def __init__(self, main_game, chap):
            """传入游戏地基"""
            self.deos_game = main_game
            self.chap = chap
            # 游戏实例初始化
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
                # self.deos_game.hero_hurt = 0
            return False  # 不抑制异常

    class Interface:
        """掌管欢迎界面的类"""
        def __init__(self, deos_game):
            """引入并初始化"""
            self.screen = deos_game.screen
            self.screen_rect = deos_game.screen_rect
            self.settings = deos_game.settings
            self.bg = pygame.image.load(self.settings.interface_bg)
            # 标记按钮是否被点击
            self.play_clicked = False

        def run(self):
            """运行欢迎界面，点击了button返回True"""
            while not self.play_clicked:
                self._create_play_button()
                self._check_events()
                self._update_screen()
            return True

        def _create_play_button(self):
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
                self.play_clicked = True

        def _update_screen(self):
            """绘制屏幕"""
            self.screen.blit(self.bg, self.screen_rect)
            self.play_button.draw_button()

            # 让最近绘制的屏幕可见
            pygame.display.flip()

    class Welcome(Interface):
        """欢迎界面"""
        def __init__(self, deos_game):
            """初始化"""
            super().__init__(deos_game)
            self.logo = CreateSurface(deos, self.screen_rect.centerx,
                                      self.screen_rect.centery + self.settings.logo_center_height)

        def run(self):
            """运行主循环"""
            while not self.play_clicked:
                self._create_play_button()
                self._create_logo()
                self._check_events()
                self._update_screen()
            return True
        def _create_logo(self):
            """加载logo"""
            self.logo.image_fill_surface(self.settings.logo, (self.settings.logo_width, self.settings.logo_height))

        def _update_screen(self):
            """绘制屏幕"""
            self.screen.blit(self.bg, self.screen_rect)
            self.play_button.draw_button()
            self.logo.blitme()

            # 让最近绘制的屏幕可见
            pygame.display.flip()

    class NextChapt(Interface):
        """掌管下一章节界面的类"""
        def __init__(self, deos_game, next_chap):
            """初始化与欢迎界面完全一致"""
            super().__init__(deos_game)
            self.deos_game = deos_game
            self.chapter_msg = CreateSurface(deos_game)
            self.next_chap = next_chap
            self.logo_2_path = self.settings.logo_2
            self.logo_2 = CreateSurface(deos_game, self.screen_rect.centerx, self.screen_rect.centery)

        def _create_play_button(self):
            """重写play_button为Enter!"""
            self.play_button = Button(self, self.settings.play_button_width,
                                      self.settings.play_button_height,
                                      self.settings.play_button_x,
                                      self.settings.play_button_y,
                                      self.settings.play_button_color,
                                      self.settings.play_color,
                                      self.settings.play_font,
                                      self.settings.play_size, "Enter!")

        def _create_next_chap_msg(self):
            """绘制下一章通知"""
            self.chapter_msg.text_fill_surface(70, f"Next: chapter. {self.next_chap}")
            self.chapter_msg.rect.top = self.screen_rect.top + self.settings.nx_chap_top_dist
            self.chapter_msg.rect.centerx = self.screen_rect.centerx

        def _crate_logo_2(self):
            """创造logo2"""
            self.logo_2.image_fill_surface(self.logo_2_path)

        def run(self):
            """点击按钮返回True"""
            while not self.play_clicked:
                self._create_play_button()
                self._create_next_chap_msg()
                self._crate_logo_2()
                self._check_events()
                self._update_screen()
            return True

        def _update_screen(self):
            """绘制屏幕"""
            self.screen.blit(self.bg, self.screen_rect)
            self.play_button.draw_button()
            self.chapter_msg.blitme()
            self.logo_2.blitme()

            # 让最近绘制的屏幕可见
            pygame.display.flip()

    class Defeat(NextChapt):
        """掌管失败界面的类"""

        def __init__(self, deos_game, current_chap):
            """初始化与欢迎界面完全一致"""
            super().__init__(deos_game, current_chap)

        def _create_play_button(self):
            """重写play_button为try_again"""
            self.play_button = Button(self, self.settings.try_again_width,
                                      self.settings.play_button_height,
                                      self.settings.play_button_x,
                                      self.settings.play_button_y,
                                      self.settings.play_button_color,
                                      self.settings.play_color,
                                      self.settings.play_font,
                                      self.settings.play_size, "Try Again")

        def _create_next_chap_msg(self):
            """绘制本章章通知"""
            self.chapter_msg.text_fill_surface(70, f"chapter. {self.next_chap}")
            self.chapter_msg.rect.top = self.screen_rect.top + self.settings.nx_chap_top_dist
            self.chapter_msg.rect.centerx = self.screen_rect.centerx

    class Winning(Interface):
        def __init__(self, deos_game):
            super().__init__(deos_game)
            self.con_path = self.settings.congratulations
            self.con_surface = CreateSurface(deos_game, self.screen_rect.centerx, self.screen_rect.centery)
            self.sound = pygame.mixer.Sound(self.settings.winning_sound)
            self.sound.play()

        def _create_congratulations(self):
            self.con_surface.image_fill_surface(self.con_path)

        def _check_events(self):
            """响应输入指令"""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

        def run(self):
            """运行欢迎界面，点击了button返回True"""
            while not self.play_clicked:
                self._check_events()
                self._create_congratulations()
                self._update_screen()
            return True

        def _update_screen(self):
            """绘制屏幕"""
            self.screen.blit(self.bg, self.screen_rect)
            self.con_surface.blitme()

            # 让最近绘制的屏幕可见
            pygame.display.flip()




    class GhJumpFace:
        """gh跳脸界面"""
        def __init__(self, game):
            self.screen = game.screen
            self.screen_rect = game.screen_rect
            self.settings = game.settings

            self.clock = pygame.time.Clock()

            self.small_surface = CreateSurface(game, self.screen_rect.centerx, self.screen_rect.centery)
            self.small_surface.image_fill_surface(self.settings.gh_face, (self.settings.jf_small_width,
                                                                          self.settings.jf_small_width))
            self.large_surface = CreateSurface(game, self.screen_rect.centerx, self.screen_rect.centery)
            self.large_surface.image_fill_surface(self.settings.gh_face, (self.settings.jf_large_width,
                                                                          self.settings.jf_large_width))

            self.jp_sound = pygame.mixer.Sound(self.settings.jump_face_sound)
            self.switch = False

            self.interval = self.settings.jp_interval * 60
            self.lifespan = self.settings.jf_lifespan * 60
            self.tik = 0

            # 结束跳脸界面标志
            self.end_life = False

        def _check_tik(self):
            """计时"""
            self.tik += 1
            if self.tik >= self.interval:
                self._switch_status()
            if self.tik >= self.lifespan:
                self.end_life = True

        def _switch_status(self):
            """突脸"""
            if not self.switch:
                self.jp_sound.play()
                self.switch = True

        def run(self):
            """运行主循环"""
            while not self.end_life:
                self.clock.tick(60)
                self._check_tik()
                self._update_screen()

        def _update_screen(self):
            """绘制屏幕"""
            self.screen.fill((0, 0, 0))
            if not self.switch:
                self.small_surface.blitme()
            else:
                self.large_surface.blitme()

            pygame.display.flip()


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

            # 初始化游戏变量
            self.bullet_counter = self.settings.bullet_fire_blanking
            self.hero_hurt = 0
            self.hurt_counter = 0
            self.hurt_count_start = False
            self.hero_blood_max = self.settings.sgzy_blood
            self.hero_blood = self.hero_blood_max
            self.prod_waves_complete = False
            self.prod_sp_enemy_waves = None
            self.head_exist = False
            self.head_prod = False
            self.prod_waves_complete = False
            self.complete_prod_inf_sp_waves = False

            # 初始化游戏对象
            self.clock = pygame.time.Clock()
            self.hero = heroes.Sgzy(self)
            self.hero_blood_bar = BloodBar(self, self.hero, self.hero_blood_max, self.settings.blood_bar_width)
            self.simple_enemies = pygame.sprite.Group()
            self.enemies_for_target = pygame.sprite.Group()
            self.bullets = pygame.sprite.Group()
            self.timers = []


            # 默认事件
            self.hero.center_hero()

        def host_game(self):
            """游戏主循环，返回 'Victory' 或 'Defeat'"""
            self.prod_sp_enemy_waves = self.ManageSimpleEnemyWaves(
                self, self.settings.simple_enemy_wave,
                self.settings.simple_enemy_prod_blank,
                self.settings.simple_enemy_number)

            while True:
                self.clock.tick(60)
                self._check_events()

                self._tik()
                self._update_object_status()

                # 检查游戏状态
                game_status = self.hurt_manage()
                if game_status == "Defeat":
                    self.died_sound.play()
                    return "Defeat"
                elif self._check_victory():  # 新增：检查是否胜利
                    return "Victory"

                self._update_screen()


        def _tik(self):
            """计时"""
            self.prod_waves_complete = self.prod_sp_enemy_waves.check_prod()
            if self.prod_waves_complete and self.complete_prod_inf_sp_waves is False:
                if self.settings.sp_inf:
                    self.prod_inf_sp_enemy_waves = self.ManageSimpleEnemyWaves(
                        self, self.settings.inf_simple_enemy_wave,
                        self.settings.inf_simple_enemy_prod_blank,
                        self.settings.inf_simple_enemy_number)
                    self.complete_prod_inf_sp_waves = True

            if self.complete_prod_inf_sp_waves:
                self.prod_inf_sp_enemy_waves.check_prod()

            if self.head_exist:
                # 如果不处于无敌状态
                if not self.head_invincible:
                    self._check_bullet_head_collisions()
                self.gh_skill_manage.check_prod()
                self._check_carrots_hero_collisions()
                if self.hitevision_exist:
                    self.hitevision.check_life()
                if self.gh.skill_framework:
                    self.skill_frame.check_life()


            return "Quit"  # 如果主动退出

        def _update_object_status(self):
            """更新对象状态"""
            self.hero.update()
            self._update_simple_enemies()
            self._bullet_launcher()
            self._update_bullet()
            self.hero_blood_bar.update()
            self._check_hero_hurt()
            if self.head_exist:
                self.gh.update(self.hero)
                self.gh_blood_bar.update()
                self.head_hurt_manage()

        def _check_victory(self):
            """检查是否胜利（击败所有敌人）"""
            if not self.enemies_for_target and self.prod_waves_complete and not self.head_exist:
                if self.settings.chap_head is None or self.head_prod:
                    pygame.mixer.music.stop()
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
            else:
                # noinspection PyTypeChecker
                self.enemies_for_target.empty()
                self.head_exist = False
                self.gh.kill()
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
                # noinspection PyTypeChecker
                self.simple_enemies.add(enemy)
                # 将该敌人加入攻击目标
                # noinspection PyTypeChecker
                self.enemies_for_target.add(enemy)

        def prod_head(self):
            """产生头目"""
            if self.head_name == 'gh':
                self.gh = enemies.Gh(self, 960, 540)
                # noinspection PyTypeChecker
                self.enemies_for_target.add(self.gh)

                # 血条与伤害
                self.gh_blood = self.settings.gh_blood
                self.gh_blood_bar = BloodBar(self, self.gh, self.gh_blood, self.settings.gh_blood_bar_width)
                self.gh_blood_bar.color = self.settings.gh_blood_bar_color
                self.gh_hurt = 0

                self.gh_group = pygame.sprite.Group()
                # noinspection PyTypeChecker
                self.gh_group.add(self.gh)

                # 技能计时
                self.gh_skill_manage = self.HeadSkillManage(self, self.settings.gh_skill_blank)
                # 初始化技能HiteVision
                self.hitevision = None
                self.hitevision_exist = False
                # 初始化技能重骨架
                self.skill_frame = None
                self.head_invincible = False

            self.head_exist = True
            self.head_prod = True

        class ManageSimpleEnemyWaves:
            """产生waves波怪，每波间隔blank秒，每波number个怪"""

            def __init__(self, deos_game, waves, blank, number):
                """初始化设定的间隔、当前间隔、当前波次"""
                self.deos_game = deos_game
                self.settings = deos_game.settings
                self.waves = waves
                self.number = number
                self.blank = blank * 60

                self.current_blank = self.blank / 2
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

                    # 未完成
                    return False

                else:
                    if not self.deos_game.head_prod and self.deos_game.head_name:
                        self.deos_game.prod_head()

                    # 完成，return True
                    return True

        class HeadSkillManage(ManageSimpleEnemyWaves):
            """计算头目技能时机"""
            def __init__(self, deos_game, blank):
                """初始化计数"""
                super().__init__(deos_game, 0, blank, 0)

                # 上次的技能序号，不与本次相同
                self.last_skill = 0
                self.current_skill = 0

                self.head = deos_game.gh

            def check_prod(self):
                """计时器"""
                if self.current_blank >= self.blank:
                    self.prod_skill()
                    self.current_blank = 0
                else:
                    self.current_blank += 1

            def prod_skill(self):
                """随机产生技能"""
                while self.current_skill == self.last_skill:
                    self.current_skill = random.randint(1, 3)  # 有几种技能

                if self.current_skill == 1:
                    # 从1到最大胡萝卜数量发射
                    self.head.carrot(random.randint(1, self.settings.carrot_numb)
                                             , self.settings.carrot_speed)
                elif self.current_skill == 2:
                    self.deos_game.hitevision = self.head.HiteVision(self.deos_game, self.head)
                    self.deos_game.hitevision_exist = True

                elif self.current_skill == 3:
                    self.deos_game.skill_frame = self.deos_game.gh.SkillFramework(self.deos_game, self.head)

                self.last_skill = self.current_skill



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
            # noinspection PyTypeChecker
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

        def _check_carrots_hero_collisions(self):
            """萝卜是否与hero相碰"""
            for carrot in self.gh.carrots:
                if pygame.sprite.collide_rect(carrot, self.hero) and carrot.hit is False:
                    self.hero.move_can = False
                    carrot.hit = True

        def _check_hero_hurt(self):
            """响应hero受到攻击"""
            # 如果变脸了，读秒
            if self.hurt_count_start:
                self.hurt_counter += 1
            # 如果受击了，变脸并加速
            if self.hero_hurt != 0:
                self.hero.hurt = True
                self.hero.speed = self.settings.hero_hurt_speed_up * self.settings.heroes_speed
                # 重置并开始读秒
                self.hurt_counter = 0
                self.hurt_count_start = True
            # 如果读秒满了，变脸变回
            if self.hurt_counter == self.settings.hurt_time * 60:
                self.hero.hurt = False
                self.hero.speed = self.settings.heroes_speed
                self.hurt_count_start = False


        def _update_screen(self):
            """绘制屏幕"""
            # 用纯色填充背景
            self.screen.blit(self.bg, self.screen_rect)

            # 鸿合在bullet之下
            if self.head_exist:
                if self.hitevision_exist:
                    self.hitevision.blitme()

            # bullet在hero之下
            for bullet in self.bullets:
                bullet.draw_bullet()

            # head在hero之下
            if self.head_exist:
                self.gh.draw_enemy()
                self.gh_blood_bar.draw_blood_blank()
                self.gh_blood_bar.draw_blood_bar(self.gh_blood)

            self.hero.blitme()

            for enemy in self.simple_enemies:
                enemy.draw_enemy()

            self.hero_blood_bar.draw_blood_blank()
            self.hero_blood_bar.draw_blood_bar(self.hero_blood)

            pygame.display.flip()


if __name__ == '__main__':
    deos = DeadEndOfSZSY()
    deos.run_game()