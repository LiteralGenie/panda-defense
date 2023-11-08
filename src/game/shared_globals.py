from game.state.game_state import GameState


class SharedGlobals:
    state: GameState


SG = SharedGlobals
