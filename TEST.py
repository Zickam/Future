import pygame
screen = pygame.display.set_mode((410, 220))
def clamp(num, min_value, max_value):
    num = max(min(num, max_value), min_value)
    return num
import time



class LogoDisplayer():
    def __init__(self, Speed, ScreenRes):
        self.Speed = Speed
        self.AnimSpeed = 5
        self.State = 0
        self.res = ScreenRes
        self.delaytime = time.time()

        self.surface = pygame.Surface(self.res)
        self.FLogo = pygame.image.load("Modules/Original.png")
        self.RestLogo = pygame.image.load("Modules/Rest.png")
        self.ScaledF = pygame.transform.scale(self.FLogo, (self.FLogo.get_width() * 0.35, self.FLogo.get_height() * 0.35))
        self.ScaledRest = pygame.transform.scale(self.RestLogo, (self.RestLogo.get_width() * 0.35, self.RestLogo.get_height() * 0.35))


        self.LogoLeftPush = 0
        self.RestLeftPush = 0

        self.rectscale = 0
        self.rectupscale = 0
        self.currspeed = 0

    def Update(self, framedelta, screen):
            if self.State == 0:
                if self.delaytime + 1 < time.time():
                    self.delaytime = time.time()
                    self.State = 1

            if self.State == 1:
                self.currspeed -= (self.currspeed - 100) * framedelta

                if self.LogoLeftPush < 160:
                    self.LogoLeftPush += self.currspeed / self.AnimSpeed
                if self.RestLeftPush < 235:
                    self.RestLeftPush+= self.currspeed / self.AnimSpeed
                if self.rectscale < 200:
                    self.rectscale += self.currspeed / self.AnimSpeed


                if self.rectscale >= 199:

                    self.State = 2

            if self.State == 2:
                self.rectupscale -= (self.rectupscale - 100) * self.currspeed / 1000



            pygame.draw.rect(self.surface, (20, 20, 20), (0, 0, self.res[0], self.res[1]))
            pygame.draw.rect(self.surface, (255, 255, 255), (self.surface.get_width() / 2 - self.rectscale, self.surface.get_height() / 2 + self.ScaledF.get_height() / 2 + 20, self.rectscale * 2, 1))

            pygame.draw.rect(self.surface, (255, 255, 255), (self.surface.get_width() / 2 - 200,
                                                             self.surface.get_height() / 2 + self.ScaledF.get_height() / 2 - self.rectupscale + 21,
                                                             1, self.rectupscale))


            screen.blit(self.surface, (0, 0))


loading = LogoDisplayer(0.3, (410, 220))
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    screen.fill((0, 0, 0))


    loading.Update(0.01, screen)



    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()