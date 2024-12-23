# 4x2  Q := Quiver( 8, [ [1,2,"l1"], [2,3,"l2"], [3,4, "l3"], [5,6, "u1"], [6,7, "u2"], [7,8, "u3"], [1,5, "v1"], [2,6, "v2"], [3, 7, "v3"],  [4,8, "v4"]]); 
# 5x2  
Q := Quiver( 10, [ [1,2,"l1"], [2,3,"l2"], [3,4, "l3"], [4,9, "l4"], [5,6, "u1"], [6,7, "u2"], [7,8, "u3"], [8, 10, "u4"], [1,5, "v1"], [2,6, "v2"], [3, 7, "v3"],  [4,8, "v4"], [9,10, "v5"]]);
kQ := PathAlgebra(GF(2), Q);
AssignGeneratorVariables(kQ);

# 4x2  relations := [ l1*v2 - v1*u1, l2*v3 - v2*u2, l3*v4 - v3*u3];
# 5v2
relations := [ l1*v2 - v1*u1, l2*v3 - v2*u2, l3*v4 - v3*u3, l4*v5 - v4*u4];

A := kQ/relations;
TestFromProjectives(A, 10)
