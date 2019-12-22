from scipy.optimize import curve_fit

class Fit:
    def __init__(self, **kwargs):
        self._func = kwargs

    def __getattribute__(self, key):
        if key in object.__getattribute__(self, '_func'):
            return object.__getattribute__(self, '_func')[key]
        else:
            return object.__getattribute__(self, key)

    def fit(self, fname, xs, ys):
        func = self._func[fname]
        popt, pcov = curve_fit(func, xs, ys)
        yvs = func(xs, *popt)
        yavg = ys.mean()
        dy =  ys - yvs
        dyavg = ys - yavg
        R2 = 1 - (dy * dy).sum() / (dyavg * dyavg).sum()
        print(fname + '\nparameter=' + str(popt) + '\nR^2=' + str(R2) + '\n')
        return dict(func=fname, \
                    popt=popt.tolist(), \
                    pcov=pcov.tolist(), \
                    R2=R2.tolist())
