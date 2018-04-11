# def combinations(iterable, r):
#     # combinations('ABCD', 2) --> AB AC AD BC BD CD
#     # combinations(range(4), 3) --> 012 013 023 123
#     pool = tuple(iterable)
#     n = len(pool)
#     if r > n:
#         return
#     indices = range(r)
#     yield tuple(pool[i] for i in indices)
#     while True:
#         for i in reversed(range(r)):
#             if indices[i] != i + n - r:
#                 break
#         else:
#             return
#         indices[i] += 1
#         for j in range(i+1, r):
#             indices[j] = indices[j-1] + 1
#         yield tuple(pool[i] for i in indices)


# def findsubsetcomb(s, k):
#     return set(combinations(s, k))

# print findsubsetcomb(set([2,4,5]), 2)


def accept(cur, nei, temp):
    if nei > cur:
        return 1.
    return math.exp((cur - nei)/temp)

def test():
    x = [i/100. for i in range(-300, 500)]
    y = [i**3 +i**2 - math.exp(i) for i in x]
    cur = float(x[1])
    ycur = cur**3 + cur**2 - math.exp(cur)
    best = float(cur)
    ybest = best**3 + best**2 - math.exp(best)
    temp = 5
    rri = 3

    while temp > 1:
        rri = random.randint(0, 799)
        neighbour = float(x[rri])
        yneighbour = neighbour**3 + neighbour**2 - math.exp(neighbour)
        
        if accept(ycur, yneighbour, temp) > random.random():
            cur = float(neighbour)
            ycur = cur**3 + cur**2 - math.exp(cur)
        if ycur > ybest:
            best = float(cur)
            ybest = best**3 + best**2 - math.exp(best)
    
        temp = temp * 0.99
    print best
    print best**3 + best**2 - math.exp(best)

    print max(y)
    plt.plot(x,y)
    plt.show()
    
class Fac(object):
	def __init__(self, n):
		self.n = n 
		self.product = 1

	def __iter__(self):
		return self

	def next(self):
		if self.n == 0:
			raise StopIteration()
		if self.n > 0:
			r = self.product
			r *= self.n
			self.n = self.n - 1
			return r
		
			

for i in Fac(5):
	print i