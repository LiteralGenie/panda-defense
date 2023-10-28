### decoupling game logic from rendering logic
    game state is updated at different frequency than fps (aka "tick rate")
        under the assumption fps >> tick rate
    why?
        a headless server can replay and validate state without rendering anything (eg for multiplayer)
        downside is that this adds code complexity (two classes for everything)
    game layer
        game state is pure data (eg hp, position)
        changes to game state (movement, upgrades) are called actions
        actions are accumulated between ticks and applied on next tick
            where "applied" means combining previous state + actions to generate new state
    engine layer
        on each tick, the game state is converted into desired Node props and an interval to update the current Node props is started
            interval spans the period between ticks

    (diagram)
