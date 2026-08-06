# Fly-In

Fly-In Simulation is a Python-based turn-by-turn simulation and visualization tool for drone logistics. It calculates and animates the movement of multiple drones navigating through a network of zones (hubs) and connections (routes) to reach their destination.

The project features a powerful underlying simulation engine and a smooth 2D visualizer built with the `arcade` library, complete with timeline navigation and real-time movement logs.

##  Features

*   **Smart Parsing & Pathfinding:** Parses a custom map layout and automatically plans the paths for all drones.
*   **2D Visualization:** A dynamic window displaying zones, connections, and drone sprites.
    *   *Smooth Animations:* Drones glide smoothly between zones using Linear Interpolation (Lerp).
    *   *Smart Positioning:* Drones waiting on the same zone automatically arrange themselves in a circular orbit to avoid overlapping.
*   **Interactive Playback:** Behave like a video player! Watch the simulation unfold automatically or take manual control to analyze specific turns.
*   **On-Screen HUD:** Displays real-time logs of drone movements and zone capacities directly on the screen.
*   **Output Generation:** Automatically generates an `output.txt` file containing the detailed logs of the entire simulation upon completion.

## Requirements

*   Python 3.10+ (Recommended)
*   [Arcade Library](https://api.arcade.academy/en/latest/) (`arcade`)

To install the required dependencies, simply run:
```bash
make install
```
## Usage
Run the program via the command line by providing a map file.
```
python3 main.py <filepath>
```
Arguments:
filepath (Required): The path to the map configuration file (e.g., map.txt).

You can also use the following Makefile command:
```
make run ARGS=<filpath>
```

## Visualizer Controls
Once the window opens, the simulation starts in Manual mode. You can use your keyboard to control the playback:

- **Space**	: Toggle between Auto-Play and Manual mode.

- **Right arrow** (→) :	Step forward by one turn (Forces Manual mode).

- **Left arrow** (←) : Step backward by one turn (Forces Manual mode).

- **Q** : Quit visualization

## Output
When you close the visualizer window, the program automatically writes the simulation history to an output.txt file in the root directory. It also prints the final logs to the standard output (terminal).

The log format per turn looks like this:
```
D1-roof1 D2-corridorA
D1-roof2 D2-tunnelB
D1-goal D2-goal
```
(Drones that do not move during a turn are smartly filtered out of the logs to keep the output clean).


## Architecture Overview

**Parser**: Reads the text file and generates the map topology (Zones and Connections).

**Simulation & Drone**: The logical brain. Calculates pathfinding, turns in transit, and records the history of drone positions for time-travel navigation.

**Visualizer**: The arcade.Window class responsible for drawing the map, animating the drones, rendering the HUD, and handling keyboard inputs.