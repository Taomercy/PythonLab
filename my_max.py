from collections.abc import Iterable


def my_max(*args, key=None, default=None):
    def inner_max(arg):
        max_value = arg[0]
        if not key:
            for i in arg[1:]:
                if i > max_value:
                    max_value = i
        else:
            for i in arg[1:]:
                if key(i) >= key(max_value):
                    max_value = i
        return max_value

    if len(args) == 1:
        assert isinstance(args[0], Iterable)
        if len(args[0]) == 0:
            return default
        return inner_max(args[0])
    elif len(args) > 1:
        return inner_max(args)
    else:
        raise Exception('parameter error')


a = [1, 3, 2, 5]
b = [3, 2, 3, 1, "6"]
c = [[1, 2], (1, 3)]


print(max(a))
print(my_max(b, key=int))
print(my_max(c, key=lambda x: x[1]))
