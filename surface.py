import pygame

class CreateSurface:
    """在deos_game的screen中创建一个surface用于显示文字或图像"""
    def __init__(self, deos_game, centerx=0, centery=0):
        self.screen = deos_game.screen
        self.centerx = centerx
        self.centery = centery

        self.surface = None
        self.rect = None

    def text_surface(self, font_size, msg, color='white'):
        """创建文字surface"""
        # 渲染
        font = pygame.font.Font(None, font_size)
        self.surface = font.render(msg, True, color)

        # 获取rect
        self.rect = self.surface.get_rect()

        # 设置位置
        self.rect.center = (self.centerx, self.centery)

    def image_surface(self, path, scale=None):
        """创建图案surface"""
        try:
            self.surface = pygame.image.load(path)
        except pygame.error as e:
            self.text_surface(36, "ERROR", "red")
            return

        if scale:
            self.surface = pygame.transform.scale(self.surface, scale)

        self.rect = self.surface.get_rect()

        self.rect.center = (self.centerx, self.centery)

    def blitme(self):
        """绘制屏幕"""
        self.screen.blit(self.surface, self.rect)