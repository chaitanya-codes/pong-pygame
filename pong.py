import pygame
import os

pygame.init()
window = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Pong")
background = pygame.image.load(os.path.dirname(__file__) + "\\background.png")
background = pygame.transform.scale(background, (window.get_width(), window.get_height()))

clock = pygame.time.Clock()
deltaTime = 0

class Bat:
    x = 0
    y = 0
    width = 5
    height = 70
    rect = None
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    def draw(self):
        self.rect = pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, self.width, self.height))

class Ball:
    x = 0
    y = 0
    radius = 25
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    def move(self, velocity: list) -> None:
        global score1, score2, ball
        if self.x < bat1.width:
            if bat1.rect.colliderect(pygame.Rect(self.x, self.y, self.radius, self.radius)):
                velocity[0] = -velocity[0]
            else:   
                score2 += 1
                ball = Ball(window.get_width()/2, window.get_height()/2)
        elif self.x > window.get_width()-self.radius:
            if bat2.rect.colliderect(pygame.Rect(self.x, self.y, self.radius, self.radius)):
                velocity[0] = -velocity[0]
            else:
                score1 += 1
                ball = Ball(window.get_width()/2, window.get_height()/2)

        if self.y < 0 or self.y > window.get_height()-self.radius:
            velocity[1] = -velocity[1]
        self.x += velocity[0] * deltaTime
        self.y += velocity[1] * deltaTime
    def draw(self):
        pygame.draw.circle(window, (205, 255, 50), (self.x, self.y), self.radius)

class Text:
    string = ""
    x = 0; y = 0
    text, textRect = None, None
    def __init__(self, string, x, y, size):
        self.string = string
        self.x = x; self.y = y
        font = pygame.font.SysFont("SansSerif.ttf", size)
        self.text = font.render(string, 1, (180, 55, 0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)
    def render(self):
        window.blit(self.text, self.textRect)

bat1 = Bat(0, window.get_height()/2)
bat2 = Bat(window.get_width()-5, window.get_height()/2)
ball = Ball(window.get_width()/2, window.get_height()/2)
score1, score2 = 0, 0
velocity = [400, 340]
batSpeed = 450

playing = False
player = Text("Player", 300, 300, 60)
computer = Text("Computer", 650, 300, 60)
computerPlaying = False

running = True
while running:
    window.fill((0, 0, 0))
    window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not playing:
            playertextrect = player.textRect
            computertextrect = computer.textRect
            if event.pos[0] in range(playertextrect.left, playertextrect.right) and event.pos[1] in range(playertextrect.top, playertextrect.bottom):
                playing = True
            elif event.pos[0] in range(computertextrect.left, computertextrect.right) and event.pos[1] in range(computertextrect.top, computertextrect.bottom):
                playing = True
                computerPlaying = True
    if not playing:
        player.render()
        computer.render()
        pygame.draw.rect(window, (0, 130, 130), player.textRect)
        pygame.draw.rect(window, (0, 130, 130), computer.textRect)
        window.blit(player.text, player.textRect)
        window.blit(computer.text, computer.textRect)
        pygame.display.update()
        continue
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and bat1.y > 0:
        bat1.y -= batSpeed * deltaTime
    elif keys[pygame.K_s] and bat1.y < window.get_height()-bat1.height:
        bat1.y += batSpeed * deltaTime
    if keys[pygame.K_UP] and bat2.y > 0 and not computerPlaying:
        bat2.y -= batSpeed * deltaTime
    elif keys[pygame.K_DOWN] and bat2.y < window.get_height()-bat2.height and not computerPlaying:
        bat2.y += batSpeed * deltaTime

    if computerPlaying:
        if velocity[1] < 0 and bat2.y > 0:
            bat2.y -= (batSpeed-100) * deltaTime
        elif velocity[1] > 0 and bat2.y < window.get_height()-bat2.height:
            bat2.y += (batSpeed-100) * deltaTime

    bat1.draw()
    bat2.draw()
    ball.draw()

    Score1 = Text("Player 1 Score: " + str(score1), 150, 50, 40)
    Score2 = Text("Player 2 Score: " + str(score2), window.get_width()-150, 50, 40)
    Score1.render()
    Score2.render()

    if (score1 >= 3 or score2 >= 3):
        ball = Ball(window.get_width()/2, window.get_height()/2)
        if score1>=3:
            score1 = -1; score2 = 0;
            Score1 = Text("Player 1 wins!", window.get_width()/2, 50, 40)
            Score1.render()
        elif score2>=3:
            score2 = -1; score1 = 0;
            Score2 = Text("Player 2 wins!", window.get_width()/2, 50, 40)
            Score2.render()
        bat1 = Bat(0, window.get_height()/2)
        bat2 = Bat(window.get_width()-5, window.get_height()/2)
        pygame.display.update()
        pygame.time.wait(2000)
    else:
        ball.move(velocity)
    # pygame.image.save(window, "preview.png")
    pygame.display.update()
    deltaTime = clock.tick(165) / 1000