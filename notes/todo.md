# PoC
gold / health
gold / health gui
validate tower placement
prevent tower placement under gui
tower description on hover
tower stats on instance click
sell tower
unit stats on instance click
main menu
settings menu
logging
campaign levels
throwaway art

# later
progression
db schema
art
replayable levels
camera controls
        pan / zoom
        orthogonal view

# eventually
market
deploy server
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


# done
[x] rxpy for gui to respond to changes since it doesnt receive render events
[x] tower placement
[x] tower shop
[x] get rid of vdom tree, everything should be child of render
[x] replace render-via-state-tracking with render-via-message-queue
[x] investigate pre-generating all enemies for a wave
        just skip rendering if not-spawned or dead
        trades more memory for faster deletions
[x] use in-memory db for UnitManager
[x] dont create new actor with same model for all units