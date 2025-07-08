import pygame
import random
import time
import os

pygame.font.init()

WIDTH, HEIGHT = 1200, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Falling Objects")

BG = pygame.image.load("bg.jpeg")
PLAYER_IMG = pygame.image.load("aircraft.png")
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, (60, 60))


PLAYER_WIDTH, PLAYER_HEIGHT = 60, 60
PLAYER_VEL = 5

METEOR_WIDTH, METEOR_HEIGHT = 20, 30
METEOR_VEL = 3
METEOR_IMG = pygame.image.load("meteor.png")
METEOR_IMG = pygame.transform.scale(METEOR_IMG, (METEOR_WIDTH, METEOR_HEIGHT))

FONT = pygame.font.SysFont("comicsans", 30)
BIG_FONT = pygame.font.SysFont("comicsans", 60)

HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

def draw(player, elapsed_time, meteor_list, score, highscore, shield_rect, shield_active, speed_rect, speed_active, lives, paused):
    WIN.blit(BG, (0, 0))
    WIN.blit(PLAYER_IMG, (player.x, player.y))
    time_text = FONT.render(f"Time Survived: {elapsed_time:.2f}s", 1, "white")
    score_text = FONT.render(f"Score: {score}", 1, "yellow")
    highscore_text = FONT.render(f"High Score: {highscore}", 1, "cyan")
    lives_text = FONT.render(f"Lives: {lives}", 1, "red")
    WIN.blit(time_text, (10, 10))
    WIN.blit(score_text, (10, 40))
    WIN.blit(highscore_text, (10, 70))
    WIN.blit(lives_text, (10, 100))
    for meteor in meteor_list:
        WIN.blit(METEOR_IMG, (meteor.x, meteor.y))
    if shield_rect and not shield_active:
        pygame.draw.ellipse(WIN, (0, 200, 255), shield_rect)
    if shield_active:
        pygame.draw.circle(WIN, (0, 200, 255), player.center, PLAYER_WIDTH // 2 + 10, 4)
    if speed_rect and not speed_active:
        pygame.draw.ellipse(WIN, (0, 255, 0), speed_rect)
    if speed_active:
        speed_text = FONT.render("SPEED!", 1, "green")
        WIN.blit(speed_text, (player.x, player.y - 30))
    if paused:
        pause_text = BIG_FONT.render("PAUSED", 1, "white")
        WIN.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))
    pygame.display.update()

def handle_player_movement(keys, player, player_vel):
    if keys[pygame.K_LEFT] and player.x - player_vel >= 0:
        player.x -= player_vel
    if keys[pygame.K_RIGHT] and player.x + player_vel + PLAYER_WIDTH <= WIDTH:
        player.x += player_vel
    if keys[pygame.K_UP] and player.y - player_vel >= 0:
        player.y -= player_vel
    if keys[pygame.K_DOWN] and player.y + player_vel + PLAYER_HEIGHT <= HEIGHT:
        player.y += player_vel

def main_menu():
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title = BIG_FONT.render("Meteor Doge", 1, "yellow")
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 200))
        start_text = FONT.render("Press SPACE to Start", 1, "white")
        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 100))
        instr1 = FONT.render("Arrow Keys: Move", 1, "white")
        instr2 = FONT.render("P: Pause", 1, "white")
        instr3 = FONT.render("Collect blue for shield, green for speed!", 1, "cyan")
        instr4 = FONT.render("Avoid Meteors! You have 3 lives.", 1, "red")
        instr5 = FONT.render("Press ESC to Quit", 1, "white")
        WIN.blit(instr1, (WIDTH // 2 - instr1.get_width() // 2, HEIGHT // 2))
        WIN.blit(instr2, (WIDTH // 2 - instr2.get_width() // 2, HEIGHT // 2 + 40))
        WIN.blit(instr3, (WIDTH // 2 - instr3.get_width() // 2, HEIGHT // 2 + 80))
        WIN.blit(instr4, (WIDTH // 2 - instr4.get_width() // 2, HEIGHT // 2 + 120))
        WIN.blit(instr5, (WIDTH // 2 - instr5.get_width() // 2, HEIGHT // 2 + 160))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return False

def main():
    if not main_menu():
        return

    run = True
    player = pygame.Rect(WIDTH // 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    meteor_add_increment = 2000
    last_meteor_add_time = pygame.time.get_ticks()
    meteor_list = []
    hit = False
    score = 0
    highscore = load_highscore()
    lives = 3

    # Power-up variables
    shield_rect = None
    shield_active = False
    shield_timer = 0
    SHIELD_DURATION = 4000  # ms

    speed_rect = None
    speed_active = False
    speed_timer = 0
    SPEED_DURATION = 3000  # ms
    player_vel = PLAYER_VEL

    paused = False

    while run:
        clock.tick(120)
        if not paused:
            elapsed_time = time.time() - start_time

        current_time = pygame.time.get_ticks()
        if not paused and current_time - last_meteor_add_time >= meteor_add_increment:
            for _ in range(5):
                meteor_x = random.randint(0, WIDTH - METEOR_WIDTH)
                meteor = pygame.Rect(meteor_x, -100, METEOR_WIDTH, METEOR_HEIGHT)
                meteor_list.append(meteor)
            last_meteor_add_time = current_time

            # Randomly spawn shield power-up
            if not shield_rect and random.random() < 0.15:
                shield_x = random.randint(0, WIDTH - 40)
                shield_rect = pygame.Rect(shield_x, -100, 40, 40)
            # Randomly spawn speed power-up
            if not speed_rect and random.random() < 0.10:
                speed_x = random.randint(0, WIDTH - 40)
                speed_rect = pygame.Rect(speed_x, -100, 40, 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if paused:
            draw(player, elapsed_time, meteor_list, score, highscore, shield_rect, shield_active, speed_rect, speed_active, lives, paused)
            continue

        keys = pygame.key.get_pressed()
        handle_player_movement(keys, player, player_vel)

        for meteor in meteor_list[:]:
            meteor.y += METEOR_VEL
            if meteor.y > HEIGHT:
                meteor_list.remove(meteor)
                score += 1
            elif meteor.colliderect(player):
                if shield_active:
                    meteor_list.remove(meteor)
                else:
                    meteor_list.remove(meteor)
                    lives -= 1
                    if lives <= 0:
                        hit = True
                        run = False
                        break

        # Shield power-up logic
        if shield_rect:
            shield_rect.y += METEOR_VEL
            if shield_rect.y > HEIGHT:
                shield_rect = None
            elif shield_rect.colliderect(player):
                shield_active = True
                shield_timer = pygame.time.get_ticks()
                shield_rect = None

        if shield_active and pygame.time.get_ticks() - shield_timer > SHIELD_DURATION:
            shield_active = False

        # Speed power-up logic
        if speed_rect:
            speed_rect.y += METEOR_VEL
            if speed_rect.y > HEIGHT:
                speed_rect = None
            elif speed_rect.colliderect(player):
                speed_active = True
                speed_timer = pygame.time.get_ticks()
                speed_rect = None
                player_vel = PLAYER_VEL * 2

        if speed_active and pygame.time.get_ticks() - speed_timer > SPEED_DURATION:
            speed_active = False
            player_vel = PLAYER_VEL

        draw(player, elapsed_time, meteor_list, score, highscore, shield_rect, shield_active, speed_rect, speed_active, lives, paused)

        if hit:
            if score > highscore:
                save_highscore(score)
                highscore = score
            lost_text = BIG_FONT.render("Game Over!", 1, "red")
            WIN.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2 - lost_text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            restart = True
            while restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            main()
                            return
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return
                restart_text = FONT.render("Press R to Restart or ESC to Quit", 1, "white")
                WIN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 60))
                pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
