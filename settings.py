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
        # 按钮设置
        self.play_button_width, self.play_button_height = 300, 100
        self.play_button_x, self.play_button_y = 960, 740
        self.play_button_color = (50, 200, 200)
        self.play_color = (255, 255, 255)
        self.play_font = None
        self.play_size = 60

        # 背景设置
        self.bg_color = (33, 40, 118)
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

        # enemies设置
        self.simple_enemy_width = 20
        self.simple_enemy_harm = 5
        self.simple_enemy_hurt_blank = 0.5

        self.gh_speed = 0.5
        self.gh_harm = 20
        self.gh_blood = 120
        self.gh_hurt_blank = 1
        self.gh_image = 'images/gh.jpg'
        self.gh_width = 132.3
        self.gh_height = 151.8
        self.gh_skill_blank = 15
        self.gh_face = 'images/gh_face.jpg'
        self.jump_face_sound = 'bgm/jump_face.wav'

        # 技能
        self.carrot_width = 40
        self.carrot_nor = 'images/carrot - 1.jpg'
        self.carrot_prep = 'images/carrot - 2.jpg'

        # bullet 设置
        self.bullet_fire_blanking = 0.5
        self.bullet_speed = 5.0
        self.bullet_radius = 8
        self.bullet_color = (255, 255, 255)

        # blood_bar设置
        self.blood_bar_width = 55
        self.blood_bar_height = 15
        self.blood_bar_color = (0, 200, 50)
        self.blood_bar_pos_height = 10
        self.blood_bar_border_width = 3

        self.gh_blood_bar_width = 130
        self.gh_blood_bar_color = (200, 0, 50)

        # 关卡设置

    def chap_1(self):
        """广播：将进行chap_1"""
        self.bgm = "bgm/Andrew Prahlow - Travelers' encore.mp3"
        self.bg_image = 'images/bg - 2.jpg'

        self.simple_enemy_number = 5
        self.simple_enemy_wave = 2
        self.simple_enemy_speed = 1.5
        self.simple_enemy_prod_blank = 10
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
        self.bg_image = 'images/bg - 3.jpg'

        # 无限前
        self.simple_enemy_number = 10
        self.simple_enemy_wave = 5
        self.simple_enemy_speed = 1.2
        self.simple_enemy_prod_blank = 3
        # sp的图像
        self.sp_1 = 'images/sp - 5.jpg'
        self.sp_2 = 'images/sp - 6.jpg'
        self.sp_3 = 'images/sp - 7.jpg'
        self.sp_4 = 'images/sp - 8.jpg'

        # 源源不断的小兵
        self.sp_inf = True
        # 无限后
        self.inf_simple_enemy_number = 5
        self.inf_simple_enemy_wave = 3
        self.inf_simple_enemy_prod_blank = 10

        self.chap_head = 'gh'
