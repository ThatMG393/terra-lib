from terralib.effects import Buff
from terralib.items import Item
from terralib.utils import decode, binary


class PlayerInventory:
    def __init__(self, items: list[Item]):
        self.items = items

    def __str__(self):
        tmp = []

        for index, item in enumerate(self.items):
            tmp.append(f"Item: [ {item} ] on Index: {index}")

        return tmp.__str__()

    def get_item_at(self, index: int) -> Item:
        return self.items[index]

    def set_item_at(self, index: int, item: Item):
        self.items[index] = item


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
    def __init__(self, name: str, stats: PlayerStats, inventory: PlayerInventory, effects: list[Buff] = None):
        self.name = name
        self.stats = stats
        self.inventory = inventory
        self.effects = effects

    def __str__(self):
        tmp = []

        for effect in self.effects:
            tmp.append(effect.__str__())

        return f"Player Name: {self.name}, Player Stats: [ {self.stats} ], " \
               f"Player Inventory: {self.inventory}, Player Potion Effects: {tmp}"

    def get_name(self) -> str:
        return self.name

    def get_player_stats(self) -> PlayerStats:
        return self.equipments

    def set_name(self, name: str):
        self.name = name

    def set_player_stats(self, player_stats: PlayerStats):
        self.equipments = player_stats


def open_player(player_file_path: str) -> Player:
    decoded_player = decode.decode_player(player_file_path)
    reader = binary.BinaryReader(decoded_player)
    decode.deserialize_player(reader)


def save_player(player: Player) -> None:
    print(player)
