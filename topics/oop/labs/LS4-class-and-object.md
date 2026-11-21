---
title: LS4 · Class and Object
subtitle: Lab session with solutions
course: OOP · USTHB Master RT 2026/2027
---

# Objective

## Objective
- In this lab session we handle the **first fundamental notion** of object-oriented programming: the **object** and its **class**
- Three exercises:
  1. a `Complex` class
  2. a `Vector` class
  3. a `Student` class

# Exercise 1 · Complex

## Exercise 1: statement
- Define a `Complex` class with two attributes `a` and `b` that denote the real and imaginary parts
- Add two attributes `mod` and `phas` that denote the modulus and the phase of the number
- The **constructor** initializes `a` and `b` to values chosen by the user, and sets `mod` and `phas` to 0
- Define two methods `Calculate` and `Display`:
  - `Calculate` calculates the modulus and the phase of the complex number
  - `Display` displays the values of all the attributes
- Create a complex object and call the `Calculate` and `Display` methods

## Exercise 1: solution
```python
import math

class Complex:
    def __init__(self):
        self.a = float(input("Real part a: "))
        self.b = float(input("Imaginary part b: "))
        self.mod = 0
        self.phas = 0

    def Calculate(self):
        self.mod = math.sqrt(self.a ** 2 + self.b ** 2)     # modulus
        self.phas = math.atan2(self.b, self.a)              # phase, in radians

    def Display(self):
        print("a =", self.a, " b =", self.b, " mod =", self.mod, " phase =", self.phas)

z = Complex()          # Real part a: 3     Imaginary part b: 4
z.Calculate()
z.Display()            # a = 3.0  b = 4.0  mod = 5.0  phase = 0.9272952180016122
```

## Exercise 1: remarks
- **Modulus**: `|z| = √(a² + b²)`. For `3 + 4i` it is 5
- **Phase**: the angle of the number, `atan2(b, a)`, in **radians** (0.927 rad is about 53.13°). `math.degrees()` converts it
- `atan2(b, a)` is better than `atan(b / a)`: it works when `a = 0` and it gives the right quadrant
- `input()` always returns a string, so we convert with `float(...)`

# Exercise 2 · Vector

## Exercise 2: statement
- Create a `Vector` class that contains:
  - a numpy array called `vect` as first attribute
  - a second attribute `a` that defines the **size** of `vect`
- The constructor asks the user to choose the size of the vector, which is **initialized with random values**
- Add a `Calculation` method without arguments that returns the **power** of `vect`
- The power is the sum of all the elements (taken to the power of 2) divided by `a`
- In the main program, create a `Vector` object and call the methods

## Exercise 2: solution
```python
import numpy as np

class Vector:
    def __init__(self):
        self.a = int(input("Size of the vector: "))
        self.vect = np.random.random(self.a)                # random values

    def Calculation(self):
        return np.sum(self.vect ** 2) / self.a              # power

v = Vector()                                                # Size of the vector: 5
print(v.vect.round(2))                                      # [0.55 0.72 0.6  0.54 0.42]
print("power =", round(v.Calculation(), 4))                  # power = 0.3305
```
- `self.vect ** 2` squares **every element** at once (a numpy operation)
- Power = `(1/a) × Σ vect[i]²`

# Exercise 3 · Student

## Exercise 3: statement
- To manage digital student information, we create a `Student` class with the attributes: **Last Name**, **First Name** and **Exam marks** (a numpy array of 8 elements)
1. The class must contain the following methods:
   - `Input` and `Display`: they allow to enter and display the student's marks
   - `Average`: returns the student's average mark and displays whether he is **admitted** or **deferred**
2. Instantiate the class with **two objects**. Enter the marks and compare their averages. Display the result of the comparison (which one is higher ranked?)

## Exercise 3: solution, the class
```python
import numpy as np

class Student:
    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name
        self.marks = np.zeros(8)                            # 8 exam marks

    def Input(self):
        for i in range(8):
            self.marks[i] = float(input(f"Mark {i + 1}: "))

    def Display(self):
        print(self.last_name, self.first_name, self.marks)

    def Average(self):
        avg = self.marks.mean()
        print("average =", avg, "->", "admitted" if avg >= 10 else "deferred")
        return avg
```
- The marks start as an array of zeros and are filled by `Input`
- `Average` both **displays** the status and **returns** the average, so the main program can compare

## Exercise 3: solution, the two objects
```python
s1 = Student("Haddad", "Sara")
s1.Input()                       # 14 9 12 16 11 13 15 10
s1.Display()                     # Haddad Sara [14.  9. 12. 16. 11. 13. 15. 10.]
a1 = s1.Average()                # average = 12.5 -> admitted

s2 = Student("Benali", "Omar")
s2.Input()                       # 8 7 10 9 12 6 11 9
s2.Display()                     # Benali Omar [ 8.  7. 10.  9. 12.  6. 11.  9.]
a2 = s2.Average()                # average = 9.0 -> deferred

if a1 > a2:
    print(s1.first_name, "is ranked higher")        # Sara is ranked higher
elif a2 > a1:
    print(s2.first_name, "is ranked higher")
else:
    print("same average")
```
- Each object has **its own** attributes: `s1.marks` and `s2.marks` are two different arrays
- The comparison uses the values **returned** by `Average`
