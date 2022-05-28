import src.pymazegen as pymazegen
from src.pymazegen import Algo, Mode


#TODO add pymazegen-to-animation
#TODO add docstrings
#TODO create pymazegen package
#TODO add grid-to-matrix
#TODO add img-to-graph (matrix)
#TODO add solver
#TODO add solver-to-animation

def main():
    pymazegen.init_maze(5, mode=Mode.RECT)
    pymazegen.build_maze(algo=Algo.RECURSIVE_BACKTRACKING, anim=True)
    pymazegen.show_img()
    pymazegen.save_anim("animation")

    pymazegen.build_maze(algo=Algo.ELLER)
    pymazegen.show_img()


if __name__ == '__main__':
    main()
