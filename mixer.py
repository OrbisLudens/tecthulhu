#!/usr/bin/env python
#
# Title:      Sound playback for Raspberry Pi
# Author:     Martin Brenner
#
# Hardware: using USB audio
# in ~/.asoundrc:
# pcm.!default {
# 	type hw
# 	card 1
# }
# ctl.!default {
# 	type hw
# 	card 1
# }

import pygame
import time

class tsound:

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.sounddir = "sounds/"
        pygame.mixer.music.load(self.sounddir + "backgroundloop1.ogg")
        print "playing music"
        pygame.mixer.music.play(-1)


    def deploy(self):
        sound = pygame.mixer.Sound(self.sounddir + "sfx_resonator_power_up.ogg")
        sound.play()


    def main(self):
        try:  
            self.deploy()
            time.sleep(2)
        except KeyboardInterrupt:
            self.cls(self.ledpixels)
            sys.exit(0)

if __name__ =='__main__':
        audio = tsound()
        audio.main()



