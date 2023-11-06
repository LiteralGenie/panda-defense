# panda
panda creates globals by creating props on builtins module
no type hints for common classes like...
    render
not obvious when model files fail to load
    nothing rendered but no warnings
actor docs missing functions
    lerp helpers like posInterval()
practical distinction between PandaNode and NodePath is muddled
    which constructors / functions accept which?
(!) directgui coords are funky
    on a landscape screen, no way to specify "X occupies 10% of the screen width"
        (and is positioned with left edge starting at 90%_of_viewport)
    because the min / max x coord depends on the vertical axis height
    workaround is to manually recalculate layout when window size changes

# python
generics suck
    no defaults (open PEP) or otherwise equivalent of
    `function someFunction<T extends MyClass = MyClass>() { ... }`

# mine
targeting logic is overengineered
    complexity comes from (premature?) optimizations
        to avoid checking every tile in range for enemies,
        we're filtering out tiles that don't intersect with a path,
        and chunking together consecutive tiles (intervals) along the path
        this is all a one-time calculation at game start

        on each tick we then iterate over each interval and search for enemies (which involves a one-time sorting the enemies by distance traveled)
    at the very least, the intermediary types / functions shouldnt pollute autocomplete suggestions somehow

component communication
    MVC works nice for some parts
        play (controller) updates game state (model)
        animations (view) for individual are mostly derived from current game state
        key is that each model / view is independent (eg unit animations dont depend on tower animations)
            controller handles interconnection but the model / views dont really care
            technically some animations need to be synced (turret rotation and unit movement) but controller can cheat and sync these

multiprocessing...
    serializing / deserializing dataclasses
    no intersection type