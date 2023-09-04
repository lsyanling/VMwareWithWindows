param target[T]:=read "tasks2.txt" as "<1s> 6s" comment "#";
#param pri[T]:=read "tasks2.txt" as "<1s> 7n" comment "#";

subto premapped:
forall <i> in T: 
	if target[i] != "None" then A[i,target[i]] == 1 end;
#subto premapped2:
#forall <i> in T: 
#	if pri[i]!=0 then PI[i,pri[i]]==1 end;
