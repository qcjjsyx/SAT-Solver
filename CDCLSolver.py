from sympy import Symbol
from sympy.logic.boolalg import Not
from typing import *
from copy import deepcopy

from tornado.autoreload import watch

from CNF import Clause, CNF





class Node:
    def __init__(self,lit,decisionL,reason):
        self.lit = lit
        self.level = decisionL
        self.reason = reason
            
    def __repr__(self):
        return f'<({self.level}) {self.lit} {self.reason}>'
    def __eq__(self, o):
        return self.lit == o.lit and self.level == o.level and self.reason == o.reason
    def __hash__(self):
        return hash((self.lit, self.level))



class DecisionLevel:
    
    def __init__(self,decisionL) -> None:
        self.level = decisionL
        self.nodes = []
    def __repr__(self) -> str:
          return str(self.nodes)
    



class Trail:
    def __init__(self) -> None:
        self.levels = [DecisionLevel(0)]
        
    def addLevel(self,level):
        self.levels.append(DecisionLevel(level))
    
    def addNodeToCurLevel(self, lit,reason):
        self.levels[-1].nodes.append(Node(lit,self.levels[-1].level,reason))
    
    def __repr__(self) -> str:
        return str(self.levels)
    



class CDCLSolver:
    def __init__(self, clauses):
        # CDCLSolver的构造函数
        self.cnf = []
        self.trail = Trail() # 迹
        self.assignments = dict() # 当前赋值
        self.var_assignments = dict()
        self.watch_list_lit_to_clause = dict()
        self.watch_list_clause_to_lit = dict()
        i=0
        for clause in clauses:
            self.cnf.append(Clause(clause,i))
            i+=1
            for lit in clause:
                if lit not in self.assignments and -lit not in self.assignments:
                    self.assignments[lit] = None

        self.initWatchList()
#######################################################################################
    def slove(self):
        self.CDCL()
#######################################################################################
    def initWatchList(self):
        self.watch_list_lit_to_clause.clear()
        for clause in self.cnf:
            if len(clause)>=2:
                lit1 = clause.lits[0]
                lit2 = clause.lits[-1]

                self.addToWatchList(lit1,clause)
                self.addToWatchList(lit2,clause)
#######################################################################################
    def addToWatchList(self,clause,lit):
        if lit not in self.watch_list_lit_to_clause:
            self.watch_list_lit_to_clause[lit] = []
            self.watch_list_lit_to_clause[lit].append(clause)
        if clause not in self.watch_list_clause_to_lit:
            self.watch_list_clause_to_lit[clause] = []
            self.watch_list_clause_to_lit[clause].append(clause)
#######################################################################################
    def removeFromWatchList(self,clause,lit):
        if clause in self.watch_list_lit_to_clause[lit]:
            self.watch_list_lit_to_clause[lit].remove(clause)
        if lit in self.watch_list_clause_to_lit[clause]:
            self.watch_list_clause_to_lit[clause].remove(lit)
########################################################################################
    def updateClauseState_new(self, clause):
        if len(self.watch_list_clause_to_lit[clause]) == 2:
            clause.state = None
        if len(self.watch_list_clause_to_lit[clause]) == 1:
            clause.state = True  ###实际上应该是implied
        if len(self.watch_list_clause_to_lit[clause]) == 0:
            clause.state = False


    def updateWatchList(self,lit):##lit为假的时候需要更新
        if lit in self.watch_list_lit_to_clause:
            for clause in self.watch_list_lit_to_clause[lit]:
                self.watch_list_clause_to_lit[clause].remove(lit)
                new_lit = None
                for other_lit in clause.lits:
                    if other_lit==lit:
                        continue
                    if self.assignments[other_lit] is None:
                        new_lit = other_lit
                        break

                if new_lit is not None:
                    self.watch_list_lit_to_clause[new_lit].append(clause)
                    self.watch_list_clause_to_lit[clause].append(new_lit)
                self.updateClauseState_new(clause)
            self.watch_list_lit_to_clause[lit].clear()



########################################################################################
    def getFinalAssign(self):
        for lit, value in self.assignments.items():
            if abs(lit) not in self.var_assignments:
                if lit<0:
                    self.var_assignments[abs(lit)] = not value
                else:
                    self.var_assignments[abs(lit)] = value
#########################################################################################          
    def getValue(self, lit):
        # 获取文字l的赋值
        if lit in self.assignments:
            return self.assignments[lit]
        if -lit in self.assignments:
            r = self.assignments[-lit]
            if r is None:
                return None
            else:
                return not r

#############################################################################################  
    def setValue(self,lit):
        if lit in self.assignments:
            self.assignments[lit] = True
        if -lit in self.assignments:
            self.assignments[-lit] = False
#############################################################################################            
    def cleanValue(self,lit):
        if lit in self.assignments:
            self.assignments[lit] = None
        if -lit in self.assignments:
            self.assignments[-lit] = None
            
#############################################################################################            
    def getUnitClause(self):
        for clause in self.cnf:
            unassign_num = 0
            false_num = 0
            true_num = 0
            unassign_lit = None
            for lit in clause.lits:
                value = self.getValue(lit)

                if value==False:
                    false_num += 1
                elif value==None:
                    unassign_lit = lit
                    unassign_num += 1
                
            if unassign_num==1 and false_num == len(clause)-1:
                return unassign_lit, clause
        return None, None


    def getUnitClause_new(self):
        for clause in self.cnf:
            if len(self.watch_list_clause_to_lit[clause])==1:
                return self.watch_list_clause_to_lit[clause][0], clause
        return None, None
##########################################################################################
    def updateClauseState(self):
        for clause in self.cnf:
            true_num = 0
            false_num = 0
            for lit in clause.lits:
                r = self.getValue(lit)
                if r==True:
                    true_num += 1
                elif r==False:
                    false_num += 1
            if true_num>=1:
                clause.state = True
            elif false_num==len(clause):
                clause.state = False
            else:
                clause.state = None


################################################################################    
    def litPropagete(self, lit, clause):
        self.setValue(lit)
        self.updateClauseState()
        self.trail.addNodeToCurLevel(lit,clause)

    def litPropagate_new(self, lit, clause):
        self.setValue(lit)
        self.updateWatchList(-lit)
        self.trail.addNodeToCurLevel(lit,clause)
###############################################################################
    def unitPropagate(self):
        lit = None
        while True:
            lit,clause = self.getUnitClause()
            if lit==None:
                break
            # self.litPropagete(lit,clause)
            self.litPropagate_new(lit,clause)
###################################################################################
    def selectLit(self):
        for lit, value in self.assignments.items():
            if value==None:
                return lit
        return None
##################################################################################
    def detectConflict(self):
        for clause in self.cnf:
            if clause.state==False:
                return clause
        return None
##################################################################################
    def clauseLearning(self,conflict_clause):
        latest_level_nodes = self.trail.levels[-1].nodes
        can_be_UIP = dict()
        for node in latest_level_nodes:
            can_be_UIP[node] = True
    
        conflict_node = Node(Node, self.trail.levels[-1].level, conflict_clause)
        end_level_nodes = latest_level_nodes+[conflict_node]
        V = set() ###建图
        for level in self.trail.levels:
            for node in level.nodes:
                V.add(node)
        V.add(conflict_node)
    
        adj_list = dict()
        for node in end_level_nodes:
            adj_list[node] = []
    
    
        lit_to_node = dict()
        for node in V:
            lit_to_node[node.lit] = node
    
        end_level_lit = set()
        for node in end_level_nodes:
            end_level_nodes.add(node.lit)
    
        for node in end_level_nodes:##构造邻接表
            rs = node.reason
            if rs!=None:
                for lit in rs.lits:
                    if lit != node.lit and -lit in end_level_lit:
                        from_node = lit_to_node[-lit]
                        adj_list[from_node].append(node)
                 

        i = iter(end_level_nodes)
        for from_node in end_level_nodes:
            next(i)
            for to_node in adj_list[from_node]:
                j = deepcopy(i)
                while True:
                    try:
                        k = next(j)
                    except StopIteration:
                        break
                    if k==to_node:
                        break
                    can_be_UIP[k] = False
    
        UIP = None
        for node in reversed(latest_level_nodes):
            if can_be_UIP[node]:
                UIP = node
                break
    
        can_reach_conflict_node = set()
        Q = [conflict_node]
        while len(Q)>0:
            front = Q[0]
            can_reach_conflict_node.add(front)
            del Q[0]
            rs = front.reason
            if rs is not None:
                for lit in rs.lits:
                    if lit != front.lit and -lit in end_level_lit:
                        node = lit_to_node[-lit]
                        Q.append(node)
    
            successor_of_UIP = set() # 唯一蕴含点的所有后继
            Q = [UIP] # 仍然广度优先搜索进行计算
            while len(Q) > 0:
                front = Q[0]
                del Q[0]
                for node in adj_list[front]:
                    successor_of_UIP.add(node)
                    Q.append(node)       

            B = can_reach_conflict_node.intersection(successor_of_UIP)
            A = V-B
        
            R = set()
        
            entire_adj_list = dict()
            for node in V:
                entire_adj_list[node] = []
            for node in V:
                rs = node.reason
                if rs is not None:
                    for lit in rs.lits:
                        if lit!=node.lit:
                            from_node = lit_to_node[-lit]
                            entire_adj_list[from_node].append(node)
        
            for node in A: # 找出R中的元素
                for to in entire_adj_list[node]:
                    if to in B:
                        R.add(node)
                        break
            new_clause = []
            for node in R:
                new_clause.append(-node.lit)
            learned_clause = Clause(new_clause,len(self.cnf))
            # for lit in new_clause:
            #     if l
            self.cnf.append(learned_clause)
        
            R_levels = sorted(list(set([node.level for node in R])))
            # R的元素的决策层集合
            backtrack_level = 0
            if len(R_levels) > 1:
                backtrack_level = R_levels[-2] # 第二大
            return learned_clause, backtrack_level
        
################################################################################################   
    def backtrack(self,  level: int, learned_clause): # 回溯到第level层
        lit1 = None
        while self.trail.levels[-1].level > level: # 考察在第level层之后的层
            for node in self.trail.levels[-1].nodes:
                lit1 = node.lit
                self.cleanValue(node.lit) # 文字重新退回到未赋值状态
            self.trail.levels.pop() # 从迹中删除该层
        self.updateClauseState() # 更新子句的值
        # self.litPropagete(lit1, learned_clause)
############################################################################################
    def CDCL(self):
        decision_level = 0
        while True:
            self.unitPropagate()
            conflict_clause = self.detectConflict()
            if conflict_clause is not None:
                if decision_level == 0:
                    return False
                else:
                    learned_clause, back_level = self.clauseLearning(conflict_clause)
                    self.backtrack(back_level,learned_clause)
                    decision_level = back_level
            else:
                lit = self.selectLit()
                if lit == None:
                    self.getFinalAssign()
                    print(self.var_assignments)
                    return True
                else:
                    decision_level += 1 # 开始一个新的决策层
                    self.trail.addLevel(decision_level)
                    self.litPropagete(lit, None)
   

    
    



#######################################################################3
cnf = [[1,-2,3], [-1,2], [3,-4,5], [-5,4]]

solver = CDCLSolver(cnf)
# print(solver.watch_list)
print(solver.CDCL())
# print(solver.assignments)

# solver.setValue(5)
# print(solver.assignments)

# solver.cleanValue(5)
# print(solver.assignments)


# 1 -2 3 0
# -1 2 0
# 3 -4 5 0
# -5 4 0
##############