import pygame
import os
from random import *

pygame.init() # 초기화 함수

screen_width = 480
screen_height = 720

pygame.display.set_mode((screen_width , screen_height))
pygame.display.set_caption("우상의 게임")  #게임 이름

running = True # boolean 변수 선언

current_path = os.path.dirname(__file__)  # 상대경로 설정

# 배경 설정
background = pygame.image.load(os.path.join(current_path, 'background.png'))

background_space = pygame.image.load(os.path.join(current_path, 'background_space.png'))
background_universe = pygame.image.load(os.path.join(current_path, 'background_universe.png'))


background_universe=background_space=background

# 캐릭터 설정
character = pygame.image.load(os.path.join(current_path, 'character.png'))
character_immune = pygame.image.load(os.path.join(current_path, 'character_immune.png'))

character_xpos = screen_width/2 - 30
character_ypos = screen_height - 120
tox = 0
toy = 0
#4-4 캐릭터 무적 스킬 설정(4-4)
character_isimmune = False
character_immunecooldown = 0

start_time = 0
prev_time = 0
current_time = 0
space_time = 0
dojumped = False
starttick = 0
t = 0


# 적 설정
enemy = pygame.image.load(os.path.join(current_path, 'enemy.png'))

enemy_xpos = randint(0,540)
enemy_ypos = 0

enemy_do_exist = True # 적이 있는가?

enemy_speed = 1

screen = pygame.display.set_mode((screen_width, screen_height))

score = 0


# 라이프 설정
life = 3


# 레이저 설정
laser = pygame.image.load(os.path.join(current_path,'laser.png'))
laser_do_exist = False
laser_do_damage = False

laser_ypos = 0
laser_damaged = True
laser_score = randint(1,8)

laser_activated = False


# 새로운 적

enemy_2_picture = pygame.image.load(os.path.join(current_path, 'enemy_2.png'))


# 발사체

flyer_pic = pygame.image.load(os.path.join(current_path, 'character_flyer.png'))








# 폰트 로딩

try:
    font = pygame.font.Font(None, 40)
except:
    print("에러! 폰트 로딩에 실패하였습니다!")














def enemy_regen():
    pygame.time.set_timer(pygame.USEREVENT, randint(1000,1800), 1)


message_do_exist = False
message_text = ''

def message(str, time=2000):
    global message_do_exist, message_text
    message_text = str
    message_do_exist = True
    pygame.time.set_timer(pygame.USEREVENT + 1, time)
    
    

def char_jumpcode():
    global character_xpos , character_ypos , tox , toy,  space_time,t,dojumped,starttick
    
    space_time = pygame.time.get_ticks()
    t = pygame.time.get_ticks()
    dojumped = True
    starttick = pygame.time.get_ticks()




background = background_universe




def char_jumpto():
    global character_xpos , character_ypos , tox , toy, space_time , t, dojumped, starttick
    if  dojumped == True:
        if character_ypos > 720-120:
          character_ypos = 720-120 ; dojumped = False ;toy=0 ;return

      
        t = (pygame.time.get_ticks() - starttick) / 1000

        print(t)
        toy  =   (0.15 * (50 - 140*t))
    



def percentange(percent):  # percent의 확률로 '참'을 리턴하는 코드
    global score
    a = randint(1,100)

    if score < 50:
        return False
    
    elif score >= 50 and score < 100:
        if a<=10 :
            return True
        else:
            return False 
    elif score >= 100 and score < 200:
        if a<=15 :
            return True
        else:
            return False   
    
    elif score >= 200 and score < 300:
        if a<=20 :
            return True
        else:
            return False  
    else:
        if a<=25 :
            return True
        else:
            return False  


def laser_phase1():
    global laser_do_exist, laser_do_damage, laser_ypos, laser_damaged, laser_score, laser_activated
    laser_do_exist = True
    laser_do_damage = False
    laser_ypos = randint(120, 660)
    laser_damaged = False # 추가된 부분
    laser_score = randint(1,7) # 추가된 부분
    laser_activated = True ## 5-1
    pygame.time.set_timer(pygame.USEREVENT + 4 , 400, 1)

def laser_phase2():
    global laser_do_exist, laser_do_damage
    laser_do_exist = False
    laser_do_damage = False
    pygame.time.set_timer(pygame.USEREVENT + 5 , 800, 1)

def laser_phase3():
    global laser_do_exist, laser_do_damage
    laser_do_exist = True
    laser_do_damage = True
    pygame.time.set_timer(pygame.USEREVENT + 6 , 4000, 1)
    
def laser_phase4():
    global laser_do_exist, laser_do_damage, laser_damaged, laser_score, score, laser_activated
    if laser_damaged == False:
        score += laser_score # 추가된 부분 : 피해를 입지 않았으면 점수+
    laser_activated = False ## 5-1

    laser_do_exist = False
    laser_do_damage = False



class Enemy:
    
    def __init__(self, picture, hp, max_hp,xpos, ypos, speed, do_exist):
        self.picture = picture
        self.hp = hp
        self.xpos = xpos
        self.ypos = ypos
        self.speed = speed
        self.do_exist = do_exist
        self.max_hp = max_hp
    
    def spawn(self):
        global screen_width
        
        self.do_exist = True
        self.max_hp = randint(3,6)
        self.speed = randint(2,4) / 10
        self.xpos = randint(0, screen_width - 60)
        self.ypos = 0
        self.hp = self.max_hp
    
    def attackedandkilled(self):
        self.hp -= 1
        if self.hp <= 0:
            self.do_exist = False
            pygame.time.set_timer(pygame.USEREVENT + 7, randint(12000,18000),1)
            # 재생성까지 설정하기
    
    def move(self):
        global screen_height
        if self.do_exist == False:
            return
               
        if self.ypos < screen_height:
        
            self.ypos += self.speed
        else:
            self.do_exist = False
            global life, running
            life -= 1
            if life <= 0:
                running = False
            pygame.time.set_timer(pygame.USEREVENT + 7, 8000, 1)
    

class flyer:
    def __init__(self,picture, xpos, ypos, do_exist):
        self.xpos = xpos  
        self.picture = picture
        self.ypos = ypos
        self.do_exist  = do_exist
        
    def move(self):
        
        if self.do_exist == False:
            return
        
        if self.ypos > 0:
            
            self.ypos -= 6
        if self.ypos <= 0:
            self.do_exist = False 
    
    def spawn(self):
        global character_xpos # 캐릭터의 x좌표 가져오기
        
        self.xpos = character_xpos + 25 # 정 중앙
        self.ypos = character_ypos - 10
        self.do_exist = True
                   
            
        
        
            
            
    
               
enemy_2 = Enemy(enemy_2_picture, 3, 3, randint(0,300), 0, 0.2, False) # 적 정의하기

char_flyer = flyer(flyer_pic, 0,0,False)
        
        
fffff










pygame.time.set_timer(pygame.USEREVENT + 7, 3000,1) # 30s 후부터 생성 사이클 시작



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #반복문 탈출
            
        if event.type == pygame.USEREVENT:
            enemy_do_exist = True
            enemy_xpos = randint(0,540-60) # X좌표 랜덤 설정
            enemy_ypos = 0
            enemy_speed = 0.9 + random()  # 4-1차시에 나오는 내용입니다.
            
        if event.type == pygame.USEREVENT + 1:  # 4-3차시에 나오는 내용입니다.
            message_do_exist = False
        
        if event.type == pygame.USEREVENT + 2:
            character_isimmune = False
            
            
            
        if event.type == pygame.USEREVENT + 3:
            if character_immunecooldown > 0:
                character_immunecooldown -= 1
                pygame.time.set_timer(pygame.USEREVENT + 3, 1000, 1)
            
        if event.type == pygame.USEREVENT + 4:
            laser_phase2()
        if event.type == pygame.USEREVENT + 5:
            laser_phase3()
        if event.type == pygame.USEREVENT + 6:
            laser_phase4()
        
        if event.type == pygame.USEREVENT + 7:
            enemy_2.spawn()
        
        if event.type == pygame.USEREVENT + 8:
            laser_phase1()
            
            
        # 마우스 버튼
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and char_flyer.do_exist == False:
                char_flyer.spawn()
                
                
            
            
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT and not character_isimmune:
                tox -= 2
            if event.key == pygame.K_RIGHT and not character_isimmune:
                tox += 2
            if event.key == pygame.K_SPACE and not character_isimmune:
                char_jumpcode()
                start_time = pygame.time.get_ticks()
                
            
                
            if event.key == pygame.K_x:
                if character_immunecooldown <= 0:
                    pygame.time.set_timer(pygame.USEREVENT + 3, 1000, 1)
                    character_isimmune = True
                    pygame.time.set_timer(pygame.USEREVENT + 2, 2000, 1)
                    message("Used Immune")
                    character_immunecooldown = 30
                else:
                    message("Immune is on cooldown.")
                    
                    
                                
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                tox = 0
        
    
    character_xpos += tox
        
    
    if enemy_2.do_exist: # bool 값이므로 참일때만
        enemy_2.move()  
        
    if char_flyer.do_exist: #적처럼 똑같이
        char_flyer.move()
        
        
    # 화면 나감 처리
    if character_xpos < 0:
        character_xpos = 0
    if character_xpos > screen_width - 60:
        character_xpos = screen_width - 60
    
    if character_ypos < 0:
        character_ypos = 0
        starttick -= 300
    
    
    
    
    
    
    
    

    char_jumpto() # 4-5
    
    
    
    character_ypos -= toy
    
    
    
    
    
    
    
    
    
    
    
    
    
    # 충돌 처리를 위한 rect 정보 불러오기
    character_rect = character.get_rect()
    character_rect.left = character_xpos
    character_rect.top = character_ypos
    
    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_xpos
    enemy_rect.top = enemy_ypos
    
    # 4-5
    laser_rect = laser.get_rect()
    laser_rect.top = laser_ypos
    laser_rect.left = 0 # x좌표는 null 고정
    
    
    enemy_2_rect = enemy_2.picture.get_rect()
    enemy_2_rect.top = enemy_2.ypos
    enemy_2_rect.left = enemy_2.xpos
    
    cfr = char_flyer.picture.get_rect()
    cfr.top = char_flyer.ypos
    cfr.left = char_flyer.xpos
    
    
    # 충돌 처리
    
    if character_rect.colliderect(enemy_rect) and enemy_do_exist: #이게 없으면 투명 적이 된다.
        # running = False
        # print("충돌했어요")
        if not character_isimmune:
            
            life -= 1
            message("Warning! Life left {}!".format(life)) 
            
        if character_isimmune:
            message("Immune!")# 4-3 강의 내용
        if life <= 0:
            print("라이프가 모두 사라졌습니다. 점수 : {}".format(score))
            running = False
            
        enemy_do_exist = False
        enemy_ypos = 0
        enemy_regen()    # 4-2 강의 내역입니다.
    
    
    if character_rect.colliderect(laser_rect) and laser_damaged == False and laser_do_damage == True and laser_do_exist == True:
        life -= 1
        laser_damaged = True
        if life <= 0:
            running = False
        
        message("Laser damaged..")
    
    
    if cfr.colliderect(enemy_2_rect) and char_flyer.do_exist :
        enemy_2.attackedandkilled()
        char_flyer.do_exist = False
    
    
    
    
    if score < 30:
    
        screen.blit(background, (0,0))
    if score >=30 and score <60:
        screen.blit(background_space, (0,0))
    if score >= 60:
        screen.blit(background_universe, (0,0))
    
    
    # 배경-캐릭터 사이에
    
    if char_flyer.do_exist:
        screen.blit(char_flyer.picture, (char_flyer.xpos, char_flyer.ypos))
    
    
    
    if not character_isimmune:
        
        screen.blit(character, (character_xpos, character_ypos))
    if character_isimmune:
        screen.blit(character_immune, (character_xpos, character_ypos))
        
    
    score_text = "Score : {:,}".format(score) # :,는 3자리마다 콤마 찍기
    score_bar = font.render(score_text, True, (0,0,0)) # RGB 설정만 잘 하기
    screen.blit(score_bar, (0,0)) # 화면에 그리기
    

    if laser_do_exist:
        screen.blit(laser, (0,laser_ypos))
    
    
    
    if enemy_do_exist:
        screen.blit(enemy, (enemy_xpos, enemy_ypos))
        enemy_ypos += enemy_speed
        
        if enemy_ypos >= screen_height- 60:
            enemy_ypos = 0
            enemy_do_exist = False
            score += randint(1,6)
            
            
            if percentange(10) and not laser_activated  :
                laser_phase1()
                
            
            
            
            enemy_regen()
            
            
   
    # 적 표시하기(5-4 과정)
    if enemy_2.do_exist:
        screen.blit(enemy_2.picture, (enemy_2.xpos, enemy_2.ypos))         
            
            
            
    # 라이프 표시하기(4-1 과정)
    life_text = "Life : "+"V "* life
    life_bar = font.render(life_text, True, (255,0,0))
    screen.blit(life_bar, (0,40))
    
    
    
     
    
    
    # 메시지 표시하기(4-2 과정)
    if message_do_exist:
        screen.blit(font.render(message_text, True, (0,0,255)), (80,600))
    
        
    if character_immunecooldown > 0:
        screen.blit(font.render("Immnue Cooldown : {}s".format(character_immunecooldown), True, (205,205,0)), (0,80))
    
    
    pygame.display.update()
            

pygame.quit()



score_grade = ['D', 'D+', 'C', 'C+', 'B', 'B+', 'A', 'A+', 'S', 'S+', 'SS', 'SS+', 'SSS', 'SSS+','MASTER']

print("최종 결과 : {:,} 점")
if score < 700:
    print("Rank : {}".format(score_grade[score//50]))
else:
    print("Rank : GrandMaster")