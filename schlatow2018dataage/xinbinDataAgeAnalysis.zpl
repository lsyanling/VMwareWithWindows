
# U[i, j]表示第i个任务和第j个任务在相同处理器，且第i个任务的优先级更高
var U[Tasks_X_Tasks];

# 
subto Constraint_5_12:
    forall <Task_i> in Tasks:
        forall <Task_j> in Tasks - { Task_i }:
            U[Task_i, Task_j] >= 1 - (2 - V[Task_i, Task_j] - Q[Task_i, Task_j]);

#
subto Constraint_5_13:
    forall <Task_i> in Tasks:
        forall <Task_j> in Tasks - { Task_i }:
            U[Task_i, Task_j] + U[Task_j, Task_i] <= V[Task_i, Task_j];

var MaxDataAge[Chains];

# Max Data Age
subto Constraint_5_16:
    forall <Chain_i> in Chains:
        MaxDataAge[Chain_i] = sum deta