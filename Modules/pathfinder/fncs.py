import pygame

class Button():
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
        pygame.font.init()
        self.font = pygame.font.SysFont("Microsoft Sans Serif", 20, False, False)
        self.MBDown = False
        self.State = False
        self.Size = (140, 25)

    def Update(self, mousepos, screen):
        button = pygame.draw.rect(screen, (50, 20, 200), (self.pos[0], self.pos[1], self.Size[0], self.Size[1]))
        if self.State == True:
            pygame.draw.rect(screen, (50, 50, 50), (self.pos[0]+2, self.pos[1]+2, self.Size[0]-4, self.Size[1]-4))
        else:
            pygame.draw.rect(screen, (100, 100, 100), (self.pos[0]+2, self.pos[1]+2, self.Size[0]-4, self.Size[1]-4))
        rect = self.font.render(str(self.name), True, (200, 200, 200,))
        screen.blit(rect, (button.centerx - rect.get_width() / 2, button.centery - rect.get_height() / 2))





        if mousepos[0] > self.pos[0] and mousepos[0] < self.pos[0] + self.Size[0] and mousepos[1] > self.pos[1] and mousepos[1] < self.pos[1] + self.Size[1]:
            if pygame.mouse.get_pressed()[0] == True:
                self.MBDown = True
            if pygame.mouse.get_pressed()[0] == False and self.MBDown == True:
                self.MBDown = False
                self.State = not self.State
                return self.State
        else:
            self.MBDown = False