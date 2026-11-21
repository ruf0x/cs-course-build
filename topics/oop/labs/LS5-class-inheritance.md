---
title: LS5 · Class inheritance
subtitle: Lab session with solutions
course: OOP · USTHB Master RT 2026/2027
---

# Objective

## Objective
- In this lab session we cover two essential concepts of object-oriented programming: **inheritance** and **polymorphism**
- Three exercises:
  1. a library: `archive`, `thesis`, `book`
  2. electronic components: `Junction`, `Diode`, `Transistor`, `Activate`
  3. signal processing: `signal`, `Processing`

# Exercise 1 · The library

## Exercise 1: statement
- To manage the content of a library, we create an **`archive`** class with two attributes:
  - `nbr`: the number of manuscripts
  - `dic`: a dictionary containing the number of works by category
- Add a **`save`** method that retrieves the type of the document (by `input`) and adds it as a key to the dictionary with an initial value of 1. If the key is already present, it **increments** its value
- Add a **`display`** method to display the attributes of `archive`

## Exercise 1: statement, the child classes
2. Define a class **`thesis`** that inherits from `archive`. `thesis` has a **list** as an attribute and a `display` function that displays it. Its `stock` method calls `save` to increment the dictionary by the number specified in the `nbr` attribute of `archive`, and adds to the list the **title** of each archived thesis (the program asks for the title)
3. Define a class **`book`** that inherits from `archive` and also has a list as attribute and a `display` method to display all the attributes. Its `stock` method calls `save` to store the book type according to `nbr`. The program asks for the **title** and the **author's name**, and puts them in a **tuple** added to the list
4. Instantiate `thesis` and `book` with numbers of your choice and call `stock` and `display` for each object. Check that the program executes the `display` methods of the **child classes** and not the method of the base class

## Exercise 1: solution, the classes
```python
class archive:
    def __init__(self, nbr):
        self.nbr = nbr                           # number of manuscripts
        self.dic = {}                            # number of works by category

    def save(self):
        kind = input("Type of the document: ")
        if kind in self.dic:
            self.dic[kind] += 1                  # already there: increment
        else:
            self.dic[kind] = 1                   # new key
    def display(self):
        print("nbr =", self.nbr, " dic =", self.dic)


class thesis(archive):
    def __init__(self, nbr):
        super().__init__(nbr)
        self.titles = []                         # the list of titles

    def stock(self):
        for i in range(self.nbr):
            self.save()                          # inherited method
            self.titles.append(input("Title: "))

    def display(self):                           # same name as the parent: overriding
        print("thesis:", self.titles)


class book(archive):
    def __init__(self, nbr):
        super().__init__(nbr)
        self.works = []                          # the list of (title, author)

    def stock(self):
        for i in range(self.nbr):
            self.save()
            title = input("Title: ")
            author = input("Author: ")
            self.works.append((title, author))

    def display(self):
        super().display()                        # the parent display + our own list
        print("books:", self.works)
```

## Exercise 1: solution, the main program
```python
t = thesis(2)
t.stock()                  # PFE / Networks / PFE / Radar
t.display()                # thesis: ['Networks', 'Radar']

b = book(2)
b.stock()                  # Novel / Dune / Herbert / Science / Cosmos / Sagan
b.display()                # nbr = 2  dic = {'Novel': 1, 'Science': 1}
                           # books: [('Dune', 'Herbert'), ('Cosmos', 'Sagan')]
```

## Exercise 1: remarks
- `class thesis(archive)`: `thesis` **inherits** from `archive`, so it has `nbr`, `dic`, `save` and `display`
- `super().__init__(nbr)` calls the constructor of the parent to build `nbr` and `dic`
- `t.save()` is **inherited**: `thesis` doesn't define it, Python finds it in `archive`
- `display` is defined in the parent **and** in the children: this is **overriding**. `t.display()` runs the version of `thesis`, `b.display()` runs the one of `book`
- `book.display` calls `super().display()` first, then displays its own list
- In the example the type `PFE` is saved twice, so `dic = {'PFE': 2}` for the thesis

# Exercise 2 · Electronic components

## Exercise 2: statement, Junction and Diode
1. To simulate the function of semiconductor-based electronic components, we consider a class **`Junction`** with the attributes: `N` (concentration type N), `P` (concentration type P), `Nbr` (number of junctions), `E` (blocked state `False` or conducting `True`)
   - The constructor initializes `N` and `P` with values chosen by the user, `E` to `False` and `Nbr` to 1
   - A function `Display` displays the attributes, and a function `Eval` returns the absolute difference between `P` and `N`
2. A **`Diode`** class that inherits from `Junction`. The attributes `S` (threshold voltage) and `R` (internal resistance) are initialized to 0
   - An `Eval` function receives two arguments `a` and `b` used to define `S` by `exp(-(P-N)/a)` and `R` by `S / b`
   - A `Display` function displays the attributes of `Diode` and calls the `Display` function of `Junction`

## Exercise 2: statement, Transistor and Activate
3. A **`Transistor`** class that inherits from `Junction` with two attributes `B` (static gain) and `Z` (input impedance) and one `Diode` attribute
   - The constructor initializes the attributes to user-defined values, and sets `Nbr` to 2
   - A `Display` function displays the attributes of `Transistor` and calls the `Display` of `Junction`
4. A class **`Activate`** that operates **independently** from all the other classes, with two functions:
   - `FDiode`: receives a `Diode` object and two parameters `x` and `y`. It calls `Eval` with `x` and `y`. If the threshold value is positive, the state `E` of the object is set to `True`. It finishes by calling `Display`
   - `FTransistor`: receives a `Transistor` object and two parameters `x`, `y`. It calls the `Eval` of the transistor's diode attribute, and sets the gain `B` to `100 S` and `Z` to `1000 R` (`S` and `R` are the attributes of the diode). It finishes by calling `Display`

## Exercise 2: solution, Junction and Diode
- The constructors accept values as parameters. If a value is missing, they ask the user with `input`
```python
import math

class Junction:
    def __init__(self, N=None, P=None):
        self.N = float(input("N concentration: ")) if N is None else N
        self.P = float(input("P concentration: ")) if P is None else P
        self.Nbr = 1                              # number of junctions
        self.E = False                            # blocked (False) or conducting (True)

    def Display(self):
        print("Junction: N =", self.N, " P =", self.P, " Nbr =", self.Nbr, " E =", self.E)

    def Eval(self):
        return abs(self.P - self.N)


class Diode(Junction):
    def __init__(self, N=None, P=None):
        super().__init__(N, P)
        self.S = 0                                # threshold voltage
        self.R = 0                                # internal resistance

    def Eval(self, a, b):                         # same name, other parameters: overriding
        self.S = math.exp(-super().Eval() / a)    # S = exp(-|P - N| / a)
        self.R = self.S / b                       # R = S / b

    def Display(self):
        print("Diode: S =", round(self.S, 4), " R =", round(self.R, 4))
        super().Display()                         # calls the Display of Junction
```
- The statement writes `exp(-(P-N)/a)`. We use the absolute difference given by `Eval` of `Junction` (`super().Eval()`), so `S` is always between 0 and 1

## Exercise 2: solution, Transistor and Activate
```python
class Transistor(Junction):
    def __init__(self, N=None, P=None, B=None, Z=None):
        super().__init__(N, P)
        self.Nbr = 2                              # a transistor has 2 junctions
        self.B = float(input("Static gain B: ")) if B is None else B
        self.Z = float(input("Input impedance Z: ")) if Z is None else Z
        self.diode = Diode(self.N, self.P)        # a Diode object as attribute

    def Display(self):
        print("Transistor: B =", self.B, " Z =", self.Z)
        super().Display()


class Activate:                                   # independent from the other classes
    def FDiode(self, d, x, y):
        d.Eval(x, y)
        if d.S > 0:                               # positive threshold: conducting
            d.E = True
        d.Display()

    def FTransistor(self, t, x, y):
        t.diode.Eval(x, y)
        t.B = 100 * t.diode.S
        t.Z = 1000 * t.diode.R
        t.Display()
```
- `Transistor` **has** a `Diode` (composition) and **is** a `Junction` (inheritance)
- `Activate` doesn't inherit from anything: its functions just receive the objects as arguments

## Exercise 2: the main program and the conclusion
```python
d = Diode(3, 5)
t = Transistor(3, 5, 10, 20)
act = Activate()

act.FDiode(d, 2, 4)
# Diode: S = 0.3679  R = 0.092
# Junction: N = 3  P = 5  Nbr = 1  E = True

act.FTransistor(t, 2, 4)
# Transistor: B = 36.787944117144235  Z = 91.96986029286059
# Junction: N = 3  P = 5  Nbr = 2  E = False
```
- **What can we conclude?** `d.Display()` runs the `Display` of `Diode`, **not** the one of `Junction`, because the child class **overrides** the method (**polymorphism**)
- The method of the parent is **not lost**: `super().Display()` calls it, so `Diode` only adds its own part (`S` and `R`) and reuses the rest
- `Nbr` is 1 for the diode and 2 for the transistor: each child sets its own value after calling the parent constructor
- The state `E` of the transistor stays `False`: `FTransistor` doesn't change it

# Exercise 3 · Signals

## Exercise 3: statement
- Define a class **`signal`** with 4 attributes: `n` (number of samples), `m` (mean of the signal), `st` (standard deviation) and a numpy vector containing the samples. The class has 4 methods:
  - a **constructor** that asks the user for the number of samples, initializes `m` and `st` to 0, and creates a numpy `data` vector of size `n` initialized to 0
  - a **`values`** function that initializes `data` with random values in the range [0, 50]
  - a **`stat`** function that calculates the mean and the standard deviation of `data` (with your own program, then compare with numpy's `mean` and `std`)
  - a **`display`** function that displays all the attributes

## Exercise 3: statement, Processing
1. A **`Processing`** class which has a **`shift`** function (with a `signal` object as argument) that normalizes the data values according to: `data[i] = (data[i] − m)² / std`
2. To test the class programs: create an instance of `signal`, call `values` and `stat`, apply `shift` and put the result in a **new `signal` object** whose attributes are displayed with `display`
- Place the classes in a **module** to be imported into the main file. Instantiate the classes and test the execution of the functions

## Exercise 3: solution, the module signals.py
```python
import numpy as np


class signal:
    def __init__(self, n=None):
        self.n = int(input("Number of samples: ")) if n is None else n
        self.m = 0                                     # mean
        self.st = 0                                    # standard deviation
        self.data = np.zeros(self.n)                   # the samples

    def values(self):
        self.data = np.random.uniform(0, 50, self.n)   # random values in [0, 50]

    def stat(self):
        total = 0
        for x in self.data:                            # our own calculation
            total += x
        self.m = total / self.n
        ss = 0
        for x in self.data:
            ss += (x - self.m) ** 2
        self.st = (ss / self.n) ** 0.5
        print("own program :", round(self.m, 4), round(self.st, 4))
        print("numpy       :", round(np.mean(self.data), 4), round(np.std(self.data), 4))

    def display(self):
        print("n =", self.n, " m =", round(self.m, 3), " st =", round(self.st, 3))
        print("data =", self.data.round(1))


class Processing:
    def shift(self, s):                                # s is a signal object
        new = signal(s.n)                              # a new signal object
        new.data = (s.data - s.m) ** 2 / s.st          # data[i] = (data[i] - m)^2 / std
        new.m = np.mean(new.data)
        new.st = np.std(new.data)
        return new
```

## Exercise 3: solution, the main program
```python
from signals import signal, Processing

S = signal(6)                  # signal() alone asks the number of samples with input()
S.values()
S.stat()
# own program : 18.3134 8.2491
# numpy       : 18.3134 8.2491
S.display()
# n = 6  m = 18.313  st = 8.249
# data = [21.8  1.3 27.5 21.8 21.  16.5]

new = Processing().shift(S)
new.display()
# n = 6  m = 8.249  st = 12.471
# data = [ 1.5 35.1 10.2  1.4  0.9  0.4]
```
- The two calculations of the mean and the standard deviation give **the same values**: our loops compute the population standard deviation, like `np.std`
- `shift` doesn't change `S`: it builds and returns a **new** `signal` object
- The mean of the new data is equal to the old standard deviation: the mean of `(x − m)²` is the variance, divided by `std`
