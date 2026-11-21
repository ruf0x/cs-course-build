---
title: Advanced Programming in Python
subtitle: Course summary · Chapters 1 to 3
course: OOP · USTHB Master RT 2026/2027
---

# Chapter 1 · Overview of OOP and Python
What OOP is, what a class and an object are, and the Python tools we use.

## Why OOP?
- OOP is a programming **paradigm** to build advanced software that is:
  - **Extensible**: easy to change
  - **Reusable**: parts can solve other problems
  - **Portable**: the same program works in several implementations
- A program is organized into **objects**
- An object = **data** (attributes) + **procedures** (methods) that act on this data

## Object, class, instance
- **Object**: a self-contained, modular entity with its own data and code
  - **Attributes**: what the object **knows**
  - **Methods**: what the object **can do**
- **Class**: the family, type or nature of the object (a **Laptop**)
- **Instance**: one realization of a class (**my** laptop, **his** laptop)
- Once a class exists, we can create **as many objects as we want**

## Object vs instance: what is the difference?
- A **class** is a plan (like the plan of a house): you cannot live in it
- `A = Circle()` builds one real thing from the plan: that thing is an **object**
- So yes: **the instances of a class are objects**
- **Object** and **instance** are the same thing, seen from two points of view:
  - **object**: what it is: a thing in memory, with data and methods
  - **instance**: how it is related to a class: "A is an instance **of Circle**"
- We say "instance" when we want to mention the class it was built from

## Object vs instance: example
| Word | Meaning | In the code |
|---|---|---|
| class | the plan | `Circle` |
| object | a real thing built from the plan | `A`, `B` |
| instance | an object, seen as "built from class X" | `A` is an instance of `Circle` |
```python
class Circle:
    pass

A = Circle()                     # A is an object
B = Circle()                     # B is another object
print(isinstance(A, Circle))     # True: A is an instance of Circle
print(A is B)                    # False: two different objects
print(isinstance(5, int))        # True: even 5 is an instance of int
```

## In practice
- An object is an **enhanced variable**: it stores data and performs operations on itself
- A program is a group of objects that tell each other what to do by **sending messages**
- A class is a set of objects that share common **characteristics** and **behaviors**
- **Methods** are the public part: the operations offered to the user
- **Attributes** are the internal data. Private in C++ / Java, but **public in Python**

## First class: Circle
- Interface of the class: its name + its attributes + its methods
- `__init__`: the **constructor**, it initializes the attributes
- `self`: the **current object**
- `"""..."""`: the documentation comment of the class
```python
class Circle:
    """This class creates circle objects"""
    def __init__(self):
        self.rayon = 1
        self.abs = 0
        self.ord = 0

    def Move(self, a, b):
        self.abs += a
        self.ord += b

    def Zoom(self, a):
        self.rayon *= a

    def Area(self):
        return 3.14 * self.rayon ** 2
```

## Why does __init__ have double underscores?
- `__init__` is a **special method**: Python itself calls it, you never do
- The double underscores on both sides (called **dunder**: double underscore) mean: **this name belongs to Python**
- Python calls `__init__` automatically at the exact moment you write `Circle()`
- Other special methods: `__str__` (called by `print`), `__len__` (called by `len`), `__new__` (creates the object)
- The underscores also avoid clashes with the names you choose for your own methods
> Careful: `__init__` is **not private**. It's special, not hidden. A name is private when it starts with two underscores and does **not** end with two (like `__ray`).

## Special methods: example
```python
class Circle:
    def __init__(self, r=1):         # called by Python when you write Circle()
        print("init called")
        self.rayon = r

    def __str__(self):               # called by Python when you print(...)
        return "Circle of radius " + str(self.rayon)

A = Circle(2)        # init called
print(A)             # Circle of radius 2
```

## Why do we write self in the methods?
- A class keeps **one** copy of each method, shared by all its objects
- When you write `A.Zoom(3)`, the method must know **which object** to work on
- So Python passes `A` automatically as the **first argument**: `self` is the parameter that receives it
- `A.Zoom(3)` is exactly the same as `Circle.Zoom(A, 3)`
```python
class Circle:
    def __init__(self, r=1):
        self.rayon = r
    def Zoom(self, a):
        self.rayon *= a

A = Circle(2)
B = Circle(5)
A.Zoom(3)               # self is A → A.rayon = 6
Circle.Zoom(B, 2)       # same thing written in full: self is B → B.rayon = 10
print(A.rayon, B.rayon) # 6 10
```

## Can we skip self?
- **As the first parameter: no.** The object is always passed, so a method without a parameter breaks
- The name `self` is only a **convention**: `this` or `me` would work, but everybody reads `self`
- Inside the method, write `self.rayon`: without `self.`, `rayon` is just a local variable and the object's attribute is not touched
```python
class Circle:
    def Zoom(a):                 # forgot self
        print(a)

Circle().Zoom(3)     # TypeError: Zoom() takes 1 positional argument but 2 were given
```

## A method without self: @staticmethod
- A method that doesn't need the object has no `self`, but it must be marked `@staticmethod`
- It belongs to the class, and is called through the class name
```python
class Maths:
    @staticmethod
    def double(x):               # no self: no object needed
        return 2 * x

print(Maths.double(4))           # 8
```

## Naming conventions and instances
| Name | Meaning |
|---|---|
| `method` | public: callable from anywhere |
| `_method` | **protected**: usable by child classes |
| `__method` | **private**: only inside the class (even not by child classes) |
- **Instantiate** = create a variable of the class type:
```python
A = Circle()          # A is an object (instance) of Circle
C1 = Circle()
C1.color = "Red"      # Python allows adding attributes after creation
```

## Public, protected, private
- **Yes**: the same 3 levels exist for **attributes** and for **methods**
| Level | Who can use it | Python syntax | Example |
|---|---|---|---|
| **public** | everyone: the class, its child classes, the outside | `name` | `owner` |
| **protected** | the class and its **child classes**. Outside: please don't | `_name` (one underscore) | `_bank` |
| **private** | the class **only** | `__name` (two underscores) | `__balance` |
- **Public**: the part you offer to the users (the interface)
- **Protected**: shared with child classes (chapter 4), not meant for the outside
- **Private**: internal details, free to change later without breaking anybody

## Public, protected, private: code
```python
class Account:
    def __init__(self, owner, balance):
        self.owner = owner               # public attribute
        self._bank = "BNA"               # protected attribute
        self.__balance = balance         # private attribute

    def deposit(self, x):                # public method
        self.__check(x)
        self.__balance += x

    def __check(self, x):                # private method
        if x <= 0:
            raise ValueError("amount must be positive")

    def get_balance(self):               # public: the way to read the private attribute
        return self.__balance
```

## Who can access what?
```python
A = Account("Sara", 1000)
print(A.owner)             # Sara           public: OK
print(A._bank)             # BNA            protected: works, but "do not touch" (convention)
print(A.get_balance())     # 1000           the right way to read a private attribute
print(A.__balance)         # AttributeError private: hidden from the outside
```
```python
class Savings(Account):               # a child class (chapter 4)
    def info(self):
        print(self._bank)             # OK: protected is for child classes
        print(self.__balance)         # AttributeError: private is hidden from the child too
```

## Python does not really lock the door
- **Protected** is only a convention: Python does not stop you
- **Private** is a **renaming**: inside the class, `__balance` becomes `_Account__balance`
- So it protects against **mistakes**, not against someone who really wants to get in
- Java and C++ enforce it; Python trusts the programmer
```python
print(A._Account__balance)    # 1000: it works! Python only renamed it
print(A.__dict__)             # {'owner': 'Sara', '_bank': 'BNA', '_Account__balance': 1000}
```

## Public, protected, private in 3 languages
| | Python | Java | JavaScript |
|---|---|---|---|
| public | `x` | `public int x;` | `x` (default) |
| protected | `_x` (convention) | `protected int x;` | `_x` (convention) |
| private | `__x` (renamed) | `private int x;` | `#x` (really private) |
- Java: checked by the compiler
- JavaScript: `#x` is enforced, `_x` is only a habit
- Python: everything is a convention or a renaming

## Public, protected, private: Java
```java
class Account {
    public String owner;           // public
    protected String bank = "BNA"; // protected: class, child classes, same package
    private double balance;        // private: this class only

    public double getBalance() { return balance; }
}
```

## Public, protected, private: JavaScript
```javascript
class Account {
    owner = "Sara";       // public
    _bank = "BNA";        // protected (convention only)
    #balance = 1000;      // private: really enforced by JavaScript

    getBalance() { return this.#balance; }
}
```

## Abstraction and encapsulation
- **Data abstraction**: show only the **interface**, hide the implementation details
- **Data encapsulation**: bind the data and the functions that use it together, and protect them from outside misuse
- Encapsulation leads to **data hiding**

## Abstraction: example
- **Abstraction** = show **what** an object does, hide **how** it does it
- You press one button on a coffee machine: you don't know about the pump or the heater
- If the inside changes tomorrow, `make_coffee()` stays the same for the user
```python
class CoffeeMachine:
    def make_coffee(self):              # the interface: one simple method
        self.__heat_water()
        self.__grind_beans()
        self.__pour()
        print("Coffee ready")

    def __heat_water(self):  print("heating water...")    # hidden details
    def __grind_beans(self): print("grinding beans...")
    def __pour(self):        print("pouring...")
```

## Abstraction: using it
- The user only knows **one** method: `make_coffee()`
- The private methods (the details) are hidden
```python
m = CoffeeMachine()
m.make_coffee()          # heating water... / grinding beans... / pouring... / Coffee ready
m.__pour()               # AttributeError: the details are hidden
```

## Encapsulation: the problem
- **Encapsulation** = keep the data and the methods together, and **protect the data**
- Without it, anybody can put the object in a wrong state
```python
class BadAccount:
    def __init__(self, balance):
        self.balance = balance          # public: anybody can change it

B = BadAccount(100)
B.balance = -999                        # nobody checks anything!
print(B.balance)                        # -999
```

## Encapsulation: the solution
- The data is **private**: the only door is a method that **checks the rules**
```python
class Account:
    def __init__(self, balance):
        self.__balance = balance        # hidden data

    def withdraw(self, x):              # the only door, with a rule
        if 0 < x <= self.__balance:
            self.__balance -= x
        else:
            print("refused")

    def get_balance(self):
        return self.__balance

A = Account(100)
A.withdraw(30)
print(A.get_balance())     # 70
A.withdraw(500)            # refused
A.__balance = -999         # does NOT touch the real balance: it creates a new attribute
print(A.get_balance())     # 70
```

## Interface: what is it?
- The word has **two meanings**:
  - The **interface of a class** (chapter 1): its public methods, the "buttons" users can press. For `Circle`: Move, Zoom, Area
  - An **interface as a contract**: a list of methods that every class which "signs" it **must** provide
- A contract says **what**, never **how**
- Real life: a power socket. Any device with the right plug works. The socket doesn't care if it's a lamp or a laptop

## Why an interface and not just a class?
- A normal class mixes the **what** and the **how**, and you can create an object from it
- An interface only says the **what**, and you **cannot** create an object from it
- A plain parent class doesn't force anything: a child can forget a method and nobody complains until the day it is called
- With an interface:
  - **Guarantee**: a class that forgets a method cannot even be created
  - **Polymorphism**: code written for the interface works with any class that signs it, even one written tomorrow
  - **Change without breaking**: swap one class for another, the rest of the program stays the same
  - **Teamwork**: agree on the interface first, then each person writes a class

## When do we use an interface?
| Situation | Interface | Classes that sign it |
|---|---|---|
| Payment | `pay(amount)` | CardPayment, PaypalPayment |
| Storage | `save(data)` | FileStorage, DatabaseStorage |
| Notification | `send(msg)` | EmailNotifier, SmsNotifier |
| Shapes | `area()` | Circle, Rectangle |
> Use one when **several classes do the same job in different ways** and the rest of the program should not care which one it gets.

## Interface in Python: the contract
- Python has no `interface` keyword: we use an **abstract class** from the `abc` module
- `@abstractmethod`: a method with **no body**, it only says what must exist
- `class Circle(Shape)`: Circle **signs** the contract (it inherits from Shape: chapter 4)
```python
from abc import ABC, abstractmethod

class Shape(ABC):                  # the interface
    @abstractmethod
    def area(self):                # only says WHAT
        pass

class Circle(Shape):               # signs the contract
    def __init__(self, r):
        self.r = r
    def area(self):                # must implement it
        return 3.14 * self.r ** 2
```

## Interface in Python: a second class and one function
- Another class signs the same contract
- `total_area` is written for the **interface only**: it works with any shape
```python
class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h
    def area(self):
        return self.w * self.h

def total_area(shapes):
    return sum(s.area() for s in shapes)

print(total_area([Circle(1), Rectangle(2, 3)]))   # 9.14
```

## Interface in Python: what it protects
```python
Shape()            # TypeError: an abstract class cannot be created

class Triangle(Shape):
    pass           # forgot area()

Triangle()         # TypeError: Triangle does not implement area()
```
> `total_area` works with any shape, today's or tomorrow's: it only knows the interface.

## Interface in Java and JavaScript
- **Java**: the `interface` keyword, checked by the compiler: a class that forgets a method does not compile
```java
interface Shape {
    double area();                           // only WHAT
}
class Circle implements Shape {              // signs the contract
    double r;
    Circle(double r) { this.r = r; }
    public double area() { return 3.14 * r * r; }
}
```

## Interface in JavaScript
- JavaScript has **no** `interface` keyword
- Use a base class that refuses to be used directly, or simply rely on: "if it has `area()`, it works"
- TypeScript, the typed version of JavaScript, has real interfaces
```javascript
class Shape {
  area() { throw new Error("area() must be implemented"); }
}
class Circle extends Shape {
  constructor(r) { super(); this.r = r; }
  area() { return 3.14 * this.r ** 2; }
}
```

## Python tools
- Python is **object-oriented**: every variable, even an `int`, is an object
- **Anaconda** distribution, with two environments:
  - **Spyder**: scientific IDE, code in `.py` files. `F5` runs all, `F9` runs a selection
  - **Jupyter Notebook**: code split into **cells**, run in any order
- Install libraries in the Anaconda prompt with `pip install <name>`

# Chapter 2 · Python programming concepts
Variables, control flow, containers, numpy and functions: everything needed before OOP.

## Input, output and typing
- `print()`: displays one or more variables
- `input()`: reads user input, **always a string** → convert it
- Typing is **dynamic**: Python picks the type from the value (no declarations like C++ / Java)
```python
A = int(input("Enter a number: "))
B = float(input("Enter a real: "))
A, B, C = 3, 4.5, "course"     # multiple assignment
```

## Operators
- Examples with `a = 7` and `b = 2`
- Don't confuse `==` (test) with `=` (assignment)
| Operator | Meaning | Example |
|---|---|---|
| `+` | addition | `a + b = 9` |
| `-` | subtraction | `a - b = 5` |
| `*` | multiplication | `a * b = 14` |
| `/` | division (always gives a float) | `a / b = 3.5` |
| `%` | modulo (remainder) | `a % b = 1` |
| `**` | power | `a ** b = 49` |
| `//` | integer division | `a // b = 3` |
| `E` | exponent | `2E5 = 200000.0` |
| `==`, `!=`, `<`, `>`, `<=`, `>=` | comparison | `a == b` gives `False` |

## Control flow
- Blocks are defined by **indentation**
```python
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

for i in range(5):          # also: np.arange(...)
    if i == 3:
        break               # stop the loop
    if i == 1:
        continue            # skip to the next iteration
while x < 10:
    x += 1
```

## Exceptions
- `try`: runs a block and checks it for errors
- `except`: runs if an error happens in `try`
- `finally`: always runs, whatever the result
```python
try:
    A = int(input("Number: "))
    print(10 / A)
except:
    print("Error!")
finally:
    print("End")
```

## Strings
- A string is a **composite** type: one object, or a sequence of characters
- Examples with `C = "hello world"`
| Code | Meaning | Example on C |
|---|---|---|
| `C[2:]` | from the 3rd character to the end | `'llo world'` |
| `C[1:5]` | characters 1, 2, 3 and 4 | `'ello'` |
| `C[-1]` | last character | `'d'` |
| `C[-3:]` / `C[:-3]` | last three / all but the last three | `'rld'` / `'hello wo'` |
| `C.upper()`, `C.lower()` | uppercase / lowercase | `'HELLO WORLD'` / `'hello world'` |
| `C.isalpha()`, `C.isdigit()` | only letters? only digits? | `False` / `False` |

## Strings: more methods
- Same variable: `C = "hello world"`
- A method returns a **new** string: `C` itself never changes (a string is immutable)
| Code | Meaning | Example on C |
|---|---|---|
| `len(C)` | number of characters | `11` |
| `C.capitalize()` | first letter in uppercase | `'Hello world'` |
| `C.title()` | first letter of each word in uppercase | `'Hello World'` |
| `C.replace("world", "python")` | replace a part | `'hello python'` |
| `C.find("world")` | position of a part (-1 if missing) | `6` |
| `C.count("o")` | number of occurrences | `2` |
| `C.startswith("hello")` | starts with? | `True` |
| `C.endswith("x")` | ends with? | `False` |

## Strings: split, join, strip and operators
- Same variable: `C = "hello world"`
| Code | Meaning | Example on C |
|---|---|---|
| `C.split(" ")` | cut into a list | `['hello', 'world']` |
| `"-".join(["a", "b"])` | join a list with a separator | `'a-b'` |
| `"  hi  ".strip()` | remove the spaces around | `'hi'` |
| `C + "!"` | addition: concatenation | `'hello world!'` |
| `C * 2` | multiplication: repetition | `'hello worldhello world'` |
| `C - "d"`, `C / 2` | subtraction, division: not possible | `TypeError` |

## Lists
- An **ordered** collection, accessed by **index**, can mix types and dimensions
- Each example starts again from `L = [3, 1, 2]`
| Method | Action | Example | Result |
|---|---|---|---|
| `append(x)` | add `x` at the end | `L.append(5)` | `[3, 1, 2, 5]` |
| `insert(i, x)` | insert `x` at position `i` | `L.insert(1, 9)` | `[3, 9, 1, 2]` |
| `extend(L2)` | add all elements of `L2` | `L.extend([7, 8])` | `[3, 1, 2, 7, 8]` |
| `remove(x)` | delete the first `x` | `L.remove(1)` | `[3, 2]` |
| `pop(i)` | delete the element at `i` | `L.pop(0)` | gives `3`, `L` = `[1, 2]` |
| `index(x)` | position of `x` | `L.index(2)` | `2` |
| `sort()` / `reverse()` | sort / reverse the order | `L.sort()` / `L.reverse()` | `[1, 2, 3]` / `[2, 1, 3]` |

## Lists: operators and slicing
- Examples with `M = [1, 2, 3]`
| Code | Meaning | Example on M |
|---|---|---|
| `M + [4]` | addition: joins two lists | `[1, 2, 3, 4]` |
| `M * 2` | multiplication: repeats the list | `[1, 2, 3, 1, 2, 3]` |
| `M - [1]`, `M / 2` | subtraction, division: not possible | `TypeError` |
| `M[0]`, `M[-1]` | first / last element | `1` / `3` |
| `M[1:]` | from the 2nd element | `[2, 3]` |
| `len(M)` | number of elements | `3` |
| `2 in M` | is 2 in the list? | `True` |

## Tuples and sets
- **Tuple**: like a list but **immutable** (no modification, no `del`, no `remove`)
```python
Z = 'A', 'B', 2, 7.8, 'word'
```
- **Set**: **unordered**, **no duplicates**. Used to extract distinct values

## Tuples: methods
- Examples with `T = ("a", "b", "a", 5)`
- A tuple has only **two** methods, because it cannot be modified
| Code | Meaning | Example on T |
|---|---|---|
| `T.count("a")` | how many times | `2` |
| `T.index("b")` | position | `1` |
| `len(T)` | number of elements | `4` |
| `T[0]`, `T[-1]` | first / last element | `'a'` / `5` |
| `T + (1,)` | addition: joins | `('a', 'b', 'a', 5, 1)` |
| `T * 2` | multiplication: repeats | `('a', 'b', 'a', 5, 'a', 'b', 'a', 5)` |
| `T[0] = "z"` | modification: not possible | `TypeError` |

## Sets: methods
- Each example starts again from `S = {1, 2, 3}`
| Method | Action | Example | Result |
|---|---|---|---|
| `S.add(x)` | adds `x` to the set | `S.add(4)` | `{1, 2, 3, 4}` |
| `S.remove(x)`, `S.discard(x)` | removes `x` (`remove` gives an error if `x` is missing) | `S.remove(2)` | `{1, 3}` |
| `S.clear()` | removes all elements | `S.clear()` | `set()` |
| `S2 = S.copy()` | returns a copy | `S2 = S.copy()` | `S2` = `{1, 2, 3}` |
| `S.pop()` | removes an element | `S.pop()` | gives one element, e.g. `1` |

## Sets: operations between two sets
- Examples with `S = {1, 2, 3}` and `T = {2, 3, 4}`
| Method | Operator | Meaning | Result |
|---|---|---|---|
| `S.union(T)` | `S \| T` | all the elements | `{1, 2, 3, 4}` |
| `S.intersection(T)` | `S & T` | elements in both | `{2, 3}` |
| `S.difference(T)` | `S - T` | elements of S that are not in T | `{1}` |

## Dictionaries
- A **modifiable**, **non-sequential** collection of `key: value` pairs
- Elements are accessed by **key**, not by position
- Values can be anything: numbers, strings, lists, dictionaries, functions, classes
```python
dic = {1: "First cycle"}
dic[2] = "Second cycle"     # add: no append needed
del dic[1]                  # delete by key
len(dic), dic.keys(), dic.values()
for k, v in dic.items():    # (key, value) pairs
    print(k, v)
if 2 in dic:                # membership test
    print(dic.get('T', 0))  # value of 'T', or 0 if missing
```

## Dictionaries: methods
- Each example starts again from `D = {"name": "Sara", "age": 20}`
- `+`, `-`, `*` and `/` do not work on dictionaries
| Code | Meaning | Example on D |
|---|---|---|
| `D["name"]` | value of a key | `'Sara'` |
| `D["city"] = "Algiers"` | add a key (no append needed) | `{'name': 'Sara', 'age': 20, 'city': 'Algiers'}` |
| `D["age"] = 21` | change a value | `{'name': 'Sara', 'age': 21}` |
| `D.get("phone", "none")` | value, or a default if the key is missing | `'none'` |
| `del D["age"]` | remove a key | `{'name': 'Sara'}` |
| `D.pop("age")` | remove a key and give its value | `20` |

## Dictionaries: keys, values, items
- Each example starts again from `D = {"name": "Sara", "age": 20}`
| Code | Meaning | Example on D |
|---|---|---|
| `D.keys()` | the keys | `dict_keys(['name', 'age'])` |
| `D.values()` | the values | `dict_values(['Sara', 20])` |
| `D.items()` | the (key, value) pairs | `dict_items([('name', 'Sara'), ('age', 20)])` |
| `D.update({"city": "Oran"})` | add or change several keys | `{'name': 'Sara', 'age': 20, 'city': 'Oran'}` |
| `len(D)` | number of elements | `2` |
| `"name" in D` | is the key present? | `True` |

## Numpy arrays
- `import numpy as np`: the main module for vectors and matrices
- Unknown size? Fill a **list** first, then convert: `N = np.array(T)`
- Examples with `D = np.array([1, 2, 3, 4, 5, 6])`
| Code | Meaning | Example | Result |
|---|---|---|---|
| `np.empty([2,2])`, `np.zeros(...)` | create (empty / zeros) | `np.zeros(3)` | `[0. 0. 0.]` |
| `D.ndim`, `D.shape`, `D.size` | dimensions, rows × columns, number of elements | `D.ndim`, `D.shape`, `D.size` | `1`, `(6,)`, `6` |
| `D.reshape(15,5)` | reshape | `D.reshape(2, 3)` | `[[1 2 3] [4 5 6]]` |
| `D.T` | transpose | `D.reshape(2, 3).T` | `[[1 4] [2 5] [3 6]]` |

## np.empty: why are the values strange?
- `np.empty([2,2])` creates an array of the given shape (2 rows, 2 columns)
- But it **does not initialize the values**
- It simply grabs a block of memory from the computer and gives it to the array
- Whatever data was left in that memory by previous processes is what you see
- So the values look random (like `1.78759415e-315`) and are different on each run
- Use `np.zeros` when you need zeros. Use `np.empty` only when you fill every element right after
```python
E = np.empty([2, 2])
print(E)     # [[1.78759415e-315 0.00000000e+000] [...]]
Z = np.zeros([2, 2])
print(Z)     # [[0. 0.] [0. 0.]]
```

## Numpy arrays: functions
| Code | Meaning | Example on D | Result |
|---|---|---|---|
| `np.dot(A,B)` | dot product | `np.dot(D, D)` | `91` |
| `np.arange(0,10)` | vector 0 … 9 | `np.arange(0, 10)` | `[0 1 2 3 4 5 6 7 8 9]` |
| `np.identity(4)` | identity matrix | `np.identity(2)` | `[[1. 0.] [0. 1.]]` |
| `np.full((3,3),5)` | matrix filled with 5 | `np.full((2, 2), 5)` | `[[5 5] [5 5]]` |
| `np.zeros_like(D)` | zeros with the shape of `D` | `np.zeros_like(D)` | `[0 0 0 0 0 0]` |

## Numpy: operators
- Operators work **element by element** on the whole array
- Examples with `D = np.array([1, 2, 3, 4, 5, 6])`
| Code | Meaning | Example on D |
|---|---|---|
| `D + 10` | addition | `[11 12 13 14 15 16]` |
| `D - 1` | subtraction | `[0 1 2 3 4 5]` |
| `D * 2` | multiplication | `[ 2  4  6  8 10 12]` |
| `D / 2` | division | `[0.5 1.  1.5 2.  2.5 3. ]` |
| `D.sum()` | sum of all elements | `21` |
| `D.mean()` | mean | `3.5` |
| `D.max()` | maximum | `6` |

## Functions
- Group code that is **repeated**, and call it when needed
- **Local** variables: created at the call, deleted at the end
- **Global** variables: created outside any function, visible everywhere
- Parameters can have **default values**; `*args` accepts any number of arguments
```python
def Fonct(x, y, k=2):         # k has a default value
    return x * y * k

def total(*args):             # any number of parameters
    return sum(args)

C = Fonct(A, B)               # call with concrete variables
```

## Functions: things to remember
- **Overloading**: several functions with the same name → Python **keeps only the last one**
  - real overloading happens with **inheritance** (chapter 4)
  - one function with **default parameters** can be called in several ways
- Reassigning a parameter inside a function does **not** change the caller's variable
- Modules: `import random as rd` → `rd.randint(10, 50)`

## match / case (Python 3.10+)
- Avoids long `if / elif / else` chains
```python
def choice(x):
    match x:
        case 1:
            return "one"
        case 2:
            return "two"
        case _:
            return "other"
```

## Built-in tools
- Data: `names = ["Sara", "Omar", "Lina"]`, `grades = [15, 9, 18]`
- **lambda** = a function with **no name**: `lambda g: g >= 10` is the same as `def f(g): return g >= 10`, used once inside `filter`, `map` or `sorted`
| Function | Role | Example | Result |
|---|---|---|---|
| `zip(a, b)` | pairs the lists (stops at the shortest) | `list(zip(names, grades))` | `[('Sara', 15), ('Omar', 9), ('Lina', 18)]` |
| `enumerate(it, start=0)` | adds a counter | `list(enumerate(names, start=1))` | `[(1, 'Sara'), (2, 'Omar'), (3, 'Lina')]` |
| `filter(fct, it)` | keeps what `fct` accepts | `list(filter(lambda g: g >= 10, grades))` | `[15, 18]` |
| `map(fct, it)` | applies `fct` to each element | `list(map(lambda g: g + 1, grades))` | `[16, 10, 19]` |
| `sorted(it, key, reverse)` | sorts (ascending) | `sorted(grades, reverse=True)` | `[18, 15, 9]` |
| `lambda` | small one-line function | `(lambda g: g >= 10)(9)` | `False` |

## Built-in tools: all together on student grades
- Which student passed? Who is first?
```python
names  = ["Sara", "Omar", "Lina"]
grades = [15, 9, 18]

for i, (n, g) in enumerate(zip(names, grades), start=1):
    print(i, n, g)                  # 1 Sara 15 / 2 Omar 9 / 3 Lina 18

passed = list(filter(lambda p: p[1] >= 10, zip(names, grades)))
print(passed)                       # [('Sara', 15), ('Lina', 18)]

ranking = sorted(zip(names, grades), key=lambda p: p[1], reverse=True)
print(ranking)                      # [('Lina', 18), ('Sara', 15), ('Omar', 9)]
```

# Chapter 3 · Class and Object
Constructors, class attributes, encapsulation, and how objects work together.

## Class and object
- A class is a **type** that groups **data** (attributes / member data) and **processing** (methods / member functions)
- An object (instance) is a variable of a class type: a **storage space** with its data and the operations on it
- Objects **collaborate by sending messages**, each with its own responsibilities
  - attributes = the **static** part, methods = the **dynamic** part
- In Python, **everything is an object**: `int`, `float`, `str`… are classes

## Constructors
- **Default constructor**: attributes get fixed default values
- **Constructor with parameters**: values chosen at creation
- Python has **one** constructor per class (no multiple constructors as in C++) → use **default parameter values**
```python
class Circle:
    """This class creates circle objects"""
    def __init__(self, a=1, b=0, c=0):
        self.rayon = a
        self.abs = b
        self.ord = c

A = Circle()           # rayon 1
B = Circle(2, 4, 4)    # rayon 2
C = Circle(2.5)        # rayon 2.5
```

## Methods and instantiation
- Methods are functions **inside** the class
- Running the class code only declares a **new type**: no variable is created yet
- Instantiate, then use attributes and methods **through the object**
- In Python, attributes and methods are **public** (unlike C++)
```python
A = Circle()
A.Zoom(3.5)
print(A.rayon)        # 3.5
print(A.Area())
```

## Class attributes
- Attributes in `__init__` (`self.x`) are **object-specific**
- Attributes defined **outside** the constructor are **shared by all objects**, accessed with the **class name**
```python
class Circle:
    compt = 0                     # class attribute: shared
    Att = 0
    def __init__(self, a=1, b=0, c=0):
        Circle.compt += 1         # counts created objects
        print("you have created:", Circle.compt, "Circle objects")
        self.rayon = a

    def Zoom(self, a):
        self.rayon *= a
        Circle.Att += a
```

## Adding attributes at runtime
- Attributes can be added during execution:
  - `ClassName.AttributeName = value` → for the class (all objects)
  - `ObjectName.AttributeName = value` → for one object
```python
A = Circle()
Circle.Form = "Cercle"     # added to the class
Circle.Color = "Red"
A.Color = "blue"           # A's own value
print(A.Color, A.Form)     # blue Cercle
```

## Intrinsic attributes
- Python gives **every class and every object** these attributes for free
- Examples with the `Circle` class (next slide) and the object `A = Circle(2, 3, 4)`
| Attribute | Meaning | Example | Result |
|---|---|---|---|
| `__name__` | the name of the class, as a string | `Circle.__name__` | `'Circle'` |
| `__module__` | the module (file) where the class is defined | `Circle.__module__` | `'__main__'` |
| `__base__` | the parent class (chapter 4), `object` by default | `Circle.__base__` | `<class 'object'>` |
| `__doc__` | the text written in `"""..."""` under `class` | `Circle.__doc__` | `'This class creates circle objects'` |
| `__dict__` of a class | the class attributes and methods | `Circle.__dict__` | `{'__init__': ..., 'Zoom': ..., ...}` |
| `__dict__` of an object | the attributes of this object | `A.__dict__` | `{'rayon': 2, 'abs': 3, 'ord': 4}` |

## Intrinsic attributes: the Circle class
- `__module__` is `'__main__'` when you run the file itself. If the class is imported, it is the name of the file
```python
class Circle:
    """This class creates circle objects"""
    def __init__(self, a=1, b=0, c=0):
        self.rayon = a
        self.abs = b
        self.ord = c

print(Circle.__name__)         # Circle
print(Circle.__module__)       # __main__
print(Circle.__base__)         # <class 'object'>
print(Circle.__doc__)          # This class creates circle objects
```

## Intrinsic attributes: on an object
- `__dict__` is where Python **stores** the attributes of an object: `A.color = "red"` just adds a key
- The class name of an object: `A.__class__.__name__` (`A.__name__` does not exist)
```python
A = Circle(2, 3, 4)            # the same Circle class
print(A.__dict__)              # {'rayon': 2, 'abs': 3, 'ord': 4}
A.color = "red"
print(A.__dict__)              # {'rayon': 2, 'abs': 3, 'ord': 4, 'color': 'red'}
print(A.__class__.__name__)    # Circle
```

## Special functions
| Function | Role |
|---|---|
| `getattr(obj, 'attr')` | returns the attribute's value |
| `hasattr(obj, 'attr')` | does it have this attribute? |
| `setattr(obj, 'attr', value)` | changes the value |
| `delattr(obj, 'attr')` | deletes the attribute |
```python
class Etudiant:
    name = "Nom"
    age = 22
    country = "Algeria"

print(hasattr(Etudiant, 'section'))   # False
setattr(Etudiant, 'name', "Nom222")
print(getattr(Etudiant, 'name'))      # Nom222
delattr(Etudiant, 'name')
```

## self vs cls
- `self`: the method works on the **object** → call it through an object
- `cls`: the method works on the **class** → call it through the class
```python
class Test:
    a = 0
    def T(self):                # access by object
        print(Test.a + 10)

class Test2:
    a = 0
    @classmethod
    def T(cls):                 # access by class
        print(cls.a + 10)

obj = Test(); obj.T()
Test2.T()
```

## __new__ vs __init__
- Writing `Circle(...)` does **two steps**, always in this order:
  1. `__new__` **creates** an empty object in memory
  2. `__init__` **fills** it: it initializes the attributes
- `__new__` receives the class (`cls`), `__init__` receives the new object (`self`)
- Most of the time we only write `__init__`: the default `__new__` of Python is enough
- Careful: `__init__` does not call `__new__`. It is the other way round: new first, then init

## __new__: the code explained
- `cls`: the class itself (`Cercle`)
- `*args, **kwargs`: all the values written in `Cercle(...)`
- `super().__new__(cls)`: asks the parent class (`object`) to create the empty object
- `return instance`: gives the object back. Without it, `__init__` is never called
```python
class Cercle:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)    # create the empty object
        print("fonction new")
        return instance                    # then Python calls __init__
    def __init__(self, a=1, b=0, c=0):
        self.rayon, self.abs, self.ord = a, b, c
        print(self.rayon, self.abs, self.ord)

S = Cercle()     # prints: fonction new, then 1 0 0
```

## What is __new__ used for?
- **Control how many objects exist**: the **Singleton** pattern (chapter 5, used in the exams)
- **Subclass immutable types** (`int`, `str`, `tuple`): their value must be set at creation
- **Reuse an object** instead of creating a new one (a cache)
```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:                  # first call: create the object
            cls._instance = super().__new__(cls)
        return cls._instance                       # next calls: give the same object

a = Singleton()
b = Singleton()
print(a is b)      # True: there is only one object
```

## Encapsulation
- Prevents attribute values from being changed **by mistake**, and limits access
- Make attributes private with an underscore prefix
- To reach private attributes and methods, go through the class's **public methods**
```python
class Circle:
    def __init__(self, a=1, b=0, c=0):
        self.__ray = a       # private attribute
        self.abs = b
        self.ord = c

C = Circle(2, 1, 1)
C.ray     # AttributeError: 'Circle' object has no attribute 'ray'
```
- Any method can call another method of the same class, or itself (**recursion**)

## Nested classes
- A class can be declared **inside** another class
- Use it when the inner class only makes sense **inside** the outer one: an `Engine` belongs to a `Car`
```python
class Car:
    class Engine:                          # nested class
        def __init__(self, power):
            self.power = power
        def start(self):
            print("engine", self.power, "hp started")
    def __init__(self, model, power):
        self.model = model
        self.engine = Car.Engine(power)    # the car builds its own engine
    def start(self):
        self.engine.start()
        print(self.model, "is moving")
```

## Nested classes: using it
- Inside the outer class, write `Car.Engine(...)`
- Outside, refer to the nested class with its **fully qualified name**: `Car.Engine`
```python
c = Car("Golf", 110)
c.start()                  # engine 110 hp started / Golf is moving

e = Car.Engine(90)         # from outside: the full name
print(e.power)             # 90
```

## Nested classes: the example of the course
- Classes are taken into the scope of the enclosing class and can be used within that scope
```python
class Circle:
    class Shape:
        def __init__(self, a, b):
            self.abs, self.ord = a, b
        class Rectangle:
            def __init__(self, a=1, b=4):
                self.width, self.height = b, a
            def area(self):
                return self.width * self.height

C = Circle()
S = Circle.Shape(5.5, 6)
R = Circle.Shape.Rectangle(2, 8)
```

## Sending messages between objects
- Objects communicate by **calling each other's methods**
  - **send** a message = call a method of an object
  - **receive** a message = run the body of the called method
- This is the key mechanism of an OOP program

## Objects as arguments
- An object is passed to a function like any variable
- The class name can be added as a hint: `c: Circle`
```python
class Point:
    def __init__(self, a, b):
        self.x, self.y = a, b
    def modify(self, a, b):
        self.x *= a
        self.y *= b
    def display(self):
        print('class attributes are:', self.x, 'et', self.y)
    def values(self, c: "Circle"):      # receives a Circle
        c.abs = self.x
        c.ord = self.y
        self.display()
```

## Objects as arguments
- Circle and Point send messages to each other:
```python
class Circle:
    def __init__(self, a=1, b=0, c=0):
        self.ray, self.abs, self.ord = a, b, c
    def Move(self, a, b, c: Point):     # receives a Point
        c.modify(a, b)
        self.abs += a
        self.ord += b

C = Circle(2, 4, 5)
P = Point(2, 2)
C.Move(3, 6, P)      # Circle calls Point.modify
P.values(C)          # Point changes C's attributes
print(C.abs, C.ord)  # 6 12
```

## Objects as attributes: composition
- An object can be an **attribute** of another class
- A **composite class** has at least one object of another class among its attributes
- Its objects get access to all the attributes and methods of the inner object
```python
class Circle:
    """Composite class with a Point object as attribute"""
    def __init__(self, a=1, b=0, c=0):
        self.rayon = a
        self.p = Point(b, c)          # the centre is a Point

    def Move(self, a, b):
        print("call the move function of Point")
        self.p.move(a, b)

A = Circle(2, 3, 4)
print(A.p.x, A.p.y)    # 3 4
A.Move(2, 2)
A.p.display()          # Point attributes are: 5 and 6
```

## Summary
| Concept | Chapter |
|---|---|
| Class, object, attributes, methods, `self`, `__init__` | 1, 3 |
| Abstraction, encapsulation, private `__x` / protected `_x` | 1, 3 |
| Python basics: control flow, containers, numpy, functions | 2 |
| Class attributes, runtime attributes, `__dict__`, getattr… | 3 |
| `self` vs `cls`, `__new__` vs `__init__` | 3 |
| Nested classes, messages, objects as arguments / attributes, composition | 3 |
- Next: **Chapter 4 · Inheritance and Polymorphism**, **Chapter 5 · Design Patterns**
