from binascii import unhexlify

from Crypto.Cipher import AES

ENC_KEY = unhexlify('6800330079005F006700550079005A00')
# ENC_KEY = 'h3y_gUyZ'.encode('utf-16-le')

MAGIC_NUM = 27981915666277746


def decode_player(player_file_path: str) -> bytes:
    aes_cipher = AES.new(ENC_KEY, AES.MODE_CBC, ENC_KEY)

    with open(player_file_path, 'rb') as plr_file:
        contents = plr_file.read()
        decoded_plr = aes_cipher.decrypt(contents)

        return decoded_plr
