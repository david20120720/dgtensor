#1. 파이게임 모듈을 불러온다
import pygame
import math
import random

#2.초기화 시킨다
pygame.init()
width,height=640,480
screen=pygame.display.set_mode((width,height))
acc=[0,0]
arrows=[]
badtimer=100
badtimer1=0
badguys=[[640,100],]
healthvalue=194
pygame.mixer.init()



#3. 이미지를 가져온다
#3-1. 장고에 올릴때는 c:/ 부터시작하는 절대경로로 입력이 필요함.
#3-2. \ 가 아닌 /로 구분해야함
player=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/dude.png")
grass=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/grass.png")
castle=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/castle.png")
arrow=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/bullet.png")
badguyimg=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/badguy.png")
healthbar=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/healthbar.png")
health=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/health.png")
gameover=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/gameover.png")
youwin=pygame.image.load("C:/0work/tensorproject/tensorproject/resources/images/youwin.png")

keys=[False,False,False,False]
playpos=[100,100]

#3.1 load audio
hit = pygame.mixer.Sound("C:/0work/tensorproject/tensorproject/resources/audio/explode.wav")
enemy = pygame.mixer.Sound("C:/0work/tensorproject/tensorproject/resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("C:/0work/tensorproject/tensorproject/resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('C:/0work/tensorproject/tensorproject/resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)


#4. 계속 화면이 보이도록 한다.


running=1
exitcode=0

while running:
    badtimer=badtimer-1
    #5. 화면을 깨끗하게 한다.
    screen.fill((0,0,0)) #(R,G,B)    
    #6. 모든 요소들을 다시 그린다. 
    
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))     
    screen.blit(castle,(0,30))
    screen.blit(castle,(0,135))
    screen.blit(castle,(0,240))
    screen.blit(castle,(0,345))
          
    #6.1 -set player positionand rotation
    position=pygame.mouse.get_pos()
    angle=math.atan2(position[1]-(playpos[1]+32),position[0]-(playpos[0]+26))
    #rotate함수는 반시계방향이 + 방향인듯.. 데이비드
    #따라서 마우스가 수평선 하단 90도 일때,반시계방향으로 360-90=270도 만큼 회전시킴
    playerrot=pygame.transform.rotate(player,360-angle*57.29)
    #player의 중심을 기준으로 회전하도록 위치를 잡아줌
    #즉 플레이어의 위치에, 플레이어 크기의 반만큼 각각 더해준 위치가, 플레이어의 
    #위치가 되고, 그 위치로 부터 마우스까지의 각도를 계산해서 회전시키게됨
    playerpos1=(playpos[0]-playerrot.get_rect().width//2,playpos[1]-playerrot.get_rect().height//2)
    screen.blit(playerrot,playerpos1)
    
    #6.2 -draw arrows
    
    #for bullet in arrows: # bullet <= [각도,플레이의 x좌표,y좌표 ]
    for bullet in arrows:
        index=0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] = bullet[1]+velx
        bullet[2] = bullet[2]+vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index = index+1        
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
   
    #6.3 -draw badguys
     # 6.3 - 오소리 공격
    if badtimer == 0:
        badguys.append([640, random.randint(50,430)])
        badtimer = 100-(badtimer1*2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 = badtimer1+5
    index=0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
        else:
            badguy[0] = badguy[0]-7
            
        # 6.3.1 - 성 공격
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            healthvalue = healthvalue-random.randint(5,20)
            badguys.pop(index)     
        #6.3.2 -check for collisions        
        index1 = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] = acc[0]+1
                badguys.pop(index)
                arrows.pop(index1)
            index1 = index1+1 
       #6.3.3 -next guy  
        index=index+1
    for badguy in badguys:
        screen.blit(badguyimg,badguy)
        
    #6.4 -draw clock    
    # 6.4 - 남은시간
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str(int((90000-pygame.time.get_ticks())/60000))+\
        ":"+str(int((90000-pygame.time.get_ticks())/1000)%60).zfill(2), \
        True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright = [635,5]
    screen.blit(survivedtext, textRect)

    # 6.5 - 남은 생명을 표시
    screen.blit(healthbar, (5,5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8,8))
       
        
    #7. 화면을 다시 그린다(화면업데이트).
    pygame.display.flip()
    
    #8.게료임을 종료한다.
    for event in pygame.event.get():
        # x를 눌렀으면,
        if event.type==pygame.QUIT:
            #게임종료한다
            pygame.quit()
            exit(0)
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                keys[0]=True
            elif event.key==pygame.K_a:
                keys[1]=True
            if event.key==pygame.K_s:
                keys[2]=True
            elif event.key==pygame.K_d:
                keys[3]=True                
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:
                keys[0]=False
            elif event.key==pygame.K_a:
                keys[1]=False
            if event.key==pygame.K_s:
                keys[2]=False
            elif event.key==pygame.K_d:
                keys[3]=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position=pygame.mouse.get_pos()
            acc[1]=acc[1]+1
            arrows.append([math.atan2(position[1]-(playpos[1]+32),\
                position[0]-(playpos[0]+26)),playerpos1[0]+32,\
                playerpos1[1]+32])

    #9. move player
    if keys[0]:
        playpos[1]=playpos[1]-5
    elif keys[2]:
        playpos[1]=playpos[1]+5
    if keys[1]:
        playpos[0]=playpos[0]-5
    elif keys[3]:
        playpos[0]=playpos[0]+5
        
#10 - Win/Lose 검사
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = acc[0]*1.0/acc[1]*100
    else:
        accuracy = 0
    
# 11 - Win/lose 디스플레이
if exitcode == 0:    # 패배 (LOSE)
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+"{0:.2f}".format(accuracy)+"%", True, (255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover, (0,0))
    screen.blit(text, textRect)

else:    # 게임승리 (WIN)
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy: "+"{0:.2f}".format(accuracy)+"%", True, (0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin, (0,0))
    screen.blit(text, textRect)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()