from copy import deepcopy
import argparse

try:
    import pygame
except Exception:
    pygame = None

class tableau:
    def __init__(self, longueur, largeur, grille):
        self.longueur = int(longueur)
        self.largeur = int(largeur)
        self.grille = grille

    def voisins_vivants(self, x, y):
        count=0
        dirs=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dir in dirs:
            dx,dy=dir
            x1=x+dx
            y1=y+dy
            if 0<=x1<self.longueur and 0<=y1<self.largeur:
                count+=self.grille[x1][y1]
        return count

    def nextframe(self):
        next=deepcopy(self.grille)
        for x in range(self.longueur):
            for y in range(self.largeur):
                if self.voisins_vivants(x,y)<2:
                    next[x][y]=0
                elif self.voisins_vivants(x,y)>3:
                    next[x][y]=0
                elif self.voisins_vivants(x,y)==3:
                    next[x][y]=1
        self.grille=next      

    @classmethod
    def from_file(cls, path: str):
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        if not lines:
            raise ValueError("Input file is empty")
        longueur = len(lines)
        largeur = len(lines[0])
        grille = [[int(ch) for ch in line] for line in lines]
        return cls(longueur, largeur, grille)
    
def run_pygame(jeu, steps, cell_size=8, fps=10):
    """Run a simple pygame visualization for the game of life.

    `jeu` is a `tableau` instance. `steps` is number of simulation steps to show.
    """
    if pygame is None:
        raise RuntimeError("pygame is not importable in this Python interpreter. Install it into the environment you use to run the script, e.g. `python -m pip install pygame` or `conda install -c conda-forge pygame`.")
    pygame.init()
    width_px = jeu.largeur * cell_size
    height_px = jeu.longueur * cell_size
    screen = pygame.display.set_mode((width_px, height_px))
    clock = pygame.time.Clock()
    running = True
    step = 0
    while running and (step < steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        # draw
        screen.fill((0, 0, 0))
        for x in range(jeu.longueur):
            for y in range(jeu.largeur):
                if jeu.grille[x][y]:
                    rect = pygame.Rect(y * cell_size, x * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, (255, 255, 255), rect)
        pygame.display.flip()
        clock.tick(fps)
        jeu.nextframe()
        step += 1
    pygame.quit()
    
def parse_args():
            # Définit et retourne les arguments de ligne de commande.
    parser = argparse.ArgumentParser(description="Simule le Game of Life à partir d'un fichier texte.")
    parser.add_argument("--input", "-i", required=True, help="Conditions initiales (fichier)")
    parser.add_argument("--output", "-o", required=True, help="Fichier de sortie, état final")
    parser.add_argument("--steps", "-m", required=True, type=int, help="Nombre d'étapes à simuler")
    parser.add_argument("--display", "-d", action="store_true", help="Afficher l'évolution avec pygame")
    parser.add_argument("--fps", type=int, default=10, help="Images par seconde pour l'animation")
    parser.add_argument("--cell-size", type=int, default=8, help="Taille d'une cellule en pixels")
    parser.add_argument("--width", help="Largeur de l'écran (optionnel)")
    parser.add_argument("--height", help="Hauteur de l'écran (optionnel)")
    return parser.parse_args()
    

if __name__ == "__main__":
    args = parse_args()
    jeu = tableau.from_file(args.input)
    if args.display:
        # Show GUI and simulate for `steps` frames
        run_pygame(jeu, args.steps, cell_size=args.cell_size, fps=args.fps)
    else:
        for _ in range(args.steps):
            jeu.nextframe()
    with open(args.output, "w", encoding="utf-8") as f:
        for row in jeu.grille:
            f.write("".join(str(r) for r in row) + "\n")


