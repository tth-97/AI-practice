import random

class LakeWorld():
    def __init__(self):
        self.x = start_x
        self.y = start_y

    def step(self, a):
        if a==0:
            self.move_up()
        elif a==1:
            self.move_right()
        elif a==2:
            self.move_down()
        elif a==3:
            self.move_left()

        reward = self.get_reward()
        terminated = self.is_terminated()
        return (self.x, self.y), reward, terminated

    def move_up(self):
        if self.x==0:
            pass
        else:
            self.x -= 1

    def move_right(self):
        if self.y==col-1:
            pass
        else:
            self.y += 1
            
    def move_down(self):
        if self.x==row-1:
            pass
        else:
            self.x += 1

    def move_left(self):
        if self.y==0:
            pass
        else:
            self.y -= 1
    
    def is_terminated(self):
        if lake[self.x][self.y]=='H' or lake[self.x][self.y]=='G':
            return True
        else:
            return False

    def get_reward(self):
        if lake[self.x][self.y]=='H':
            return -1
        elif lake[self.x][self.y]=='G':
            return 1
        else:
            return 0

    def reset(self):
        self.x = start_x
        self.y = start_y
        return (self.x, self.y)


class QAgent():
    def __init__(self):
        #row=x축(세로), col=y축(가로), depth=z축(높이)인 3차원 리스트생성  
        self.q_table = [[[0 for c in range(col)] for r in range(row)] for depth in range(a_num)]
        self.gamma = 0.5
        self.eps = 0.9

    def select_action(self, s):
        x, y = s
        coin = random.random()
        if coin < self.eps:
            action = random.randint(0,3)
        else:
            action = 0
            action_val = self.q_table[0][x][y]
            for i in range(a_num):
                tmp = self.q_table[i][x][y]
                if tmp>action_val:
                    action_val = tmp
                    action = i
        return action

    def update_table(self, transition):
        s, a, r, s_prime = transition
        x, y = s
        next_x, next_y = s_prime

        maxQ = self.q_table[0][next_x][next_y]
        for i in range(a_num):
            tmp = self.q_table[i][next_x][next_y]
            if tmp>maxQ:
                maxQ = tmp
        #Q러닝 업데이트 식 사용
        self.q_table[a][x][y] = r + self.gamma * maxQ

    def get_best_action_list(self):
        best_action_list = [[0 for i in range(col)] for j in range(row)]
        for i in range(row):
            for j in range(col):
                action = 0
                action_val = self.q_table[0][i][j]
                for k in range(a_num):
                    tmp = self.q_table[k][i][j]
                    if tmp>action_val:
                        action_val = tmp
                        action = k
                    if action_val == 0:
                        action = 'x'
                best_action_list[i][j] = action

        return best_action_list
        

def main(file_number):
    env = LakeWorld()
    agent = QAgent()

    for n in range(700000):
        terminated = False
        s = env.reset()
        while not terminated:
            a = agent.select_action(s)
            s_prime, r, terminated = env.step(a)
            agent.update_table((s,a,r,s_prime))
            s = s_prime
    best_action_list = agent.get_best_action_list()

    #output파일처리
    if file_number==1:
        f = open('FrozenLake_1_output.txt', 'w')
    elif file_number==2:
        f = open('FrozenLake_2_output.txt', 'w')
    elif file_number==3:
        f = open('FrozenLake_3_output.txt', 'w')
    f.write(str(file_number)+" "+str(row)+ " "+str(col)+"\n")
    
    (x_, y_) = env.reset()
    path=[]
    while(best_action_list[x_][y_]!='x'):
        best_action=best_action_list[x_][y_]
        if best_action==0:
            x_ -= 1
        elif best_action==1:
            y_ += 1
        elif best_action==2:
            x_ += 1
        elif best_action==3:
            y_ -= 1
        path.append((x_,y_))

    for i in range(row):
        for j in range(col):
            if lake[i][j]=='F':
                in_path = False
                for k in range(len(path)):
                    if path[k]==(i,j):
                        in_path = True
                if in_path:
                    f.write('R')
                else:
                    f.write('F')
            elif lake[i][j]=='S':
                f.write('S')
            elif lake[i][j]=='H':
                f.write('H')
            elif lake[i][j]=='G':
                f.write('G')
        f.write('\n')
    f.close()


if __name__ == "__main__":

    with open("FrozenLake_1.txt", 'r') as f1:
        lines1 = f1.read().splitlines()

    with open("FrozenLake_2.txt", 'r') as f2:
        lines2 = f2.read().splitlines()
    
    with open("FrozenLake_3.txt", 'r') as f3:
        lines3 = f3.read().splitlines() 

    files = { 1:lines1, 2:lines2, 3:lines3}
    
    global row, col
    global lake
    global start_x, start_y
    global a_num

    a_num = 4

    for f in [1,2,3]:
        info = files[f].pop(0)
        row = int(info.split()[1])
        col = int(info.split()[2])
        lake = files[f]
        for i in range(row):
            for j in range(col):  
                if f==1:
                    if lake[i][j]=='S':
                        start_x = i
                        start_y = j
                elif f==2:
                    if lake[i][j]=='S':
                        start_x = i
                        start_y = j
                elif f==3:
                    if lake[i][j]=='S':
                        start_x = i
                        start_y = j
        main(f)