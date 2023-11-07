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


### globals
    global state... isnt inherently evil
    
    in web apps the backend / db typically acts as global state and is frequently queried
    by deeply nested components like dialogs, not just the root component
        but as an optimization, data that's needed by multiple linked components is typically queried once and shared via props
    
    notifying distant components of updates eventually means some kind of pub-sub / observer like design
    
### current arch
    Still MVC, where the models are stored in a giant dict
    through python magic, the controller / view interact with class instances rather than this global state
    through further magic, the controller and view run in separate processes, with each having a copy of the state
        at the beginning of each tick the controller mutates its copy of the state
        and once finalized, the view's copy is updated with these changes

    more specifically, each change to the state made by the controller generates a StateEvent
    at the end of each tick, a list of all the StateEvents are submitted to the process the view is running in
    the view iterates over these events and runs whatever necessary animations

    in the case where an animation involves multiple models (eg tower attacking a unit)
    an additional event (in addition to the StateEvent) may be emitted to the renderer
