from CNF import CNF
from Slover import Solver


cnf =  CNF([[1, 2], [-1, 3], [-2, -3], [4, -5], [-4, 5]])
# print(str(cnf))

solver = Solver(cnf)


solution = solver.solve()

if solution:
    print(solution)
else:
    print("No")

