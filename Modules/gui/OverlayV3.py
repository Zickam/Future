import pygame
import win32api
import win32gui
import win32con
import os

class Overlay:
    def __init__(self, rect: pygame.Rect):
        print("[overlay V0.6] > Initializing")
        pygame.init()
        os.environ["SDL_VIDEO_WINDOW_POS"] = str(pygame.display.Info().current_w) + "," + str(pygame.display.Info().current_h)

        # initialize window and make it transparent
        self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
        self.overlay_hwnd = pygame.display.get_wm_info()["window"]

        # get resolution / position
        self.winsize = rect
        self.old_winsize = rect

        # for fps
        self.framecap = 1000
        self.fps = 1
        self.clock = pygame.time.Clock()

        self.show_value = 10
        self.increaser = 5

        self.show_fps = False
        self.show = False

        self.overlay_mode = False
        self.window_mode = True

    def draw_fps(self):
        self.show_fps = True

    def overlaymode(self, rect: pygame.Rect):
        # move window and make it visible

        current_rect_pos = list(win32gui.GetWindowRect(self.overlay_hwnd))
        current_rect_pos[2] = current_rect_pos[2] - current_rect_pos[0]
        current_rect_pos[3] = current_rect_pos[3] - current_rect_pos[1]

        self.old_winsize = current_rect_pos
        self.winsize = rect

        win32gui.MoveWindow(self.overlay_hwnd, self.winsize[0], self.winsize[1], self.winsize[2], self.winsize[3], True)
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)

        win32gui.SetWindowLong(self.overlay_hwnd, win32con.WS_EX_LAYERED, win32gui.GetWindowLong(self.overlay_hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(self.overlay_hwnd, win32api.RGB(0, 0, 0), 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
        win32gui.BringWindowToTop(self.overlay_hwnd)
        self.overlay_mode = True
        self.window_mode = False

    def windowmode(self):
        # move window and make it visible

        self.winsize = self.old_winsize
        win32gui.MoveWindow(self.overlay_hwnd, self.winsize[0], self.winsize[1], self.winsize[2], self.winsize[3], True)
        win32gui.ShowWindow(self.overlay_hwnd, win32con.SW_SHOW)


        win32gui.SetWindowLong(self.overlay_hwnd, win32con.WS_EX_LAYERED, win32gui.GetWindowLong(self.overlay_hwnd, -16))
        win32gui.BringWindowToTop(self.overlay_hwnd)
        self.overlay_mode = False
        self.window_mode = True

    def show_window(self):
        self.show = True

    def set_cap(self, framecap: int):
        self.framecap = framecap

    def update(self):
        # print("overlay runs")
        self.clock.tick(self.framecap)
        self.fps = 1 + self.clock.get_fps()
        win32gui.SetWindowPos(self.overlay_hwnd, -1, 0, 0, 0, 0, 2 | 1)

        if self.show_fps:
            self.font = pygame.font.SysFont("Courier", 20, True, False)
            self.sprite = self.font.render(str(round(self.fps)), True, (255, 255, 0))
            pygame.draw.rect(self.screen, (40, 40, 40), (self.winsize[2] - self.sprite.get_width() - 5, 5, self.sprite.get_width(), 20))
            self.screen.blit(self.sprite, (self.winsize[2] - self.sprite.get_width() - 5, 5))

        if self.show:
            if self.show_value >= 250:
                self.increaser = -300 * (1 / self.fps)
            if self.show_value <= 5:
                self.increaser = 300 * (1 / self.fps)
            self.show_value += self.increaser
            pygame.draw.rect(self.screen, (0, max(min(self.show_value, 255), 0), 0), (0, 0, self.winsize[2], self.winsize[3]), 2)


        pygame.display.flip()
        return pygame.event.get()

