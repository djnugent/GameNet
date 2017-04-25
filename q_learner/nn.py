
from sknn.mlp import Regressor, Layer
import World
import threading
import time
import numpy as np


mdl = Regressor(
    layers=[
        Layer("Tanh", units=12),
        Layer("Tanh", units=4),
        Layer("Linear")],
    learning_rate=0.02,
    n_iter=2)



x = np.array([[1,2,0,0,0,1],[4,2,0,1,0,0],[1,1,0,0,1,0]])
y = np.array([1,-7,6])
mdl.fit(x,y)


def do_action(action):
    s = World.player
    r = -World.score
    if action == 0:
        World.try_move(0, -1)
    elif action == 1:
        World.try_move(0, 1)
    elif action == 2:
        World.try_move(-1, 0)
    elif action == 3:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    return s, action, r, s2


actions = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]



def run():
    global discount
    time.sleep(1)

    t = 1
    X = np.zeros((1,6))
    Y = np.zeros(1)
    x = []
    while True:
        s = World.player
        q = []
        for a in actions:
            s_a = np.append(s,a)
            q.append(mdl.predict(np.array([s_a]))[0])

        action = np.argmax(q)


        n = np.random.rand(1)%1
        if n < t:
            print("ran")
            action = np.random.randint(0,4, size=1)[0]

        x.append(np.append(s,actions[action]))
        do_action(action)
        print("do action:",action)

        if World.has_restarted():
            t *= 0.98
            score = World.score
            x = x[-20:]
            y = np.zeros(len(x))
            for i in range(0,len(y)):
                print(score / (len(y)-i))
                y[i] = score / (len(y)-i)

            X = np.concatenate((X,np.array(x)),axis=0)
            Y = np.concatenate((Y,y))

            print(len(X),len(Y))
            mdl.fit(X,Y)

            x = []
            y = []
            World.restart_game()
            #time.sleep(0.01)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(0.1)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()

input = state, output = action
