"""
MakeyMakey 반응속도 게임
왼쪽/오른쪽 화살표(호일 버튼)로 플레이합니다.

준비:
- EARTH: 손 또는 접지 패드
- LEFT 핀 -> 왼쪽 호일 버튼
- RIGHT 핀 -> 오른쪽 호일 버튼

조작:
- 화면에 "LEFT!" 가 뜨면 왼쪽 호일을 터치
- 화면에 "RIGHT!" 가 뜨면 오른쪽 호일을 터치
- 반응 시간(초)이 기록되고, 5라운드 후 평균 기록을 보여줍니다.
"""

import pygame
import random
import sys
import time

# ---------- 설정 ----------
WIDTH, HEIGHT = 640, 400
ROUNDS = 5
MIN_DELAY = 1.0   # 자극이 뜨기 전 최소 대기 시간(초)
MAX_DELAY = 3.0   # 자극이 뜨기 전 최대 대기 시간(초)

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (220, 60, 60)
BLUE = (60, 100, 220)
GREEN = (60, 180, 100)
GRAY = (150, 150, 150)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MakeyMakey 반응속도 게임")

# 한글 지원 폰트 찾기 (없으면 기본 폰트로 대체 -> 이 경우 한글이 깨질 수 있음)
def find_korean_font():
    candidates = [
        "applegothic",      # macOS 기본 한글 폰트
        "applesdgothicneo",
        "malgungothic",     # Windows
        "notosanscjkkr",
        "nanumgothic",
    ]
    available = pygame.font.get_fonts()
    for name in candidates:
        if name in available:
            return name
    return None

_korean_font = find_korean_font()

def make_font(size):
    if _korean_font:
        return pygame.font.SysFont(_korean_font, size)
    return pygame.font.SysFont(None, size)

font_big = make_font(80)
font_mid = make_font(40)
font_small = make_font(28)
clock = pygame.time.Clock()


def draw_center_text(text, font, color, y_offset=0):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(surface, rect)


def wait_screen(message, sub_message="", color=WHITE):
    screen.fill(BLACK)
    draw_center_text(message, font_mid, color, -20)
    if sub_message:
        draw_center_text(sub_message, font_small, GRAY, 30)
    pygame.display.flip()


def run_round(round_num):
    """한 라운드를 실행하고 반응 시간(초)을 반환. 잘못 누르면 None 반환."""
    direction = random.choice(["LEFT", "RIGHT"])
    key_map = {"LEFT": pygame.K_LEFT, "RIGHT": pygame.K_RIGHT}
    wrong_key = pygame.K_RIGHT if direction == "LEFT" else pygame.K_LEFT

    # 대기 화면 (너무 빨리 누르면 반칙)
    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    start_wait = time.time()
    while time.time() - start_wait < delay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in key_map.values():
                wait_screen("너무 빨랐어요!", "자극이 뜰 때까지 기다리세요", RED)
                pygame.display.flip()
                pygame.time.wait(1000)
                return None
        wait_screen(f"라운드 {round_num}/{ROUNDS}", "준비하세요...", GRAY)
        clock.tick(60)

    # 자극 표시 + 시간 측정 시작
    stim_color = RED if direction == "LEFT" else BLUE
    screen.fill(BLACK)
    draw_center_text(f"{direction}!", font_big, stim_color)
    pygame.display.flip()
    stim_time = time.time()

    # 입력 대기
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == key_map[direction]:
                    reaction_time = time.time() - stim_time
                    return reaction_time
                elif event.key == wrong_key:
                    wait_screen("반대 방향이에요!", "", RED)
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    return None
        clock.tick(60)


def show_results(times):
    valid_times = [t for t in times if t is not None]
    screen.fill(BLACK)
    if valid_times:
        avg = sum(valid_times) / len(valid_times)
        best = min(valid_times)
        draw_center_text("결과", font_mid, GREEN, -80)
        draw_center_text(f"평균 반응시간: {avg*1000:.0f} ms", font_small, WHITE, -20)
        draw_center_text(f"최고 기록: {best*1000:.0f} ms", font_small, WHITE, 20)
        draw_center_text(f"성공: {len(valid_times)}/{ROUNDS}", font_small, WHITE, 60)
    else:
        draw_center_text("기록된 반응이 없어요", font_mid, RED)
    draw_center_text("ESC를 눌러 종료", font_small, GRAY, 120)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        clock.tick(30)


def main():
    wait_screen("MakeyMakey 반응속도 게임", "아무 키나 눌러 시작", WHITE)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(30)

    results = []
    for i in range(1, ROUNDS + 1):
        result = run_round(i)
        results.append(result)

    show_results(results)


if __name__ == "__main__":
    main()