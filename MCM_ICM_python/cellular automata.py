import numpy as np
import matplotlib.pyplot as plt
'''
1． 如果一个细胞周围有3个细胞为生（一个细胞周围共有8个细胞），
    则该细胞为生（即该细胞若原先为死，则转为生，若原先为生，则保持不变） 。
2． 如果一个细胞周围有2个细胞为生，则该细胞的生死状态保持不变；
3． 在其它情况下，该细胞为死（即该细胞若原先为生，则转为死，若原先为死，则保持不变）
    设定图像中每个像素的初始状态后依据上述的游戏规则演绎生命的变化，
    由于初始状态和迭代次数不同，将会得到令人叹服的优美图案。
'''

class cellular_automata(object):

    def __init__(self, cells_shape):
        #   cells_shape为元祖
        self.cells = np.zeros(cells_shape)

        #   真实的长度和宽度,边界
        real_width = cells_shape[0] - 2
        real_height = cells_shape[1] - 2


        self.cells[1:-1, 1:-1] = np.random.randint(2, size=(real_width, real_height))
        '''
        np.random.randint(2,size=(6,6))
        array([     [0, 0, 1, 1, 1, 1],
                    [0, 0, 1, 1, 1, 1],
                    [0, 0, 0, 0, 1, 0],
                    [1, 0, 1, 0, 1, 0],
                    [1, 1, 0, 1, 0, 0],
                    [1, 0, 1, 0, 1, 0]      ])
        '''
        self.timer = 0  #迭代次数

        #   卷积的第一个向量
        self.mask = np.ones(9)
        #   仅仅需要计算周围八个，不需要中间的值
        self.mask[4] = 0

    def update_state(self):
        """更新一次状态"""
        buf = np.zeros(self.cells.shape)
        cells = self.cells
        for i in range(1, cells.shape[0] - 1):
            for j in range(1, cells.shape[0] - 1):
                # 计算该细胞周围的存活细胞数,转化为向量
                neighbor = cells[i - 1:i + 2, j - 1:j + 2].reshape((-1,))
                '''
                In [48]: a
                array([[ 0,  1,  2,  3],
                       [ 4,  5,  6,  7],
                       [ 8,  9, 10, 11]])

                In [49]: a.reshape(1,12)
                Out[49]: array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11]])
                
                In [50]: a.reshape((-1,)).shape
                Out[50]: (12,)
                '''

                #   卷积
                neighbor_num = np.convolve(self.mask, neighbor, 'valid')[0]

                #test = sum(neighbor)

                if neighbor_num == 3:
                    buf[i, j] = 1
                elif neighbor_num == 2:
                    buf[i, j] = cells[i, j]
                else:
                    buf[i, j] = 0

        #更新cells和时间timer
        self.cells = buf
        self.timer += 1

    def plot_state(self):
        """画出当前的状态"""
        plt.title('Iter :{}'.format(self.timer))
        plt.imshow(self.cells)
        plt.show()

    def update_and_plot(self, n_iter):
        """更新状态并画图
        Parameters
        ----------
        n_iter : 更新的轮数
         如果想更新曲线的时候，在一个figure上画出不断更新的曲线的时候，
         需要用到plt.ion()和plt.ioff()以及plt.show()的配合
        """
        plt.ion()
        for _ in range(n_iter):
            plt.title('Iter :{}'.format(self.timer))
            plt.imshow(self.cells)
            self.update_state()
            plt.pause(0.2)
        plt.ioff()
        #   防止闪退
        plt.show()


if __name__ == '__main__':
    game = cellular_automata(cells_shape=(60, 60))
    game.update_and_plot(20)
