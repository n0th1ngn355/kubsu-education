import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

class State:
    healthy = 0
    infected = 1
    zombie = 2
    recovered = 3
    v_scaler = [1, 0.9, 0.85, 1]
    r_scaler = [1, 1, 1.1, 1]
    a_scaler = [1, 1, 0.75, 1]

t_inc_min = 1
t_inc_max = 10

class Agent:
    def __init__(self, id, v, r):
        self.id = id
        self.coords = np.random.randint(0, 101, 2)
        self.t_inc = -1
        self.state = State.healthy
        
        self.ang = np.random.randint(90, 151)
        self.v = v
        self.r = r

        self.dir = np.random.rand(2)*2-1 # направление движения
        self.dir /= np.linalg.norm(self.dir) # нормализация
        # self.a_h = self.a # а здорового агента
    
    def move(self):
        self.coords = self.coords + self.dir*self.v*State.v_scaler[self.state]
        if not 0<self.coords[0]<101:
            self.dir[0] *= -1
        if not 0<self.coords[1]<101:
            self.dir[1] *= -1

    def __repr__(self):
        return f"Agent{self.id} ({self.x}, {self.y})"
    
    def __str__(self):
        return self.__repr__()



def draw(agents, t):
    plt.clf()  # Очистка текущего графика
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    for i in agents:
        plt.scatter(*i.coords, c='gyrb'[i.state])
        plt.quiver(*i.coords, *(i.dir), width=0.005)
        # print(*i.coords, *(i.dir*i.v), i.dir*i.v)
        # plt.text(*i.coords, i.dir)
    # plt.axis([0,100,0,100])
    plt.title(f'Состояние среды {t}')



r = 5
v = 2
n = 10
agents = []
for i in range(n):
    agents.append(Agent(i, v, r))

t_init = np.random.randint(1, 20)
m = n//5
m_agents = np.random.choice(n, m, replace=False)
print(m_agents)
T = 100
for t in range(t_init):
    for a in agents:
        a.move()
for i in m_agents:
    agents[i].t_inc = np.random.randint(t_inc_min, t_inc_max)
    agents[i].state = State.infected

def sim(t):
    for a in agents:
        if a.t_inc != -1 and a.t_inc == t:
            a.state = State.zombie
        a.move()
    draw(agents, t)



fig = plt.figure()
ani = animation.FuncAnimation(fig, sim, frames=T, interval=20, repeat=False)
plt.show()