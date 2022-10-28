import pygame

screen = pygame.display.set_mode((430, 412), pygame.NOFRAME)

pygame.font.init()

class holder:
    def __init__(self, pos, size, items, name):
        self.pos = pos
        self.size = size
        self.items = items

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.font = pygame.font.SysFont("Microsoft Sans Serif", 13, False, False)
        self.sprite = self.font.render(str(name), True, (200, 200, 200))
        self.render_surf = pygame.Surface((self.size[0] - 20, self.size[1] - 30))

        self.item_height = 5 + len(items) * 20
        if self.item_height > self.size[1]:
            self.scrollbar = True
        else:
            self.scrollbar = False

        # 0 - 100
        self.scroll_state = 0

        # scroll bar multiplier
        self.scroll_mult1 = (self.size[1] - 65) / 100

        # item scroll multiplier
        self.scroll_mult2 = abs(self.item_height - self.size[1] + 20) / 100

        self.color_dark = 25, 25, 25
        self.color_bright = 40, 40, 40
        self.color_bright2 = 70, 70, 70

    def update(self, mousepos, globalevent):

        pygame.draw.rect(screen,self.color_dark, (self.pos[0], self.pos[1] + 10, self.size[0], self.size[1] - 10))
        screen.blit(self.sprite, (self.pos[0] + 10, self.pos[1] + 10 - self.sprite.get_height() / 2))

        pointslist = (self.pos[0] + 5, self.pos[1] + 10), (self.pos[0], self.pos[1] + 10), (self.pos[0], self.pos[1] + self.size[1]), (self.pos[0] + self.size[0], self.pos[1] + self.size[1]), (self.pos[0] + self.size[0], self.pos[1] + 10), (self.pos[0] + 15 + self.sprite.get_width(), self.pos[1] + 10)

        pygame.draw.lines(screen, self.color_bright, False, pointslist)

        if self.scrollbar:
            pygame.draw.rect(screen, self.color_bright, (self.pos[0] + self.size[0] - 10, self.pos[1] + 10, 10, self.size[1] - 10))

            pygame.draw.rect(screen,self.color_bright2, (self.pos[0] + self.size[0] - 7, self.pos[1] + 13 + self.scroll_state * self.scroll_mult1, 5, 50), border_radius=50)

            if self.rect.collidepoint(mousepos[0], mousepos[1]):
                for event in globalevent:
                    if event.type == pygame.MOUSEWHEEL:
                        if self.scroll_state > 0 and event.y > 0:
                            self.scroll_state -= event.y * 10

                        if self.scroll_state < 100 and event.y < 0:
                            self.scroll_state -= event.y * 10

                if self.scroll_state < 0:
                    self.scroll_state = 0

                if self.scroll_state > self.size[1] - 65:
                    self.scroll_state = self.size[1] - 65

        self.render_surf.fill((self.color_dark))
        for i in range(0, len(self.items)):
            sprite = self.font.render(str(self.items[i]), True, (200, 200, 200))
            self.render_surf.blit(sprite, (10, i * 20 - self.scroll_state * self.scroll_mult2))
        screen.blit(self.render_surf, (self.pos[0] + 10, self.pos[1] + 20))


holdlist = []
holdlist.append(holder((10, 3), (200, 200), ["Aimbot", "Enemy", "Team", "Multipoint", "Damage", "Test", "Thirdperson", "ESP", "Bunny hop", "Box", "Bones", "Triggerbot", "Grenade Prediction", "Almasz", "Aimbot", "Enemy", "Team", "Multipoint", "Damage", "Test", "Thirdperson", "ESP", "Bunny hop", "Box", "Bones", "Triggerbot", "Grenade Prediction", "Almasz"], "Settings"))
holdlist.append(holder((220, 3), (200, 400), ["Aimbot", "Enemy", "Team", "Multipoint", "Damage", "Test", "Thirdperson", "ESP", "Bunny hop", "Box", "Bones", "Triggerbot", "Grenade Prediction", "Almasz"], "Settings"))

while True:
    globalevent = pygame.event.get()
    screen.fill((15, 15, 15))

    for i in range(0, len(holdlist)):
        holdlist[i].update(pygame.mouse.get_pos(), globalevent)

    pygame.display.flip()
    for event in globalevent:
        if event.type == pygame.QUIT:
            pygame.quit()