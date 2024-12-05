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
    
    def get_rad(self):
        return self.r*State.r_scaler[self.state]
    
    def get_ang(self):
        return self.ang*State.a_scaler[self.state]

    # Возвращаем угол и расстояние до другого агента
    def look(self, other):
        a, b = self.dir.copy(), other.coords-self.coords
        dot_product = np.dot(a, b)
        det = a[0] * b[1] - a[1] * b[0]
        angle = np.arctan2(det, dot_product)
        return np.degrees(angle), np.linalg.norm(b)

    def move(self, run=False):
        v = self.v*State.v_scaler[self.state] # факт. скорость
        self.coords = self.coords + self.dir*v*[1,1.25][run]
        if not 0<=self.coords[0]<101:
            self.dir[0] *= -1
            self.coords[0] = 100-(self.coords[0]%100)
        if not 0<=self.coords[1]<101:
            self.dir[1] *= -1
            self.coords[1] = 100-(self.coords[1]%100)

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
    plt.title(f'Состояние среды t={t}')


def rotate_vector(vector, angle_degrees):
    angle_radians = np.radians(angle_degrees)
    
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians)],
        [np.sin(angle_radians), np.cos(angle_radians)]
    ])
    rotated_vector = rotation_matrix.dot(vector)
    return rotated_vector / np.linalg.norm(rotated_vector)


def sim_init(n, m):
    r = 5
    v = 5
    agents = []
    for i in range(n):
        agents.append(Agent(i, v, r))

    t_init = np.random.randint(1, 20)
    m_agents = np.random.choice(n, m, replace=False)
    print(m_agents)
    for t in range(t_init):
        for a in agents:
            a.move()

    for i in m_agents:
        agents[i].t_inc = t + np.random.randint(t_inc_min, t_inc_max)
        agents[i].state = State.infected
    return agents


agents = sim_init(10, 5)

def sim(t):
    for a in agents:
        # Прошел инкубационный период
        if a.t_inc != -1 and a.t_inc == t:
            a.state = State.zombie
            a.t_inc = -1
            print(f'{t}: Agent{a.id} стал зомби')
            
        # Вероятность выздороветь 1%
        if a.state == State.zombie:
            if np.random.choice(2, p=[0.99, 0.01]):
                a.state = State.recovered
                print(f'{t}: Agent{a.id} выздоровел')
            
        # Бежит ли агент
        run = False
        temp = []
            
        # Собираем агентов из области видимости
        for b in agents:
            if b.id != a.id:
                ang, dist = a.look(b)
                if abs(ang) <= a.get_ang()/2 and dist <= a.get_rad():
                    temp.append((b, ang, dist))
            
        match a.state:
            # Здоровый агент убегает если рядом зомби
            case State.healthy:
                right, left = False, False
                for b,ang,dist in temp:
                    if b.state == State.zombie:
                        if ang <= 0:
                            right = True
                        else:
                            left = True
                if right or left:
                    run = True
                    if right and left:
                        a.dir *= -1
                    elif right:
                        a.dir = rotate_vector(a.dir, a.ang/2)
                    else:
                        a.dir = rotate_vector(a.dir, -a.ang/2)
            # Зомби заражает агента из области действия
            # или бежит за ближайшим агентом из области видимости
            case State.zombie:
                r_min = -1
                an_min = -1
                    
                for b,ang,dist in temp:
                    if b.state in [State.recovered, State.healthy]:
                        if dist <= a.get_rad()*0.93 and abs(ang) <= a.get_ang()*0.93:
                            # Заражаем агентов из области действия
                            if b.state == State.healthy:
                                b.state = State.infected
                                print(f'{t}: Agent{a.id} заболел')
                                b.t_inc = t + np.random.randint(t_inc_min, t_inc_max)
                            # С вероятностью 25% обращаем в зомби выздоровевшего агента
                            elif np.random.choice(2, p=[0.75, 0.25]):
                                b.state = State.zombie
                                print(f'{t}: Agent{a.id} стал зомби')
                        # Гонимся за ближайшим здоровым агентом
                        elif b.state == State.healthy:
                            if r_min == -1:
                                r_min = dist
                                an_min = ang
                            elif r_min > dist:
                                r_min = dist
                                an_min = ang
                if r_min != -1:
                    a.dir = rotate_vector(a.dir, an_min)
                

        a.move(run)
    draw(agents, t)

T = 100

fig = plt.figure()
ani = animation.FuncAnimation(fig, sim, frames=T, interval=200, repeat=False)
plt.show()