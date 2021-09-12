from envVar import *


# Class game
class SoundMenu:
    def __init__(self, w, h):
        self.width = w
        self.height = h

        self.volume_value = 100
        self.music_volume_value = 100
        self.sound_effect_volume_value = 100

        self.name = GameNameFont.render("Sound", False, (0, 0, 0))
        self.name_rect = self.name.get_rect()
        self.name_rect.x = int(self.width / 2 - self.name_rect.width / 2)
        self.name_rect.y = int(self.height * 0.25)

        self.less_volume_button = GameMenuFont.render("<-", False, (0, 0, 0))
        self.less_volume_button_rect = self.less_volume_button.get_rect()
        self.less_volume_button_rect.y = int(self.height * 0.4)

        self.volume = GameMenuFont.render("Volume : " + str(self.volume_value), False, (0, 0, 0))
        self.volume_rect = self.volume.get_rect()
        self.volume_rect.y = int(self.height * 0.4)

        self.more_volume_button = GameMenuFont.render("->", False, (0, 0, 0))
        self.more_volume_button_rect = self.more_volume_button.get_rect()
        self.more_volume_button_rect.y = int(self.height * 0.4)

        self.volume_rect.x = int(self.width / 2 - self.volume_rect.width / 2)
        self.less_volume_button_rect.x = int(self.volume_rect.x - self.less_volume_button_rect.width)
        self.more_volume_button_rect.x = int(self.volume_rect.x +
                                             self.volume_rect.width + self.more_volume_button_rect.width)

        self.less_volume_music_button = GameMenuFont.render("<-", False, (0, 0, 0))
        self.less_volume_music_button_rect = self.less_volume_music_button.get_rect()
        self.less_volume_music_button_rect.y = int(self.height * 0.5)

        self.volume_music = GameMenuFont.render("Music: " + str(self.music_volume_value), False, (0, 0, 0))
        self.volume_music_rect = self.volume_music.get_rect()
        self.volume_music_rect.y = int(self.height * 0.5)

        self.more_volume_music_button = GameMenuFont.render("->", False, (0, 0, 0))
        self.more_volume_music_button_rect = self.more_volume_music_button.get_rect()
        self.more_volume_music_button_rect.y = int(self.height * 0.5)

        self.volume_music_rect.x = int(self.width / 2 - self.volume_music_rect.width / 2)
        self.less_volume_music_button_rect.x = int(self.volume_music_rect.x - self.less_volume_music_button_rect.width)
        self.more_volume_music_button_rect.x = int(self.volume_music_rect.x +
                                                   self.volume_music_rect.width +
                                                   self.more_volume_music_button_rect.width)

        self.less_volume_sound_effect_button = GameMenuFont.render("<-", False, (0, 0, 0))
        self.less_volume_sound_effect_button_rect = self.less_volume_sound_effect_button.get_rect()
        self.less_volume_sound_effect_button_rect.y = int(self.height * 0.6)

        self.volume_sound_effect = GameMenuFont.render("Sound effect: " +
                                                       str(self.sound_effect_volume_value), False, (0, 0, 0))
        self.volume_sound_effect_rect = self.volume_sound_effect.get_rect()
        self.volume_sound_effect_rect.y = int(self.height * 0.6)

        self.more_volume_sound_effect_button = GameMenuFont.render("->", False, (0, 0, 0))
        self.more_volume_sound_effect_button_rect = self.more_volume_sound_effect_button.get_rect()
        self.more_volume_sound_effect_button_rect.y = int(self.height * 0.6)

        self.volume_sound_effect_rect.x = int(self.width / 2 - self.volume_sound_effect_rect.width / 2)
        self.less_volume_sound_effect_button_rect.x = int(self.volume_sound_effect_rect.x -
                                                          self.less_volume_sound_effect_button_rect.width)
        self.more_volume_sound_effect_button_rect.x = int(self.volume_sound_effect_rect.x +
                                                          self.volume_sound_effect_rect.width +
                                                          self.more_volume_sound_effect_button_rect.width)

        self.back_button = GameMenuFont.render("Back", False, (0, 0, 0))
        self.back_button_rect = self.back_button.get_rect()
        self.back_button_rect.x = int(self.width / 2 - self.back_button_rect.width / 2)
        self.back_button_rect.y = int(self.height * 0.7)

    def update(self, screen):
        screen.blit(self.name, self.name_rect)

        screen.blit(self.less_volume_button, self.less_volume_button_rect)
        screen.blit(self.volume, self.volume_rect)
        screen.blit(self.more_volume_button, self.more_volume_button_rect)

        screen.blit(self.less_volume_music_button, self.less_volume_music_button_rect)
        screen.blit(self.volume_music, self.volume_music_rect)
        screen.blit(self.more_volume_music_button, self.more_volume_music_button_rect)

        screen.blit(self.less_volume_sound_effect_button, self.less_volume_sound_effect_button_rect)
        screen.blit(self.volume_sound_effect, self.volume_sound_effect_rect)
        screen.blit(self.more_volume_sound_effect_button, self.more_volume_sound_effect_button_rect)

        screen.blit(self.back_button, self.back_button_rect)

    def check_event(self, event):
        # Mouse event - clique left
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            if self.back_button_rect.collidepoint(pygame.mouse.get_pos()):
                return False

            elif self.less_volume_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.volume_value > 0:
                    self.volume_value -= 10
                    self.volume = GameMenuFont.render("Volume: " + str(self.volume_value), False, (0, 0, 0))

            elif self.more_volume_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.volume_value < 100:
                    self.volume_value += 10
                    self.volume = GameMenuFont.render("Volume: " + str(self.volume_value), False, (0, 0, 0))

            elif self.less_volume_music_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.music_volume_value > 0:
                    self.music_volume_value -= 10
                    self.volume_music = GameMenuFont.render("Music: " + str(self.music_volume_value),
                                                            False, (0, 0, 0))

            elif self.more_volume_music_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.music_volume_value < 100:
                    self.music_volume_value += 10
                    self.volume_music = GameMenuFont.render("Music: " + str(self.music_volume_value),
                                                            False, (0, 0, 0))

            elif self.less_volume_sound_effect_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.sound_effect_volume_value > 0:
                    self.sound_effect_volume_value -= 10
                    self.volume_sound_effect = GameMenuFont.render("Sound effect: " +
                                                                   str(self.sound_effect_volume_value),
                                                                   False, (0, 0, 0))

            elif self.more_volume_sound_effect_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.sound_effect_volume_value < 100:
                    self.sound_effect_volume_value += 10
                    self.volume_sound_effect = GameMenuFont.render("Sound effect: " +
                                                                   str(self.sound_effect_volume_value),
                                                                   False, (0, 0, 0))

            main_sound.set_volume(self.volume_value / 100 * self.music_volume_value / 100)

            for sound in sound_end:
                sound_end[sound].set_volume(self.volume_value / 100 * self.sound_effect_volume_value / 100)

        return True
