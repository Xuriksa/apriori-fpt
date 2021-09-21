import time, argparse, sys, os

from utils import parse_file
from print_utils import *
from Apriori import Apriori
from FPTreeMiner import fpt_itemsets

input_help='''
    The input file containing the normalized database. Comma separators are used. The first line should have
    the minimum support (positive integer), minimum confidence (floating point between 0 and 1), and minimum
    lift (unbounded positive floating point). The remaining lines are the records of a normalized
    transaction database (i.e. each line has customer and an item). There is only one item in each record so
    multiple lines may be needed to handle one customer.
'''

parser = argparse.ArgumentParser(description='Frequent Pattern Mining with Apriori and/or Frequent Pattern Tree.')
parser.add_argument('infile', nargs=1, type=argparse.FileType('r'), help=input_help)
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="File to print the output. Defaults to console.")
parser.add_argument('-ap', action='store_true', help='Mine with the Apriori algorithm?')
parser.set_defaults(ap=False)
parser.add_argument('-fpt', action='store_true', help='Mine with the Frequent Pattern Tree algorithm?')
parser.set_defaults(fpt=False)
parser.add_argument('-pin', action='store_true', help='Print minimums and denormalized transactions?')
parser.set_defaults(pin=False)
parser.add_argument('-pr', action='store_true', help='Print Association Rules? {A,B...} ==> {C,D...} [support, confidence, lift]')
parser.set_defaults(pr=False)
args = parser.parse_args()

infile = args.infile[0]

if infile is not None:    
    try:
        min_sup, min_conf, min_lift, transactions = parse_file(infile)
    except Exception as e:
        print("Error parsing the input file!\n" + input_help)
        sys.exit(1)

    outfile = args.outfile    

    if args.pin:
        print_inputs(outfile, min_sup, min_conf, min_lift, transactions)
        file_write(outfile)

    if args.ap:
        file_write(outfile, "Apriori:\n")

        start = time.time()
        ap_results = Apriori(min_sup, transactions)
        end = time.time()
        ap_time = end - start

        print_results(outfile, args.pr, ap_results, min_sup, min_conf, min_lift, transactions)
        file_write(outfile, "Time: " + str(ap_time))
        file_write(outfile, "==================================================")
        

    if args.fpt:
        file_write(outfile, "Frequent Pattern Tree:\n")

        start = time.time()
        fpt_results = fpt_itemsets(min_sup, transactions)
        end = time.time()
        fpt_time = end - start

        print_results(outfile, args.pr, fpt_results, min_sup, min_conf, min_lift, transactions)
        file_write(outfile, "Time: " + str(fpt_time))
        file_write(outfile, "==================================================")

    infile.close()
    outfile.close()
    sys.exit(0)