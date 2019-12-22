##A Solution of a problem by program##  
  
Problem: You have been given an unlimited pass to take airline flights of your choosing, and you wish to cover all N cities possible. You start at City 1, and every day you take a flight to a random city (you choose one at random from the remaining N-1 cities). You continue this process the next day from thte city you are at currently, and so on until you see all the cities at least once. How many days does it take you, on expectation, to do this?  
~N or ~N log(N) or ~N^2  
  
To run this program:  
  
(1) Installation  
Install python3, and package scipy.  

(2) Run  
Run city_problem.py with python. Arguments are optional.  
  
usage: city_problem.py [-h] [-x XMAX] [-mc MAX_COUNT] [-r READ_RESULT]  
                       [-m MEMO] [-cm CONV_MODE] [-e EPSILON] [-sn SUM_NUM]  
  
optional arguments:  
  -h, --help            Show this help message and exit.  
  -x XMAX, --xmax XMAX  The max of x to be calculated. (default: 30)  
  -mc MAX_COUNT, --max-count MAX_COUNT  
                        Max count of iteration. Set a non-positive number to  
                        disable max count. (default: -1)  
  -rd RES_DIR, --res-dir RES_DIR  
                        Directory of result. (default: result)  
  -r READ_RESULT, --read-result READ_RESULT  
                        Read result from existing file or not. If true, -x and  
                        -cm will be required. (default: False)  
  -m MEMO, --memo MEMO  Directory of memo for calculate. (default: memo.pk)  
  -cm CONV_MODE, --conv-mode CONV_MODE  
                        Convergence mode. "D":D'Alembert's test. "C":Cauchy  
                        test. (default: C)  
  -e EPSILON, --epsilon EPSILON  
                        Epsilon for convergence test. (default: 0.125)  
  -sn SUM_NUM, --sum-num SUM_NUM  
                        The number of sum if using Cauchy test. (default:  
                        1000)  
  
e.g. python city_problem.py -x 100 -cm C  
  
Note: Cauchy test might be faster and cheaper than D'Alembert's test.  
  
(3) Result  
Exceptation and sample count will be saved in "result_<CONV_MODE>_<XMAX>.json".  
And fitting results will be saved in "fit_n_<CONV_MODE>_<XMAX>.json", "fit_nlogn_<CONV_MODE>_<XMAX>.json", "fit_n2_<CONV_MODE>_<XMAX>.json".  
You can use these json files for other usages.  
Also, some cache for calculation will be saved in "memo.pk", and calculation will be faster if run again.  
