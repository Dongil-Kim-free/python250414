import pygame
import time
import random
import os

# 초기화
pygame.init()

# 색상 정의
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# 화면 크기
width = 800
height = 600

# 게임 화면 생성
game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption('뱀 게임')

# 시계 객체 생성
clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

# 한글 폰트 설정
font_path = pygame.font.match_font('malgun gothic')  # Windows에서 한글 폰트 경로 가져오기
font_style = pygame.font.Font(font_path, 25)
score_font = pygame.font.Font(font_path, 35)

# 점수 표시 함수
def your_score(human_score, ai_score):
    human_text = score_font.render(f"사람 점수: {human_score}", True, yellow)
    ai_text = score_font.render(f"기계 점수: {ai_score}", True, yellow)
    game_display.blit(human_text, [10, 10])
    game_display.blit(ai_text, [10, 50])

# 뱀 그리기 함수
def our_snake(snake_block, snake_list, color):
    for x in snake_list:
        pygame.draw.rect(game_display, color, [x[0], x[1], snake_block, snake_block])

# 메시지 표시 함수
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_display.blit(mesg, [width / 6, height / 3])

# 게임 루프
def game_loop():
    game_over = False
    game_close = False

    # 사람 뱀 초기 위치
    x1 = width / 4
    y1 = height / 2
    x1_change = 0
    y1_change = 0

    # 기계 뱀 초기 위치
    x2 = 3 * width / 4
    y2 = height / 2
    x2_change = 0
    y2_change = 0

    snake_list = []
    ai_snake_list = []
    length_of_snake = 1
    length_of_ai_snake = 1

    human_score = 0
    ai_score = 0

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            game_display.fill(blue)
            message("게임 오버! 다시 시작하려면 C, 종료하려면 Q", red)
            your_score(human_score, ai_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # 기계 뱀 랜덤 이동
        ai_direction = random.choice(['LEFT', 'RIGHT', 'UP', 'DOWN'])
        if ai_direction == 'LEFT':
            x2_change = -snake_block
            y2_change = 0
        elif ai_direction == 'RIGHT':
            x2_change = snake_block
            y2_change = 0
        elif ai_direction == 'UP':
            y2_change = -snake_block
            x2_change = 0
        elif ai_direction == 'DOWN':
            y2_change = snake_block
            x2_change = 0

        # 벽 충돌 체크
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        if x2 >= width or x2 < 0 or y2 >= height or y2 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change

        game_display.fill(blue)
        pygame.draw.rect(game_display, red, [foodx, foody, snake_block, snake_block])

        # 사람 뱀 업데이트
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # 기계 뱀 업데이트
        ai_snake_head = [x2, y2]
        ai_snake_list.append(ai_snake_head)
        if len(ai_snake_list) > length_of_ai_snake:
            del ai_snake_list[0]

        # 자기 자신과 충돌 체크
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True
        for x in ai_snake_list[:-1]:
            if x == ai_snake_head:
                game_close = True

        # 뱀 그리기
        our_snake(snake_block, snake_list, black)
        our_snake(snake_block, ai_snake_list, green)
        your_score(human_score, ai_score)

        pygame.display.update()

        # 음식 먹기
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            human_score += 1
        elif x2 == foodx and y2 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_ai_snake += 1
            ai_score += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_loop()