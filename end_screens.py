"""Win/lose screens: show the result, take a name if it's a highscore,
then offer clickable buttons to continue."""

import sys
import pygame

_BG = (8, 8, 18)
_GOLD = (255, 213, 0)


def _frame(screen: pygame.Surface, color: tuple[int, int, int]) -> None:
    """Draw a glowing border frame around the whole screen."""
    rect = screen.get_rect().inflate(-40, -40)
    pygame.draw.rect(
        screen,
        tuple(c // 4 for c in color),
        rect.inflate(10, 10),
        width=6,
        border_radius=24)
    pygame.draw.rect(screen, color, rect, width=3, border_radius=20)


def _button(screen: pygame.Surface, rect: pygame.Rect, text: str,
            font: pygame.font.Font, color: tuple[int, int, int]) -> None:
    """Draw one glowing, filled, rounded button with centered text."""
    pygame.draw.rect(
        screen,
        tuple(c // 4 for c in color), rect.inflate(8, 8), border_radius=18)
    pygame.draw.rect(screen, color, rect, border_radius=14)
    label = font.render(text, True, "black")
    screen.blit(label, label.get_rect(center=rect.center))


def _end_screen(
        screen: pygame.Surface, title: str, title_color: tuple[int, int, int],
        score: int, is_top_10: bool, continue_label: str | None,
) -> tuple[str, str | None]:
    """Shared logic for both end screens."""
    clock = pygame.time.Clock()
    width, height = screen.get_size()
    big_font = pygame.font.SysFont(None, 76, bold=True)
    font = pygame.font.SysFont(None, 32)

    name = ""
    typing = is_top_10

    buttons = [("menu", "Main Menu", (200, 200, 210))]
    if continue_label:
        buttons.insert(0, ("continue", continue_label, _GOLD))

    panel = pygame.Rect(0, 0, 700, 460)
    panel.center = (width // 2, height // 2)

    btn_w, btn_h, gap = 220, 60, 24
    total_w = len(buttons) * btn_w + (len(buttons) - 1) * gap
    start_x = panel.centerx - total_w // 2
    rects = [
        (action, label, color, pygame.Rect(
            start_x + i * (btn_w + gap), panel.bottom - 90, btn_w, btn_h))
        for i, (action, label, color) in enumerate(buttons)
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if typing and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 10 and event.unicode.isalnum():
                    name += event.unicode
            if not typing and event.type == pygame.MOUSEBUTTONDOWN:
                for action, _label, _color, rect in rects:
                    if rect.collidepoint(event.pos):
                        return action, (name.strip() or None)

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        _frame(screen, title_color)

        title_surf = big_font.render(title, True, title_color)
        shadow = big_font.render(
            title,
            True,
            tuple(c // 4 for c in title_color))
        screen.blit(
            shadow,
            shadow.get_rect(centerx=panel.centerx + 3, y=panel.top + 30))
        screen.blit(
            title_surf,
            title_surf.get_rect(centerx=panel.centerx, y=panel.top + 27))

        score_surf = font.render(f"Final Score: {score:,}", True, "white")
        screen.blit(
            score_surf,
            score_surf.get_rect(centerx=panel.centerx, y=panel.top + 120))

        if typing:
            hint = font.render(
                "New highscore! Type your name + Enter:",
                True,
                _GOLD)
            screen.blit(
                hint,
                hint.get_rect(centerx=panel.centerx, y=panel.top + 190))
            box = pygame.Rect(0, 0, 320, 54)
            box.center = (panel.centerx, panel.top + 260)
            pygame.draw.rect(screen, (28, 28, 50), box, border_radius=12)
            pygame.draw.rect(screen, _GOLD, box, width=2, border_radius=12)
            entry = font.render(name, True, "white")
            screen.blit(entry, entry.get_rect(center=box.center))
        else:
            for _action, label, color, rect in rects:
                _button(screen, rect, label, font, color)

        pygame.display.update()
        clock.tick(60)


def show_game_over(
        screen: pygame.Surface,
        score: int,
        is_top_10: bool) -> tuple[str, str | None]:
    """Show the Game Over screen. Returns ("replay"/"menu", name)."""
    return _end_screen(
        screen,
        "YOU LOST",
        (220, 60, 60),
        score, is_top_10,
        "Play Again")


def show_victory(
        screen: pygame.Surface,
        score: int,
        is_top_10: bool,
        has_next_level: bool,
) -> tuple[str, str | None]:
    """Show the Victory screen. Returns ("continue"/"menu", name)."""
    label = "Next Level" if has_next_level else None
    return _end_screen(screen,
                       "YOU WIN!",
                       (100, 220, 120),
                       score,
                       is_top_10,
                       label)
