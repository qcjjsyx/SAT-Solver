from CNF import CNF
from Slover import Solver

filename = "cnf.txt"
cnf = CNF.readCNFFile(filename)
print(str(cnf))

solver = Solver(cnf)


solution = solver.solve()

if solution:
    print(solution)
else:
    print("No")

