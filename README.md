# Introduction

A python script tries to decode numbers and export Latex code producing a pictorial representation of a *frieze*. A frieze is encoded with numbers in range 0 to 15 which associated with a particular point `p` such that:

* If the rightmost digit of the representation of number `n` in base 2 is equal to 1 then `p` is to be connected to its northern neighbour using sign `|`
* If the second rightmost digit of the representation of number `n` in base 2 is equal to 1 then `p` is to be connected to its north-eastern neighbour `/`
* If the third rightmost digit of the representation of number `n` in base 2 is equal to 1 then `p` is to be connected to its eastern neighbour `-`
* If the fourth rightmost digit of the representation of number `n` in base 2 is equal to 1 then `p` is to be connected to its south-eastern neighbour `\`

For example, if a file `freieze.txt` has the following contents:

```
4  4 12 4 4  4 12 4 4 4 12 4 4 4 12 4 4 4 12 4 4 4 12 4 0
0  2 0  8 0  2 0  8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0
10 0 8  0 10 0 8  0 10 0 8 0 10 0 8 0 10 0 8 0 10 0 8 0 0
0  2 0  2 0  2 0  2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0  1 0  1 0  1 0  1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
0  9 0  9 0  9 0  9 0 9 0 9 0 9 0 9 0 9 0 9 0 9 0 9 0
10 0 2  0 10 0 2  0 10 0 2 0 10 0 2 0 10 0 2 0 10 0 2 0 0
0  8 0  2 0  8 0  2 0 8 0 2 0 8 0 2 0 8 0 2 0 8 0 2 0
4  4 6  4 4  4 6  4 4 4 6 4 4 4 6 4 4 4 6 4 4 4 6 4 0
```

When we run the python script:

```
$ python3
>>> from frieze import *
>>> frieze = Frieze(’frieze.txt’)
>>> frieze.analyse()
Pattern is a frieze of period 4 that is invariant under translation,
horizontal and vertical reflections, and rotation only.
>>> frieze.display()
```

The effect of executing `frieze.display()` is to produce a file named `frieze.tex` that can be given as argument to `pdflatex` to produce a file named `frieze.pdf` that views as follows.

![Screen Shot 2020-04-02 at 4.59.05 pm](https://i.imgur.com/pGZeFkn.png)

PLEASE REFERENCE THIS PROJECT PROPERLY OTHERWISE YOU MAY INVOLVE IN PLAGIARISM!

