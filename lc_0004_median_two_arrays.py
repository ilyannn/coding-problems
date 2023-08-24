import unittest
from typing import List


def median(nums):
    if nums:
        return (nums[(len(nums) - 1) // 2] + nums[len(nums) // 2]) / 2


def median_lr(nums, l, r):
    if r > l:
        return (nums[l + (r - l - 1) // 2] + nums[l + (r - l) // 2]) / 2


class Solution:
    def findMedianSortedArrays(self, nums1_g: List[int], nums2_g: List[int]) -> float:
        def find(nums1, nums2, n1l, n1r, n2l, n2r) -> float:
            if n1r + n2r - n1l - n2l < 30:
                return median(sorted(nums1[n1l:n1r] + nums2[n2l:n2r]))

            m1 = median_lr(nums1, n1l, n1r)
            m2 = median_lr(nums2, n2l, n2r)

            if m1 is None:
                return m2
            if m2 is None:
                return m1

            if m1 > m2:
                nums1, nums2 = nums2, nums1
                n1l, n2l = n2l, n1l
                n1r, n2r = n2r, n1r

            len1 = n1r - n1l
            len2 = n2r - n2l

            if nums1[len1 - 1 + n1l] <= nums2[n2l]:
                return median(nums1[n1l:n1r] + nums2[n2l:n2r])

            t1 = max((len1 - 6), 0) // 2  # 1
            t2 = max((len2 - 6), 0) // 2  # 0

            l1 = t1  # 1
            r2 = len2 - t2  # 1

            if t2 > t1:
                r1 = len1
                l2 = t2 - t1
            else:
                r1 = len1 - t1 + t2  # 3
                l2 = 0  # 0

            return find(nums1, nums2, n1l + l1, n1l + r1, n2l + l2, n2l + r2)

        return find(nums1_g, nums2_g, 0, len(nums1_g), 0, len(nums2_g))


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.solution = Solution()

    def test_failing1(self):
        self.assertEqual(self.solution.findMedianSortedArrays([1, 2, 4, 5], [3]), 3)

    def test_failing2(self):
        self.assertEqual(
            self.solution.findMedianSortedArrays([2], [1, 3, 4, 5, 6, 7, 8, 9, 10]), 5.5
        )


if __name__ == "__main__":
    unittest.main()
