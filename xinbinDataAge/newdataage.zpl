#T是任务
#C是处理器
#P是优先级
#定义需要的变量，与公式相对应
var Deta[<c,i> in CHAINID] integer >= 0;   # deta^+_{i,i+1}
var Fai[<c,i> in CHAINID] integer>=0;   # fai^+_{i,i+1}
var AGE[S]              integer >= 0;   # DA
var offset[<c,i> in CHAINID] integer >=0;
var RO[TT] integer >=0;
#help function	
defnumb add_period(c,i,n) := n * period[CHAINTASKS[c,i]]; # n个任务i的周期
defnumb taskperiod(c,i) := period[CHAINTASKS[c,i]]; # 任务周期
defbool offbig(c,i,j) := OFF[CHAINTASKS[c,i]] > OFF[CHAINTASKS[c,j]]
#初始化
subto lastdelay:
	forall <c> in S:
		Deta[c,CHAINLEN[c]] == 0;
#公式
subto offset:
	forall <x> in T:
		forall <i> in T - {x} :
			offset[x,i]==OFF[x] mod OFF[i];
subto RT_OFF:
	forall <x> in T:
		forall <i> in T:
			RO[x,i]==RT[x]-OFF[i];
subto test:
	forall <c> in S:
		forall <i> in {1 to CHAINLEN[c]-1}:
				Fai[c,i] >= offset[i, i+1] / CHAINNGOD[c,i];
#subto test:
#	forall <c> in S:
#		forall <i> in {1 to CHAINLEN[c]-1}:
#				Fai[c,i] == max( ((offset[CHAINTASKS[c,i],CHAINTASKS[c,i+1]]) mod CHAINNGOD[c,i] ),( (offset[CHAINTASKS[c,i],CHAINTASKS[c,i+1]]+#(ceil(offset[CHAINTASKS[c,i+1],CHAINTASKS[c,i]]/taskperiod(c,i)) * taskperiod(c,i))) mod (CHAINNGOD[c,i])) );

subto formulation2:
	forall <c> in S:
		forall <i> in {1 to (CHAINLEN[c]-1)}:
			if (X[CHAINTASKS[c,i],CHAINTASKS[c,i+1]]and V[CHAINTASKS[c,i],CHAINTASKS[c,i+1]]) then 
				if (fai[c,i] == 0 ) then 
					Deta[c,i]==taskperiod(c,i)-CHAINNGOD[c,i]
				else 
					Deta[c,i]==taskperiod(c,i)-fai[c,i]
					
			else 
				if (fai[c,i] == 0) then
					if (RT[CHAINTASKS[c,i]] mod CHAINNGOD[c,i]) == 0 then
						Deta[c,i] == RT[CHAINTASKS[c,i]]+taskperiod(c,i) - CHAINNGOD[c,i]
					else 
						Deta[c,i]==RT[CHAINTASKS[c,i]]+taskperiod(c,i) - (RT[CHAINTASKS[c,i]] mod CHAINNGOD[c,i])
						
				else
#这里只用到了off[i]，暂时没改
					if ((RO[CHAINTASKS[c,i],CHAINTASKS[c,i+1]]) mod CHAINNGOD[c,i]) == 0 then 
						Deta[c,i]==RT[CHAINTASKS[c,i]]+taskperiod(c,i)-fai[c,i]
					else 
						Deta[c,i]==RT[CHAINTASKS[c,i]]+taskperiod(c,i)-(fai[c,i]+(RT[CHAINTASKS[c,i]] mod CHAINNGOD[c,i])) mod CHAINNGOD[c,i]
			end;
			
	
subto chain_age:               
	forall <c> in S:
		AGE[c] == OFF[CHAINTASKS[c,1]] + sum <i> in {1 to CHAINLEN[c]}: RT[CHAINTASKS[c,i]] ;

minimize age:
	sum <t> in T: 
		period[t] * (sum <c> in S: AGE[c] + (sum <t> in T: RT[t]));

