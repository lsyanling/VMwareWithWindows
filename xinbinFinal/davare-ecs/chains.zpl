set S := { read "chains2.txt" as "<1n>" comment "#"};
set CHAINID:={ read "chains2.txt" as "<1n,2n>" comment "#"};
param CHAINLEN[<c> in S] := max <a, b> in CHAINID: 
																													if a == c then b else 0 end;
param CHAINTASKS[CHAINID] :=
	read "chains2.txt" as "<1n,2n> 3s" comment "#";

do forall <c> in S do forall <i> in {1 to CHAINLEN[c]-1} 
	do print CHAINTASKS[c,i], "-", CHAINTASKS[c,i+1];
