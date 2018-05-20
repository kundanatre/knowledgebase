# Setup Development environment for Machine Learning

## Prerequisites
Install the Python and Anaconda environment as described in the [Install Anaconda][] page.

## Setup for Development
Assuming you have created an environment as `ML365` where it is using the `Python v3.6.5`, Activate the environment by going to the working projects folder and issuing the command 
```
$ source activate ML365
``` 

Now install the required libraries most frequently required for Machine learning  

### NumPy  
[NumPy][] is the fundamental package for scientific computing with Python. It contains among other things
+ a powerful N-dimensional array object
+ sophisticated (broadcasting) functions
+ tools for integrating C/C++ and Fortran code
+ useful linear algebra, Fourier transform, and random number capabilities

Besides its obvious scientific uses, NumPy can also be used as an efficient multi-dimensional container of generic data. Arbitrary data-types can be defined. This allows NumPy to seamlessly and speedily integrate with a wide variety of databases.  

### Matplotlib  
[Matplotlib][] is a Python 2D plotting library which produces publication quality figures in a variety of hardcopy formats and interactive environments across platforms.

### Pandas  
[Pandas][] library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.  

### Scikit-Learn
[Scikit-Learn][] is a Machine Learning library in Python.  
+ Simple and efficient tools for data mining and data analysis
+ Accessible to everybody, and reusable in various contexts
+ Built on NumPy, SciPy, and matplotlib

```
(ML365) jarvis@BRAIN:~$ conda install numpy matplotlib pandas
```

[numpy]:http://www.numpy.org/
[Matplotlib]:https://matplotlib.org/
[Pandas]:https://pandas.pydata.org/
[Scikit-Learn]:http://scikit-learn.org/stable/
[Install Anaconda]:Install%20Anaconda.md
