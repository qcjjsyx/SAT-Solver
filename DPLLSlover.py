from CNF_bak import CNF

# # 创建CNF实例
# filename = "cnf.txt"
# cnf = CNF.readCNFFile(filename)

# print(str(cnf))

class DPLLSolver:
    def __init__(self,cnf):
        self.cnf = cnf
        self.assignments = dict()
        for lit in cnf.variables:
             self.assignments[lit] = None
    
    
    def applyAssignment(self,var,value):
        self.assignments[var] = value
    
    def clearAssignment(self,var):
        self.applyAssignment[var] = None
    
    def solve(self):
        return self.dpll(self.cnf, {})
        # return self.assignments
    
    
    def dpll(self,cnf,assignment):
        # print(str(cnf))
        cnf, assignment = self.preProcess(cnf,assignment)
        print(self.assignments)
        # print(assignment)
        if cnf.isSatisfied():
            return assignment
        
        if cnf.containsEmptyClause():
            return None
        
        var = self.selectVariable(cnf,assignment)
        if var is None:
            return assignment
        new_assignment = assignment.copy()
        new_assignment[var] = True
        self.applyAssignment(var,True)
        result = self.dpll(cnf.applyAssignment({var:True}),new_assignment)
        if result is not None:
            return result
        
        self.clearAssignment(var)###要给回溯的信号
        
        new_assignment = assignment.copy()
        new_assignment[var] = False
        self.applyAssignment(var,False)
        return self.dpll(cnf.applyAssignment({var: False}), new_assignment)

        
    
    def preProcess(self, cnf, assignment):
        while True:
            new_cnf,new_assignment = self.unitPropagate(cnf,assignment)
            newnew_cnf, newnew_assignment = self.pureEliminate(new_cnf,new_assignment)
            
            if(new_cnf==cnf) and (newnew_cnf==new_cnf):
                return newnew_cnf,newnew_assignment
            cnf, assignment = newnew_cnf, newnew_assignment
    
    
    
    
    
    
    
    def unitPropagate(self,cnf,assignment):
        while True:
            unit_clause = cnf.getUnitClauses()
            if not unit_clause:
                return cnf,assignment

            lit = unit_clause[0]
            var = abs(lit)
            value = lit>0
            
            if var in assignment:
                if assignment[var] != value:
                    return CNF([[]]),assignment
                else:
                    cnf = cnf.applyAssignment({var:value})
                    continue
                
            assignment  = assignment.copy()
            assignment[var] = value
            self.applyAssignment(var, value)
            cnf = cnf.applyAssignment({var:value})
            
    def pureEliminate(self,cnf,assignment):
        pure_symbol = cnf.getPureSymbol()
        while pure_symbol:
            var,value = pure_symbol.popitem()
            if var in assignment:
                if value!=assignment[var]:
                    return CNF([[]]), assignment
                else:
                    continue
            assignment = assignment.copy()
            assignment[var] = value
            self.applyAssignment(var, value)
            cnf.applyAssignment({var:value})
            pure_symbol = cnf.getPureSymbol()
            
        return cnf, assignment
    
    def selectVariable(self,cnf,assignment):
        for var in cnf.variables:
            if var not in assignment:
                return var
        