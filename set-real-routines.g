CounitFreeForget := function(M)
local A, F, Arrows, Vertices, M_set, Matrices_for_free, M_free, f, i, j;

A := RightActingAlgebra(M);
F := LeftActingDomain(A);
M_set := [];
for i in [1..Length(DimensionVector(M))] do
  M_set[i] := AsList(F^DimensionVector(M)[i]);
  od;

Arrows := ArrowsOfQuiver(QuiverOfPathAlgebra(A));
Vertices := VerticesOfQuiver(QuiverOfPathAlgebra(A));

Matrices_for_free := [];
for m in [1..Length(Arrows)] do
  Matrices_for_free[m] := NullMat(Length(M_set[Position(Vertices, SourceOfPath(Arrows[m]))]),
        Length(M_set[Position(Vertices, TargetOfPath(Arrows[m]))]), F);
  for i in [1..Length(M_set[Position(Vertices, SourceOfPath(Arrows[m]))])] do
    for j in [1..Length(M_set[Position(Vertices, TargetOfPath(Arrows[m]))])] do
      if M_set[Position(Vertices, TargetOfPath(Arrows[m]))] = [[]] then
        Matrices_for_free[m][i][j] := One(F);
      else
        if M_set[Position(Vertices, SourceOfPath(Arrows[m]))][i] = [] then
          if j = 1 then
            Matrices_for_free[m][i][j] := One(F);
          fi;
        else
          if M_set[Position(Vertices, SourceOfPath(Arrows[m]))][i] * MatricesOfPathAlgebraModule(M)[m] =
                M_set[Position(Vertices, TargetOfPath(Arrows[m]))][j] then
            Matrices_for_free[m][i][j] := One(F);
          fi;
        fi;
      fi;
    od;
  od;
od;

for i in [1..Length(DimensionVector(M))] do
  if M_set[i] = [[]] then
    M_set[i] := [[ 0*One(F) ]];
    fi;
  od;

M_free := RightModuleOverPathAlgebra(A, Matrices_for_free);
f := RightModuleHomOverAlgebra(M_free, M, M_set);

return [M_free, f];
end;

IsInduced := function(M)
return IsSplitEpimorphism(CounitFreeForget(M)[2]);
end;

TestFromProjectives := function(A, n)
local M, j, i;

for j in [1..Length(IndecProjectiveModules(A))] do
  M := IndecProjectiveModules(A)[j];
  Print("  Projective ");
  Print(DimensionVector(M));
  Print(":\n");
  Print("    ");
  Print(IsInduced(M));
  Print("\n");
  if not IsInjectiveModule(M) then
    for i in [1..n] do
      M := TrD(M);
      if IsInjectiveModule(M) then
        Print("  Injective ");
      else
        Print("  Module ");
      fi;
      Print(DimensionVector(M));
      Print(":\n");
      Print("    ");
      Print(IsInduced(M));
      Print("\n");
      if IsInjectiveModule(M) then
        break;
      fi;
    od;
  fi;
od;

end;

TestQuiet := function(A, n)
local M, j, i;
for j in [1..Length(IndecProjectiveModules(A))] do
  M := IndecProjectiveModules(A)[j];
  if not IsInjectiveModule(M) then
    for i in [1..n] do
      M := TrD(M);
      if not IsInduced(M) then
        #Print(DimensionVector(M));
        Print(" is not induced\n");
        return 0;
      fi;
      if IsInjectiveModule(M) then
        break;
      fi;
      if i=n then
        Print("Warning: n too small!\n");
        return 2;
      fi;
    od;
  fi;
od;
return 1;
end;




