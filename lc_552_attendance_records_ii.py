"""Use matrix multiplication with memoization to count the records and then cheat.

The main idea comes from https://leetcode.com/problems/student-attendance-record-ii/discuss/101633/Improving-the-runtime-from-O(n)-to-O(log-n)

---

Runtime: 32 ms
Memory Usage: 15 MB

"""

# Some matrix math modulo N
from itertools import count

N = 10 ** 9 + 7


def dot(v, w):
    assert len(v) == len(w)
    return sum(ve * we for ve, we in zip(v, w)) % N


def mat_mul(a, b):
    return [[dot(row, col) for col in zip(*b)] for row in a]


assert mat_mul([[1, 2]], [[3], [4]]) == [[11]]

# Ok, here we cheat a bit

d = {1: [[0, 0, 1, 0, 0, 0], [1, 0, 1, 0, 0, 0], [0, 1, 1, 0, 0, 0], [0, 0, 1, 0, 0, 1], [0, 0, 1, 1, 0, 1],
         [0, 0, 1, 0, 1, 1]],
     2: [[0, 1, 1, 0, 0, 0], [0, 1, 2, 0, 0, 0], [1, 1, 2, 0, 0, 0], [0, 1, 2, 0, 1, 1], [0, 1, 3, 0, 1, 2],
         [0, 1, 3, 1, 1, 2]],
     4: [[1, 2, 4, 0, 0, 0], [2, 3, 6, 0, 0, 0], [2, 4, 7, 0, 0, 0], [2, 5, 12, 1, 2, 4], [3, 7, 17, 2, 3, 6],
         [3, 8, 19, 2, 4, 7]],
     8: [[13, 24, 44, 0, 0, 0], [20, 37, 68, 0, 0, 0], [24, 44, 81, 0, 0, 0], [56, 118, 244, 13, 24, 44],
         [82, 174, 362, 20, 37, 68], [94, 200, 418, 24, 44, 81]],
     16: [[1705, 3136, 5768, 0, 0, 0], [2632, 4841, 8904, 0, 0, 0], [3136, 5768, 10609, 0, 0, 0],
          [15776, 30956, 60504, 1705, 3136, 5768], [23780, 46732, 91460, 2632, 4841, 8904],
          [27820, 54736, 107236, 3136, 5768, 10609]],
     32: [[29249425, 53798080, 98950096, 0, 0, 0], [45152016, 83047505, 152748176, 0, 0, 0],
          [53798080, 98950096, 181997601, 0, 0, 0], [560052736, 63367377, 17030242, 29249425, 53798080, 98950096],
          [854712776, 623420113, 80397619, 45152016, 83047505, 152748176],
          [9569297, 918080153, 640450355, 53798080, 98950096, 181997601]],
     64: [[752119970, 611476256, 890873279, 0, 0, 0], [279397023, 363596219, 502349528, 0, 0, 0],
          [611476256, 890873279, 254469491, 0, 0, 0],
          [709863468, 120233913, 915989103, 752119970, 611476256, 890873279],
          [904881918, 830097381, 36223009, 279397023, 363596219, 502349528],
          [508757664, 25115824, 746086477, 611476256, 890873279, 254469491]],
     128: [[78811611, 913296203, 885290616, 0, 0, 0], [971994420, 992107814, 798586812, 0, 0, 0],
           [913296203, 885290616, 877398423, 0, 0, 0],
           [115998817, 334153082, 290694752, 78811611, 913296203, 885290616],
           [71251061, 450151899, 624847834, 971994420, 992107814, 798586812],
           [420856886, 405404143, 740846651, 913296203, 885290616, 877398423]],
     256: [[378695226, 16459982, 159625346, 0, 0, 0], [143165364, 395155208, 176085328, 0, 0, 0],
           [16459982, 159625346, 554780554, 0, 0, 0], [649396696, 799269580, 477091610, 378695226, 16459982, 159625346],
           [518196691, 448666269, 276361183, 143165364, 395155208, 176085328],
           [782809598, 317466264, 925757879, 16459982, 159625346, 554780554]],
     512: [[792800282, 32427199, 631130698, 0, 0, 0], [598703499, 825227481, 663557897, 0, 0, 0],
           [32427199, 631130698, 456358172, 0, 0, 0], [684422438, 215093308, 171928517, 792800282, 32427199, 631130698],
           [325704518, 899515746, 387021825, 598703499, 825227481, 663557897],
           [182666109, 540797826, 71444256, 32427199, 631130698, 456358172]],
     1024: [[703517207, 60734600, 290364440, 0, 0, 0], [229629840, 764251807, 351099040, 0, 0, 0],
            [60734600, 290364440, 54616240, 0, 0, 0], [729227563, 71862397, 595621906, 703517207, 60734600, 290364440],
            [233395069, 801089960, 667484303, 229629840, 764251807, 351099040],
            [11127797, 305257466, 396711859, 60734600, 290364440, 54616240]],
     2048: [[457542142, 760006910, 847996723, 0, 0, 0], [87989813, 217549045, 608003626, 0, 0, 0],
            [760006910, 847996723, 65545761, 0, 0, 0],
            [744735192, 359066367, 285379301, 457542142, 760006910, 847996723],
            [78316218, 103801552, 644445668, 87989813, 217549045, 608003626],
            [599059464, 437382585, 389180853, 760006910, 847996723, 65545761]],
     4096: [[288004644, 593634099, 310351083, 0, 0, 0], [716716991, 881638743, 903985182, 0, 0, 0],
            [593634099, 310351083, 191989819, 0, 0, 0],
            [875506184, 74636044, 614502503, 288004644, 593634099, 310351083],
            [229515376, 950142228, 689138547, 716716991, 881638743, 903985182],
            [481001952, 304151420, 564644724, 593634099, 310351083, 191989819]],
     8192: [[837676962, 377720293, 652751872, 0, 0, 0], [275031579, 215397248, 30472158, 0, 0, 0],
            [377720293, 652751872, 868149120, 0, 0, 0],
            [972861508, 156900880, 645155000, 837676962, 377720293, 652751872],
            [835502255, 129762381, 802055880, 275031579, 215397248, 30472158],
            [779180594, 992403135, 774917381, 377720293, 652751872, 868149120]],
     16384: [[252803333, 784480421, 905090014, 0, 0, 0], [120609593, 37283747, 689570428, 0, 0, 0],
             [784480421, 905090014, 942373761, 0, 0, 0],
             [73513253, 251847292, 127357808, 252803333, 784480421, 905090014],
             [970420516, 325360545, 379205100, 120609593, 37283747, 689570428],
             [467366878, 222267801, 452718353, 784480421, 905090014, 942373761]],
     65536: [[987392856, 348254956, 238601869, 0, 0, 0], [890346920, 335647805, 586856825, 0, 0, 0],
             [348254956, 238601869, 574249674, 0, 0, 0],
             [467234412, 239698793, 145271018, 987392856, 348254956, 238601869],
             [666970363, 706933205, 384969811, 890346920, 335647805, 586856825],
             [891443844, 906669156, 852204223, 348254956, 238601869, 574249674]]}


# Magic function

def pow_a(n):
    """Relatively fast matrix exponentiation"""
    if n not in d:
        pow2 = next(2 ** (x - 1) for x in count() if 2 ** x >= n)
        d[n] = mat_mul(pow_a(pow2), pow_a(n - pow2))
    return d[n]


class Solution:
    def checkRecord(self, n):
        return pow_a(n + 1)[5][2]


# LeetCode test

assert Solution().checkRecord(10101) == 183236316
