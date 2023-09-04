
# U[i, j]表示第i个任务和第j个任务在相同处理器，且第i个任务的优先级更高
var U[Tasks_X_Tasks] binary;

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

set Chains_X_Tasks_X_Tasks = Chains cross Tasks_X_Tasks;
var deta[Chains_X_Tasks_X_Tasks] >= 0;
var MaxDataAge[Chains];

# Max Data Age
subto Constraint_5_16:
    forall <Chain_i> in Chains:
        MaxDataAge[Chain_i] = (sum <Chain_i, Chain_i_Task_i, Chain_i_Task_j> in deta with Chain_i_Task_i + 1 == Chain_i_Task_j : deta[Chain_i, Chain_i_Task_i, Chain_i_Task_j]) + ResponseTime[Chains_TasksName[Chain_i, card(Chains[Chain_i])]];

# deta
subto Constraint_5_17:
    forall <Chain_i> in Chains:
        forall <Chain_i, Chain_i_Task_i> in Chains_Tasks:
            forall <Chain_i, Chain_i_Task_j> in Chains_Tasks - { <Chain_i, Chain_i_Task_i> }:
                deta[Chain_i, Chain_i_Task_i, Chain_i_Task_j] <= Periods[Chains_TasksName[Chain_i, Chain_i_Task_i]] + U[Chains_TasksName[Chain_i, Chain_i_Task_i], Chains_TasksName[Chain_i, Chain_i_Task_j]] * ResponseTime[Chains_TasksName[Chain_i, Chain_i_Task_i]];

forall <Chain_i> in Chains:
    minimize DataAge:
        MaxDataAge[Chain_i];
	# two-objectives: first data age, second response 
	#                 times (to make the RTA tight)
	# sum <t> in T: 
	# 	period[t] * sum <c> in S: AGE[c] + sum <t> in T: RT[t];
