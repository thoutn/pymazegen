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
    # easiest way to generate a maze
    pymazegen.build_maze()
    pymazegen.show_img()

    # generates a 5x5 square maze
    pymazegen.init_maze(5, mode=Mode.RECT)
    pymazegen.build_maze(algo=Algo.RECURSIVE_BACKTRACKING, anim=True)
    pymazegen.show_img()
    pymazegen.save_anim("animation")    # saves the animation into a gif file

    # rewrites the maze using a different algorithm
    pymazegen.build_maze(algo=Algo.ELLER)
    pymazegen.show_img()

    # changes the default img settings - wall and passage at same size
    pymazegen.img_config(cell_size=20, wall_thickness=20)
    pymazegen.show_img()

    # generates a circular maze
    pymazegen.init_maze(10, mode=Mode.CIRC)
    pymazegen.build_maze(algo=Algo.KRUSKAL)
    pymazegen.img_config()  # resets the img settings to default
    pymazegen.show_img()

if __name__ == '__main__':
    main()
