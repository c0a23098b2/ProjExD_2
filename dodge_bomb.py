import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))
screen =pg.display.set_mode((WIDTH,HEIGHT))

def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]: #衝突識別関数
    yoko, tate =True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top <0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def Draw_rect():
    """
    surfaceの設定 1600×900
    黒い四角を描画 上0左0 幅1600高さ900
    半透明
    四角をblit
    """
    over_img = pg.Surface(( 1600, 900 ))
    pg.draw.rect(over_img, (0, 0, 0),(0, 0, 1600, 900) , 0)
    over_img.set_alpha( 150 )
    screen.blit(over_img,[0, 0])

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    #screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_n = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    clock = pg.time.Clock()
    tmr = 0
    bd_img =pg.Surface((20,20)) #爆弾
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx, vy = +5 , +5
    move = {
        pg.K_UP:(0,-5),
        pg.K_DOWN:(0,+5),
        pg.K_LEFT:(-5,0),
        pg.K_RIGHT:(+5,0)
    }
    while True: #追加機能1
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect( bd_rct ): #衝突
                Draw_rect() #関数呼び出し
                fonto = pg.font.Font(None, 100) #文字の大きさ
                txt = fonto.render("Game over", True, (255,255,255)) #文字の描画
                screen.blit(txt, [610,420]) #文字の貼り付け
                screen.blit(kk_n, [480,380]) #こうかとんの貼り付け
                screen.blit(kk_n, [1010,380])
                pg.display.update() #画面の更新
                time.sleep( 5 ) #5秒で終了させる
                return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k,v in move.items():
            if key_lst[k]: #こうかとんの移動速度
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)

        if check_bound(kk_rct) != (True, True): #こうかとんと壁の衝突判定
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx,vy)
        screen.blit(bd_img,bd_rct)

        yoko, tate =check_bound(bd_rct) #爆弾と壁の衝突判定
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
