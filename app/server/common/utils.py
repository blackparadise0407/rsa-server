from time import time
import random

from .rsa import RSA


def current_timestamp():
    return round(time())


def hex_to_bin(h: str):
    return bin(int(h, 16))[2:].zfill(len(h) * 4)


def bin_to_hex(b: str):
    return hex(int(b, 2))


def generate_random_sym_key():
    return hex(random.getrandbits(128))


def get_fdecrypted_sym_key(pem_pair: str, sym_key: str) -> str:
    exponent, pem = pem_pair.split(".")
    decrypted_sym_key = RSA.decrypt(sym_key, pem, exponent)
    return bin_to_hex(decrypted_sym_key)[2:]

