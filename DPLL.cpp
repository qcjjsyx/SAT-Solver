#include <cstdio>
#include <vector>
#include <iostream>
#include <string>
#include <list>
#include <set>
#include <algorithm>
using namespace  std;



typedef long long ll;
typedef unsigned long long ull;


enum Status{
    satisfied,
    unsatisfied,
    undetermined
};


class Literal {
public:
    int value;//编号
    bool isTrue;//真值 ture表示正文字，false表示负文字
    Literal(int value,bool isTrue):value(value),isTrue(isTrue){}
    Literal getOpposite(){ //取反
        return Literal(value,!isTrue);
    }
};


class Clause{
public:
    list<Literal> literals;


    void addLiteral(const Literal& literal){
        literals.push_back(literal);
    }

    void removeLiteral(int value){
        for(auto it = literals.begin();it!=literals.end();it++){
            if(it->value==value){
                literals.erase(it);
                break;
            }
        }
    }
    
    bool isEmpty(){
        return literals.empty();
    }

    bool isUnitClause(){
        return literals.size()==1;
    }

    void printClause(){
        for (auto& literal : literals) {
            if (literal.isTrue) {
                std::cout << literal.value;
            } else {
                std::cout << "-" << literal.value;
            }
            if (&literal != &literals.back()) {
                std::cout << " v ";
            }
        }
    }
    

};


class CNF{
public:
    list<Clause> clauses;
    vector<int> assignment; //赋值 -1，表示为赋值，0表示false，1表示true
    int n;//变元个数


    void addClause(const Clause& clause){
        clauses.push_back(clause);
    }

    // void removeClause(){
    //    clauses.erase()
    // }


    //变量赋值
    void assign(int var,bool value){
        assignment[var]=value?1:0;
    }

    //取消变量赋值
    void unassign(int var){
        assignment[var]=-1;
    }

    // 初始化CNF
    //可以增加 若单个语句中同时有a和非a的情况，不把语句加入进去，相当于一个预处理
    void initCNF(){
        cout<<"clauseNum: ";
        int clauseNum;
        cin>>clauseNum;
        cout<<"varNum: ";
        cin>>n;
        assignment.resize(n+1,-1);//从1开始编号
        //cout<<clauseNum<<n<<endl;
        for(int i=0;i<clauseNum;i++){
            Clause clause;
            cout<<"clause "<<i+1<<": ";
            while(true){
                int literal;
                cin>>literal;
                if(literal==0) break;
                if(literal>0){
                    clause.addLiteral(Literal(literal,true));
                }else{
                    clause.addLiteral(Literal(-literal,false));
                }
            }
            addClause(clause);
        }
    }


    void printCNF(){
        cout<<"CNF:"<<endl;
        for(auto& clause:clauses){
            clause.printClause();
            cout<<endl;
        }
    }


    //单子句传播
    int uintPropagate(){
        set<int> unitClauses;
        for(auto it = clauses.begin();it!=clauses.end();++it){
            Clause clause  = *it;
            if(clause.isUnitClause()){
                Literal literal=clause.literals.front();
                if(assignment[literal.value]==-1){
                    assign(literal.value,literal.isTrue);
                    unitClauses.insert(literal.value);
                }else{// 有类似 a 和 -a的单子句直接给出冲突
                    int pre_assign = assignment[literal.value];
                    int now_assign = literal.isTrue?1:0;
                    if(pre_assign!=now_assign){
                        cout<<"conflict"<<endl;
                        return Status::unsatisfied;
                    }
                }   
            }
        }
        
        for(auto it = clauses.begin();it!=clauses.end();it++){
            Clause& clause = *it;
            if(clause.isUnitClause()){clauses.erase(it--);continue;}//删除单子句
            //list<Literal> literals = clause.literals;
            for(auto it1 = clause.literals.begin();it1!=clause.literals.end();it1++){
                Literal& literal = *it1;
                if(unitClauses.find(literal.value)!=unitClauses.end()){
                    int assign_value = assignment[literal.value];
                    if(assign_value==1&&literal.isTrue||assign_value==0&&!literal.isTrue){
                        clauses.erase(it--);
                        break;
                    }else{
                        cout<<"delete literal"<<endl;
                        clause.literals.erase(it1--);
                        cout<<"end"<<endl;
                    }

                }
            }
        }
       
        return Status::undetermined;
    }



};



int main(int argc, char const *argv[])
{
    CNF formula;
    formula.initCNF();
    formula.printCNF();
    int first = formula.uintPropagate();
    formula.printCNF();
    return 0;
}
