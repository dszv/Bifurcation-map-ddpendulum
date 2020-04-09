import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')
from scipy.integrate import solve_ivp

q = 2.0
u = 2.0/3.0
t_0 = 0
t_N = 1150
h = 0.001


def reduce(angle):
    if(angle < 0):
        while(angle < -np.pi):
            angle = angle + 2 * np.pi
    else:
        while(angle > np.pi):
            angle = angle - 2 * np.pi
    return angle

def f(t , X):
    return [X[1] , - (1/q) * X[1] - np.sin(X[0]) + a * np.cos(X[2]) , u]

def main():
    A = np.linspace(0.5 , 2 , 200)

    fig, ax = plt.subplots(figsize=(16, 12))

    N = int((t_N - t_0)/h)
    t = np.linspace(t_0, t_N, N+1)

    print("Working on it...")

    global a
    for a in A:
        
        X_0 = [np.pi/4 , 0 , 0]    #initial conditions 

        sol = solve_ivp(f , [t_0, t_N] , X_0 , method = 'DOP853' , t_eval = t) #dense_output=True

        x = sol.y[0].T
        r = np.empty(N+1 , dtype=float)    #reduced x
        y = sol.y[1].T
        z = sol.y[2].T

        for i in range (N+1):
            r[i] = reduce(x[i])

        j = t_N/(2 * h)
        n = 1
        k = np.abs((2 * np.pi)/(h * u))

        while(j <= N):
            #print(n , j)
            #print(r[int(j)] , y[int(j)])
            plt.plot(a , np.around(y[int(j)] , 2) , '.' , color = 'blue')
            j = j + k
            n = n + 1

    ax.set_xlabel('a')
    ax.set_ylabel('$\omega$')
    plt.tight_layout()
    fig.savefig('bifurcation-map.pdf')
    plt.show()

if __name__ == "__main__":
    main()
