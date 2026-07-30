import sys
from src import Parser, Simulation, Visualizer


def main() -> None:
    if len(sys.argv) != 2:
        print("[Error] Wrong number of arguments.")
        sys.exit(1)

    parser = Parser()
    parser.parse(sys.argv[1])
    map_zone = parser.create_map()
    simulation = Simulation(map_zone)
    visualizer = Visualizer(simulation)
    visualizer.run()


if __name__ == "__main__":
    main()
