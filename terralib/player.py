from terralib.utils import decode


class PlayerStats:
    def __init__(self, health: int, defense: int, mana: int):
        self.health = health
        self.defense = defense
        self.mana = mana

    def __str__(self):
        return f"Health: {self.health}, Defense: {self.defense}, Mana: {self.mana}"

    def get_health(self) -> int:
        return self.health

    def get_defense(self) -> int:
        return self.defense

    def get_mana(self) -> int:
        return self.mana


class Player:
    def __init__(self, name: str, stats: PlayerStats):
        self.name = name
        self.stats = stats

    def __str__(self):
        return f"Player Name: {self.name}, Player Stats: [ {self.stats} ]"

    def get_name(self) -> str:
        return self.name

    def get_player_stats(self) -> PlayerStats:
        return self.stats

    def set_name(self, name: str):
        self.name = name

    def set_player_stats(self, player_stats: PlayerStats):
        self.stats = player_stats


def open_player(player_file_path: str) -> Player:
    decoded_player = decode.decode_player(player_file_path)

    byte = decoded_player.read(1)
    while byte != b"":
        print(byte)
        byte = decoded_player.read(1)

    return None


def save_player(player: Player) -> None:
    print(player)
