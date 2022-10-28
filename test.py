import pygame, time

from Modules.gui.OverlayV3 import Overlay

overlay = Overlay(pygame.Rect(10, 10, 500, 500))
overlay.overlaymode()

overlay.show = 1
overlay_mode = 1

time_updated = time.time()
while 1:
    if time_updated + 1 < time.time():
        if overlay_mode:
            overlay.windowmode()
            # overlay.show_fps = False
        else:
            overlay.overlaymode()
            overlay.show_fps = True

        overlay_mode = not overlay_mode
        time_updated = time.time()
        print("updated to", overlay_mode)
    overlay.update()