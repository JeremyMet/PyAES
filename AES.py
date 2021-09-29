from constants import *
from misc import *

# AES 128
class AES_key(object):

    def __init__(self, key=None):
        self.basekey = key;
        self.round_keys = [0 for _ in range(44)];
        if key:
            self.generate_round_keys();

    @classmethod
    def _subword(cls, val):
        ret = 0;
        for i in range(4):
            tmp_val = val & 0xFF;
            ret = (SBOX[tmp_val] << (8*i)) ^ ret;
            val >>= 8;
        return ret;

    def generate_round_keys(self):
        rc = [0x01000000, 0x02000000, 0x04000000, 0x08000000 , 0x10000000, 0x20000000, 0x40000000, 0x80000000 , 0x1B000000, 0x36000000];
        rotword = lambda x : ((x << 8) & 0xFFFFFF00) ^ (x >> 24);
        N = 4 ; # 4 mots de 32 bits pour une clef de 128-bit.
        R = 11 ; # Nb rounds pour une clef de 128 bits.
        for round in range(4*R):
            if round < N:
                W = self.basekey[round];
            elif (round >= N and (round%N)==0):
                index = round//N-1;
                W = self.round_keys[round-N] ^ AES_key._subword(rotword(W)) ^ rc[index] ;
            elif (round >= N and round > 6 and round%N==4):
                W = self.round_keys[round-N] ^ AES_key._subword(W);
            else:
                W = self.round_keys[round-N] ^ W;
            self.round_keys[round] = W;

#

class AES(object):


    def __init__(self, key=None):
        self.key = AES_key(key);

    def set_key(self, key):
        self.key = AES_key(key);

    def encrypt(self, source):
        state = list(source);
        # First Round,
        state = misc.a_xor(state, self.key.basekey);
        # Middle Rounds,
        k = 4;
        s0, s1, s2, s3 = state[0], state[1], state[2], state[3];
        for round in range(9):
            t0 = self.key.round_keys[k+0] ^ apply_tboxes(s0 >> 24, s1 >> 16, s2 >> 8, s3);
            t1 = self.key.round_keys[k+1] ^ apply_tboxes(s1 >> 24, s2 >> 16, s3 >> 8, s0);
            t2 = self.key.round_keys[k+2] ^ apply_tboxes(s2 >> 24, s3 >> 16, s0 >> 8, s1);
            t3 = self.key.round_keys[k+3] ^ apply_tboxes(s3 >> 24, s0 >> 16, s1 >> 8, s2);
            s0, s1, s2, s3 = t0, t1, t2, t3;
            k+=4;
        # Last Round.
        s0 = (sb(t0 >> 24) << 24) | (sb(t1 >> 16) << 16) | (sb(t2 >> 8) << 8) | sb(t3);
        s1 = (sb(t1 >> 24) << 24) | (sb(t2 >> 16) << 16) | (sb(t3 >> 8) << 8) | sb(t0);
        s2 = (sb(t2 >> 24) << 24) | (sb(t3 >> 16) << 16) | (sb(t0 >> 8) << 8) | sb(t1);
        s3 = (sb(t3 >> 24) << 24) | (sb(t0 >> 16) << 16) | (sb(t1 >> 8) << 8) | sb(t2);

        s0 ^= self.key.round_keys[k+0];
        s1 ^= self.key.round_keys[k+1];
        s2 ^= self.key.round_keys[k+2];
        s3 ^= self.key.round_keys[k+3];

        return [s0, s1, s2, s3];


def block2array(val):
    ret = [0 for _ in range(4)];
    ret[0] = (val >> 96) & 0xFFFFFFFF;
    ret[1] = (val >> 64) & 0xFFFFFFFF;
    ret[2] = (val >> 32) & 0xFFFFFFFF;
    ret[3] = (val >>  0) & 0xFFFFFFFF;
    return ret;

if __name__ == "__main__":
    print(mult_0x02(0x01));
    apply_tboxes(0, 0, 0, 0);

    key = block2array(0x2b7e151628aed2a6abf7158809cf4f3c);
    msg = block2array(0xae2d8a571e03ac9c9eb76fac45af8e51);

    beautiful_hex = lambda X : ["0x"+hex(x)[2:].zfill(8) for x in X];

    print(beautiful_hex(key), beautiful_hex(msg));

    my_AES = AES(key);
    print(my_AES.key.round_keys);
    print([hex(i) for i in my_AES.encrypt(msg)]);
