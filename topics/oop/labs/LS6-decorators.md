---
title: LS6 · Decorators
subtitle: Lab session with solutions
course: OOP · USTHB Master RT 2026/2027
---

# Objective

## Objective
- In this practical work we discuss **function decorators** and **class decorators**
- Three exercises:
  1. a dictionary of sessions, decorated with `Deco`
  2. a clothing production, decorated with `Sort`
  3. a bank account, with a `Profit` decorator on the method `Feed`

## What is a decorator?
- A **decorator** is a function that receives a function and returns a **new function**, which runs the original one and adds some processing around it
- Writing `@Deco` above `def Select(...)` is exactly the same as writing `Select = Deco(Select)` after the definition
```python
def Deco(func):                  # receives the function to decorate
    def wrapper(*args):          # the new function
        print("before")
        result = func(*args)     # the original function runs here
        print("after")
        return result
    return wrapper

@Deco                            # same as: hello = Deco(hello)
def hello():
    print("hello")

hello()                          # before / hello / after
```

# Exercise 1 · Sessions

## Exercise 1: statement
1. To record the progress in some subjects, create a **dictionary** with the keys: `course` (class sessions), `TD`, `TP`
   - `course`: a list of tuples with the name of each subject and the number of sessions: `[(POO, 14), (CNA, 20), (TAS, 14)]`
   - `TD`: `[(POO, 0), (CNA, 12), (TAS, 12)]`
   - `TP`: `[(POO, 7), (CNA, 4), (TAS, 6)]`
2. A **`Select`** function that receives the dictionary as a parameter and displays the tuples that have a session count **greater than 10**
3. A **`Deco`** decorator that receives `Select` as a parameter. It adds the key `class` with a tuple such as `[('RT', 80)]` and displays all the keys of the dictionary
4. Call `Select` **before and after** adding the decorator

## Exercise 1: solution
```python
# 1. the dictionary
Prog = {
    "course": [("POO", 14), ("CNA", 20), ("TAS", 14)],
    "TD":     [("POO", 0), ("CNA", 12), ("TAS", 12)],
    "TP":     [("POO", 7), ("CNA", 4), ("TAS", 6)],
}

# 2. Select: displays the tuples with more than 10 sessions
def Select(dic):
    for key, lst in dic.items():
        for name, sessions in lst:
            if sessions > 10:
                print(key, name, sessions)

# 3. the decorator
def Deco(func):
    def wrapper(dic):
        func(dic)                                # first the original function
        dic["class"] = [("RT", 80)]              # then we add the key "class"
        print(list(dic.keys()))                  # and display all the keys
    return wrapper

# 4. before and after the decoration
print("--- before ---")
Select(Prog)

Select = Deco(Select)                            # same as writing @Deco above def Select

print("--- after ---")
Select(Prog)
```

## Exercise 1: the output
```text
--- before ---
course POO 14
course CNA 20
course TAS 14
TD CNA 12
TD TAS 12
--- after ---
course POO 14
course CNA 20
course TAS 14
TD CNA 12
TD TAS 12
['course', 'TD', 'TP', 'class']
```
- After the decoration, `Select` does the same selection **and** adds the key `class` and displays the keys
- The decoration **replaces** the name `Select`: the call `Select(Prog)` now runs `wrapper`
- The decorator adds the key **after** the selection. If it added it before, `('RT', 80)` would also be selected (80 > 10)

# Exercise 2 · Clothing

## Exercise 2: statement
1. A company produces clothing (pants, shirts and jackets). For each product, create a **list** containing the name and the number of items produced. The 3 lists are placed in a list that encompasses them
2. A **`Stock`** function that receives the list as a parameter. For each product, a **label** 1 (the product is good) or 0 (the product has defects) is randomly added. To save this information, create a numpy array called `Quality`, whose size is the number of items. It is randomly filled with 0 and 1 and **added to the list of the product**
3. A decorator **`Sort`** that separates the good items from the defective ones. It starts by executing the content of `Stock`. Then, for each product, it extracts the good products (label 1), **deletes the numpy array**, and adds the **list of indexes** of the good items to the product list. Use `np.where` to retrieve the labels, `pop` to delete the array and `insert` to add the tuple of indexes
4. Run the program **before and after** the decoration and display the list each time

## Exercise 2: solution
```python
import numpy as np

# 1. one list per product: [name, number of items]; the 3 lists are in one list
Products = [["pants", 6], ["shirts", 5], ["jackets", 4]]

# 2. Stock: adds to each product an array of labels (1 = good, 0 = defective)
def Stock(P):
    for p in P:
        Quality = np.random.randint(0, 2, p[1])      # as many labels as items
        p.append(Quality)

# 3. the decorator Sort
def Sort(func):
    def wrapper(P):
        func(P)                                      # first the original function
        for p in P:
            Quality = p.pop()                        # remove the numpy array
            good = np.where(Quality == 1)[0]         # indexes of the good items
            p.insert(2, tuple(good.tolist()))        # add them as a tuple
    return wrapper

# 4. before and after the decoration
np.random.seed(4)                                    # same random labels in both runs
Stock(Products)
print(Products)

Products = [["pants", 6], ["shirts", 5], ["jackets", 4]]
np.random.seed(4)
Stock = Sort(Stock)                                  # same as @Sort above def Stock
Stock(Products)
print(Products)
```

## Exercise 2: the output
```text
[['pants', 6, array([0, 0, 1, 1, 1, 0])],
 ['shirts', 5, array([1, 0, 0, 1, 0])],
 ['jackets', 4, array([0, 1, 1, 0])]]

[['pants', 6, (2, 3, 4)], ['shirts', 5, (0, 3)], ['jackets', 4, (1, 2)]]
```
- **Before**: each product ends with its `Quality` array of 0 and 1
- **After**: the array is replaced by the tuple of the **indexes of the good items**: the pants number 2, 3 and 4 are good
- `np.where(Quality == 1)[0]` gives the positions where the label is 1. `p.pop()` removes the last element (the array) and `p.insert(2, ...)` puts the tuple in its place
- The seed is fixed before each run only so that both runs use the **same random labels**

# Exercise 3 · Bank account

## Exercise 3: statement
To manage a customer's bank account, an object-oriented program is proposed:
1. An **`Account`** class with an attribute `S` (balance) initialized to a sum of your choice, an attribute `State` initialized to `True`, a dictionary `d` with two keys `debited` and `credited` whose values are initialized to 0 and `S`
2. A **`Consult`** method that checks if the balance exceeds **1000 DA**. Otherwise the account is **blocked** (`State` set to `False`)
3. A **`Withdraw`** method that asks the customer for the desired amount. If `State` is `True`, if the balance is greater than this amount, and if the sum of this amount with the `debited` value is less than **100000 DA**, the withdrawal is granted: a message says that the operation has been validated, the balance is reduced, and `Consult` is called

## Exercise 3: statement, Feed and Profit
4. A **`Feed`** method that adds the amount received as a parameter to the balance, increases the `credited` value of the dictionary by that amount, and sets `State` to `True`
5. A decorator **`Profit`** on the `Feed` method. `Profit` calls `Feed`, checks the **difference between the debit and credit values**, calculates the profit rate as **10 %** of that difference, which is **added to the balance** and **returned** to the calling program
6. Create an `Account` object with an amount of your choice and call `Consult`, `Withdraw` and `Feed`. For `Feed`, call it **before and after** applying the decorator

## Exercise 3: solution, the decorator and the class
```python
# 5. the decorator Profit
def Profit(func):
    def wrapper(self, x):
        func(self, x)                                       # Feed
        diff = abs(self.d["debited"] - self.d["credited"])  # difference debit / credit
        profit = 0.1 * diff                                 # 10 % of the difference
        self.S += profit                                    # added to the balance
        return profit                                       # and returned
    return wrapper


class Account:
    def __init__(self, S=3000):                             # 1. the attributes
        self.S = S                                          # balance
        self.State = True
        self.d = {"debited": 0, "credited": S}

    def Consult(self):                                      # 2. the balance must exceed 1000 DA
        if self.S <= 1000:
            self.State = False                              # the account is blocked

    def Withdraw(self):                                     # 3.
        x = float(input("Amount to withdraw: "))
        if self.State and self.S > x and x + self.d["debited"] < 100000:
            print("withdrawal validated")
            self.S -= x
            self.d["debited"] += x
            self.Consult()
        else:
            print("withdrawal refused")

    def Feed(self, x):                                      # 4.
        self.S += x
        self.d["credited"] += x
        self.State = True
```
- A decorator for a **method** takes `self` as the first parameter of `wrapper`
- `Withdraw` also adds the amount to `debited`, so the limit of 100000 DA works over time

## Exercise 3: solution, the main program
```python
# 6. the main program
A = Account(3000)
A.Consult()
A.Withdraw()                       # Amount to withdraw: 300  ->  withdrawal validated
print(A.S, A.State, A.d)           # 2700.0 True {'debited': 300.0, 'credited': 3000}
A.Withdraw()                       # Amount to withdraw: 5000  ->  withdrawal refused

A.Feed(1000)                       # before the decoration: no profit
print(A.S)                         # 3700.0

Account.Feed = Profit(Account.Feed)     # same as writing @Profit above def Feed
print(A.Feed(1000))                     # 470.0  Feed now returns the profit
print(A.S, A.d)                         # 5170.0 {'debited': 300.0, 'credited': 5000}
```

## Exercise 3: how the profit is computed
| | Value |
|---|---|
| `debited` | 300 |
| `credited` | 5000 (3000 + 1000 + 1000) |
| difference | 4700 |
| profit (10 %) | 470 |
| balance | 3700 + 1000 (the amount) + 470 (the profit) = **5170** |
- Before the decoration, `Feed` only adds the amount
- After it, the same call also adds the **profit** and **returns** it
- In the class, the decoration is written with `@Profit` on the line above `def Feed`
