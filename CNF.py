class Clause:
    def __init__(self,c:list) -> None:
        self.lits = c
        self.state = None
    
    
    def __repr__(self):
        return f'[Clause {self.lits} ' + f'state={self.state}]'
    def __eq__(self, o):
        if hasattr(o, 'clause'):
            return self.lits == o.lits
        else:
            return False
        
    def __len__(self):
        return len(self.lits)


      
class CNF:
    def __init__(self,clauses) -> None:
        self.clauses = []
        for clause in clauses:
            self.clauses.append(Clause(clause))
    
    @property
    def variables(self):
        return {abs(lit) for clause in self.clauses for lit in clause}
    
    def getUnitClauses(self):
        return [clause for clause in self.clauses if len(clause) == 1]
    
    
    def __repr__(self):
        return f"CNF({self.clauses})"

    def __eq__(self, other):
        return self.clauses == other.clauses

    def __len__(self):
        return len(self.clauses)
    
    
    



# cnf =  CNF([[1, 2], [3], [-2, -3], [-5], [-4, 5]])
# print(cnf.getUnitClauses())