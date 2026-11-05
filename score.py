from constants import *
import pygame
from logger import log_event

class Score():
    def __init__(self):
        self.current_score: int = 0
        self.high_scores: list[int] = self.read_scores_file()
        self.high_score: int = 0
        if len(self.high_scores) > 0:
            self.high_score = self.high_scores[0]
        self.font = pygame.font.Font(None, 30)

    def increase(self, asteroid_kind: int) -> None:
        self.current_score += ASTEROIDS_SCORE[asteroid_kind]
        if self.high_score < self.current_score:
            self.high_score = self.current_score

    def read_scores_file(self) -> list[int]:
        """
        Read the scores in 'file' and return a them as a list in descending order if present
        Return an empty list if the file is empty or doesn't exist
        """
        scores = []
        try:
            with open(SCORES_FILE, "r") as f:
                scores_txt = f.readlines()
                scores = [int(s[:-1]) for s in scores_txt]
                scores.sort(reverse=True)
        except OSError:
            log_event("[ERROR] Score file doesn't exists")
        except:
            log_event("[ERROR] Score file if wrongly formated")
        return scores
    
    def update_scores(self) -> None:
        """
        Update the scores file with the score after each game.
        Only keep the HIGH_SCORES_TAB_LENGTH bests
        """
        try:
            scores = self.read_scores_file()
            scores.append(self.current_score)
            scores.sort(reverse=True)

            with open(SCORES_FILE, "w") as f:
                f.writelines([str(sc) + "\n" for sc in scores[:HIGH_SCORES_TAB_LENGTH]])
        except OSError:
            log_event("[ERROR] Score file doesn't exists")
        except:
            log_event("[ERROR] Failed to write scores file")

    def draw(self, screen: pygame.Surface) -> None:
        score_text = self.font.render(f"score : {self.current_score}", False, "white")
        high_score_text = self.font.render(f"high score : {self.high_score}", False, "white")
        
        text_x = SCREEN_WIDTH - TEXT_MARGIN_FROM_BORDER
        if score_text.get_width() < high_score_text.get_width():
            text_x -= high_score_text.get_width()
        else:
            text_x -= score_text.get_width()

        screen.blit(high_score_text, (text_x, TEXT_MARGIN_FROM_BORDER ))
        screen.blit(score_text, (text_x, 2 * TEXT_MARGIN_FROM_BORDER + score_text.get_height()))
