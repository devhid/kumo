import unittest
from funcs.transform import *

class TransformTest(unittest.TestCase):

    def test_lower(self):
        transform_lower_to_lower = list(generate_transformations(['test']).values())[0]
        transform_upper_to_lower = list(generate_transformations(['ALL CAPS']).values())[0]
        assert transform_lower_to_lower.lower == 'test'
        assert transform_upper_to_lower.lower == 'all caps'

    def test_upper(self):
        transform_lower_to_upper = list(generate_transformations(['test']).values())[0]
        transform_upper_to_upper = list(generate_transformations(['ALL CAPS']).values())[0]
        assert transform_lower_to_upper.upper == 'TEST'
        assert transform_upper_to_upper.upper == 'ALL CAPS'

    def test_reverse(self):
        transform = list(generate_transformations(['reverse']).values())[0]
        assert transform.reverse == 'esrever'

    def test_leet(self):
        transform_a_to_4 = list(generate_transformations(['abcABCAa4']).values())[0]
        transform_e_to_3 = list(generate_transformations(['3needEE3']).values())[0]
        transform_l_to_1 = list(generate_transformations(['llLL11']).values())[0]
        transform_t_to_7 = list(generate_transformations(['ttTT77']).values())[0]
        transform_o_to_0 = list(generate_transformations(['ooOO00']).values())[0]
        transform_mix = list(generate_transformations(['the quick brown fox jumped over the lazy dog']).values())[0]

        assert transform_a_to_4.leet == '4bc4BC444'
        assert transform_e_to_3.leet == '3n33d333'
        assert transform_l_to_1.leet == '111111'
        assert transform_t_to_7.leet == '777777'
        assert transform_o_to_0.leet == '000000'
        assert transform_mix.leet == '7h3 quick br0wn f0x jump3d 0v3r 7h3 14zy d0g'