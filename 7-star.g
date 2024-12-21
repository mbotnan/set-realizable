// A representation of the 7 star quiver with all arrows pointing outwards. 
// It is not in the additive image if p=2 but it is in the additive image if p=3.

p:=2; 
Q:=Quiver(8, [[1,2, "a1"], [1,3, "a2"], [1,4, "a3"], [1,5, "a4"], [1,6, "a5"], [1,7, "a6"], [1, 8, "a7"]]);
KQ := PathAlgebra(GF(p), Q);
AssignGeneratorVariables(KQ);
A:=KQ;
mat := [["a1", [[1,0], [1,1],[0,1]]*One(GF(p))], ["a2", [[1,0], [0,1], [0,0]]*One(GF(p))], ["a3", [[1,0], [0,1], [0,1]]*One(GF(p))], ["a4", [[1,0], [0,1], [1,0]]*One(GF(p))], ["a5", [[0,0], [1,0],[0,1]]*One(GF(p))], ["a6", [[1,0], [0,0], [0,1]]*One(GF(p))], ["a7", [[1,0], [1,0],[0,1]]*One(GF(p))]];
N:= RightModuleOverPathAlgebra(A,mat);
