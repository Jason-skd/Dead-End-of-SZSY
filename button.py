import pygame.font

class Button:
    """为游戏创建按钮的类"""

    def __init__(self, deos_game, width, height, button_color, text_color, font, font_size, msg):
        """初始化按钮的属性"""
        self.screen = deos_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = deos_game.settings

        # 设置按钮的尺寸和其他属性
        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(font, font_size)

        # 创建按钮的rect对象并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将msg渲染为图像并使其在按钮上居中"""
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
