import pygame
import random

# 초기화
pygame.init()

# 화면 크기
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (255, 0, 0),    # 빨강
    (0, 255, 0),    # 초록
    (0, 0, 255),    # 파랑
    (255, 255, 0),  # 노랑
    (0, 255, 255),  # 청록
    (255, 0, 255),  # 자홍
]

# 테트리스 블록 모양
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 1, 1],
     [1, 1, 0]],

    [[1, 1, 0],
     [0, 1, 1]],

    [[1, 1],
     [1, 1]],

    [[1, 1, 1, 1]],

    [[1, 1, 1],
     [1, 0, 0]],

    [[1, 1, 1],
     [0, 0, 1]],
]

# 게임 화면 설정
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("테트리스")

# 게임 그리드 초기화
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# 블록 클래스
class Block:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def can_move(self, dx, dy):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return False
                    if new_y >= 0 and grid[new_y][new_x]:
                        return False
        return True

    def freeze(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid[self.y + y][self.x + x] = self.color

# 줄 삭제
def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < GRID_HEIGHT:
        grid.insert(0, [0 for _ in range(GRID_WIDTH)])

# 블록 그리기
def draw_block(block):
    for y, row in enumerate(block.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    block.color,
                    (block.x * BLOCK_SIZE + x * BLOCK_SIZE,
                     block.y * BLOCK_SIZE + y * BLOCK_SIZE,
                     BLOCK_SIZE, BLOCK_SIZE)
                )

# 그리드 그리기
def draw_grid():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                pygame.draw.rect(
                    screen,
                    grid[y][x],
                    (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                )
            pygame.draw.rect(
                screen,
                GRAY,
                (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1
            )

# 게임 루프
def main():
    clock = pygame.time.Clock()
    block = Block()
    running = True
    fall_time = 0
    fall_speed = 50  # 블록이 자동으로 내려오는 속도 (밀리초)

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_block(block)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and block.can_move(-1, 0):
                    block.x -= 1
                elif event.key == pygame.K_RIGHT and block.can_move(1, 0):
                    block.x += 1
                elif event.key == pygame.K_DOWN and block.can_move(0, 1):
                    block.y += 1
                elif event.key == pygame.K_UP:
                    block.rotate()
                    if not block.can_move(0, 0):
                        block.rotate()
                        block.rotate()
                        block.rotate()
                elif event.key == pygame.K_SPACE:  # 스페이스바로 블록을 맨 아래로 이동
                    while block.can_move(0, 1):
                        block.y += 1
                    block.freeze()
                    clear_lines()
                    block = Block()
                    if not block.can_move(0, 0):
                        running = False

        fall_time += clock.get_rawtime()
        clock.tick(30)

        # 블록이 자동으로 내려오도록 수정
        if fall_time > fall_speed:
            fall_time = 0
            if block.can_move(0, 1):
                block.y += 1
            else:
                block.freeze()
                clear_lines()
                block = Block()
                if not block.can_move(0, 0):
                    running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()