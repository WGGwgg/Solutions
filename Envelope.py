import numpy as np
class solution():
    def __init__(self,envelopes):
        self.envelopes = envelopes
        self.n = np.size(envelopes,0)
        self.dim = np.size(envelopes,1)
        
    def solver(self):
        if not self.envelopes:
            return 0
        envelopes.sort(key=lambda x:(x[0],-x[1]))
        f = [1]*self.n
        for i in range(self.n):
            for j in range(i):
                if self.envelopes[j][1]<self.envelopes[i][1]:
                    f[i] = max(f[i],f[j]+1)
        return max(f)
        
    def main(self):
        self.output = self.solver()
        print('输出为：',self.output)
if __name__ == '__main__':
    envelopes = [[5,4],[6,4],[6,7],[2,3]]
    # envelopes = [[1,1],[1,1],[1,1]]
    example = solution(envelopes)
    example.main()
