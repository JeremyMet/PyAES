class misc(object):

    a_xor = lambda A, B : [(x^y) for (x,y) in zip(A, B)];
    a_and = lambda A, B : [(x&y) for (x,y) in zip(A, B)];


    @classmethod
    def a_2int(cls, val):
        ret = 0;
        for v in val:
            ret = (ret << 8)^v;
        return ret;
