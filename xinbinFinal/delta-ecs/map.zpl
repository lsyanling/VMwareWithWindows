param target[T]:=read "tasks2.txt" as "<1s> 6s" comment "#";

subto premapped:
forall <i> in T: 
	if target[i] != "None" then A[i,target[i]] == 1 end;
