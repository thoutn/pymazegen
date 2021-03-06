# pymazegen

A maze generator written in Python 3.9. The package implements several algorithms 
to generate rectangular or circular mazes. It also includes a feature to visualise 
the generated maze, or to animate the build steps and return the animation in a 
`.gif` document. 

To see the older version of this project, which contains some experimentation with 
implementation choices and optimisation, go 
[here](https://github.com/thoutn/archive_pymazegen). 

## Folder structure

The project follows a standard folder structure:
- `exemples/` contains a file with examples on how to use the package. 
- `src/` contains the source code, the main package. 
The `pymazegen` package has several subpackages:
  - `algos/` contains all the implemented maze generation algorithms. 
  Each algorithm is contained in its own module. 
  - `maze/` contains the classes that are used to represent the maze - `Cell` and `Grid` 
  for generating rectangular mazes, and `CirCell` and `CircGrid` for circular mazes 
  represented in polar coordinates. 
  - `presenter/` contains the main methods to visualise the generated mazes. 
  - `misc/` contains some additional and useful code, not related to but used in the project. 
- `tests/` is the folder for unit or integration tests. 

## How to install and run the project

### Installation

To run the project, first download it from this repo. 

> **Note** *Before installing the package, the recommended way is to set up a virtual 
> environment to avoid system pollution. If you are not familiar with the python virtual 
> environment, you can learn more about it for example at [RealPython][A].*

[A]: (https://realpython.com/python-virtual-environments-a-primer/)

You will find a `setup.py` file in the root folder. To install the package, 
run the following command in terminal:

```
python setup.py install
```

This should install the following dependencies - external libraries: 
- `numpy`
- `pillow`

### Overview

The project implements several algorithms to generate mazes. There are seven functions, 
which enable to fine tune the way the code generates mazes.
- `init_maze` is used to initialise the maze geometry - size and shape 
    (`Mode.RECT` or `Mode.CIRC`). 
- `build_maze` generates a random maze using one of the selected algorithms.
    If parameter `anim` is set to `true` the builder logs the build steps. 
- `get_maze` returns the maze in its raw format => a python object representing the 
    maze internally in the `pymazegen` package.
- `img_config` configures the graphical representation of the generated maze.
    Available parameters of the function are:
  - `cell_size` – the height of the cell used for the maze visualisation;
  - `wall_thickness` – the line thickness the wall is drawn with.
- `show_img` renders the generated image of the maze in a pop-up window.
- `save_img` saves the generated image of the maze. It has one parameter, which is the
    filename without the file extension (.png by default). 
- `save_anim` renders and saves an animation of the building process of the maze. 
    Creates a visual representation of the selected mazegen algorithm. 
    It has two parameters:
  - `filename` – the name of the file without extension (.gif by default) 
      the generated animation is saved to; 
  - `mspf` – milliseconds per frame; the duration of one animation frame in milliseconds.

> **Note** *The method to animate the build steps is not yet fully implemented. 
> Currently, it works only for the **recursive backtracker** algorithm.*

## How to use the project

### The basics

The simplest way to generate a maze is to run the following code
```
import pymazegen
pymazegen.build_maze()
```

This will create a `20x20` square maze using the default algorithm, which is the 
`RECURSIVE_BACKTRACKING`. 

Once you have the maze, you can use the function below to show it as an image. 
```
pymazegen.show_img()
```

### Adjusting size

If you want to change the grid size of the maze, you can do it as follows
```
pymazegen.init_maze(10, 10)
pymazegen.build_maze()
```

For a square maze, you don't have to specify both the width and height of the maze. 

You can also change the size of the passages and walls, thus adjust the way the 
maze is rendered. By default, the maze is rendered with thin walls. However, you can 
change this to create a maze with passages and walls having the same size. 
You can do this by calling function `img_config`. 
```
pymazegen.img_config(cell_size=20, wall_thickness=20)
```

### Beyond the default algo

In case you would like to change the algorithm, the code is using to generate the maze, 
you need to import the `Algo` class. You can then change the default algorithm to 
any from this list: 
`BINARY_TREE`,
`SIDEWINDER`,
`RECURSIVE_BACKTRACKING`,
`PRIM`,
`KRUSKAL`,
`ELLER`,
`HUNT_AND_KILL`,
`ALDOUS_BRODER`,
`WILSON`,
`RECURSIVE_DIVISION`,
`GROWING_TREE`(*not yet implemented*).

For example, to change the builder algorithm to `SIDEWINDER` you can do it like this
```
from pymazegen import Algo
pymazegen.init_maze(10)
pymazegen.build_maze(algo=Algo.SIDEWINDER)
```

### Rectangular and what more...?
Rectangular shape is only one of the two geometries the code can work with. 
It is able to generate circular mazes too. For this, you will need to import the 
`Mode` class and change the maze geometry. Below is an example of creating a circular
maze with a height (radius) of 15. 
```
from pymazegen import Mode
pymazegen.init_maze(10, mode=Mode.CIRC)
pymazegen.build_maze(algo=Algo.SIDEWINDER)
```

> **Note** *Circular mazes take only one 'size' argument, which is the radius of 
> the maze. The number of cells in a row (at a given radius) is calculated such 
> that each cell has a similar width to its height.*  

### Animate it

You can also save the animation of the maze building steps. For example, the below 
code saves the visualisation of the Backtracking algorithm to the `anim1.gif` file. 
```
pymazegen.build_maze(algo=Algo.RECURSIVE_BACKTRACKING, anim=True)
pymazegen.save_anim("anim1")
```

### Other

Folder `examples/` contains a file `example_builder.py`, which provides further examples 
on how to use the main functions of the module. 

## Credits

The initial inspiration for this project came from a Diploma thesis, which 
aims to study human problem-solving by analysing strategies in maze solving [[1]](#1). 
The thesis references various useful sources. One notable is Walter Pullen's 
site [[2]](#2).

Another influential reading was Jamis Buck's blog posts on mazes [[3]](#3). 
His Ruby implementation [[4]](#4) of the `Cell` and `Grid` classes is rewritten in
Python and used in this project.  

## References

<a id="1">[1]</a> 
Foltin, M.
*Automated Maze Generation and Human Interaction*. 2011. 
Diploma thesis. 
Masaryk university. Faculty of Informatics.

<a id="2">[2]</a>
Pullen, W. 
*Maze algorithms* \[online\].
Available [here](http://www.astrolog.org/labyrnth/algrithm.htm). 

<a id="3">[3]</a>
Buck, J. 
*Maze Generation: ...* \[online\]. 
Available [here](http://weblog.jamisbuck.org/archives.html).

<a id="4">[4]</a>
Buck, J. 
*Mazes for Programmers*. 
The Pragmatic Bookshelf. 2015. 
ISBN 9781680500554 (in print). 
Available [here](https://pragprog.com/titles/jbmaze/mazes-for-programmers/). 


## Licence

[MIT License](LICENSE)