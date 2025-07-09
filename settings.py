class Settings:
    """存储《DeadEndOfSZSY》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1920
        self.screen_height = 1080

        # 声音设置
        self.bgm_volume = 0.3

        # 欢迎界面设置
        # logo偏离中心高度
        self.logo = 'images/logo.png'
        self.logo_center_height = -100
        self.logo_width = 559
        self.logo_height = 583
        # 按钮设置
        self.play_button_width, self.play_button_height = 300, 100
        self.play_button_x, self.play_button_y = 960, 840
        self.play_button_color = (191, 0, 0)
        self.play_color = (255, 255, 255)
        self.play_font = None
        self.play_size = 100

        # try again 界面
        self.try_again_width = 400
        self.logo_2 = 'images/logo - 2.png'

        # winning界面
        self.congratulations = 'images/congratulations.png'

        # 章节广播设置
        self.nx_chap_top_dist = 150

        # 背景设置
        self.bg_color = (33, 40, 118)
        self.interface_bg = 'images/bg.png'
        self.bg_image = 'images/bg - 1.jpg'

        # heroes设置
        self.heroes_width = 40.5
        self.heroes_height = 59.25
        self.heroes_speed = 2

        self.sgzy_normal_image = 'images/sgzy - normal.jpg'
        self.sgzy_hurt_image = 'images/sgzy - hurt.jpg'

        self.sgzy_blood = 100

        # 受伤变脸的时间
        self.hurt_time = 0.5

        # 受击加速
        self.hero_hurt_speed_up = 2

        # enemies设置
        self.simple_enemy_width = 20
        self.simple_enemy_harm = 4
        self.simple_enemy_hurt_blank = 0.5

        self.gh_speed = 0.5
        self.gh_harm = 20
        self.gh_blood = 120
        self.gh_hurt_blank = 1.5
        self.gh_image = 'images/gh.jpg'
        self.gh_width = 132.3
        self.gh_height = 151.8
        self.gh_skill_blank = 10
        self.gh_face = 'images/gh_face.png'
        self.jump_face_sound = 'bgm/jump_face.wav'

        # 技能
        self.carrot_width = 40
        self.carrot_nor = 'images/carrot - 1.png'
        self.carrot_prep = 'images/carrot - 2.png'
        self.carrot_flying_duration = 3
        self.carrot_numb = 8
        self.carrot_speed = 2
        self.carrot_dominate_duration = 1.5
        self.carrot_lifespan = 60

        self.board_width = 589
        self.board_height = 227
        self.board_centerx = 959.5
        self.board_centery = 309.5
        self.hv_image = 'images/Hite Vision.png'
        self.hv_lifespan = 5
        self.hv_hurt_blank = 0.5
        self.hv_hurt = 5

        self.zaijia = 'bgm/再加三周.wav'
        self.chuchu = 'bgm/处处有提醒.wav'
        self.ganshen = 'bgm/干什么呢 都高三了.wav'
        self.bachu = 'bgm/拔出萝卜.wav'
        self.kange = 'bgm/看个通知.wav'
        self.zhonggu = 'bgm/重骨架.wav'
        self.hit = 'bgm/打击.wav'

        self.skill_f_duration = 3
        self.frame_speed_up = 4
        self.benzene = 'images/benzene.png'

        # bullet 设置
        self.bullet_fire_blanking = 0.5
        self.bullet_speed = 5.0
        self.bullet_radius = 8
        self.bullet_color = (180, 180, 180)

        # blood_bar设置
        self.blood_bar_width = 55
        self.blood_bar_height = 15
        self.blood_bar_color = (0, 200, 50)
        self.blood_bar_pos_height = 10
        self.blood_bar_border_width = 3

        self.gh_blood_bar_width = 130
        self.gh_blood_bar_color = (200, 0, 50)

        # 跳脸
        self.jump_face = 'images/gh_face.jpg'
        self.jf_small_width = 20
        self.jp_interval =1.5
        self.jf_large_width = 1920
        self.jf_lifespan = 2.5

        # 关卡设置

    def chap_1(self):
        """广播：将进行chap_1"""
        self.bgm = "bgm/Andrew Prahlow - Travelers' encore.mp3"
        self.bg_image = 'images/bg - 1.png'

        self.simple_enemy_number = 15
        self.simple_enemy_wave = 8
        self.simple_enemy_speed = 1.5
        self.simple_enemy_prod_blank = 7
        # sp的图像
        self.sp_1 = 'images/sp - 1.jpg'
        self.sp_2 = 'images/sp - 2.jpg'
        self.sp_3 = 'images/sp - 3.jpg'
        self.sp_4 = 'images/sp - 4.jpg'

        # 源源不断地小兵
        self.sp_inf = False

        self.chap_head = None

    def chap_2(self):
        """广播：将进行chap_2"""
        self.bgm = "bgm/BLESSED MANE - Death Is No More.mp3"
        self.bg_image = 'images/bg - 2.jpg'

        # 无限前
        self.simple_enemy_number = 15
        self.simple_enemy_wave = 5
        self.simple_enemy_speed = 1.2
        self.simple_enemy_prod_blank = 5
        # sp的图像
        self.sp_1 = 'images/sp - 5.jpg'
        self.sp_2 = 'images/sp - 6.jpg'
        self.sp_3 = 'images/sp - 7.jpg'
        self.sp_4 = 'images/sp - 8.jpg'

        # 源源不断的小兵
        self.sp_inf = True
        # 无限后
        self.inf_simple_enemy_number = 15
        self.inf_simple_enemy_wave = 9999
        self.inf_simple_enemy_prod_blank = 7

        self.chap_head = 'gh'

        self.winning_sound = 'bgm/顶楼的马戏团 - 义务为豪大大鸡排所作个广告歌.mp3'
