import sys
from src import Parser


def main() -> None:
    if len(sys.argv) != 2:
        print("[Error] Wrong number of arguments.")
        print("Usage: python main.py <map_file>")
        sys.exit(1)

    try:
        parser = Parser()
        parser.parse(sys.argv[1])
        map_zone = parser.create_map()

        print("Map créée avec succès ! Lancement de la simulation...")
        map_zone.start_simulation()

    except FileNotFoundError:
        print(f"[Error] The file '{sys.argv[1]}' was not found.")
        sys.exit(1)

    except Exception as e:
        print(f"[Error] Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
