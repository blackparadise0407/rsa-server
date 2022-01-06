import random
import math
import base64

# Hàm tìm ước chung lớn nhất
def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


# Hàm kiểm tra số nguyên tố
def checkPrime(p):
    n = int(math.sqrt(p))
    for i in range(2, n + 1):
        if p % i == 0:
            return False
    return True


# Hàm tạo 2 số nguyên tố p1 p2
def createPrime():
    x = random.randint(2, 100)
    p1 = x
    while 1:
        if checkPrime(p1) == True:
            break
        p1 += 1
    p2 = p1 + random.randint(2, 100)
    while 1:
        if checkPrime(p2) == True:
            break
        p2 += 1
    return p1, p2


# Hàm tạo số nguyên tố p lớn (p>10000)
def createBigPrime(p1):
    if p1 > 10000:
        return p1
    while 1:
        a = 2
        for k in range(2, 2 * p1 + 2):
            p2 = 2 * k * p1 + 1
            if gcd(pow(a, k) + 1, p2) == 1 and (pow(a, k * p1) + 1) % p2 == 0:
                return createBigPrime(p2)


# Hàm kiểm tra nguyên tố cùng nhau với khóa công khai E
def createE(totient):
    e = random.randint(2, 1000)
    while True:
        if gcd(e, totient) == 1:
            message = f"{e:08b}"
            message_bytes = message.encode("ascii")
            base64_bytes = base64.b64encode(message_bytes)
            return base64_bytes.decode("ascii")
        e += 1


# Hàm tìm d sao cho e*d = 1 mod (phi)
def createD(e, totient):
    i = -1
    while 1:
        if (1 - totient * i) % e == 0:
            d = (1 - totient * i) // e
            message = f"{d:08b}"
            message_bytes = message.encode("ascii")
            base64_bytes = base64.b64encode(message_bytes)
            return base64_bytes.decode("ascii")
        i -= 1


# Hàm tính đồng dư cho số lớn
def powerMod(x, y, n):
    # Phân tích y ra nhị phân
    size = f"{y:08b}".__len__()
    Y = 1
    for i in range(size):
        Y = (Y * Y) % n
        if f"{y:08b}"[i] == "1":
            Y = (Y * x) % n
    return Y


class RSA:
    @staticmethod
    def gen_key_pair():
        # Tạo 2 số nguyên tố nhỏ
        p1, p2 = createPrime()
        # Tạo 2 số nguyên tố lớn
        p = createBigPrime(p1)
        q = createBigPrime(p2)
        totient = (p - 1) * (q - 1)
        exponent = p * q

        # Tạo e
        base64_message = createE(totient)
        base64_bytes = base64_message.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode("ascii")
        pub = int(message, 2)

        # Tạo d
        base64_message = createD(pub, totient)
        base64_bytes = base64_message.encode("ascii")
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode("ascii")
        pem = int(message, 2)
        return exponent, pem, pub

    @staticmethod
    def encrypt(m: str, pub: int, exponent: int):
        pub = int(pub)
        exponent = int(exponent)
        length = len(m) // 8
        s = []  # Chứa chuỗi 8 phần tử của m
        c = []  # Chứa dãy nhị phân của 1 phần tử s
        for i in range(length):
            s.append(m[8 * i : 8 * i + 8])
            c.append(f"{powerMod(int(s[i], 2), pub, exponent):08b}")
        encrypt = " ".join(c)
        return encrypt

    @staticmethod
    def decrypt(cipher_text: str, pem: int, exponent: int):
        pem = int(pem)
        exponent = int(exponent)
        s = cipher_text.split(" ")
        decrypt = ""
        length = len(s)
        for i in range(length):
            decrypt += f"{powerMod(int(s[i], 2), pem, exponent):08b}"
        return decrypt
