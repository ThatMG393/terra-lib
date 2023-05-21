import json
from binascii import unhexlify

from Crypto.Cipher import AES

from terralib.exceptions import InvalidPlayerException
from terralib.items import EquipableItem, PrefixedItem, InventoryItem
from terralib.utils import binary

ENC_KEY = unhexlify('6800330079005F006700550079005A00')
# ENC_KEY = 'h3y_gUyZ'.encode('utf-16-le')

MAGIC_NUM = 27981915666277746


def decode_player(player_file_path: str) -> bytes:
    aes_cipher = AES.new(ENC_KEY, AES.MODE_CBC, ENC_KEY)

    with open(player_file_path, 'rb') as plr_file:
        contents = plr_file.read()
        decoded_plr = aes_cipher.decrypt(contents)

        return decoded_plr


def deserialize_player(reader: binary.BinaryReader):
    version = reader.ReadInt32()
    if version >= 135:
        integrity = (reader.ReadULong64() & 72057594037927935)
        if integrity != MAGIC_NUM:
            raise InvalidPlayerException("Expected a valid ReLogic file signature")

        file_type = (MAGIC_NUM >> 53) & 255  # 255 = byte.MaxValue
        if file_type != 3:
            raise InvalidPlayerException("Expected a ReLogic player file format")

        revision = reader.ReadUInt32()
        is_favorite = (reader.ReadULong64() & 1) == 0
    else:
        revision = 0
        is_favorite = False

    name = reader.ReadString()

    if version >= 10:
        if version >= 17:
            difficulty = reader.ReadByte()
        elif reader.ReadBoolean():
            difficulty = 2

    if version >= 138:
        play_time = reader.ReadInt64()
    else:
        play_time = 0

    hair = reader.ReadInt32()

    if version >= 82:
        hair_dye = reader.ReadByte()

    if version >= 124:
        hidden_bits = {}

        visuals = reader.ReadByte()
        for i in range(0, 8):
            hidden_bits[i] = binary.bit_from_byte(visuals, i)

        visuals = reader.ReadByte()
        for i in range(9, 16):
            hidden_bits[i] = binary.bit_from_byte(visuals, i)
    elif version >= 83:
        hidden_bits = {}

        visuals = reader.ReadByte()
        for i in range(0, 8):
            hidden_bits[i] = binary.bit_from_byte(visuals, i)

    if version >= 119:
        hidden_misc = reader.ReadByte()

    if version >= 17:
        if hair == 5 or hair == 6 or hair == 9 or hair == 11:
            is_male = False
        else:
            is_male = True
    elif version < 107:
        is_male = reader.ReadBoolean()
    else:
        skin_variant = reader.ReadByte()

        if version < 161 and skin_variant == 7:
            skin_variant = 9

    health = reader.ReadInt32()
    health_max = reader.ReadInt32()
    mana = reader.ReadInt32()
    mana_max = reader.ReadInt32()

    if version >= 125:
        extra_accessory = reader.ReadBoolean()

    if version >= 229:
        unlocked_biome_torches = reader.ReadBoolean()
        using_biome_torches = reader.ReadBoolean()

        if version >= 256:
            ate_artisan_bread = reader.ReadBoolean()

        if version >= 260:
            used_aegis_crystal = reader.ReadBoolean()
            used_aegis_fruit = reader.ReadBoolean()
            used_arcane_crystal = reader.ReadBoolean()
            used_galaxy_pearl = reader.ReadBoolean()
            used_gummy_worm = reader.ReadBoolean()
            used_ambrosia = reader.ReadBoolean()

    if version >= 182:
        ooa_defeated = reader.ReadBoolean()

    if version >= 128:
        tax_money = reader.ReadInt32()

    if version >= 254:
        deaths_pve = reader.ReadInt32()
        deaths_pvp = reader.ReadInt32()

    hair_color = reader.ReadColor()
    skin_color = reader.ReadColor()
    eye_color = reader.ReadColor()
    shirt_color = reader.ReadColor()
    ushirt_color = reader.ReadColor()
    pants_color = reader.ReadColor()
    shoe_color = reader.ReadColor()

    if version > 38:
        if version < 124:
            armors = {}
            armor_slots = 11
            if version >= 81: armor_slots = 16
            for i in range(0, armor_slots):
                item = reader.ReadInt32()
                prfx = reader.ReadByte()
                armors[i] = EquipableItem(item, "jjej", 1, prfx)
        else:
            armors = {}
            for i in range(0, 20):
                item = reader.ReadInt32()
                prfx = reader.ReadByte()
                armors[i] = EquipableItem(item, "jjej", 1, prfx)

        if version >= 47:
            dyes = {}
            dye_slots = 3
            if version >= 124:
                dye_slots = 10
            elif version >= 81:
                dye_slots = 8

            for i in range(0, dye_slots):
                item = reader.ReadInt32()
                if item != 1:
                    prfx = reader.ReadByte()
                    dyes[i] = EquipableItem(item, f"Dye #{i}", 1, prfx)

        inventory = {}
        if version >= 58:
            inventory_count = 58

            for i in range(0, inventory_count):
                item_type = reader.ReadInt32()
                if item_type >= 99999999:
                    print(f"Item at {i} with ID of {item_type}")
                    inventory[i] = 0
                    reader.ReadInt32()
                    reader.ReadByte()

                    if version >= 114: fv = reader.ReadBoolean()
                else:
                    item = item_type
                    sk = reader.ReadInt32()
                    pr = reader.ReadByte()

                    if version >= 114: fv = reader.ReadBoolean()
                    inventory[i] = InventoryItem(item, f"Inventory Item #{i}", sk, pr, fv)
        else:
            inventory_count = 48

            for i in range(0, inventory_count):
                item_type = reader.ReadInt32()
                if item_type >= 99999999:
                    inventory[i] = 0
                    reader.ReadInt32()
                    reader.ReadByte()
                else:
                    item = item_type
                    sk = reader.ReadInt32()
                    pr = reader.ReadByte()

                    inventory[i] = InventoryItem(item, f"Inventory Item #{i}", sk, pr, fv)

        if version >= 117:
            misc = {}
            if version < 136:
                for i in range(0, 5):
                    if i != 1:
                        item_type = reader.ReadInt32()
                        if item_type >= 5124:
                            misc[i] = 0
                            reader.ReadByte()
                        else:
                            item = item_type
                            prfx = reader.ReadByte()

                            misc[i] = EquipableItem(item, f"Misc #{i}", 1, prfx)
                        # Just following the source...
                        item_type = reader.ReadInt32()
                        if item_type >= 5124:
                            misc[i] = 0
                            reader.ReadByte()
                        else:
                            item = item_type
                            prfx = reader.ReadByte()

                            misc[i] = EquipableItem(item, f"Misc #{i}", 1, prfx)
            else:
                for i in range(0, 5):
                    item_type = reader.ReadInt32()
                    if item_type >= 5124:
                        misc[i] = 0
                        reader.ReadByte()
                    else:
                        item = item_type
                        prfx = reader.ReadByte()

                        misc[i] = EquipableItem(item, f"Misc #{i}", 1, prfx)
                    # Just following the source...
                    item_type = reader.ReadInt32()
                    if item_type >= 5124:
                        misc[i] = 0
                        reader.ReadByte()
                    else:
                        item = item_type
                        prfx = reader.ReadByte()

                        misc[i] = EquipableItem(item, "hdjsj", 1, prfx)

            storage_size = 20
            if version >= 58:
                storage_size = 40

            piggy = {}
            for i in range(0, storage_size):
                item = reader.ReadInt32()
                stck = reader.ReadInt32()
                prfx = reader.ReadByte()

                piggy[i] = PrefixedItem(item, f"Piggy Item #{i}", stck, prfx)

            safe = {}
            for i in range(0, storage_size):
                item = reader.ReadInt32()
                stck = reader.ReadInt32()
                prfx = reader.ReadByte()

                safe[i] = PrefixedItem(item, f"Safe Item #{i}", stck, prfx)

            if version >= 182:
                forge = {}
                for i in range(0, 40):
                    item = reader.ReadInt32()
                    stck = reader.ReadInt32()
                    prfx = reader.ReadByte()

                    forge[i] = PrefixedItem(item, f"Forge Item #{i}", stck, prfx)

            if version >= 198:
                void = {}  # Just a guess, im still not sure...
                for i in range(0, 40):
                    item = reader.ReadInt32()
                    stck = reader.ReadInt32()
                    prfx = reader.ReadByte()
                    fvrt = False

                    if version >= 255:
                        fvrt = reader.ReadBoolean()

                    void[i] = InventoryItem(item, f"Void Vault Item #{i}", stck, prfx, fvrt)

            if version >= 199:
                void_vault_info = reader.ReadByte()
    else:
        armors = {}
        armor_slots = 8
        if version >= 6: armor_slots = 11

        for i in range(0, armor_slots):
            item = reader.ReadInt32()
            prfx = 0
            if version >= 36:
                prfx = reader.ReadByte()

            armor_slots[i] = EquipableItem(item, f"Armor #{i}", 1, prfx)

        inventory = {}
        for i in range(0, 44):
            item = reader.ReadInt32()
            stck = reader.ReadInt32()
            prfx = 0

            if version >= 36:
                prfx = reader.ReadByte()

        piggy = {}
        for i in range(0, 44):
            item = reader.ReadInt32()
            stck = reader.ReadInt32()
            prfx = 0

            if version >= 36:
                prfx = reader.ReadByte()

        if version >= 20:
            safe = {}
            for i in range(0, 44):
                item = reader.ReadInt32()
                stck = reader.ReadInt32()
                prfx = 0

                if version >= 36:
                    prfx = reader.ReadByte()

    if version < 58:
        for i in range(40, 48):
            inventory[i + 10] = inventory[i]
            inventory[i] = 0

    with open('../../test.plr.json', 'w') as test:
        rdable = {}
        for i in range(0, len(inventory)):
            rdable[i] = inventory[i].__str__()

        test.truncate(0)
        json.dump(rdable, test, indent=4)
