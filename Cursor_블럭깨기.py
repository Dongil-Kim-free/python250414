import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("블럭 깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 패들 설정
paddle_width = 100
paddle_height = 20
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 40
paddle_speed = 8

# 공 설정
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5
ball_dy = -5

# 블록 설정
block_width = 80
block_height = 30
block_rows = 5
block_cols = 10
blocks = []

for i in range(block_rows):
    for j in range(block_cols):
        block = {
            'x': j * (block_width + 2) + 1,
            'y': i * (block_height + 2) + 1,
            'width': block_width,
            'height': block_height,
            'color': (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        }
        blocks.append(block)

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 패들 이동
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # 공 이동
    ball_x += ball_dx
    ball_y += ball_dy

    # 벽 충돌 처리
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_dx = -ball_dx
    if ball_y <= ball_radius:
        ball_dy = -ball_dy

    # 패들 충돌 처리
    if (ball_y + ball_radius >= paddle_y and
        ball_x >= paddle_x and
        ball_x <= paddle_x + paddle_width):
        ball_dy = -ball_dy

    # 블록 충돌 처리
    for block in blocks[:]:
        if (ball_x + ball_radius >= block['x'] and
            ball_x - ball_radius <= block['x'] + block['width'] and
            ball_y + ball_radius >= block['y'] and
            ball_y - ball_radius <= block['y'] + block['height']):
            ball_dy = -ball_dy
            blocks.remove(block)
            break

    # 게임 오버 처리
    if ball_y >= HEIGHT:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = 5
        ball_dy = -5

    # 화면 그리기
    screen.fill(BLACK)
    
    # 패들 그리기
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    
    # 공 그리기
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    
    # 블록 그리기
    for block in blocks:
        pygame.draw.rect(screen, block['color'], 
                        (block['x'], block['y'], block['width'], block['height']))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
