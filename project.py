# Being used on https://pysathq.github.io/ on "Try PySAT" section
# First block "default code on url above"

from pysat.formula import CNF
from pysat.solvers import Solver

# Second Block

from pysat.solvers import Glucose3

# Third Block

def var(r, s, i, j, k):
    return (r * s * k) + (s * i) + j + 1

# Fourth Block

def add_clauses(solver, r, s, mapa):
    # Regra 1: Para cada quadrado com atacante, pelo menos uma torre que pode eliminá-lo deve de fato eliminá-lo
    for i in range(r):
        for j in range(s):
            if mapa[i][j] == 'n':
                clause = []
                for k in range(4):
                    clause.append(var(r, s, i, j, k))
                solver.add_clause(clause)

    # Regra 2: Para cada torre, não podemos permitir que as torres que podem destruí-la de fato a destruam
    for i in range(r):
        for j in range(s):
            if mapa[i][j] == 'T':
                for k in range(4):
                    clause = []
                    for l in range(4):
                        if l != k:
                            clause.append(-var(r, s, i, j, l))
                    solver.add_clause(clause)

# Fifth Block

def solve_defesa_com_torres(r, s, mapa):
    solver = Glucose3()

    # Adicionar cláusulas ao solver
    add_clauses(solver, r, s, mapa)

    # Verificar a satisfatibilidade
    if solver.solve():
        model = solver.get_model()
        # Extrair as orientações dos canhões a partir da valoração verdadeira
        orientacoes = [['.' for _ in range(s)] for _ in range(r)]
        for i in range(r):
            for j in range(s):
                if mapa[i][j] == 'T':
                    for k in range(4):
                        if model[var(r, s, i, j, k) - 1] > 0:
                            if k == 0:
                                orientacoes[i][j] = '1'
                            elif k == 1:
                                orientacoes[i][j] = '2'
                            elif k == 2:
                                orientacoes[i][j] = '3'
                            elif k == 3:
                                orientacoes[i][j] = '4'
        return orientacoes
    else:
        return None

# Sixth Block

r, s = 5, 9
mapa = [
    ".n..T..n.",
    ".T..n....",
    ".n..#..n.",
    "....n..T.",
    ".n..T..n."
]

solucao = solve_defesa_com_torres(r, s, mapa)
if solucao is not None:
    for linha in solucao:
        print(''.join(linha))
else:
    print("Não há solução.")