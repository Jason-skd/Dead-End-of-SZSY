import pygame

class BloodBar:
    """管理血条的类"""
    def __init__(self, deos_game, target, blood_max, width):
        """初始化血条"""
        self.deos_game = deos_game

        self.screen = deos_game.screen
        self.screen_rect = deos_game.screen.get_rect()

        self.settings = deos_game.settings

        self.width = width
        self.height = self.settings.blood_bar_height
        self.color = self.settings.blood_bar_color
        self.pos_height = self.settings.blood_bar_pos_height
        self.border_width = self.settings.blood_bar_border_width

        self.target = target

        # 先在0，0画出血条描边rect再移动到屏幕正下方
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = deos_game.screen_rect.centerx
        self.rect.bottom = self.screen_rect.height - self.pos_height

        # 先在0，0画出血条内容rect再移动到屏幕正下方
        self.blood_width = self.width - 2 * self.border_width
        self.blood_height = self.height - 2 * self.border_width
        self.blood_rect = pygame.Rect(0, 0, self.blood_width, self.blood_height)
        # self.blood_rect.centerx = deos_game.screen_rect.centerx
        # self.blood_rect.bottom = self.screen_rect.height - self.pos_height

        # 创建一个带有透明通道的 Surface 来绘制血条
        self.blood_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # 初始化血量
        self.blood_max = blood_max

    def draw_blood_blank(self):
        """画出血条的描边"""
        # 清空 Surface（设置为完全透明）
        self.blood_surface.fill((0, 0, 0, 0))
        # 描边
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, self.border_width)
        self.screen.blit(self.blood_surface, (self.rect.x, self.rect.y))

    def draw_blood_bar(self, blood):
        """画出血条"""
        # 根据当前血量比例计算血条宽度
        current_width = (blood / self.blood_max) * (self.width - 2 * self.border_width)
        self.blood_rect.width = max(0, current_width)  # 确保不小于0
        pygame.draw.rect(self.screen, self.color, self.blood_rect)


    def update(self):
        """血条跟随人物移动"""
        self.rect.centerx = self.target.rect.centerx
        self.rect.centery = self.target.rect.top - self.pos_height

        # 血条与血条描边左边缘重合
        self.blood_rect.left = self.rect.left + self.border_width
        self.blood_rect.centery = self.rect.centery
