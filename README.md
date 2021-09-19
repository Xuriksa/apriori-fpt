Description:
=
A command line python program to mine frequent patterns and their association rules from a database.

Input:
=
The input is a file containing a normalized transaction database with comma separators:

| Minimum Support | Minimum Confidence | MinimumLift |
|:-:|:-:|:-:|
| 5000, | 0.8, | 1.0, |

| Customer | Item |
|:-:|:-:|
| Emily, | Soap    |
| Emily, | Beans   |
| John, | Beans    |
| John, | IceCream |
| ..., | ... |

There is a samples folder with sample input databases. 

Usage:
=
```console
python main.py [-h] [-ap] [-fpt] [-pin] [-pr] [infile] [outfile]
```

**Positional arguments**:

  infile      The input file containing the normalized database. Comma separators are used. The first line should have
              the minimum support (positive integer), minimum confidence (floating point between 0 and 1), and minimum
              lift (unbounded positive floating point). The remaining lines are the records of a normalized
              transaction database (i.e. each line has customer and an item). There is only one item in each record so
              multiple lines may be needed to handle one customer.

  outfile     File to print the output. Defaults to console.

**Optional arguments**:

  -h, --help  show this help message and exit

  -ap         Mine with the Apriori algorithm?

  -fpt        Mine with the Frequent Pattern Tree algorithm?

  -pin        Print minimums and denormalized transactions?

  -pr         Print Association Rules? {A,B...} ==> {C,D...} [support, confidence, lift]

For example:

```console
python main.py samples/chess.txt chess_out.txt -pin -ap -fpt -pr
```

Reads the chess database in the samples folder.

Prints output to a chess_out.txt file.

Prints the denormalzied transactions at the beginning.

Mines with the apriori algorithm, prints the levels of frequent itemsets and their association rules (if they exceed the confidence and lift thresholds). Prints the algorithm's execution time.

Mines with the frequent pattern tree algorithm, prints the levels of frequent itemsets and their association rules (if they exceed the confidence and lift thresholds). Prints the algorithm's execution time.

**Note**: The execution time printed pertains to the algorithm. The time to compute and print the association rules is ignored.