# The CIT Arcade

This project holds the source code for all of the software that powers the 170 square foot display
that can be installed on the face of the CIT.

Documentation and a developer guide are soon to be made public, but here are the coolest features:

- Integration with Pygame, so you can develop games using any Pygame modules you'd like
- Interactivity as a first-class citizen, so you can build games that people can control in real-time via their phones
- A clean API to develop your own bespoke graphics or games
- Interop with Racket (if you don't want to use Python to program)

Some multimedia from the project can be seen [here](https://photos.google.com/share/AF1QipOgMuZJ2tKGHjO9bG9c4xqZcxPG5v8TPbP4X1KpGGm-gHoAhOAqC2CflWsHd9m9Tw?key=UVotbWtiMXYwd0lDbHpFSTJtVDRORHJWb0d3ZHBn).

# Developer guide

## Running the stack E2E

Unfortunately, the tooling here isn't particularly seamless yet. Contributions to make this better are welcome.

1. Clone the project.
2. For development, add a `config.json` file to the root of the cloned directory with `{"is_dev": true}`
3. Create a virtual environment: `python3 -m venv env` and `source ./env/bin/activate`
4. Install the dependencies: `pip install -r ./requirements.txt`
5. From the project root, start the simulator via: `python3 -m game.driver`
6. You will be prompted to create a calibration. In development mode, this effectively just sets the dimensions of the simulator. For each prompt, respectively, you should enter: `9`, `10`, `4`, and then `4`. This is because the LED panels are 9 pixels wide, 10 pixels high, and they are arranged in a 4 by 4 pattern.

A Matplotlib window should appear. It will stay pinned to the top of your screen, for better or for worse. To control this, you'll need to run the webui:


1. Enter the webui subfolder `cd webui`
2. Install dependencies: `npm install`
3. Run the frontend: `npm run dev`
4. `http://localhost:3000` should now have the UI.

To control the screen, you'll need to get yourself a token. However, to generate a token, you must be an admin. To become an admin, do the following:


1. Navigate to `/admin`
2. Click "Refresh Passwords"
3. Enter the admin password (please contact me for it)
4. You are now an admin. You can visit `/control` to control the screen!

## Architecture overview

At a high-level, the RasPi (which controls the hardware) exposes a webserver (`webserve`) which handles authentication and user input. The user input comes from the web UI (`webui`).

Zooming in, the `webserve` component, for every (authenticated) user input, adds an `Update` to a shared buffer called `updates`.

The game engine event loop runs on the RasPi (see `game.driver`), and uses PyGame internally. The `CitArcadeGameManager` is the top-level manager of the screen state, and has the ability to run "mini" games, such as the Gif player, Snake, the static render of Tom's face, etc. Every frame tick (in `game.driver`), updates are applied to the `CitArcadeGameManager`, the new pixels are retrieved from it, and then displayed to the screen. The "updates" in question come from the `webserve` component, which, for every authenticated user input, adds an `Update` (see `game/update.py`) to a shared buffer (it uses a mutex to avoid data races). The actual displaying to the screen involves rendering a 3D matrix (2D matrix of RGB pixels) to a _serial_ LED strip. This mapping is done by `mapper/map.py`, which creates a mapping from row-major 2D array index into the 1D array index. The mapping is per-LED configuration (suppose you want to just do 2x2 panels; you could create a new mapping for it). Mappings are serialized to disk under `~/.citarcade` with the name that you give them, so that you can re-use mappings that you previously made.

## Where to start

- If you want to add another GIF to the GIF rotation, see `game/games/gifs.py`. Currently, this mini-game alphabetically reads a list of frames from a particular version-control-tracked disk location, and renders them. Thus, you'll need to use some online tool to convert a GIF into its individual frames.
- Let's say that you want to add an _entirely_ new game. You'll want to look at `mini_game.py`. You should probably also learn some basic PyGame, but you can look at `snake.py` if you just want to take a shortcut. Once you create your game, you can modify the home games list in `manager.py` to include your game.

## Contributing

Please submit contributions as a pull request from your own fork, and @neilramaswamy and @Hammad-Izhar will review them.
