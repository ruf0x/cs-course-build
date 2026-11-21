---
title: LS3 · Creation of modules and packages
subtitle: Lab session with solutions
course: OOP · USTHB Master RT 2026/2027
---

# Statement

## Objective
- In this lab session we create a **package** for managing the grades of the students of a section
- The package contains two modules:
  - `information`: the enrollment and the checking of the students
  - `treatment`: the grades, the averages and the ranking
- A main program `Main.py` uses them

## The statement: the information module
1. **`information` module** (a `.py` file) in which the following functions are defined:
   - **`enroll`**: performs the students' enrollment. It receives the **number of students** and an **empty list**. For each student, it builds a **dictionary** of two elements: `'Name': 'Student name'` and `'Matricule': student number` (the numbers start from **100**). The function returns the completed list to the main program
   - **`check`**: receives the student's **registration number** and the **list of all students**. It displays the student's information (the dictionary). If the student is not enrolled, it displays a message saying that the student cannot be found

## The statement: the treatment module
2. Another **`treatment` module**, containing the following functions:
   - **`evaluation`**: receives the student's registration number, the list of the student's grades and the list of all students. It adds an element `{grades: t}` to the student's dictionary, where `t` is an array containing **5 grades**
   - **`average`**: receives the list of students. It calculates the average of each student and adds it to his dictionary, with the **status** (passed or deferred)
   - **`ranking`**: receives a student's ID number and the list of all students. It calls `average`, retrieves the average of the received ID number into a variable, extracts the names and averages of all students into a **list of tuples**, and provides the **ranking** of the student

## The statement: the package and the main program
3. Put both `treatment` and `information` modules in a **package**: a folder called `Section`
4. The main program `Main.py` is a file in the **same directory** as `Section`. In this file, we declare a list `Base` that contains the information of all the students (the list passed as a parameter to the functions). Import the modules from the package: `import Section.treatment as TT`
   - call `enroll` (for **10 students**), then verify the information of a given student
   - for each student create a list of 5 grades (for example with `np.random.random(5)*20`) and call `evaluation`
   - choose a registration number and call `ranking` to find out the student's ranking

# Solution

## The structure
```text
project/
├── Main.py                  the main program
└── Section/                 the package (a folder)
    ├── __init__.py          empty file: marks the folder as a package
    ├── information.py       enroll, check
    └── treatment.py         evaluation, average, ranking
```
- `Main.py` is in the **same directory** as the folder `Section`
- The empty `__init__.py` tells Python that `Section` is a package (recent versions of Python also accept a folder without it)
- In the statement the checking function is called `check` in the module and `verify` in the main program: it is the same function. We call it `check`

## Section/information.py: enroll
```python
def enroll(n, L):
    """Enroll n students: each one is a dictionary {'Name': ..., 'Matricule': ...}."""
    for k in range(n):
        name = input(f"Name of student {k + 1}: ")
        L.append({'Name': name, 'Matricule': 100 + k})     # numbers start from 100
    return L
```
- `enroll` builds one dictionary per student and returns the completed list to the main program
- `100 + k`: the registration numbers start from 100 and go up by one

## Section/information.py: check
```python
def check(mat, L):
    """Display the information of the student whose matricule is mat."""
    for student in L:
        if student['Matricule'] == mat:
            print(student)
            return
    print("Student", mat, "cannot be found")
```
- `return` stops the function as soon as the student is found. The message is displayed only if the loop ends without finding him

## Section/treatment.py: evaluation and average
```python
import numpy as np


def evaluation(mat, t, L):
    """Add {'grades': t} to the dictionary of the student mat (t = array of 5 grades)."""
    for student in L:
        if student['Matricule'] == mat:
            student['grades'] = t


def average(L):
    """Add the average and the status to the dictionary of every student."""
    for student in L:
        student['average'] = float(np.mean(student['grades']))
        student['status'] = 'passed' if student['average'] >= 10 else 'deferred'
```
- The list is modified **in place**: the dictionaries of `Base` receive the new keys, so nothing has to be returned

## Section/treatment.py: ranking
```python
def ranking(mat, L):
    """Return the rank of the student mat (1 = best average)."""
    average(L)
    for student in L:
        if student['Matricule'] == mat:
            mine = student['average']                                  # the average of mat
    pairs = [(s['Name'], s['average']) for s in L]                     # list of tuples (name, average)
    pairs.sort(key=lambda p: p[1], reverse=True)                       # best first
    rank = 1 + sum(1 for name, avg in pairs if avg > mine)
    return rank
```
- The rank is 1 plus the number of students that have a **better average**

## Main.py: enroll and check
```python
import numpy as np
import Section.information as II
import Section.treatment as TT

Base = []                                   # the list of all the students

# 1. enroll 10 students, then check one of them
Base = II.enroll(10, Base)
II.check(103, Base)
II.check(250, Base)
```
- `import Section.information as II` imports the module `information` of the package `Section` under the short name `II`

## Main.py: grades and ranking
```python
# 2. 5 grades for each student (random values between 0 and 20)
for student in Base:
    t = np.random.random(5) * 20
    TT.evaluation(student['Matricule'], t, Base)

# 3. the ranking of a student
print("Rank of 105:", TT.ranking(105, Base))
for s in Base:
    print(s['Matricule'], s['Name'], round(s['average'], 2), s['status'])
```

## An example run
```text
Name of student 1: Sara
Name of student 2: Omar
...
Name of student 10: Walid
{'Name': 'Yacine', 'Matricule': 103}
Student 250 cannot be found
Rank of 105: 3
100 Sara 11.81 passed
101 Omar 6.89 deferred
102 Lina 8.36 deferred
103 Yacine 7.39 deferred
104 Nour 8.47 deferred
105 Amine 10.53 passed
106 Ines 15.1 passed
107 Karim 7.56 deferred
108 Dina 7.58 deferred
109 Walid 9.85 deferred
```
- Student 105 has the 3rd best average (10.53), behind 106 (15.1) and 100 (11.81)
- The grades are random: your numbers will be different
