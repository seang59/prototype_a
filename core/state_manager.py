


class StateManager:
    def __init__(self):
        self.prev_state = None
        self.state_stack = []

    def update(self, dt, actions):
        pass

    def draw(self, surface):
        pass

    def enter_state(self, state):
        self.prev_state = self.state_stack[-1] if self.state_stack else None
        self.state_stack.append(state)

    def exit_state(self):
        if self.state_stack:
            self.state_stack.pop()