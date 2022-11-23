import pandas as pd
import numpy as np

class DATA():
    def __init__(self,filepath):
        self.filepath = filepath

    def soduku_index(self):
        # 循环每一宫
        soduku_index = np.zeros((9,9))
        index_temp = [1,2,3,10,11,12,19,20,21]
        for i in range(9):
            a = i // 3
            b = i % 3
            addition = 27*a + 3*b
            for j in range(9):
                soduku_index[i][j] = index_temp[j] + addition
        return soduku_index

    def read_soduku(self):
         df = pd.read_excel(self.filepath)
         soduku = []
         for index in df.index:
             soduku= soduku + df.loc[index].values[0:].tolist()
         # 读取每一宫已有的数字和对应位置
         exit_num = [[] for i in range(9)]
         exit_position = [[] for i in range(9)]
         empty_position = [[] for i in range(9)]
         soduku_index = self.soduku_index()
         for i in range(9):
             for j in soduku_index[i]:
                 it = int(j-1)
                 if np.isnan(soduku[it])==True:
                     empty_position[i].append(it)
                 else:
                     exit_num[i].append(soduku[it])
                     exit_position[i].append(it)
         return exit_num,exit_position,empty_position

    def display(self,x):
        lenth = len(x)
        if lenth == 0:
            x=[0 for i in range(81)]
        solution = np.zeros((9, 9))
        x_index = 0
        for i in range(9):
            for j in range(len(self.exit_position[i])):
                row = self.exit_position[i][j] // 9
                col = self.exit_position[i][j] % 9
                solution[row][col] = self.exit_num[i][j]
            for jj in range(len(self.empty_position[i])):
                row = self.empty_position[i][jj] // 9
                col = self.empty_position[i][jj] % 9
                solution[row][col] = x[x_index]
                x_index += 1
        for i in range(9):
            string_temp = f'{solution[i][0:3]}{solution[i][3:6]}{solution[i][6:9]}'
            print(string_temp)
            if i ==2 or i==5:
                lines = '-'*30
                print(lines)

    def index_gen(self):
        index_list = []
        for i in range(9):
            if i == 0:
                temp = [0, self.empty_len[i]]
            else:
                temp = [sum(self.empty_len[:i - 1]), sum(self.empty_len[:i])]
            index_list.append(temp)
        return index_list

    def data_main(self):
        self.exit_num,self.exit_position,self.empty_position = self.read_soduku()
        self.empty_len = [len(self.empty_position[i]) for i in range(9)]
        self.index_list = self.index_gen()
        self.display([])

class ABC():
    def __init__(self,popsize,MCN,limit):
        self.popsize = popsize
        self.MCN = MCN
        self.Limit = limit

    def initialize(self):
        pop = np.zeros((self.popsize,sum(sodu.empty_len)))
        fitness = np.zeros(self.popsize)
        L = np.zeros(self.popsize)
        # 随机生成可行解
        for it in range(self.popsize):
            x = []
            for i in range(9):
                num_list = [i + 1 for i in range(9)]
                for j in sodu.exit_num[i]:
                    num_list.remove(j)
                np.random.shuffle(num_list)
                x = x + num_list
            pop[it] = x
            fitness[it] = self.calculate(pop[it])
        return pop,fitness,L

    def calculate(self,x):
        # 还原该x对应的solution
        solution = np.zeros((9,9))
        fitness = 1
        x_index = 0
        for i in range(9):
            for j in range(len(sodu.exit_position[i])):
                row = sodu.exit_position[i][j] // 9
                col = sodu.exit_position[i][j] % 9
                solution[row][col] = sodu.exit_num[i][j]
            for jj in range(len(sodu.empty_position[i])):
                row = sodu.empty_position[i][jj] // 9
                col = sodu.empty_position[i][jj] % 9
                solution[row][col] = x[x_index]
                x_index += 1
        # 计算对应solution的适应度值
        # 假定正确解的适应度为0，当前solution的适应度为各行列数字重复次数。
        for i in range(9):
            arr,count = np.unique(solution[i,:],return_counts=True)
            fitness += sum(count) - len(arr)
        for j in range(9):
            arr, count = np.unique(solution[:,j], return_counts=True)
            fitness += sum(count) - len(arr)
        return fitness

    def cross_func(self,pop1,pop2):
        x1 = np.copy(pop1)
        x2 = np.copy(pop2)
        if np.random.rand()<0.5:
            # 随机选择两点进行交叉
            pos1 = np.random.randint(0,len(x1)-1)
            pos2 = np.random.randint(1, len(x1))
            while pos1 == pos2:
                pos2 = np.random.randint(1, len(x1))
            for var in range(pos1, pos2):
                x1[var], x2[var] = x1[var], x2[var]
        else:
            rand_num = np.random.choice([i for i in range(9)],np.random.randint(1,5),replace=True)
            for i in rand_num:
                x1[sodu.index_list[i][0]:sodu.index_list[i][1]],x2[sodu.index_list[i][0]:sodu.index_list[i][1]] = x2[sodu.index_list[i][0]:sodu.index_list[i][1]],x1[sodu.index_list[i][0]:sodu.index_list[i][1]]
        # 随机选择某宫进行交叉
        fitness1 = self.calculate(x1)
        fitness2 = self.calculate(x2)
        if fitness1 < fitness2:
            return x1,fitness1
        else:
            return x2,fitness2

    def mutation_func(self,pop1):
        x = np.copy(pop1)
        # 等概率选择某一宫变异或者某一段变异
        if np.random.rand()<0.5:
            m_choose = np.random.randint(9)
            np.random.shuffle(x[sodu.index_list[m_choose][0]:sodu.index_list[m_choose][1]])
        else:
            pos1 = np.random.randint(0, len(x) - 1)
            pos2 = np.random.randint(1, len(x))
            while pos1 == pos2:
                pos2 = np.random.randint(1, len(x))
            np.random.shuffle(x[pos1:pos2])
        return x

    def main_ABC(self):
        # 初始化
        pop,fitness,L = self.initialize()
        Best_chart = np.zeros(self.MCN)
        Xbest_chart = np.zeros((self.MCN,sum(sodu.empty_len)))
        # 保存当前种群最优解和最优值
        Best_chart[0] = min(fitness)
        Xbest = pop[np.argmin(fitness)]
        Xbest_chart[0] = Xbest
        # 主循环
        for it in range(1,self.MCN):
            # 雇佣蜂
            for j in range(self.popsize):
                pop_list = [i for i in range(self.popsize)]
                pop_list.remove(j)  # 取一个不同于j的数k
                k = np.random.choice(pop_list)
                new_pop,new_fit = self.cross_func(pop[j], pop[k])
                if new_fit < fitness[j]:
                    pop[j] = new_pop
                    fitness[j] = new_fit
                    L[j] = 0
                else:
                    L[j] +=1
            # 跟随蜂
            F_val = 1 / fitness
            idx = np.random.choice([i for i in range(self.popsize)], size=self.popsize, replace=True, p=(F_val) / (F_val.sum()))
            for j in idx:
                pop_list = [i for i in range(self.popsize)]
                pop_list.remove(j)  # 取一个不同于j的数k
                k = np.random.choice(pop_list)
                new_pop,new_fit = self.cross_func(pop[j], pop[k])
                if new_fit < fitness[j]:
                    pop[j] = new_pop
                    fitness[j] = new_fit
                    L[j] = 0
                else:
                    L[j] += 1
            # 侦查蜂
            for i in range(self.popsize):
                if L[i] > self.Limit:
                    pop[i] = self.mutation_func(pop[i])
                    fitness[i] = self.calculate(pop[i])
            # 保存本次迭代的最优解和最优值
            if min(fitness) < Best_chart[it-1]:
                Best_chart[it] = min(fitness)
                Xbest = pop[np.argmin(fitness)]
                Xbest_chart[it] = Xbest
            else:
                Best_chart[it] = Best_chart[it-1]
                Xbest_chart[it] = Xbest_chart[it-1]
            print(f'第{it+1}次迭代：{Best_chart[it]}')
            if Best_chart[it] ==1:
                print(Xbest_chart[it])
                print('Soduku Solution:')
                sodu.display(Xbest_chart[it])
                break

if __name__ == '__main__':
    sodu = DATA('soduku_test1.xlsx')
    sodu.data_main()
    run = ABC(1000, 100, 10)
    run.main_ABC()
