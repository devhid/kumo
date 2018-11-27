from tests.test_transform import *
from tests.test_tokenize import *

test_transform = TransformTest()
test_transform.test_upper()
test_transform.test_lower()
test_transform.test_reverse()
test_transform.test_leet()

test_tokenize = TokenizeTest()
test_tokenize.test_one_layer()
test_tokenize.test_multiple_layers()
test_tokenize.test_link_layer()
test_tokenize.test_link_retrieval()
test_tokenize.test_link_retrieval_layers()
