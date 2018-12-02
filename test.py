from tests.test_transform import *
from tests.test_link_utils import *

test_transform = TransformTest()
test_transform.test_upper()
test_transform.test_lower()
test_transform.test_reverse()
test_transform.test_leet()

test_link_utils = LinkUtilsTest()
test_link_utils.test_one_layer()
test_link_utils.test_multiple_layers()
test_link_utils.test_link_layer()
test_link_utils.test_link_retrieval()
test_link_utils.test_link_retrieval_layers()
test_link_utils.test_link_retrieval_relative()
test_link_utils.test_login_detection()