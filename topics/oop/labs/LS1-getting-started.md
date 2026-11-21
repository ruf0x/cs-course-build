---
title: LS1 · Getting started with Python
subtitle: Lab session with solutions
course: OOP · USTHB Master RT 2026/2027
---

# Installation and modules

## Objective
- This first lab session familiarizes students with the **Python** programming language
- We cover:
  - installing Python
  - integrating libraries
  - importing modules
  - manipulating files

## Installing the Anaconda distribution
- **Anaconda**: an open source platform for Python and R programming, widely used in data science, machine learning, deep learning and scientific computing
- It includes two environments for Python programming:
  - **Spyder**: an IDE (like PyCharm and VS Code) focused on scientific computing, recommended for writing and executing **full scripts** at once
  - **Jupyter**: an interactive **web notebook** that organizes and executes code in **cells**
- Download: `https://www.anaconda.com/download`

## The libraries of the lab sessions
| Library | Role |
|---|---|
| Numpy | multi-dimensional arrays |
| Pickle | serialization and storage of data (matrices, vectors). Can be replaced by the `npy` format of numpy |
| OS | manage files and directories: we use it to find the path of the image files |
| Matplotlib | charts and plots (line charts, histograms) |
| Pandas | data manipulation and analysis (series, dataframes) |
| Skimage | image processing: filtering, transformations, features. `pip install scikit-image` |
| Opencv-Python | computer vision: read and preprocess images, extract features. `pip install opencv-python` |

## Other libraries
- The number of libraries keeps growing, in all application areas. The use of a module depends on the needs of your application
| Domain | Library |
|---|---|
| Machine Learning | `sklearn` |
| Deep Learning | `Keras`, `Pytorch`, `Tensorflow` |
| Internet protocols (FTP, HTML) | the Python standard library |
| Network applications (server) | `socket` and `sys` |
| Graphical interfaces | `tkinter` |

## Importing modules
- All the libraries we use are called **modules**: toolboxes of functions, developed in OOP and organized in classes
- Create a new file in Spyder (or Jupyter): `Initiation.py`
- By convention, the file is organized in this order:
  1. the imported modules
  2. the global variables (if any)
  3. the programs
- Three ways to import:
  - `import [module_name]`
  - `from [module_name] import [function_name]`
  - `from [module_name] import *`

## Import examples
| Instruction | What it does | Example |
|---|---|---|
| `import numpy` | all the functions, called through the object `numpy` | `A = numpy.ones((1, 10))` |
| `import numpy as np` | same, with the short name `np` | `A = np.ones((1, 10))` |
| `from random import normalvariate` | one function only, called directly (no object) | `x = normalvariate(0, 1)` |
```python
import numpy as np
from random import normalvariate

A = np.ones((1, 10))        # a vector of 10 elements equal to 1
x = normalvariate(0, 1)     # one value of the normal distribution
print(A)                    # [[1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]]
```

# Application 1 · Binary files

## Application 1: statement
- Create a program that creates **5 numpy arrays** filled with **50 random values** in the interval [0, 100], following a **uniform distribution**
- The arrays are grouped into a list `Liste`, transformed into a **numpy matrix**, and **stored in a file**
- To check the program, open the pickle file and display the data
- Steps:
  1. open a Jupyter notebook and import the `numpy`, `random` and `pickle` modules
  2. reproduce the program of Figure 1

## Application 1: solution
```python
import numpy as np
import pickle

Liste = []                                  # create an empty list
for i in range(5):                          # 5 arrays
    A = np.random.uniform(0, 100, 50)       # 50 values, uniform distribution on [0, 100]
    Liste.append(A)                         # add A to the list

M = np.array(Liste)                         # the list becomes a numpy matrix (5 x 50)

f = open('file.pkl', 'wb')                  # create a file to store the data
pickle.dump(M, f)                           # save the matrix in the file
f.close()

ff = open('file.pkl', 'rb')                 # open the file to read
L = pickle.load(ff)                         # load the file content in L
ff.close()

print(M.shape, L.shape)                     # (5, 50) (5, 50)
print(np.array_equal(M, L))                 # True: what we read is what we saved
print(L[0, :5])                             # the first 5 values of the first array
```

## Application 1: remarks
- Unlike C++, where each statement ends with `;`, in Python it is **not necessary**
- The **indentation** shows which statements are inside a loop:
  - the first `for` is followed by indented statements: they run at each iteration
  - `Liste.append(A)` is aligned with the loop body, so it runs at each iteration; a statement aligned with the `for` runs after the loop
- `append` adds the array to the **end** of the list
- In Python, **every variable is an object**, even the indexes `i` and `j`
- To delete a variable `A`: `del A`. To clear the console: `clear`
- `wb` / `rb` = write / read in **binary**. Figure 1 uses `np.save(f, Liste)` and `np.load(ff)` instead of `pickle`: same idea

# Application 2 · Images

## Application 2: statement
- We manipulate the **Opencv**, **OS** and **Matplotlib** modules
- 5 image files are placed in a directory (on the Desktop of your computer)
- The images have **variable sizes**. The program must:
  1. read the images
  2. set them to a single size of **100 × 100 pixels**
  3. store the **normalized** images in a table
  4. save the table in a file
- Also: display the images that are read

## Application 2: reading one image
- The test: read an image file located in a **different directory** than the Python file (Figure 2)
- To write a path we use `/`. The `\` is used at the end of a line to say that the instruction continues on the next line, and `\n` makes a carriage return in the console
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('C:/Users/Home/Desktop/Images/0g.jpg')    # read the image file 0g.jpg
plt.imshow(img)                                            # display it
```
- Careful: Figure 2 writes `cv2.read`. The OpenCV function is **`cv2.imread`**

## Application 2: reading many images
- To read **all** the images of a directory we need the `os` module
- First, the path of the directory in a string: `Rep = 'C:/Users/Home/Desktop/images/'`
- Then a `for` loop scans the directory:
```python
for pic in os.listdir(Rep):
    img = cv2.imread(os.path.join(Rep, pic))
```
- In Python the loop index is not necessarily an integer: here `pic` is a **string** (a file name)
- To normalize the size to 100 × 100: `cv2.resize`, or `resize` from PIL (`from PIL import Image`)

## Application 2: solution
```python
import cv2
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt

Rep = 'C:/Users/Home/Desktop/images/'             # the directory of the images
Table = []                                        # the list that will hold the images

for pic in os.listdir(Rep):                       # pic = one file name of the directory
    img = cv2.imread(os.path.join(Rep, pic))      # read the image (BGR)
    img = cv2.resize(img, (100, 100))             # same size for all: 100 x 100 pixels
    img = img / 255.0                             # normalization: values in [0, 1]
    Table.append(img)                             # add it to the list
    plt.imshow(cv2.cvtColor(img.astype('float32'), cv2.COLOR_BGR2RGB))   # display (BGR -> RGB)
    plt.show()

T = np.array(Table)                               # one table: 5 images of 100 x 100 x 3
print(T.shape)                                    # (5, 100, 100, 3)
print(T.min() >= 0, T.max() <= 1)                 # True True

with open('images.pkl', 'wb') as f:               # save the table in a file
    pickle.dump(T, f)
```

## Application 2: remarks
- `cv2.imread` reads the colors in the order **BGR**, `plt.imshow` expects **RGB**: `cv2.cvtColor` fixes the colors
- Normalization = divide by 255, so every pixel is between 0 and 1
- After resizing, all the images have the same shape, so they fit in **one numpy array** (5 × 100 × 100 × 3)
- `with open(...) as f:` closes the file by itself

# Application 3 · Signals

## Application 3: statement
- Generate random signals made of a **sine wave embedded in Gaussian noise**
- The sine signal: amplitude `A = 2 V`, frequency `F = 5`, sampling frequency `fs = 2000`, duration `d = 2` seconds
- The noise standard deviation `st` varies between **0.5 and 1.5**
- The time vector: `np.arange(0, d, 1/fs)`
- The sine signal: `x = A * np.sin(2 * np.pi * F * t)`
- The Gaussian noise: `np.random.normal(0, st, len(t))`
- Deduce the final signal and evaluate the **impact of the value of st**
- Add an **offset** to the derived signal and calculate the statistics (mean, variance, std) with numpy

## Application 3: solution
```python
import numpy as np

A, F, fs, d = 2, 5, 2000, 2                   # amplitude, frequency, sampling frequency, duration
t = np.arange(0, d, 1 / fs)                   # time vector
x = A * np.sin(2 * np.pi * F * t)             # the sine signal
offset = 1                                    # offset added to the final signal
np.random.seed(0)                             # same random numbers at each run

for st in (0.5, 1.0, 1.5):                    # noise standard deviation
    noise = np.random.normal(0, st, len(t))   # Gaussian noise
    y = x + noise + offset                    # final signal = sine + noise + offset
    snr = 10 * np.log10(np.var(x) / np.var(noise))   # signal / noise power ratio, in dB
    print(f"st={st}: mean={y.mean():.3f}  var={y.var():.3f}  std={y.std():.3f}  SNR={snr:.1f} dB")
```

## Application 3: results and impact of st
| st | mean | variance | std | SNR |
|---|---|---|---|---|
| 0.5 | 0.987 | 2.248 | 1.499 | 9.2 dB |
| 1.0 | 0.998 | 3.085 | 1.756 | 3.1 dB |
| 1.5 | 0.971 | 4.115 | 2.029 | -0.5 dB |
- The **mean** stays close to the offset (1): the noise has a zero mean
- The **variance** is about `A²/2 + st²` = `2 + st²`: the sine contributes 2, the noise `st²`
- The bigger `st`, the **lower the SNR**: the sine is more and more hidden by the noise

# Application 4 · Dataframes

## Application 4: statement
- Telecommunication data is often collected as **KPIs** (Key Performance Indicators) stored in a **DataFrame**. We consider a CSV file `drone_communication_dataset`
  1. import `DataFrame` from pandas (`import pandas as pd`) and `scatter` from matplotlib
  2. read the file with `read_csv` and display its first 5 lines with `head`
  3. remove the `timestamp` column with `drop`
  4. extract the first **500 rows** of the columns from `speed_trajectory` to `signal_noise_ratio` into a new dataframe, with `loc` **and** with `iloc`, then compare the results
  5. observe `signal_noise_ratio` as a function of `transmission_power` with `plt.scatter`

## Application 4: solution
```python
import pandas as pd
import matplotlib.pyplot as plt

# 2. read the file and display the first 5 lines
df = pd.read_csv('drone_communication_dataset.csv')
print(df.head())

# 3. remove the timestamp column
df = df.drop(columns='timestamp')

# 4. the first 500 rows of the columns from speed_trajectory to signal_noise_ratio
a = df.loc[:499, 'speed_trajectory':'signal_noise_ratio']        # with labels
i = df.columns.get_loc('speed_trajectory')
j = df.columns.get_loc('signal_noise_ratio')
b = df.iloc[:500, i:j + 1]                                       # with positions
print(a.equals(b))                                               # True: same result

# 5. signal_noise_ratio as a function of transmission_power
plt.scatter(df['transmission_power'], df['signal_noise_ratio'])
plt.xlabel('transmission_power')
plt.ylabel('signal_noise_ratio')
plt.show()
```

## loc vs iloc
| | `loc` | `iloc` |
|---|---|---|
| Selects with | **labels** (row labels, column names) | **positions** (integers) |
| The end of a slice | **included** | **excluded** |
| Example | `df.loc[:499, 'speed_trajectory':'signal_noise_ratio']` | `df.iloc[:500, i:j + 1]` |
- `loc` includes the end label: `:499` gives rows 0 to 499, which are 500 rows
- `iloc` excludes the end position: `:500` gives the same 500 rows
- The two extractions give the **same dataframe**
