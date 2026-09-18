"""Pause overlay shown mid-game: resume or return to the main menu."""

import sys

import pygame

_PAUSE_GOLD = (255, 213, 0)


def show_pause_menu(
        screen: pygame.Surface, frame_clock: pygame.time.Clock) -> str:
    """Show the pause overlay. Returns 'resume' or 'menu'"""
    width, height = screen.get_size()
    font_title = pygame.font.SysFont(None, 60, bold=True)
    font_btn = pygame.font.SysFont(None, 32)

    resume_rect = pygame.Rect(width // 2 - 130, height // 2 - 50, 260, 60)
    menu_rect = pygame.Rect(width // 2 - 130, height // 2 + 30, 260, 60)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return "resume"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if resume_rect.collidepoint(pos):
                    return "resume"
                if menu_rect.collidepoint(pos):
                    return "menu"

        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = font_title.render("PAUSED", True, _PAUSE_GOLD)
        screen.blit(
            title, title.get_rect(center=(width // 2, height // 2 - 120)))
        pygame.draw.rect(screen, _PAUSE_GOLD, resume_rect, border_radius=14)
        text = font_btn.render("Resume", True, "black")
        screen.blit(text, text.get_rect(center=resume_rect.center))
        pygame.draw.rect(screen, _PAUSE_GOLD, menu_rect, border_radius=14)
        text = font_btn.render("Main Menu", True, "black")
        screen.blit(text, text.get_rect(center=menu_rect.center))
        pygame.display.update()
        frame_clock.tick(60)
