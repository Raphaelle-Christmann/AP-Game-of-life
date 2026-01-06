# Création d'un jeu de la vie en python

# Grille d'entrée : fichier.txt composée d'une grille de 0 et 1 de la forme :
# 0001000
# 0011100
# 0000000
# Par exemple.

import argparse

class frame:
    def __init__(self, width,height,grid):
        self.width = width
        self.height = height
        self.grid = grid


    def next_cell(self,x,y):
        dirs = [(-1,-1),(0,-1),(1,-1),(1,0),(1,-1),(0,1),(-1,1),(-1,0)]
        count = 0
        for dx,dy in dirs:
            x1,y1 = x+dx,y+dy
            if 0 <= x1 < self.width and 0 <= y1 < self.height:
                count += self.grid[y1][x1]
            else:
                continue
        if self.grid[x][y]==1:
            if count < 2 or count > 3:
                return 0
            else :
                return 1
        else :
            if count == 3:
                return 1
            else:
                return 0
    
    def next_frame(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            for y in range(self.height):
                new_grid[x][y] = self.next_cell(x,y)
        self.grid = new_grid

def from_file(filename):
    # forme d'entrée acceptée : la grille d'entrée sous la forme de 0 pour case morte, 1 pour case vivante, tous collés.
    # La hauteur et la largeur sont donc implicites.
    # retourne la frame du fichier file.
    with open(filename,'r') as g:
        lines = g.readlines()
    grid = []
    for line in lines:
        row = [int(char) for char in line.strip() if char in '01']
        grid.append(row)
    return frame(len(grid[0]), len(grid), grid)


def parse_args():
    parser = argparse.ArgumentParser('Mise en place du jeu de la vie pour une grille d\'entrée et un nombre d\'itération donnés.')
    parser.add_argument("--input","-i", type = str, required = True, help = "Fichier contenant la grille initiale du jeu : une ligne de la grille de 0 et 1 par ligne, sans espaces.")
    parser.add_argument("--output", "o", type = str, required = True, help = "Fichier où est stockée la grille après la dernière itération.")
    parser.add_argument("--iterations","-m", type = int, required = True, help = "Nombre d'itération souhaitées, entier supérieur ou égal à 0.")
    return parser.parse_arg()

if __name__ == "__main__":
    args = parse_args()
    f = from_file(args.input)
    for _ in range(args.iterations):
        f.next_frame()
    with open(args.output, 'w') as res:
        for row in f.grid:
            res.write(''.join(str(cell) for cell in row) + '\n')           