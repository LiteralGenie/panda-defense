# now
tower shop
tower placement

# later
ingame gui
main menu
settings menu
camera controls
        pan / zoom
        orthogonal view

# eventually
progression
market
art
db schema
deploy server
logging
units should not move diagonally



# backlog
co-op
unit tests
e2e tests
more nuanced spawn times in scenario
organize render_queue into queue-per-event-type
        (can handling for a certain event type be independent of all possible other types?)

# dream
push rendering into its own thread / process


[x] get rid of vdom tree, everything should be child of render
[x] replace render-via-state-tracking with render-via-message-queue
[x] investigate pre-generating all enemies for a wave
        just skip rendering if not-spawned or dead
        trades more memory for faster deletions
[x] use in-memory db for UnitManager
[x] dont create new actor with same model for all units