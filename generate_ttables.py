from constants import *


if __name__ == "__main__":

    t0 = [None for _ in range(256)];
    t1 = [None for _ in range(256)];
    t2 = [None for _ in range(256)];
    t3 = [None for _ in range(256)];

    # 2 1 1 3 -> 1er colonne,
    # 3 2 1 1 -> 2ème colonne,
    # 1 3 2 1 -> 3ème colonne,
    # 1 1 3 2 -> 4ème colonne.

    s = lambda x : SBOX[x];
    for i in range(256):
        t0[i] = mult_0x02(s(i)) << 24 | mult_0x01(s(i)) << 16 | mult_0x01(s(i)) << 8 | mult_0x03(s(i));
        t1[i] = mult_0x03(s(i)) << 24 | mult_0x02(s(i)) << 16 | mult_0x01(s(i)) << 8 | mult_0x01(s(i));
        t2[i] = mult_0x01(s(i)) << 24 | mult_0x03(s(i)) << 16 | mult_0x02(s(i)) << 8 | mult_0x01(s(i));
        t3[i] = mult_0x01(s(i)) << 24 | mult_0x01(s(i)) << 16 | mult_0x03(s(i)) << 8 | mult_0x02(s(i));


    T = [t0, t1, t2, t3];
    beautiful_hex = lambda x : "0x"+hex(x)[2:].zfill(8);
    for i, t in enumerate(T):
        print("T-Table #{}:".format(i));
        print([beautiful_hex(x) for x in t]);
