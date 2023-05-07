from terralib.player import Item

ITEM_JSON = "terra-lib/asset/items.json"


def get_item_by_id(item_id: int) -> Item:
    with open(ITEM_JSON, 'r') as item_json:
        contents = item_json.read()
        item = Item(item_id, 'UNKNOWN', 0)

        name = contents[item_id]['itemName']

        item = Item(item_id, name, 0)

        return item
