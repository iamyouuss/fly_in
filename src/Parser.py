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
        self._existing_connections: set[tuple[str, str]] = set()

    def parse_metadata(self, metadata_str: str) -> dict[str, Any]:
        metadata: dict[str, Any] = {}
        data = metadata_str.replace("]", '').strip().split()
        for line in data:
            key, value = line.split("=")
            if key == "max_drones":
                if int(value) < 1:
                    raise ValueError(f"[Error] Invalid value for 'max_drones': {value}")
                metadata["max_drones"] = int(value)
            elif key == "zone":
                try:
                    Zone_Type(value)
                except ValueError:
                    raise ValueError(f"[Error] Invalid value for 'zone': {value}")
                metadata["zone_type"] = value
            elif key == "color":
                metadata["color"] = value
            else:
                raise ValueError(f"[Error] Invalid metadata key '{key}'")
        return metadata

    def init_hub(self, prefix: str, content: str) -> None:
        parts = content.split("[")
        data = parts[0].split()
        if len(data) != 3:
            raise ValueError(
                f"Invalid number of arguments for line '{content}'")
        name = data[0]
        if "-" in name:
            raise ValueError(f"[Error] Invalid format for zone name '{name}': "
                             "spaces and dashes not allowed")
        
        existing_zone = self._get_zone_by_name(name)
        if existing_zone is not None:
            raise ValueError(f"[Error] Zone name {name} already exists")
        
        x = int(data[1])
        y = int(data[2])

        if len(parts) > 1:
            metadata = self.parse_metadata(parts[1])
            hub = Zone(name, x, y, **metadata)
        else:
            hub = Zone(name, x, y)

        if prefix == "start_hub":
            if self.start is not None:
                raise ValueError("[Error] More than one start hub detected")
            self.start = hub
        elif prefix == "end_hub":
            if self.end is not None:
                raise ValueError("[Error] More than one end hub detected")
            self.end = hub
        else:
            self.hubs[hub.name] = hub

    def _get_zone_by_name(self, name: str) -> Zone | None:
        if self.start and self.start.name == name:
            return self.start
        if self.end and self.end.name == name:
            return self.end
        if name in self.hubs:
            return self.hubs[name]
        return None

    def init_connection(self, connection_str: str) -> None:
        parts = connection_str.split("[")
        a, b = [h.strip() for h in parts[0].split("-")]
        test_connection = (min(a, b), max(a, b))
        if test_connection in self._existing_connections:
            raise ValueError(
                f"[Error] Connection between {a} and {b} already exists")
        self._existing_connections.add(test_connection)
        hub_a = self._get_zone_by_name(a)
        hub_b = self._get_zone_by_name(b)
        if hub_a is None or hub_b is None:
            raise ValueError(f"[Error] Zone '{a if hub_a is None else b}' not found")
        if len(parts) > 1:
            metadata = parts[1]
            metadata = metadata.replace("]", "")
            key, value = metadata.split("=")
            if key == "max_link_capacity":
                if int(value) < 1:
                    raise ValueError(f"[Error] Invalid value for 'max_link_capacity': {value}")
                max_link_capacity = int(value)
                self.connections.append(
                    Connection(hub_a, hub_b, max_link_capacity))
            else:
                raise ValueError(f"[Error] Invalid metadata key '{key}'")
        else:
            self.connections.append(Connection(hub_a, hub_b))

    def parse(self, file_name: str) -> None:
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
                        if int(content) < 1:
                            raise ValueError(f"[Error] Invalid value for 'nb_drones': {content}")
                        self.nb_drones = int(content)
                    elif prefix in ("start_hub", "end_hub", "hub"):
                        self.init_hub(prefix, content)
                    elif prefix == "connection":
                        self.init_connection(content)
        except FileNotFoundError:
            print(f"[Error] The file '{file_name}' was not found.")
            sys.exit(1)
        except ValueError as e:
            print(f"[Error] Invalid value at line {i}: {e}")
            sys.exit(1)

    def create_map(self) -> Map:
        try:
            if self.start is None or self.end is None:
                raise ValueError(
                    "[Error] Failed to create Map: no start or end hub")
            if self.nb_drones < 1:
                raise ValueError(
                    "[Error] Failed to create map: number of drone invalid")
            if not self.hubs:
                raise ValueError(
                    "[Error] Failed to create Map: not enoug hub")
            if not self.connections:
                raise ValueError(
                    "[Error] Failed to create Map: no connection between hubs")
            map_zone = Map(self.nb_drones, self.start, self.hubs, self.end,
                       self.connections)
            print("[Success] Map created succesfully !")
        except ValueError as e:
            print(f"[Error] Failed to create map: {e}")
            sys.exit(1)
        return map_zone
            
