from random import randint, random
import numpy as np

t = 0

a, b = 1, 10
complexity = (1, 100)

n, m = 4, 40

class Agent:
  def __init__(self, id):
    self.id = id
    self.queue = []
    self.tek_time = 0
    self.count = 0
    self.time = 0
    
  def add_client(self, k):
    self.tek_time += k
    self.queue.append(k)
    self.count += 1
    self.time += k
  
  def __str__(self):
    return self.time
  def __lt__(self, other):
    return self.tek_time < other.tek_time

  def __eq__(self, other):
    return self.tek_time == other.tek_time

  def __gt__(self, other):
    return self.tek_time > other.tek_time

agents = np.array([Agent(i) for i in range(n)])
for i in range(m):
  dt = a + random()*b
  
  for ag in agents:
    ag.tek_time = max(ag.tek_time-dt, 0)
    dt1 = dt
    while ag.queue and dt1 >= ag.queue[0]:
      dt1 -= ag.queue[0]
      ag.queue.pop(0)
    if ag.queue:
      ag.queue[0] -= dt1
  
  agents[agents.argmin()].add_client(randint(*complexity))

res = sorted(agents, key=lambda x:[m-x.count, x.time])
for i in range(n):
  print(f"Агент {res[i].id} клиентов {res[i].count}, время {res[i].time}")