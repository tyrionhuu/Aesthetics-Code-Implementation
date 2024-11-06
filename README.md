# Aesthetics-Code-Implementation

This repository contains the code implementation of the paper 
_Aesthetics++: Refining Graphic Designs by Exploring Design Principles and Human Preference_
from _IEEE Transactions on Visualization and Computer Graphics_,
you can find the paper [here](https://ieeexplore.ieee.org/document/9714170/?arnumber=9714170).

## How to use

### Prerequisites

This project uses [Poetry](https://python-poetry.org/) for dependency management. You can install it following the instructions [here](https://python-poetry.org/docs/#installation).

Python 3.11 is required to run this project to avoid compatibility issues.

As for the virtual environment, you can use any tool you like.

It is not necessary but totally fine to use [Conda](https://docs.conda.io/en/latest/) to manage the Python environment. You can install it following the instructions [here](https://docs.conda.io/en/latest/miniconda.html).

## Steps

1. Clone this repository

    ``` shell
    git clone git@github.com:tyrionhuu/Aesthetics-Code-Implementation.git
    cd Aesthetics-Code-Implementation
    ```

2. Create virtual environment

   1. **conda**
   
    ``` shell
    conda create -n aesthetic_implementation python=3.11
    conda activate aesthetic_implementation
    ```
   
   2. **poetry**
   
    ``` shell
    poetry env use python3.11
    poetry shell
    ```
   
3. Install the dependencies with Poetry

    ``` shell
    poetry install
    ```

    Then Poetry should already activate the virtual environment for you. If not, you can activate it manually.

4. Install the pre-commit hooks, which you don't have to do.

    ``` shell
    pre-commit install
    ```

## Note

Due to all kinds of reasons, the implementation of the paper won't be one hundred percent the same as the paper.
