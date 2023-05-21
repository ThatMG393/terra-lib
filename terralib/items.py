import enum


class Item:
    class Prefix(enum.Enum):
        NORMAL = 0

        # Positive
        LEGENDARY = 1

    def __init__(self, item_id: int, name: str, stack_size: int = 1):
        self.id = item_id
        self.name = name
        self.stack_size = stack_size

    def __str__(self):
        return f"ItemId: {self.id}, ItemName: {self.name}, Stack Size: {self.stack_size}"


class PrefixedItem(Item):
    def __init__(self, item_id: int, name: str, stack_size: int, prefix: Item.Prefix):
        super().__init__(item_id, name, stack_size)
        self.prefix = prefix

        def __str__(self):
            return super().__str__() + f" Prefix: {self.prefix}"


class InventoryItem(PrefixedItem):
    def __init__(self, item_id: int, name: str, stack_size: int, prefix: Item.Prefix, is_favorite: bool = False):
        super().__init__(item_id, name, stack_size, prefix)
        self.is_favorite = is_favorite

    def __str__(self):
        return super().__str__() + f" Favorite: {self.is_favorite}"


class EquipableItem(PrefixedItem):
    def __init__(self, item_id: int, name: str, stack_size: int, prefix: Item.Prefix, is_hidden: bool = False):
        super().__init__(item_id, name, stack_size, prefix)
        self.is_hidden = is_hidden

    def __str__(self):
        return super().__str__() + f" Hidden: {self.is_hidden}"

# I REALLY DONT KNOW WHAT IM DOING
