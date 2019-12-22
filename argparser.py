import argparse

def argument_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-x', '--xmax', type=int, default=30,
                        help='The max of x to be calculated.\n')
    parser.add_argument('-mc', '--max-count', type=int, default=-1,
                        help='Max count of iteration.\n' +
                            'Set a non-positive number to disable max count.\n')
    parser.add_argument('-rd', '--res-dir', type=str, default='result',
                        help='Directory of result.\n')
    parser.add_argument('-r', '--read-result', type=bool, default=False,
                        help='Read result from existing file or not.\n' +
                            'If true, -x and -cm will be required.')
    parser.add_argument('-m', '--memo', type=str, default='memo.pk',
                        help='Directory of memo for calculate.\n')
    parser.add_argument('-cm', '--conv-mode', type=str, default='C',
                        help='Convergence mode.\n' +
                            '"D":D\'Alembert\'s test.\n'
                            '"C":Cauchy test.\n')
    parser.add_argument('-e', '--epsilon', type=float, default=0.125,
                        help='Epsilon for convergence test.\n')
    parser.add_argument('-sn', '--sum-num', type=int, default=1000,
                        help='The number of sum if using Cauchy test.')
    
    return parser
