---
title: LS2 · Basics of Python programming
subtitle: Lab session with solutions
course: OOP · USTHB Master RT 2026/2027
---

# Objective

## Objective
- In this practical session, we explore some fundamental concepts of Python programming:
  - strings
  - lists
  - tuples
  - dictionaries
  - numpy arrays
  - execution flow control instructions
  - functions

# Exercise 1 · Characters of a string

## Exercise 1: statement
- We consider a character string: `S = "parse in strings in python programming"`
  1. Extract the characters that make up the string and put them in a **list** with their **frequencies** of appearance
  2. Create a `while True` loop that handles the following code:
     - the list is displayed, and the user is asked to **guess the most frequent character**
     - if the user enters the correct character: the message `"Character found"` is displayed, followed by a `break`
     - otherwise: the message `"This is not the correct character"` is displayed, followed by a `continue`

## Exercise 1: solution
- The spaces are ignored: only the letters are counted
```python
S = "parse in strings in python programming"

# 1. the characters with their frequencies
freq = []
for c in S:
    if c != " " and c not in [x[0] for x in freq]:    # each character only once
        freq.append([c, S.count(c)])
best = max(freq, key=lambda x: x[1])[0]                # the most frequent one

# 2. the game
while True:
    print(freq)
    guess = input("Which character is the most frequent? ")
    if guess == best:
        print("Character found")
        break                                          # leave the loop
    else:
        print("This is not the correct character")
        continue                                       # ask again
```

## Exercise 1: an example run
```text
[['p', 3], ['a', 2], ['r', 4], ['s', 3], ['e', 1], ['i', 4], ['n', 5], ['t', 2],
 ['g', 3], ['y', 1], ['h', 1], ['o', 2], ['m', 2]]
Which character is the most frequent? a
This is not the correct character
[['p', 3], ['a', 2], ['r', 4], ...]
Which character is the most frequent? n
Character found
```
- Each element of `freq` is a small list `[character, frequency]`
- `max(freq, key=lambda x: x[1])` finds the element with the biggest frequency: here `n`, 5 times
- `break` **stops** the loop, `continue` goes to the **next iteration** (here, it asks again)

# Exercise 2 · Students and TP marks

## Exercise 2: statement
- To evaluate the students' grades in a practical exercise, we create the following code:
  1. Create a **list** in which we put a **tuple** composed of: the **Name** and a **dictionary** containing the TPs as keys (`TP1`, `TP2`, `TP3`, `TP4`, `TP5`) and the marks obtained as values. The list must contain at least **5 students**
  2. To assess each student's condition, the **average** is calculated and added to their dictionary
  3. To check the student's status (deferred or admitted), the user enters the name and the program returns the **average** and the **status**
  4. Put the code of questions 2 and 3 in a **function** that receives the student's name and returns the lab grades grouped in a **list**

## Exercise 2: solution, questions 1 and 2
```python
# 1. a list of tuples (name, dictionary of TP marks)
students = [
    ("Sara",   {"TP1": 15, "TP2": 12, "TP3": 14, "TP4": 16, "TP5": 13}),
    ("Omar",   {"TP1": 8,  "TP2": 9,  "TP3": 11, "TP4": 7,  "TP5": 10}),
    ("Lina",   {"TP1": 18, "TP2": 17, "TP3": 19, "TP4": 16, "TP5": 20}),
    ("Yacine", {"TP1": 10, "TP2": 12, "TP3": 9,  "TP4": 11, "TP5": 10}),
    ("Nour",   {"TP1": 5,  "TP2": 8,  "TP3": 6,  "TP4": 9,  "TP5": 7}),
]

# 2. the average of each student is added to his dictionary
for name, tp in students:
    tp["average"] = sum(tp.values()) / len(tp)
```
- The average is computed **before** the key `"average"` is added, so `len(tp)` is 5
- `for name, tp in students` unpacks each tuple into the name and the dictionary

## Exercise 2: solution, question 3
```python
# 3. the user enters a name: average and status
name = input("Student name: ")                        # Omar
for n, tp in students:
    if n == name:
        status = "admitted" if tp["average"] >= 10 else "deferred"
        print(n, tp["average"], status)               # Omar 9.0 deferred
```
- The student is **admitted** when the average is at least 10, **deferred** otherwise
- Omar: (8 + 9 + 11 + 7 + 10) / 5 = 9.0, so he is deferred

## Exercise 2: solution, question 4
```python
def evaluate(name):
    for n, tp in students:
        if n == name:
            marks = [v for k, v in tp.items() if k.startswith("TP")]   # the lab grades
            average = sum(marks) / len(marks)
            tp["average"] = average
            print(n, average, "admitted" if average >= 10 else "deferred")
            return marks                                               # grouped in a list
    print("student not found")
    return []

print(evaluate("Sara"))     # Sara 14.0 admitted
                            # [15, 12, 14, 16, 13]
print(evaluate("Zoe"))      # student not found
                            # []
```
- The function does the work of questions 2 and 3, and **returns** the list of marks
- `k.startswith("TP")` keeps the marks and leaves out the key `"average"`

# Exercise 3 · Matrices

## Exercise 3: statement
1. Define a **function** that receives a matrix as a parameter:
   - if the matrix is **square**, the function returns its **trace** (the sum of the diagonal elements)
   - otherwise, it extracts and displays the part that corresponds to the **square sub-matrix** of the global matrix, and returns the **sum of all the elements** of this sub-matrix
2. Create a matrix `M` of random real values: the user enters the number of rows and columns, then `np.empty` is called. Use `for` loops to fill the matrix with `np.random.random()`
3. Call the function with `M` as a parameter

## Exercise 3: solution
```python
import numpy as np

# 1. the function
def process(M):
    rows, cols = M.shape
    if rows == cols:                       # square matrix: the trace
        return sum(M[i, i] for i in range(rows))
    n = min(rows, cols)                    # otherwise: the square sub-matrix
    sub = M[:n, :n]
    print(sub)
    return sub.sum()

# 2. the matrix
rows = int(input("Rows: "))                # 3
cols = int(input("Columns: "))             # 4
M = np.empty((rows, cols))
for i in range(rows):
    for j in range(cols):
        M[i, j] = np.random.random()       # a random real value in [0, 1[

# 3. the call
print(process(M))
```

## Exercise 3: how it works
| Matrix | What the function does | It returns |
|---|---|---|
| 3 × 3 (square) | nothing to display | the trace: `M[0,0] + M[1,1] + M[2,2]` |
| 3 × 4 (not square) | displays the 3 × 3 sub-matrix `M[:3, :3]` | the sum of its 9 elements |
- `M.shape` gives `(rows, columns)`
- The square sub-matrix has the size of the **smaller** dimension: `n = min(rows, cols)`
- For a square matrix, `np.trace(M)` gives the same value
