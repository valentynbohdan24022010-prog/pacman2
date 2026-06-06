import pygame
from pathlib import Path
pygame.init()

WIDTH = 1280 
HEIGHT = 720

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, file_name):
        super().__init__()
        self.image = self.load_image(file_name, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def load_image(self, file_name, size=None):
        path = Path(__file__).parent / file_name
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Enemy(GameSprite):
    def __init__(self, x, y, width, height, file_name, speed, dx, dy):
        super().__init__(x, y, width, height, file_name)
        self.speed = speed
        self.dx = dx
        self.dy = dy
        self.start_x = x
        self.start_y = y
        self.moving_right = True
        self.moving_down = True

    def update(self):
        if self.dx > 0:
            if self.moving_right:
                self.rect.x += self.speed
                if self.rect.x >= self.start_x + self.dx:
                    self.moving_right = False
            else:
                self.rect.x -= self.speed
                if self.rect.x <= self.start_x:
                    self.moving_right = True

        if self.dy > 0:
            if self.moving_down:
                self.rect.y += self.speed
                if self.rect.y >= self.start_y + self.dy:
                    self.moving_down = False
            else:
                self.rect.y -= self.speed
                if self.rect.y <= self.start_y:
                    self.moving_down = True


class Player(GameSprite):
    def __init__(self, x, y, width, height, file_name, speed):
        super().__init__(x, y, width, height, file_name)
        self.speed = speed

    def update(self, keys):
        dx = 0
        dy = 0
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        self.rect.x += dx

        platforms = pygame.sprite.spritecollide(self, walls, False)
        for p in platforms:
            if dx > 0:
                self.rect.right = p.rect.left
            elif dx < 0:
                self.rect.left = p.rect.right

        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        self.rect.y += dy

        platforms = pygame.sprite.spritecollide(self, walls, False)
        for p in platforms:
            if dy > 0:
                self.rect.bottom = p.rect.top
            elif dy < 0:
                self.rect.top = p.rect.bottom

 
    def fire(self):
        bullet = Bullet(self.rect.right, self.rect.centery - 5, 20, 10, "bullet.png", speed=10)
        bullets.add(bullet)


class Bullet(GameSprite):
    def __init__(self, x, y, width, height, file_name, speed=10):
        super().__init__(x, y, width, height, file_name)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
 
        # Видаляємо пулю якщо вона вийшла за межі екрану
        if self.rect.x > WIDTH:
            self.kill()


bg = GameSprite(0, 0, WIDTH, HEIGHT, "bg.jpg")
finish_img = GameSprite(0,0, WIDTH, HEIGHT, 'thumb.jpg')
lose_img = GameSprite(0,0, WIDTH, HEIGHT, 'game-over_1.png')
player = Player(20, 20, 50, 50, "char.png", 5)
finish = GameSprite(1180, 300, 100, 70, "finish.png")


walls = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

enemies.add(
    Enemy(250, 50, 50, 50, "hillichurl.jpg", 3, 180, 0),
    Enemy(600, 440, 50, 50, "hillichurl.jpg", 4, 250, 0),
    Enemy(880, 0, 50, 50, "hillichurl.jpg", 3, 0, 180),
    
    
    Enemy(700, 550, 50, 50, "hillichurl.jpg", 4, 300, 0),
)

walls.add(
    GameSprite(WIDTH // 2 - 150, HEIGHT // 2, 300, 50, 'platform2.png'),
    GameSprite(370, 100, 50, 400, 'platform2_v.png'),
    GameSprite(200, 0, 50, 400, 'platform2_v.png'),
    GameSprite(0, 600, 1300, 50,'platform2.png'),
    GameSprite(600, 0, 50, 400, "platform2_v.png"),
    GameSprite(370, 350, 50, 300, "platform2_v.png"),
    GameSprite(900, 250, 50, 300, "platform2_v.png"), 
    GameSprite(700, 500, 250, 50, "platform2.png"), 
    GameSprite(1050, 100, 50, 450, "platform2_v.png"), 
    GameSprite(1050, 0, 50, 200, "platform2_v.png"),
    
)   
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()
    keys = pygame.key.get_pressed()
    
    bg.show()

    if game_over == False:
        finish.show()
        bullets.update()
        enemies.update()
        player.update(keys)
        walls.draw(window)
        bullets.draw(window)
        enemies.draw(window)
        player.show()
    if(player.rect.colliderect(finish.rect)):
        game_over = True
        finish_img.show()
        
    if(pygame.sprite.spritecollide(player, enemies, False)):
        game_over = True
        lose_img.show()

        


    # --- Колізії пуль ---

    # Пуля + стіна → видаляємо лише пулю
    pygame.sprite.groupcollide(bullets, walls, True, False)

    # Пуля + ворог → видаляємо і пулю, і ворога
    pygame.sprite.groupcollide(bullets, enemies, True, True)

    

    pygame.display.update()
    clock.tick(FPS)