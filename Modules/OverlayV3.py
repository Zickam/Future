import math
import time

import pygame
import win32api
import win32gui
import win32con
import os

class Overlay:
    def __init__(self, rect: pygame.Rect):
        print("[overlay V0.5] > Initializing")
        pygame.init()
        os.environ["SDL_VIDEO_WINDOW_POS"] = str(pygame.display.Info().current_w) + "," + str(pygame.display.Info().current_h)

        # initialize window and make it transparent
        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        self.overlay_hwnd = pygame.display.get_wm_info()["window"]

        # get resolution / position
        self.hwnd_rect = rect

        # move window and make it visible
        win32gui.MoveWindow(self.overlay_hwnd, self.hwnd_rect[0], self.hwnd_rect[1], self.hwnd_rect[2], self.hwnd_rect[3], True)
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)

        # for fps
        self.framecap = 1000
        self.fps = 1
        self.clock = pygame.time.Clock()

        self.show_value = 254
        self.increaser = 1



    def overlaymode(self):
        win32gui.SetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, win32api.RGB(0, 0, 0), 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)

    def windowmode(self):
        win32gui.SetWindowLong(self.overlay_hwnd, 16, win32gui.GetWindowLong(self.overlay_hwnd, 16))
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, win32api.RGB(1, 0, 0), 255, win32con.LWA_COLORKEY | win32con.LWA_COLORKEY)

    def clamp(self, num, min_value, max_value):
        num = max(min(num, max_value), min_value)
        return num

    def show(self):
        if self.show_value >= 254:
            self.increaser = -250 * (1 / self.fps)
        if self.show_value <= 1:
            self.increaser = 250 * (1 / self.fps)
        self.show_value += self.increaser
        pygame.draw.rect(self.screen, (0, self.clamp(self.show_value, 0, 255), 0), (0, 0, self.hwnd_rect[2], self.hwnd_rect[3]), 4)

    def set_cap(self, framecap: int):
        self.framecap = framecap

    def update(self):
        self.clock.tick(self.framecap)
        self.fps = 1 + self.clock.get_fps()

        pygame.display.flip()
        return pygame.event.get()

    def display_fps(self):
        self.font = pygame.font.SysFont("Courier", 20, True, False)
        self.sprite = self.font.render(str(round(self.fps)), True, (255, 255, 0))
        pygame.draw.rect(self.screen, (40, 40, 40), (self.hwnd_rect[2] - self.sprite.get_width() - 5, 5, self.sprite.get_width(), 20))
        self.screen.blit(self.sprite, (self.hwnd_rect[2] - self.sprite.get_width() - 5, 5))


overlay = Overlay(pygame.Rect(100, 100, 100, 100))
overlay.overlaymode()


while True:
    overlay.screen.fill((0, 0, 0))

    pygame.draw.circle(overlay.screen, (255, 255, 255), (50, 50), 30)

    overlay.show()
    overlay.update()
