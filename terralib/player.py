import enum

from terralib.exceptions import *
from terralib.utils import decode, binary


class Item:
    class Prefix(enum.Enum):
        NORMAL = 0

    def __init__(self, item_id: int, name: str, prefix: int):
        self.id = item_id
        self.name = name
        self.prefix = prefix

    def __str__(self):
        return f"ItemId: {self.id}, ItemName: {self.name}, Prefix: {self.prefix}"


class PotionEffect:
    def __init__(self, potion_id: int, duration: int):
        self.id = potion_id
        self.duration = duration

    def __str__(self):
        return f"Potion ID: {self.id}, Potion Duration: {self.duration}"

    def get_potion_id(self) -> int:
        return self.id

    def get_potion_duration(self) -> int:
        return self.duration


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
    def __init__(self, name: str, stats: PlayerStats, inventory: PlayerInventory, effects: list[PotionEffect] = None):
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
        return self.stats

    def set_name(self, name: str):
        self.name = name

    def set_player_stats(self, player_stats: PlayerStats):
        self.stats = player_stats


def open_player(player_file_path: str) -> Player:
    decoded_player = decode.decode_player(player_file_path)
    reader = binary.BinaryReader(decoded_player)

    version = reader.ReadInt32()
    if version > 135:
        integrity = (reader.ReadULong64() & 72057594037927935)
        if integrity != decode.MAGIC_NUM:
            raise InvalidPlayerException("Expected a valid ReLogic file signature")

        file_type = (decode.MAGIC_NUM >> 53) & 255  # 255 = byte.MaxValue
        if file_type != 3:
            raise InvalidPlayerException("Expected a ReLogic player file format")

        revision = reader.ReadInt32()
        is_favorite = (reader.ReadULong64() & 1) == 1

    name = reader.ReadString(20)
    print(name)

    return Player(
        "test",
        PlayerStats(500, 75, 400),
        PlayerInventory([
            Item(1, "teet", 0), Item(1, "world", 3)
        ]
        ), [
            PotionEffect(0, 69),
            PotionEffect(1, 420)
        ]
    )


def save_player(player: Player) -> None:
    print(player)
