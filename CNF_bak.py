
class CNF:
    def __init__(self,clauses=None):
        self.clauses = []
        if(clauses):
            for clause in clauses:
                self.addClause(clause)
                
    def addClause(self, literals):
        unique_literals = list({literal for literal in literals})
        self.clauses.append(sorted(unique_literals,key=abs))
        
    @property
    def variables(self):
        return {abs(lit) for clause in self.clauses for lit in clause}
    
    @classmethod
    def readCNFFile(cls,filename):
        clauses = []
        with open(filename,'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('p') or not line:
                    continue
                literals = list(map(int, line.split()[:-1]))  # 排除结尾的0
                clauses.append(literals)
            
        return cls(clauses)    
    
    
    ## assignments 的格式是字典
    def applyAssignment(self, assignments):
        new_clauses = []
        for clause in self.clauses:
            new_clause = []
            clause_satisfied = False
            for lit in clause:
                var = abs(lit)
                if var in assignments:
                    if(lit>0 and assignments[var]==1) or (lit<0 and assignments[var]==0):
                        clause_satisfied = True
                        break
                else:
                    new_clause.append(lit)
                        
            if not clause_satisfied:
                new_clauses.append(new_clause)
                    
        return CNF(new_clauses)
    
    
    
    def containsEmptyClause(self):
        return any(len(clause) == 0 for clause in self.clauses)
    
    def isSatisfied(self):
        return len(self.clauses)==0
    
    def getUnitClauses(self):
        return [clause[0] for clause in self.clauses if len(clause) == 1]
    
    def getPureSymbol(self):
        literal_signs = {}
        for clause in self.clauses:
            for lit in clause:
                var = abs(lit)
                if var not in literal_signs:
                    literal_signs[var] = set()
                literal_signs[var].add(lit>0)
                    
        
        pure_symbol = {}
        for var,signs in literal_signs.items():
            if len(signs)==1:
                pure_symbol[var] = signs.pop()
        
        return pure_symbol 
    
    
    def __str__(self):
        """字符串表示"""
        return " ^ ".join(f"({ ' V '.join(map(str,clause)) })" for clause in self.clauses)

    def __repr__(self):
        return f"CNF({self.clauses})"

    def __eq__(self, other):
        return self.clauses == other.clauses

    def __len__(self):
        return len(self.clauses)