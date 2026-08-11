import sys
from typing import Any
from .Map import Connection, Zone, Map, Zone_Type


class Parser:
    def __init__(self) -> None:
        self.start: Zone | None = None
        self.end: Zone | None = None
        self.hubs: dict[str, Zone] = {}
        self.nb_drones: int = 0
        self.connections: list[Connection] = []
        self.existing_connections: set[tuple[str, str]] = set()

    def parse_metadata(self, metadata_str: str) -> dict[str, Any]:
        """
        Parse metadata string into a dictionary.

        Args:
            metadata_str (str): The metadata string to parse.

        Returns:
            dict[str, Any]: The parsed metadata dictionary.
        """
        metadata: dict[str, Any] = {}
        data = metadata_str.replace("]", '').strip().split()
        if not data:
            return metadata
        for line in data:
            key, value = line.split("=") if "=" in line else (line, None)
            if not key or not value:
                raise ValueError(f"Invalid metadata format for '{line}' "
                                 f"(expected format: 'key=value')")
            if key == "max_drones":
                try:
                    drone = int(value)
                except ValueError:
                    raise ValueError(f"Invalid value for 'max_drones': "
                                     f"{value} is not an integer")
                if drone < 1:
                    raise ValueError("'max_drones' must be superior to 0")
                metadata["max_drones"] = int(value)
            elif key == "zone":
                try:
                    Zone_Type(value)
                except ValueError:
                    raise ValueError(
                        f"Invalid zone '{value}' (only 'normal', "
                        "'restricted', 'blocked' and 'priority' allowed)")
                metadata["zone_type"] = value
            elif key == "color":
                metadata["color"] = value
            else:
                raise ValueError(f"Invalid metadata key '{key}' (only 'color',"
                                 " 'zone_type' and 'max_drones' allowed)")
        return metadata

    def init_hub(self, prefix: str, content: str) -> None:
        """
        Initialize a hub.

        Args:
            prefix (str): The prefix for the hub.
            content (str): The content for the hub.
        """
        parts = content.split("[")
        data = parts[0].split()
        if len(data) != 3:
            raise ValueError(
                f"Invalid number of arguments for line '{content}' "
                "(expected 3: name, x, y)")
        name = data[0]
        if "-" in name:
            raise ValueError(f"Invalid zone name '{name}' "
                             "(spaces and dashes not allowed)")

        existing_zone = self.get_zone_by_name(name)
        if existing_zone is not None:
            raise ValueError(f"Zone name '{name}' already exists")

        x = int(data[1])
        y = int(data[2])

        if len(parts) > 1:
            metadata = self.parse_metadata(parts[1])
            hub = Zone(name, x, y, **metadata)
        else:
            hub = Zone(name, x, y)

        if prefix == "start_hub":
            if self.start is not None:
                raise ValueError("More than one start hub detected")
            self.start = hub
        elif prefix == "end_hub":
            if self.end is not None:
                raise ValueError("More than one end hub detected")
            self.end = hub
            self.end.max_drones = self.nb_drones
        else:
            self.hubs[hub.name] = hub

    def get_zone_by_name(self, name: str) -> Zone | None:
        """
        Get a zone by its name.

        Args:
            name (str): The name of the zone to get.

        Returns:
            Zone | None: The zone if found, otherwise None.
        """
        if self.start and self.start.name == name:
            return self.start
        if self.end and self.end.name == name:
            return self.end
        if name in self.hubs:
            return self.hubs[name]
        return None

    def init_connection(self, connection: str) -> None:
        """
        Initialize a connection between two zones.

        Args:
            connection (str): The connection string to initialize.
        """
        parts = connection.split("[")
        zones = [h.strip() for h in parts[0].split("-")]
        if len(zones) != 2 or not all(zones):
            raise ValueError(f"Invalid connection format for '{connection}'"
                             " (expected format: 'zone1-zone2')")
        a, b = zones
        test = (min(a, b), max(a, b))
        if test in self.existing_connections:
            raise ValueError(
                f"Connection between {a} and {b} already exists")
        self.existing_connections.add(test)
        hub_a = self.get_zone_by_name(a)
        hub_b = self.get_zone_by_name(b)
        if hub_a is None or hub_b is None:
            raise ValueError(
                f"Zone '{a if hub_a is None else b}' not found")
        if len(parts) > 1:
            metadata = parts[1]
            metadata = metadata.replace("]", "")
            key, value = metadata.split("=")
            if not key or not value:
                raise ValueError(
                    f"Invalid metadata format for '{connection}'"
                    "(expected format: 'key=value')"
                )
            if key == "max_link_capacity":
                try:
                    m = int(value)
                except ValueError:
                    raise ValueError(
                        f"Invalid format for 'max_link_capacity': "
                        f"'{value}' is not an integer")
                if m < 1:
                    raise ValueError(
                        "'max_link_capacity' must be superior to 0")
                max_link_capacity = m
                self.connections.append(
                    Connection(hub_a, hub_b, max_link_capacity))
            else:
                raise ValueError(f"Invalid metadata key '{key}'")
        else:
            self.connections.append(Connection(hub_a, hub_b))

    def parse(self, file_name: str) -> None:
        """
        Parse the input file.

        Args:
            file_name (str): The name of the input file to parse.
        """
        try:
            with open(file_name, "r") as f:
                for i, line in enumerate(f, start=1):
                    if line.startswith("#") or not line:
                        continue
                    cutted_line = line.split(": ")
                    if len(cutted_line) < 2:
                        continue
                    prefix, content = [c.strip() for c in cutted_line]
                    if prefix == "nb_drones":
                        if not content:
                            raise ValueError(
                                "'nb_drones' cannot be empty"
                            )
                        try:
                            nb = int(content)
                        except ValueError:
                            raise ValueError(
                                f"Invalid format for 'nb_drones': "
                                f"'{content}' is not an integer")
                        if nb < 1:
                            raise ValueError(
                                "'nb_drones' must be superior to 0")
                        self.nb_drones = nb
                    elif prefix in ("start_hub", "end_hub", "hub"):
                        self.init_hub(prefix, content)
                    elif prefix == "connection":
                        self.init_connection(content)
                    else:
                        raise ValueError(f"Invalid prefix '{prefix}' (only "
                                         "'nb_drones', 'start_hub', 'end_hub',"
                                         " 'hub' and 'connection' allowed)")
        except FileNotFoundError:
            print(f"[Error] The file '{file_name}' was not found.")
            sys.exit(1)
        except ValueError as e:
            print(f"[Error] at line {i}: {e}")
            sys.exit(1)

    def create_map(self) -> Map:
        """
        Create a map from the parsed data.

        Returns:
            Map: A Map object.
        """
        try:
            if self.start is None or self.end is None:
                raise ValueError(
                    "no start or end hub")
            if self.nb_drones < 1:
                raise ValueError(
                    "number of drone invalid")
            if not self.hubs:
                raise ValueError(
                    "no hub found")
            if not self.connections:
                raise ValueError(
                    "no connection between hubs")
            map_zone = Map(self.nb_drones, self.start, self.hubs, self.end,
                           self.connections)
            print("[Success] Map created succesfully !")
        except ValueError as e:
            print(f"[Error] Failed to create map: {e}")
            sys.exit(1)
        return map_zone
