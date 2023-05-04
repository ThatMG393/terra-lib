from binascii import unhexlify
from typing import BinaryIO

from Crypto.Cipher import AES

MAGIC = unhexlify('6800330079005F006700550079005A00')


# MAGIC = 'h3y_gUyZ'.encode('utf-16-le')


def decode_player(player_file_path: str) -> BinaryIO:
    iv = MAGIC
    password = MAGIC

    aes_cipher = AES.new(password, AES.MODE_CBC, iv)

    with open(player_file_path, 'rb') as plr_file:
        contents = plr_file.read()
        decoded_plr = aes_cipher.decrypt(contents)

        dec_plr_file = open(f"{player_file_path}.dec", 'wb+')
        dec_plr_file.write(decoded_plr)

        return dec_plr_file
