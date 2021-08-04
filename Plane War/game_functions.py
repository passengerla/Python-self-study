import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ship,ai_settings,screen,bullets):
    #响应按下
    if event.key == pygame.K_RIGHT:
        # 向右移动
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # 向左移动
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        # 向上移动
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        # 向下移动
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        # if len(bullets) < ai_settings.bullet_allowed:
        #     #创建一个子弹，并将其加到编组bullets中
        #     new_bullet = Bullet(ai_settings,screen,ship)
        #     bullets.add(new_bullet)

def check_keyup_events(event,ship):
    #响应松开
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False

def check_events(ship,ai_settings,screen,bullets,stats,play_button,aliens):
    """响应按键与鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            #KEYDOWN事件:当用户按下任意键时触发
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ship,ai_settings,screen,bullets)
            #KEYUP当用户松开任意键时触发
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #返回鼠标单机的坐标的元组
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,ai_settings,screen,ship)
def check_play_button(stats,play_button,mouse_x,mouse_y,aliens,bullets,ai_settings,screen,ship):
    """在玩家单击play按钮时开始游戏"""
    #使用collidepoint()函数检查是否在按钮的rect内
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计数据
        stats.reset_stats()
        stats.game_active = True
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
def update_screen(ai_settings,screen,ship,bullets,aliens,play_button,stats,sb):
    # 每次循环时都重回屏幕，screen.fill()，用背景色填充屏幕
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重新绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 确保这里飞船在背景刷新之前
    ship.blitme()
    aliens.draw(screen)
    #显示得分
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # 让绘制的屏幕可见
    # 让最近绘制的屏幕可见，每次执行while循环时都绘制一个空屏幕，并擦去旧屏幕，使只有新屏幕可见
    pygame.display.flip()
def update_bullets(bullets,aliens,ai_settings,screen,ship,stats,sb):
    #更新子弹的位置，并删除已经消失的子弹
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #检查子弹是否击中外星人
    #如果是这样，就删除相应的子弹和外星人
    """新增的这行代码是遍历组bullets中的每颗子弹，再遍历aliens中每个外星人。当外星人和子弹的rect重叠时，groupcollide()就在它返回的字典中添加
    一个键值对。两个实参都为True告诉pygame删除发生碰撞的子弹和外星人。{要模拟穿行的屏幕顶端的高能子弹，消失它击灭，可将第一个设为False，并让
    第二个设置为True。这样被击中的外星人消失，而子弹不会消失，所有子弹有效，到屏幕顶端消失}
#     """
#     collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
#     if len(aliens) == 0:
#         #删除现有的子弹
#         bullets.empty()
#         create_fleet(ai_settings,screen,aliens,ship)
    check_bullet_alien_collisions(bullets,aliens,ai_settings,screen,ship,stats,sb)
def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        # 创建一个子弹，并将其加到编组bullets中
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,screen):
    #计算多少个外星人
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    available_space_x = ai_settings.screen_width -2*alien_width
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    #计算屏幕可以容纳多少行外星人
    available_space_y = (ai_settings.screen_height-(2*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)
def create_fleet(ai_settings,screen,ship,aliens):
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)
def ship_hit(ai_setings,stats,screen,ship,aliens,bullets):
    if stats.ships_left >= 0:
        """响应被外星人撞到的飞船"""
        #将ship_left减1
        stats.ships_left -= 1

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群外星人，并将飞船放到屏幕底部中央
        create_fleet(ai_setings,screen,ship,aliens)
        ship.center_ship()
        ship.bottom_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
def check_aliens_bottom(ai_setings,stats,screen,ship,aliens,bullets):
    """检查外星人是否到了底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船那样处理进行处理
            ship_hit(ai_setings,stats,screen,ship,aliens,bullets)

def update_aliens(ai_settings,aliens,ship,stats,screen,bullets):
    """检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人和飞船之间碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘所采取的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    """将整群外星人下移并改变方向"""
    #sprites创建一个副本，可以更改原来的属性
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
def check_bullet_alien_collisions(bullets,aliens,ai_settings,screen,ship,stats,sb):
    """方法sprite.groupcollide()将每颗子弹的rect同每个外星人的rect进行比较，并返回一个字
典，其中包含发生了碰撞的子弹和外星人。在这个字典中，每个键都是一颗子弹，而相应的值都
是被击中的外星人"""
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    if collisions:
        for num in collisions.values():
            stats.score += ai_settings.alien_points*len(num)
            sb.prep_score()
        check_high_score(stats,sb)
    if len(aliens) == 0:
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
