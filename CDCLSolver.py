from collections import defaultdict
from Slover import Solver
from copy import deepcopy

## 

class CDCLSlover(Solver):
    
    def __init__(self, cnf):
        super().__init__(cnf)
        self.decision_level = 0
        self.var_info = {}
        
        self.decision_stack = []         # 决策栈 [(var, level)]
        self.learned_clauses = []        # 学习的冲突子句
        self.watch_list = defaultdict(list)  # 监视文字索引（可选优化）
        
        
        
    def assignVariable(self,var,value,antecedent):
        self.var_info[var] = (value,self.decision_level,antecedent)
        
        
    def unitPropagate(self):
        while True:
            new_uints = []
            for clause in self.cnf.clauses+self.learned_clauses:
                unassigned = []
                clause_satisfied = False