import pygame

class InputManager:
    def __init__(self):
        self._keys_held = set()
        self._keys_just_pressed = set()
        self._keys_just_released = set()
        self._mouse_buttons_held = set()
        self._mouse_just_pressed = set()
        self._mouse_just_released = set()
        self._mouse_pos = (0, 0)
        self._mouse_wheel = 0
        self._quit = False

    def update(self):
        self._keys_just_pressed.clear()
        self._keys_just_released.clear()
        self._mouse_just_pressed.clear()
        self._mouse_just_released.clear()
        self._mouse_wheel = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit = True
            elif event.type == pygame.KEYDOWN:
                self._keys_just_pressed.add(event.key)
                self._keys_held.add(event.key)
            elif event.type == pygame.KEYUP:
                self._keys_just_released.add(event.key)
                self._keys_held.discard(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_just_pressed.add(event.button)
                self._mouse_buttons_held.add(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_just_released.add(event.button)
                self._mouse_buttons_held.discard(event.button)
            elif event.type == pygame.MOUSEWHEEL:
                self._mouse_wheel = event.y

        self._mouse_pos = pygame.mouse.get_pos()

    def is_held(self, key) -> bool:
        return key in self._keys_held

    def is_just_pressed(self, key) -> bool:
        return key in self._keys_just_pressed

    def is_just_released(self, key) -> bool:
        return key in self._keys_just_released

    def is_mouse_held(self, button) -> bool:
        return button in self._mouse_buttons_held

    def is_mouse_just_pressed(self, button) -> bool:
        return button in self._mouse_just_pressed

    def mouse_pos(self):
        return self._mouse_pos

    def mouse_wheel(self):
        return self._mouse_wheel

    def should_quit(self) -> bool:
        return self._quit