import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreborad

def run_game():
    #初始化并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    #对象screen是一个surface，display.set_mode()返回的surface表示整个游戏窗口，每经过一个循环都将自动重绘这个surface
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption('我是你爸爸')
    #创建Play按钮
    play_button = Button(ai_settings,screen,'Play')
    ship = Ship(screen,ai_settings)
    #创建bullet组
    bullets = Group()
    #创建外星人组
    aliens = Group()
    #创建外星人群
    gf.create_fleet(ai_settings,screen,ship,aliens)
    #创建一个用于储存游戏统计信息的实例对象创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreborad(ai_settings,screen,stats)
    #开始游戏主循环
    while True:
        #监听键盘和鼠标事件
        gf.check_events(ship,ai_settings,screen,bullets,stats,play_button,aliens)
        if stats.game_active:
            #刷新一下飞船位置
            ship.update()
            #更新子弹位置及删除子弹
            gf.update_bullets(bullets,aliens,ai_settings,screen,ship,stats,sb)
            gf.update_aliens(ai_settings,aliens,ship,stats,screen,bullets)
        gf.update_screen(ai_settings,screen,ship,bullets,aliens,play_button,stats,sb)


run_game()
