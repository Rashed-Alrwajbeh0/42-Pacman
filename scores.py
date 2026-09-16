"""High Scores screen: display the persisted top 10, styled like the
rest of the game's UI."""

import pygame
from sys import exit
from conf import confing
from game import draw_background
from highscore import get_top_10

_GOLD = (255, 213, 0)
_BG_PANEL = (18, 18, 40)


def show_score(screen: pygame.Surface, conf: confing) -> None:
    """Show the top 10 highscores. Press ESC or click to return."""
    frame_clock = pygame.time.Clock()
    title_font = pygame.font.SysFont(None, 56, bold=True)
    header_font = pygame.font.SysFont(None, 28)
    row_font = pygame.font.SysFont(None, 32)

    entries = get_top_10()
    width, height = screen.get_size()
    back_rect = pygame.Rect(width // 2 - 100, height - 100, 200, 56)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and back_rect.collidepoint(event.pos):
                return

        draw_background(screen=screen, image_path="Pictures/8.jpg", alpha=200)

        title = title_font.render("HIGH SCORES", True, _GOLD)
        screen.blit(title, title.get_rect(centerx=width // 2, y=50))

        panel = pygame.Rect(width // 2 - 400, 140, 800, 620)
        pygame.draw.rect(screen, _BG_PANEL, panel, border_radius=18)
        pygame.draw.rect(screen, _GOLD, panel, width=3, border_radius=18)

        header_y = panel.top + 20
        screen.blit(header_font.render("RANK", True, _GOLD), (panel.left + 40, header_y))
        screen.blit(header_font.render("NAME", True, _GOLD), (panel.left + 180, header_y))
        screen.blit(header_font.render("SCORE", True, _GOLD), (panel.right - 160, header_y))
        pygame.draw.line(screen, _GOLD, (panel.left + 20, header_y + 34),
                          (panel.right - 20, header_y + 34), 1)

        row_y = header_y + 50
        if not entries:
            empty = row_font.render("No scores yet — be the first!", True, "white")
            screen.blit(empty, empty.get_rect(centerx=panel.centerx, y=row_y + 20))
        for i, entry in enumerate(entries[:10]):
            color = _GOLD if i < 3 else "white"
            screen.blit(row_font.render(f"{i + 1}.", True, color), (panel.left + 40, row_y))
            screen.blit(row_font.render(entry["name"], True, color), (panel.left + 180, row_y))
            screen.blit(row_font.render(str(entry["score"]), True, color), (panel.right - 160, row_y))
            row_y += 48

        pygame.draw.rect(screen, _GOLD, back_rect, border_radius=14)
        back_label = row_font.render("Back", True, "black")
        screen.blit(back_label, back_label.get_rect(center=back_rect.center))

        pygame.display.update()
        frame_clock.tick(60)