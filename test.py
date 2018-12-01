from tests.test_transform import *
from configs import configs

if __name__ == "__main__":
    # Change the value of test to change what is tested
    test = "configs"
    if test == "configs":
        config = configs.config
        for val in config:
            print("%s : %s" % (val,config[val]))
    elif test == "test_transform":
        test_transform = TransformTest()
        test_transform.test_upper()
        test_transform.test_lower()
        test_transform.test_reverse()
        test_transform.test_leet()