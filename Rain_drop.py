import matplotlib.pyplot as plt
import numpy as np


class solution():
    def __init__(self, height):
        self.height = np.array(height)
        self.n = len(height)

    def plot(self):
        x = np.arange(self.n) + 1
        plt.bar(x, height=self.height, width=1, tick_label=x, edgecolor='black')
        plt.grid(axis='y')
        plt.show()

    def solver(self):
        sum_rain = 0
        # i点的值等于左右两侧的高度最小值- height[i]
        for i in range(self.n):
            if i != 0 and i != self.n - 1:
                # 将height切成两段，取左右两侧的最大值，雨水量等于min(max_left,max_right)-height[i]
                max_left = max(height[:i])
                max_right = max(height[i + 1:])
                sum_rain += min(max_left, max_right) - height[i] if min(max_left, max_right) > height[i] else 0
        return sum_rain

    def main(self):
        self.plot()
        self.result = self.solver()


if __name__ == '__main__':
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    # height = [4,2,0,3,2,5]
    drop_rain = solution(height)
    drop_rain.main()
    print('Rain Volume is:\t', drop_rain.result)