# 在pygame中原点(0,0)在屏幕左上角，在1200*800中右下角的为(1200,800)
import pygame


class Ship:
    def __init__(self, screen,ai_settings):
        """初始化飞船并设置其初始位置"""
        self.screen = screen
        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images/ship.png')
        # 使用 get_rect()获取相应surface的属性(得到surface的矩形区域)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将每艘新飞船放在屏幕底部中央，这里是飞机的属性
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #用于改变位置位置的变量
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)
        #移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.ai_settings = ai_settings

    def update(self):
        """根据移动标志调整飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        elif self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        elif self.moving_up and self.rect.top > 0:
            self.bottom -= self.ai_settings.ship_speed_factor
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed_factor
        #更新属性
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def blitme(self):
        """指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船屏幕居中"""
        self.center = self.screen_rect.centerx

    def bottom_ship(self):
        self.bottom = self.screen_rect.bottom