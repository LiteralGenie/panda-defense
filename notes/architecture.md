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

### decoupling via VDOM doesn't work
    Inferring what to render from changes in game state isn't always possible.
    
    eg a tower attacking an enemy doesn't trigger any changes in tower state but the tower should have some kind of attack / rotation animation
    
    a sillier example is "if game ends, friendlies should start a celebratory animation"

### decoupling via message queue
    more direct approach than listening for state changes is having a message queue that's updated on every state change. It's almost the same as just rendering directly but like the state change approach still allows intercepting the render call (to either drop it because server build or it was for an old frame that was superceded)