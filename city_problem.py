import numpy as np
import os
import json
from argparser import argument_parser
from memo import Memo
from fit import Fit
from convergence import Convergence
from file import File
#from multiprocessing import Pool as ProcessPool
#from multiprocessing.dummy import Pool as ThreadPool
#import matplotlib.pyplot as plt

# p(n, t): the probability of traveling n cities using t days.
# p(a, t) = 1 / (a-1)^(t-2) if a=3, aka. p(3, t) = 1 / 2^(t-2)
# p(n, n) = (n-2)! / ((n-1)^(n-2))
# p(n+1, n+1) = (n-1)! / (n^(n-1))
# p(n+1, t+1) = p(n, t) * (((n-1)/n)^(t-2)) * ((n-1)/n)
#             + p(n, t-1) * (((n-1)/n)^(t-3)) * ((n-1)/n) * ((n-1)/n)
#             + p(n, t-2) * (((n-1)/n)^(t-4)) * ((n-1)/n) * ((n-1)/n)^2
#             + ...
#             + p(n, n) * (((n-1)/n)^(n-2)) * ((n-1)/n) * ((n-1)/n)^(t-n)
#
#             = Sum[n,t](p(n, i)) * ((n-1)/n)^(t-1)
# p(n, t) = Sum[n,t](p(n-1, i-1)) * ((n-2)/(n-1))^(t-2)

'''
e.g.
p(4, 5) = p(3, 4) * (2/3)^2 * (2/3)
        + p(3, 3) * (2/3)^1 * (2/3) * (2/3)^1
'''

DEBUG = False # DEBUG = True for more output
THREAD_COUNT = 16 # Multithread is unnecessary

args = argument_parser().parse_args()

MAX_COUNT = args.max_count
USE_MAX_COUNT = MAX_COUNT > 0
X_MAX = args.xmax
EPSILON = args.epsilon
NAME = args.memo
READ_RESULT = args.read_result
CONV_MODE = args.conv_mode
SUM_NUM = args.sum_num
RES_DIR = args.res_dir

def exp_no_rec(n, memo, conv):
    assert n >= 3

    conv.set_param(count=0, big_n=n*n, sum_num=SUM_NUM)
    
    e = 0
    while True:
        xp = (n + conv.count()) * memo.pnt(n, n + conv.count())
        e += xp
        if USE_MAX_COUNT:
            if conv.judge(xp) or conv.count() >= MAX_COUNT:
                break
        else:
            if conv.judge(xp):
                break
        xp0 = xp
    
    return e, conv.count()

#from functools import wraps
import time

def display_time(f):
    #@wraps(f)
    def func(n, memo, conv):
        use_str = 'use MAX_COUNT=%d'%USE_MAX_COUNT \
                  if USE_MAX_COUNT else 'not use MAX_COUNT'
        time_start = time.time()
        ret, count = f(n, memo, conv)
        time_end = time.time()
        print('E(%d)=%.4f, %s, time=%.3f (s), sample_count=%d\n'\
              %(n, ret, use_str, time_end - time_start, count))
        if DEBUG:
            print('pnt=\n' + str(memo._pnt) + '\n')
            print('snt=\n' + str(memo._snt) + '\n')
        return ret, count

    return func

@display_time
def expectation(n, memo=Memo(), conv=Convergence(mode=CONV_MODE, epsilon=EPSILON)):
    if n == 1 or n == 2:
        return float(n), 0
    return exp_no_rec(n, memo, conv)

def main():
    xs = list(range(1, X_MAX + 1))
    file = File(RES_DIR)
    postfix = '%s_%d'%(CONV_MODE, X_MAX)
    if not READ_RESULT:
        print('Calculating...\n')
        #memo = Memo(pool=ThreadPool(THREAD_COUNT)) # Multithread is unnecessary
        memo = Memo()
        if memo.load(NAME, file):
            print('Success to load pickle "%s".'%file.abspath(NAME))
        else:
            print('Fail to load pickle "%s".'%file.abspath(NAME))
        conv = Convergence(mode=CONV_MODE, epsilon=EPSILON)
        ys_unzip = list(map(lambda x: expectation(x, memo, conv), xs))
        ys = [y[0] for y in ys_unzip]
        ys_save = [{'expectation':y[0],'sample_count':y[1]} for y in ys_unzip]
        ans = dict(zip(xs, ys_save))
        #print('ans = ' + repr(ans))
        f = file.open('result_%s.json'%postfix, 'w')
        f.write(json.dumps(ans, sort_keys=True, indent=4, separators=(',',':')))
        f.close()
        
        if memo.save(NAME, file):
            print('Success to save pickle to "%s".'%file.abspath(NAME))
        else:
            print('Fail to save pickle to "%s".'%file.abspath(NAME))
    else:
        print('Print result only...\n')
        result_fn = 'result_%s.json'%postfix
        if result_fn not in file.listdir():
            print('Fail to load %s. Check if the file exists.'%file.abspath(result_fn))
            exit(1)
        f = file.open(result_fn, 'r')
        ans = json.loads(f.read())
        ys = [ans[str(x)]['expectation'] for x in xs]

    def func_n(x, a, b):
        return a*x + b

    def func_nlogn(x, a, b): # log means ln
        return a*x*np.log(x) + b

    def func_n2(x, a, b, c):
        return a*x*x + b*x + c

    xs = np.array(xs)
    ys = np.array(ys)
    fit = Fit(n=func_n, nlogn=func_nlogn, n2=func_n2)
    with file.open('fit_n_%s.json'%postfix, 'w') as f:
        f.write(json.dumps(fit.fit('n', xs, ys), sort_keys=True, indent=4, separators=(',',':')))
    with file.open('fit_nlogn_%s.json'%postfix, 'w') as f:
        f.write(json.dumps(fit.fit('nlogn', xs, ys), sort_keys=True, indent=4, separators=(',',':')))
    with file.open('fit_n2_%s.json'%postfix, 'w') as f:
        f.write(json.dumps(fit.fit('n2', xs, ys), sort_keys=True, indent=4, separators=(',',':')))
    

if __name__ == '__main__':
    main()
