A very small tower-defense game built with the [Panda3D](https://www.panda3d.org/) engine.

Mostly as a learning exercise.

https://www.youtube.com/watch?v=rh-obSMSaN8

# Setup

Requires Python 3.11+

Linux:
1. `git clone https://github.com/LiteralGenie/panda-defense`
1. `cd /path/to/panda-defense`
1. `python3 -m venv venv`
1. `source ./venv/bin/activate`
1. `python -m pip install -r requirements.txt`
1. `python ./src/main.py`

Windows:
1. `git clone https://github.com/LiteralGenie/panda-defense`
1. `cd C:\path\to\panda-defense`
1. `python -m venv venv`
1. `./venv/bin/activate`
1. `python -m pip install -r .\requirements.txt`
1. `python .\src\main.py`

# Architecture

`main.py` launches two processes:
  - a "controller" process that periodically updates the game state
  - a "view" process that renders the game state to the screen and accepts user input ("actions")

The reason for this split is mostly to isolate the game logic from the rendering engine. Which should make server-validation and multiplayer easier to set up.
(Also didn't trust the Panda3d engine much.)

(I realize that despite the terminology, the controller is too fat for this to be MVC ¯\\\_(ツ)_/¯ )

<blockquote>
<details>
<summary>More gory details</summary>

On each tick (250ms), the controller will...
   - check for actions from the view process
   - validate these actions and apply them to the current state (eg buying towers by subtracting gold)
   - apply other changes to the current game state (eg moving units)
   - emit all changes that occurred this tick to the view process

Although the game state is technically [one giant dictionary](https://github.com/LiteralGenie/panda-defense/blob/master/src/game/state/game_state.py), both the controller and view process interact with [proxy objects](https://github.com/LiteralGenie/panda-defense/blob/master/src/game/state/stateful_class.py) that point to small slices of this state (aka "models").

The view process will typically also generate a view instance for each model to hold rendering-related state (eg track active animations).
Invidual view instances (and gui components) are notified of changes to the underlying model via a global [RxPY](https://rxpy.readthedocs.io/en/latest/) pipe.
</details>
</blockquote>



# Notes to self

- I'm probably going to rewrite this game instead of building on it for a few reasons:
  - The data models for units / towers work for this demo, but too rigid for any unique mechanics.
  - Building the GUI components is waay too tedious.
    - Takes a dozen lines just to position / animate a slide-in-out transition. 
    - Default components are fugly.
    - Layout libraries like [DirectGuiExtension](https://github.com/fireclawthefox/DirectGuiExtension) may help but probably better to see if any of the [CEF integrations](https://github.com/Moguri/cefpanda) or [HTML libraries](https://github.com/libRocket/libRocket) are functional.
