from clify.utils.type_testing import type_of_all


def test_type_off_all(cleanup_tmp_dir):
    a = [2, 3, 4]
    t = int
    type_of_all(a, t)
    a.append(3.4)
    type_of_all(a, t)
