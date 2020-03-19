
class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)
        #Warning: You may wish to do a deepcopy here if returning objects
        return self.memo[args]
@Memoize
def factorial(k):
    if k < 2: return 1
    return k * factorial(k - 1)
def normal_factorial(k):
    if k < 2: return 1
    return k * factorial(k - 1)
for i in range(100):
    print(normal_factorial(i))