first_const = 2 ** 32 - 1
second_const = 2 ** 448 - 1
third_const = 2 ** 512 - 1
fourth_const = 2 ** 32


def hex_to_words(value):
    lst = []
    while value:
        lst.append((value & first_const))
        value = value >> 32
    return lst


def iteration_of_ch(inp):
    while inp:
        ch = inp & second_const
        size = len(bin(ch)) - 2
        ch = (ch << 1) + 1
        ch = ch << (512 - size - 1)
        ch += size
        yield ch
        inp = inp >> 448


def rot_l(num, shift):
    return ((num >> 32 - shift) | (num << shift)) & third_const


def SHA1(inp, h0, h1, h2, h3, h4):
    ans = 0
    for ch in iteration_of_ch(inp):
        word = hex_to_words(ch)
        for i in range(16, 80):
            word.append(rot_l((word[i - 3] ^ word[i - 8] ^ word[i - 14] ^ word[i - 16]), 5))
        num0 = h0
        num1 = h1
        ch = h2
        num3 = h3
        num4 = h4
        for i in range(80):
            if 60 <= i <= 79:
                f = num1 ^ ch ^ num3
                k = 0xCA62C1D6
            elif 40 <= i <= 59:
                f = (num1 and ch) or (num1 and num3) or (ch and num3)
                k = 0x8F1BBCDC
            elif 20 <= i <= 39:
                f = num1 ^ ch ^ num3
                k = 0x6ED9EBA1
            elif 0 <= i <= 19:
                f = (num1 and ch) or ((not num1) and num3)
                k = 0x5A827999
            tmp = (rot_l(num0, 5) + f + num4 + k + word[i]) % fourth_const
            num4 = num3
            num3 = ch
            ch = rot_l(num1, 30)
            num1 = num0
            num0 = tmp
        h0 = h0 + num0 % fourth_const
        h1 = h1 + num1 % fourth_const
        h2 = h2 + ch % fourth_const
        h3 = h3 + num3 % fourth_const
        h4 = h4 + num4 % fourth_const
        hash_of_ch = h0 << 128 | h1 << 96 | h2 << 64 | h3 << 32 | h4
        ans += hash_of_ch
        ans %= 1 << 512
    return ans


h0=0x67452301
h1=0xEFCDAB89
h2=0x98BADCFE
h3=0x10325476
h4=0xC3D2E1F0
print('Введите число для шифровки:')
print(hex(SHA1(int(input()), h0, h1, h2, h3, h4)))
