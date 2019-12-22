import pickle
import os

class Memo:
    def __init__(self, **kwargs):
        self._params = {
            'pnt':kwargs.get('pnt', {}),
            'snt':kwargs.get('snt', {}),
            'coe':kwargs.get('coe', {}),
            }
        self._pnt = self._params['pnt']
        self._snt = self._params['snt']
        self._coe = self._params['coe']
        self._pool = kwargs.get('pool', None)
        if self._pool:
            self.map = self._pool.map
        else:
            self.map = lambda x, *y: list(map(x, *y))

    def set_pool(self, pool):
        self._pool = pool
        if self._pool:
            self.map = self._pool.map
        else:
            self.map = lambda x, *y: list(map(x, *y))

    def _coe_aux(self, n, t):
        return ((n-2)/(n-1))**(t-2)

    def coe(self, n, t):
        if self._coe.get((n, t)) is None:
            self._coe[n, t] = self._coe_aux(n, t)
        return self._coe[n, t]

    def _pnt_aux(self, n, t):
        if n == 1 or n == 2:
            return 1.0 if t == n else 0.0
        elif n == 3:
            if t < n:
                return 0.0
            else:
                return 0.5 ** (t-2)
        else:
            return self.snt(n-1, t-1) * self.coe(n, t)

    def pnt(self, n, t):
        if self._pnt.get((n, t)) is None:
            self._pnt[n, t] = self._pnt_aux(n, t)
        return self._pnt[n, t]

    def _snt_aux(self, n, t):
        if n == 1 or n == 2:
            return float(n) if t == n else 0.0
        elif n == 3:
            if t < n:
                return 0.0
            else:
                return 1 - 0.5 ** (t-2)
        elif t == n:
            return self.pnt(n, t)
        else:
            return self.snt(n, t-1) + self.pnt(n, t)
            
    def snt(self, n, t):
        if self._snt.get((n, t)) is None:
            self._snt[n, t] = self._snt_aux(n, t)
        return self._snt[n, t]

    def save(self, name, file=None):
        if file is None:
            openf = open
        else:
            openf = file.open
        f = openf(name, 'wb')
        try:
            pickle.dump(self._params, f)
            f.close()
            return True
        except Exception as e:
            f.close()
            print(e)
            return False

    def load(self, name, file=None):
        if file is None:
            listdir = os.listdir
            openf = open
        else:
            listdir = file.listdir
            openf = file.open
        if name in listdir():
            f = openf(name, 'rb')
            try:
                tmp_params = pickle.load(f)
                self._params = tmp_params
                self._pnt = self._params['pnt']
                self._snt = self._params['snt']
                self._coe = self._params['coe']
                f.close()
                return True
            except Exception as e:
                f.close()
                print(e)
                return False
