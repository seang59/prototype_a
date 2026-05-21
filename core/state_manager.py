


class StateManager:
    def __init__(self):
        self.prev_state = None
        self.state_stack = []

    def update(self, dt, game):
        if self.state_stack:
            self.state_stack[-1].update(dt, game)

    def draw(self, surface, game):
        if self.state_stack:
            self.state_stack[-1].draw(surface, game)

    def enter_state(self, state, game):
        self.prev_state = self.state_stack[-1] if self.state_stack else None
        self.exit_state(game)  

        self.state_stack.append(state)
        state.on_enter(game)

    def exit_state(self, game):
        if self.state_stack:
            state = self.state_stack.pop()
            state.on_exit(game)

    def get_state(self):
        return self.state_stack[-1] if self.state_stack else None