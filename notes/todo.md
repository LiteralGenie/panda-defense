logging
dont create new actor with same model for all units
push rendering into its own thread / process
units should not move diagonally

[x] get rid of vdom tree, everything should be child of render
[x] replace render-via-state-tracking with render-via-message-queue
[x] investigate pre-generating all enemies for a wave
        just skip rendering if not-spawned or dead
        trades more memory for faster deletions
[x] use in-memory db for UnitManager