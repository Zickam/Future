import pygame

from gui.OverlayV3 import Overlay

overlay = Overlay(pygame.Rect(0, 0, 1500, 800))
overlay.overlaymode()

overlay.show = True
overlay.set_cap(60)

while 1:
    overlay.update()