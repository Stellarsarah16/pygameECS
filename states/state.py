class GameState:
    def handle_input(self, events):
        """Process input events."""
        raise NotImplementedError()

    def update(self, dt):
        """Update state-specific logic."""
        raise NotImplementedError()

    def render(self, screen):
        """Render the state."""
        raise NotImplementedError()

# ---------------------------------------------------------------- #

class StateManager:
    def __init__(self):
        self.states = []
        self.previous_state = None

    def push(self, state):
        self.states.append(state)

    def pop(self):
        if self.states:
            return self.states.pop()
        return None

    def pop_to_menu(self):
        self.states = [self.states[0]]  # Keep only the bottom-most state

    def get_active_state(self):
        if self.states:
            return self.states[-1]
        return None

    def get_previous_state(self):
        return self.previous_state

    def handle_input(self, events):
        """Delegate input handling to the active state."""
        active_state = self.get_active_state()
        if active_state:
            active_state.handle_input(events)

    def update(self, dt):
        """Delegate updates to the active state."""
        active_state = self.get_active_state()
        if active_state:
            active_state.update(dt)

    def render(self, screen):
        """Delegate rendering to the active state."""
        active_state = self.get_active_state()
        if active_state:
            active_state.render(screen)
