import sys
from src import Parser, Simulation, Visualizer


def main() -> None:
    """ if len(sys.argv) != 2:
            print("[Error] Wrong number of arguments.")
            sys.exit(1) """
    print(sys.argv)
    if sys.argv[2] == '--capacity_info':
        capacity_info = True
    else:
        capacity_info = False
    print(capacity_info)
    parser = Parser()
    parser.parse(sys.argv[1])
    map_zone = parser.create_map()
    simulation = Simulation(map_zone, capacity_info)
    visualizer = Visualizer(simulation)
    visualizer.run()
    with open("output.txt", "w") as f:
        f.write(simulation.output)
        print(simulation.output)


if __name__ == "__main__":
    main()
