def get_t(N, M, K):
  return 29+4+N*(4+M*K*3+(M-1)*17+5+3+16)-16+4+20
# проц. 3.1 ГГц, 1 мс = 1000 мкс = 1_000_000 нс
goal = 3_100_000 * 145 # целевое кол-во тактов


l = []
for N in range(3000, 3500):
  for M in range(3000, 3500):
    for K in range(1, 10):
      T = get_t(N, M, K)
      l.append((T, N, M, K))
l.sort(key=lambda x: abs(goal-x[0]))
print(*l[:10], sep='\n')
