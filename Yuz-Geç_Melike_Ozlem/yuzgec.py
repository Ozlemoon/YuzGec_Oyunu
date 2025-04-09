import pygame
import random
import sys

# Ekran boyutları
SCREEN_WIDTH = 430
SCREEN_HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class YuzGec:
    def __init__(self):
        self.sprite_index = 0
        self.sprite_images = [pygame.image.load(f"sprite_{i}.png") for i in range(7)]
        self.rect = self.sprite_images[0].get_rect(center=(100, 300))
        self.gravity = 0.25
        self.jump_power = 4
        self.jump_pressed = False
        self.y_velocity = 0
        self.animation_speed = 0.3

    def update(self):
        self.animate_sprite()
        if self.jump_pressed:
            self.y_velocity = -self.jump_power
            self.jump_pressed = False
        self.y_velocity += self.gravity
        self.rect.centery += self.y_velocity

    def animate_sprite(self):
        self.sprite_index += self.animation_speed
        if self.sprite_index >= len(self.sprite_images):
            self.sprite_index = 0
        self.rect = self.sprite_images[int(self.sprite_index)].get_rect(center=self.rect.center)

    def jump(self):
        self.jump_pressed = True

class Boru:
    def __init__(self, x):
        gap_height = random.randint(150, 300)
        self.top = pygame.Rect(x, 0, 55, gap_height)
        self.bottom = pygame.Rect(x, gap_height + 150, 55, SCREEN_HEIGHT - gap_height - 150)
        self.passed = False
        self.color = BLUE
        self.x_vel = -2.6

    def move(self):
        self.top.x += self.x_vel
        self.bottom.x += self.x_vel

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.top)
        pygame.draw.rect(screen, self.color, self.bottom)

class Bag:
    def __init__(self, x, y):
        self.image = pygame.image.load("bag.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.x_vel = -2.6
        self.y_vel = random.choice([-1, 1])
        self.allowed_hits = 3

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.y_vel = -self.y_vel

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Food:
    def __init__(self, x, y):
        self.image = pygame.image.load("food.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.x_vel = -2.6
        self.y_vel = random.choice([-1, 1])

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.y_vel = -self.y_vel

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = YuzGec()
        self.borus = []
        self.bags = []
        self.foods = []
        self.boru_timer = 0
        self.bag_timer = 0
        self.food_timer = 0
        self.running = False
        self.space_pressed = False
        self.score = 0
        self.backgrounds = [
            pygame.transform.scale(pygame.image.load("background.gif").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT)),
            pygame.transform.scale(pygame.image.load("background3.webp").convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        ]
        self.start_image = pygame.image.load("message.png").convert_alpha()
        self.heart_image = pygame.image.load("heart.png")
        self.hearts = [self.heart_image for _ in range(3)]
        self.hearts_rect = [self.heart_image.get_rect(topleft=(10 + i * 30, 30)) for i in range(3)]
        self.lives = 3
        self.current_background = 0
        self.bg_x = 0
        self.show_rules()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.running and not self.space_pressed:
                        self.start_game()
                    if event.key == pygame.K_SPACE and self.running:
                        self.player.jump()

            self.move_background()

            if not self.running:
                self.screen.blit(self.start_image, ((SCREEN_WIDTH - self.start_image.get_width()) // 2, (SCREEN_HEIGHT - self.start_image.get_height()) // 2))

            if self.running:
                self.player.update()
                self.spawn_borus()
                self.spawn_bags()
                self.spawn_foods()
                self.move_borus()
                self.move_bags()
                self.move_foods()
                self.check_collision()

            for boru in self.borus:
                boru.draw(self.screen)

            for bag in self.bags:
                bag.draw(self.screen)

            for food in self.foods:
                food.draw(self.screen)

            self.screen.blit(self.player.sprite_images[int(self.player.sprite_index)], self.player.rect)

            self.show_score()

            pygame.display.flip()
            self.clock.tick(60)

    def move_background(self):
        self.bg_x -= 1
        if self.bg_x <= -SCREEN_WIDTH:
            self.bg_x = 0
        self.screen.blit(self.backgrounds[self.current_background], (self.bg_x, 0))
        self.screen.blit(self.backgrounds[self.current_background], (self.bg_x + SCREEN_WIDTH, 0))

    def show_rules(self):
        WIDTH, HEIGHT = 430, 600
        BLUE = (30, 144, 255)
        WHITE = (0, 0, 0)

        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Oyun Kuralları")

        font = pygame.font.SysFont("gabriola", 34)

        rules = [
            "Oyun Kuralları:",
            "",
            "1. Kural:",
            "Eğer balık 3 kere poşete",
            "değerse oyun sonlanır.",
            "2. Kural:",
            "Balık boruya değdiği",
            "an oyun sonlanır.",
            "3. Kural:",
            "Balık yeme değerse",
            "can kazanır.",
            "",
            "Oynamak için:",
            "'Enter' tuşuna basın."
        ]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        print("Oyun başlıyor...")
                        running = False

            screen.fill(BLUE)

            y = 50
            for rule in rules:
                rule_surface = font.render(rule, True, WHITE)
                rule_rect = rule_surface.get_rect(center=(WIDTH//2, y))
                screen.blit(rule_surface, rule_rect)
                y += 40

            pygame.display.flip()

    def start_game(self):
        self.running = True
        self.space_pressed = True
        self.reset_game()

    def reset_game(self):
        self.player.rect.center = (100, 300)
        self.borus.clear()
        self.bags.clear()
        self.foods.clear()
        self.score = 0
        self.lives = 3
        self.hearts_rect = [self.heart_image.get_rect(topleft=(10 + i * 30, 30)) for i in range(3)]
        self.player.jump_pressed = False
        self.space_pressed = False
        self.current_background = 0
        self.bg_x = 0

    def spawn_borus(self):
        self.boru_timer += 1
        if self.boru_timer == 100:
            new_boru = Boru(SCREEN_WIDTH)
            self.borus.append(new_boru)
            self.boru_timer = 0

    def spawn_bags(self):
        self.bag_timer += 1
        if self.bag_timer == 150:
            y = random.randint(50, SCREEN_HEIGHT - 100)
            new_bag = Bag(SCREEN_WIDTH + 120, y)
            self.bags.append(new_bag)
            self.bag_timer = 0

    def spawn_foods(self):
        self.food_timer += 1
        if self.food_timer == 200:
            y = random.randint(50, SCREEN_HEIGHT - 100)
            new_food = Food(SCREEN_WIDTH + 120, y)
            self.foods.append(new_food)
            self.food_timer = 0

    def move_borus(self):
        for boru in self.borus:
            boru.move()
            if boru.top.right < 0:
                self.borus.remove(boru)
                self.score += 1

    def move_bags(self):
        for bag in self.bags:
            bag.move()
            if bag.rect.right < 0:
                self.bags.remove(bag)

    def move_foods(self):
        for food in self.foods:
            food.move()
            if food.rect.right < 0:
                self.foods.remove(food)

    def check_collision(self):
        for boru in self.borus:
            if self.player.rect.colliderect(boru.top) or self.player.rect.colliderect(boru.bottom):
                self.game_over()

        for bag in self.bags:
            if self.player.rect.colliderect(bag.rect):
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over()
                else:
                    self.bags.remove(bag)
                    self.hearts_rect.pop()

        for food in self.foods:
            if self.player.rect.colliderect(food.rect):
                self.lives += 1
                self.foods.remove(food)
                self.hearts.append(self.heart_image)
                self.hearts_rect.append(self.heart_image.get_rect(topleft=(10 + (self.lives - 1) * 30, 30)))

        if self.player.rect.top <= 0 or self.player.rect.bottom >= SCREEN_HEIGHT:
            self.game_over()

    def game_over(self):
        self.running = False
        self.current_background = 0
        high_score = read_high_score()
        if self.score > high_score:
            write_high_score(self.score)
            high_score = self.score
        print("Game Over! Score:", self.score, "High Score:", high_score)

    def show_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        high_score = read_high_score()
        high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
        self.screen.blit(high_score_text, (240, 10))

        for i in range(self.lives):
            self.screen.blit(self.hearts[i], self.hearts_rect[i])

        if not self.running:
            font = pygame.font.Font(None, 48)
            game_over_text = font.render(f"Score: {self.score}!", True, (0, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2))
            self.screen.blit(game_over_text, game_over_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.reset_game()
                self.start_game()

def read_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0

def write_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

if __name__ == "__main__":
    game = Game()
    game.run()
