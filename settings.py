class Settings:
    """存储《DeadEndOfSZSY》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1920
        self.screen_height = 1080

        # 背景设置
        # self.bg_color = (33, 40, 118)
        self.bg_image = 'images/bg - 1.jpg'

        # 声音设置
        self.bgm = "bgm/Andrew Prahlow - Travelers' encore.mp3"

        # heroes设置
        self.heroes_width = 27 * 1.5
        self.heroes_height = 39.5 * 1.5
        self.heroes_speed = 2

        # enemies设置
        self.simple_enemy_width = 20
        self.simple_enemy_color = (255, 248, 125)
        self.simple_enemy_speed = 1

        # bullet 设置
        self.bullet_fire_blanking = 1
        self.bullet_speed = 5.0
        self.bullet_radius = 10
        self.bullet_color = (60, 60, 60)

        # 关卡设置
        self.simple_enemy_number = 10

    def chap_1(self):
        """广播：将进行chap_1"""
        self.bg_image = 'images/bg - 1.jpg'
        self.simple_enemy_number = 10
