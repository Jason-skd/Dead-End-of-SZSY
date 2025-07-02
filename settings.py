class Settings:
    """存储《DeadEndOfSZSY》中所有设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        # 屏幕设置
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (33, 40, 118)

        # 声音设置
        self.bgm = "bgm/Andrew Prahlow - Travelers' encore.mp3"

        # heroes设置
        self.heroes_width = 27
        self.heroes_height = 39.5
        self.heroes_speed = 2

        # enemies设置
        self.simple_enemy_width = 10
        self.simple_enemy_color = (255, 248, 125)
