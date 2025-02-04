from CNF import CNF
from Slover import Solver

cnf = CNF([[1, -2], [-1, 3], [2, -3]])


solver = Solver(cnf)


solution = solver.solve()

if solution:
    print(solution)
else:
    print("No")

