from envVar import *


# Class game
class mainMenu:
    def __init__(self, w, h):

        self.width = w
        self.height = h

        self.game_name = GameNameFont.render(GameName, False, (0, 0, 0))
        self.game_name_rect = self.game_name.get_rect()
        self.game_name_rect.x = int(self.width/2 - self.game_name_rect.width/2)
        self.game_name_rect.y = int(self.height * 0.25)

        self.game_start = GameMenuFont.render("Start", False, (0, 0, 0))
        self.game_start_rect = self.game_start.get_rect()
        self.game_start_rect.x = int(self.width/2 - self.game_start_rect.width/2)
        self.game_start_rect.y = int(self.height * 0.4)

        self.game_option = GameMenuFont.render("Options", False, (0, 0, 0))
        self.game_option_rect = self.game_option.get_rect()
        self.game_option_rect.x = int(self.width/2 - self.game_option_rect.width/2)
        self.game_option_rect.y = int(self.height * 0.45)

        self.game_quit = GameMenuFont.render("Quit", False, (0, 0, 0))
        self.game_quit_rect = self.game_quit.get_rect()
        self.game_quit_rect.x = int(self.width/2 - self.game_quit_rect.width/2)
        self.game_quit_rect.y = int(self.height * 0.50)

    def update(self, screen, is_pausing):
        if is_pausing:
            self.game_start = GameMenuFont.render("Resume", False, (0, 0, 0))
        else:
            self.game_start = GameMenuFont.render("Start", False, (0, 0, 0))

        self.game_start_rect = self.game_start.get_rect()
        self.game_start_rect.x = int(self.width / 2 - self.game_start_rect.width / 2)
        self.game_start_rect.y = int(self.height * 0.4)

        screen.blit(self.game_name, self.game_name_rect)
        screen.blit(self.game_start, self.game_start_rect)
        screen.blit(self.game_option, self.game_option_rect)
        screen.blit(self.game_quit, self.game_quit_rect)

    def check_event(self, event, is_starting, is_pausing, in_configuring):
        running = True

        m_is_starting = is_starting
        m_is_pausing = is_pausing
        m_in_configuring = in_configuring

        # Mouse event - clique left
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
            if self.game_start_rect.collidepoint(pygame.mouse.get_pos()):
                m_is_starting = True
                m_is_pausing = False

            elif self.game_option_rect.collidepoint(pygame.mouse.get_pos()):
                m_in_configuring = True

            elif self.game_quit_rect.collidepoint(pygame.mouse.get_pos()):
                running = False
        return running, m_is_starting, m_is_pausing, m_in_configuring
