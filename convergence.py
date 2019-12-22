import numpy as np

class Convergence:
    def __init__(self, mode='D', epsilon=0.125):
        self._mode = mode
        self._epsilon = epsilon
        self._func = {
            'D': self._DAlembert,
            'C': self._Cauchy,
            }
        self._dict = False
        self.judge = False

    def set_param(self, **kwargs):
        self._dict = self._func[self._mode](**kwargs)
        self.count = self._dict.get('count', lambda:-1)
        self.judge = self._dict.get('judge', lambda x:x < self._epsilon)

    def _DAlembert(self, **kwargs):
        count = kwargs.get('count', 0)
        big_n = kwargs.get('big_n', 1000)
        x1 = -10
        x2 = 0

        def judge(x):
            nonlocal count, x1, x2
            count += 1
            x1 = x2
            x2 = x
            return count > big_n and \
                   x2 < x1 * self._epsilon

        return { 'count':lambda:count, 'judge':judge }
    
    def _Cauchy(self, **kwargs):
        count = kwargs.get('count', 0)
        big_n = kwargs.get('big_n', 1000)
        sum_num = kwargs.get('sum_num', 1000)
        cursor = 0
        list_count = 0
        memo_list = np.zeros((sum_num,))
        sum_list = 0

        def judge(x):
            nonlocal count, big_n, sum_num, cursor, list_count, memo_list, sum_list
            count += 1
            if list_count == sum_num:
                sum_list -= memo_list[cursor]
            else:
                list_count += 1
            memo_list.put(cursor, x)
            sum_list += x
            cursor = 0 if cursor == sum_num - 1 else cursor + 1
            return count > big_n and \
                   list_count == sum_num and sum_list < self._epsilon

        return { 'count':lambda:count, 'judge':judge }
