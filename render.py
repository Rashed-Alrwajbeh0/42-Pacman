"""Background rendering, cached so images aren't rescaled every frame."""

import pygame

_BACKGROUND_CACHE: dict[tuple[str, tuple[int, int]], pygame.Surface] = {}


def draw_background(
        screen: pygame.Surface,
        image_path: str,
        alpha: int = 50,
        base_color: tuple[int, int, int] = (8, 10, 28)) -> None:
    """Fill the screen with a base color, then blend a background image
    on top of it (cached so it isn't rescaled every single frame).

    ``base_color`` is the deep navy tone showing through the transparent
    image and also used as a safe fallback if the image can't be loaded,
    so a missing/corrupt asset never crashes the game.
    """
    screen.fill(base_color)

    window_size = screen.get_size()
    cache_key = (image_path, window_size)
    resized_image = _BACKGROUND_CACHE.get(cache_key)
    if resized_image is None:
        try:
            image = pygame.image.load(image_path).convert()
            resized_image = pygame.transform.smoothscale(
                image, window_size).convert_alpha()
            _BACKGROUND_CACHE[cache_key] = resized_image
        except (pygame.error, FileNotFoundError) as exc:
            print(f"Warning: could not load background '{image_path}': "
                  f"{exc}")
            return

    resized_image.set_alpha(alpha)
    screen.blit(resized_image, (0, 0))
