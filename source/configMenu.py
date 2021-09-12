from envVar import *


# Class game
class configMenu:
    def __init__(self, w, h):
        self.width = w
        self.height = h

        self.FPS_selected = 3
        self.res_selected = 3

        self.name = GameNameFont.render("Option", False, (0, 0, 0))
        self.name_rect = self.name.get_rect()
        self.name_rect.x = int(self.width/2 - self.name_rect.width / 2)
        self.name_rect.y = int(self.height * 0.25)

        self.lessFPS_button = GameMenuFont.render("<-", False, (0, 0, 0))
        self.lessFPS_button_rect = self.lessFPS_button.get_rect()
        self.lessFPS_button_rect.y = int(self.height * 0.4)

        self.limitFPS = GameMenuFont.render("Max FPS: " + str(FPS_available[self.FPS_selected]), False, (0, 0, 0))
        self.limitFPS_rect = self.limitFPS.get_rect()
        self.limitFPS_rect.y = int(self.height * 0.4)

        self.moreFPS_button = GameMenuFont.render("->", False, (0, 0, 0))
        self.moreFPS_button_rect = self.moreFPS_button.get_rect()
        self.moreFPS_button_rect.y = int(self.height * 0.4)

        self.limitFPS_rect.x = int(self.width/2 - self.limitFPS_rect.width/2)
        self.lessFPS_button_rect.x = int(self.limitFPS_rect.x - self.lessFPS_button_rect.width)
        self.moreFPS_button_rect.x = int(self.limitFPS_rect.x +
                                         self.limitFPS_rect.width + self.moreFPS_button_rect.width)

        self.lessRes_button = GameMenuFont.render("<-", False, (0, 0, 0))
        self.lessRes_button_rect = self.lessRes_button.get_rect()
        self.lessRes_button_rect.y = int(self.height * 0.5)

        self.resolution = GameMenuFont.render("Resolution: " + str(resolution_available[self.res_selected]),
                                              False, (0, 0, 0))
        self.resolution_rect = self.resolution.get_rect()
        self.resolution_rect.y = int(self.height * 0.5)

        self.moreRes_button = GameMenuFont.render("->", False, (0, 0, 0))
        self.moreRes_button_rect = self.moreRes_button.get_rect()
        self.moreRes_button_rect.y = int(self.height * 0.5)

        self.resolution_rect.x = int(self.width/2 - self.resolution_rect.width/2)
        self.lessRes_button_rect.x = int(self.resolution_rect.x - self.lessRes_button_rect.width)
        self.moreRes_button_rect.x = int(self.resolution_rect.x +
                                         self.resolution_rect.width + self.moreRes_button_rect.width)

        self.back_button = GameMenuFont.render("Back", False, (0, 0, 0))
        self.back_button_rect = self.back_button.get_rect()
        self.back_button_rect.x = int(self.width/2 - self.back_button_rect.width/2)
        self.back_button_rect.y = int(self.height * 0.6)

    def update(self, screen):
        screen.blit(self.name, self.name_rect)
        screen.blit(self.lessFPS_button, self.lessFPS_button_rect)
        screen.blit(self.limitFPS, self.limitFPS_rect)
        screen.blit(self.moreFPS_button, self.moreFPS_button_rect)
        screen.blit(self.lessRes_button, self.lessRes_button_rect)
        screen.blit(self.resolution, self.resolution_rect)
        screen.blit(self.moreRes_button, self.moreRes_button_rect)
        screen.blit(self.back_button, self.back_button_rect)

    def check_event(self, event):
        # Mouse event - clique left
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            if self.back_button_rect.collidepoint(pygame.mouse.get_pos()):
                return resolution_available[self.res_selected]

            elif self.lessFPS_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.FPS_selected > 0:
                    self.FPS_selected -= 1
                    self.limitFPS = GameMenuFont.render("Max FPS: " + str(FPS_available[self.FPS_selected]),
                                                        False, (0, 0, 0))

            elif self.moreFPS_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.FPS_selected < len(FPS_available) - 1:
                    self.FPS_selected += 1
                    self.limitFPS = GameMenuFont.render("Max FPS: " + str(FPS_available[self.FPS_selected]),
                                                        False, (0, 0, 0))

            elif self.lessRes_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.res_selected > 0:
                    self.res_selected -= 1
                    self.resolution = GameMenuFont.render("Resolution: " + str(resolution_available[self.res_selected]),
                                                          False, (0, 0, 0))

            elif self.moreRes_button_rect.collidepoint(pygame.mouse.get_pos()):
                if self.res_selected < len(resolution_available) - 1:
                    self.res_selected += 1
                    self.resolution = GameMenuFont.render("Resolution: " + str(resolution_available[self.res_selected]),
                                                          False, (0, 0, 0))

        return "NULL"
