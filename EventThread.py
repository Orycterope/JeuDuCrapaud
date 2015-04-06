__author__ = 'thomas'
from threading import Thread
import pygame
from pygame.locals import *


class EventThread(Thread):

    def __init__(self, fen, queue):
        Thread.__init__(self)
        self.fen = fen
        self.queue = queue
        self.closing = False

    def run(self):

        while True:
            event = pygame.event.wait()
            if event.type == MOUSEMOTION:
                continue
            if event.type == QUIT:
                self.stop()
            if event.type == KEYDOWN:
                self.queue.put(event)
                if event.key == K_z:
                    break

        if self.fen.closing == False:
            self.fen.fermer()

    def stop(self):
        # On lance un event pour débloquer toutes les boucles qui sont en stand-by
        evt = pygame.event.Event(KEYDOWN, {'scancode': 113, 'unicode': 'z', 'mod': 4096, 'key': K_z})
        pygame.event.post(evt)
        self.closing = True

