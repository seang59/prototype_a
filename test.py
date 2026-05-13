import pygame


def test():
    fonts = pygame.font.get_fonts()

    for font in fonts:
        print(font)


if __name__ == "__main__":
    print("This is a module, not a script")
    test()