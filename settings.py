class Settings:
    """存储《DeadEndOfSZSY》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1920
        self.screen_height = 1080

        # 欢迎界面设置
        # 按钮设置
        self.play_button_width, self.play_button_height = 200, 50
        self.play_button_color = (200, 50, 50)
        self.play_color = (255, 255, 255)
        self.play_font = None
        self.play_size = 48

        # 背景设置
        # self.bg_color = (33, 40, 118)
        self.bg_image = 'images/bg - 1.jpg'

        # 声音设置
        self.bgm = "bgm/Only_Gwen - 【大厅】S2惊奇游乐园 S3疯狂马戏团5【共用音乐】.mp3"

        # heroes设置
        self.heroes_width = 27 * 1.5
        self.heroes_height = 39.5 * 1.5
        self.heroes_speed = 2

        self.sgzy_normal_image = 'images/sgzy - normal.jpg'
        self.sgzy_hurt_image = 'images/sgzy - hurt.jpg'

        self.sgzy_blood = 100

        # 受伤变脸的时间
        self.hurt_time = 0.5

        # enemies设置
        self.simple_enemy_width = 20
        self.simple_enemy_color = (255, 248, 125)
        self.simple_enemy_speed = 1
        self.simple_enemy_harm = 8
        self.simple_enemy_hurt_blank = 0.5

        self.gh_speed = 2
        self.gh_harm = 8
        self.gh_hurt_blank = 0.5
        self.gh_image = 'images/gh.jpg'
        self.gh_width = 441 * 0.3
        self.gh_height = 506 * 0.3

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

        # 关卡设置
        self.simple_enemy_number = 10
        self.simple_enemy_wave = 5
        self.simple_enemy_prod_blank = 5
        self.heads = None


    def chap_1(self):
        """广播：将进行chap_1"""
        self.bg_image = 'images/bg - 1.jpg'
        self.simple_enemy_number = 1
        self.simple_enemy_wave = 1
        self.heads = None

    def chap_2(self):
        """广播：将进行chap_1"""
        self.bg_image = 'images/bg - 1.jpg'
        self.simple_enemy_number = 15
        self.simple_enemy_wave = 7
        self.heads = gh