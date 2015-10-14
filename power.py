import math
def power(b, e):
    """logarithmic divide/conquer algorithm"""
    print b,e
    if e == 0: return 1
    x = power(b, math.floor(e/2))
    print x,b,e
    if e % 2 == 0: return pow(x, 2)
    else: return b * pow(x, 2)




print power(4,10)