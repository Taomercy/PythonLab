import unittest


# solver 1
def utility_function(s, j):
    ret = list(s)
    ret.pop(j)
    return "".join(ret)


def no_name(string_a, string_b):
    if len(string_a) != len(string_b):
        return False
    for x in range(len(string_b)):
        if string_a[0] == string_b[x]:
            return no_name(utility_function(string_a, 0), utility_function(string_b, x))
    return len(string_b) == 0


# solver 2
def my_solver(string_a, string_b):
    if type(string_a) is str and type(string_b) is str:
        a, b = list(string_a), list(string_b)
        a.sort()
        b.sort()
        return a == b
    else:
        raise TypeError


# a = "light123"
# b = "thgli213"
# c = "light123"
# d = "liigh12"
# print(no_name(a, b))
# print(no_name(a, c))
# print(no_name(a, d))
# print("==========")
# print(my_solver(a, b))
# print(my_solver(a, c))
# print(my_solver(a, d))


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        print("Unittest Start")

    def test_empty_strings(self):
        """测试字符串为空的情况"""
        self.assertTrue(my_solver("", ""))
        self.assertFalse(my_solver("", "abc"))
        self.assertFalse(my_solver("aa", ""))

    def test_diff_length_strings(self):
        """测试字符串长度不同的情况"""
        self.assertFalse(my_solver("hello", "helo"))

    def test_permutation(self):
        """测试字符串全排列的情况"""
        self.assertTrue(my_solver("abc", "abc"))
        self.assertTrue(my_solver("abc", "acb"))
        self.assertTrue(my_solver("abc", "bac"))
        self.assertTrue(my_solver("abc", "bca"))
        self.assertTrue(my_solver("abc", "cab"))
        self.assertTrue(my_solver("abc", "cba"))

    def test_chinese(self):
        """测试字符串是中文的情况"""
        self.assertTrue(my_solver("一二三", "三一二"))
        self.assertFalse(my_solver("一二三", "三一二四"))

    @classmethod
    def tearDownClass(self):
        print("Unittest End")


if __name__ == "__main__":
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(Test('test_empty_strings'))
    suite.addTest(Test('test_diff_length_strings'))
    suite.addTest(Test('test_permutation'))
    suite.addTest(Test('test_chinese'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
