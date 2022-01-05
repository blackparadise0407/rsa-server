from time import time


def current_timestamp():
    return round(time())


def hex_to_bin(h):
    return bin(int(h, 16))[2:].zfill(len(h) * 4)
