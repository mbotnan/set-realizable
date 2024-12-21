import itertools
import json
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
from matplotlib.backends.backend_pdf import PdfPages

depth = 20 #How far into the AR quiver one departs from a projective. 
field = "GF(2)" # Replace with GF(n)"

def generate_all_permutations(edge_list):
    """
    Generate all permutations by replacing [a, b] with [b, a] for each sublist.
    """
    # Generate all combinations of directions for edges
    permutations = []
    for combination in itertools.product([0, 1], repeat=len(edge_list)):
        permuted_list = []
        for idx, flip in enumerate(combination):
            a, b, label = edge_list[idx]
            if flip == 0:
                permuted_list.append([a, b, label])  # Original direction
            else:
                permuted_list.append([b, a, label])  # Reversed direction
        permutations.append(permuted_list)
    return permutations

def convert_to_gap_format(permutations):
    """
    Convert a list of lists into GAP-compatible format.
    """
    gap_permutations = []
    for perm in permutations:
        gap_list = [
            f"[{a}, {b}, \"{label}\"]" for a, b, label in perm
        ]
        gap_permutations.append("[" + ", ".join(gap_list) + "]")
    return gap_permutations


def plot_graph(edge_list, gapoutput):
    G = nx.DiGraph()
    # Add edges to the graph
    for edge in edge_list:
        G.add_edge(edge[0], edge[1])

    # Draw the graph
    plt.figure() 
    if gapoutput == 1:
        plt.title("Additively surjective")
    elif gapoutput == 2:
        plt.title('Inconclusive')
    else:
        plt.title("Not additively surjective") 
    pos = nx.spectral_layout(G)  # Position nodes using a force-directed layout
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=10, font_weight="bold")
    pdf.savefig()
    plt.close()


def check_add(n,gap_list):
    gap_code = f"""
    LoadPackage("QPA");
    lst := {gap_list};
    Read("set-real-routines.g");
    Q := Quiver({n}, lst);
    kQ := PathAlgebra({field}, Q);  
    AssignGeneratorVariables(kQ); 
    TestQuiet(kQ, {depth});
    """
    gap_path = "gap"
    try:
        result = subprocess.run([gap_path, "-q"], input=gap_code, text=True, capture_output=True, check=True)
        
        # Extract only the numeric result from the output; this is the last entry. If not, there's an error.
        # An error occurs if the path-algebra is not finite-dimensional.
        last_line = result.stdout.strip().split('\n')[-1]

        if not last_line.isdigit():
            raise ValueError("Something went wrong. Is the algebra finite-dimensional?")

        return int(last_line)

    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)

def quiver_check(quiver):
    gap_list = convert_to_gap_format([quiver[1]])
    result = check_add(quiver[0],gap_list[0])
    if result == 1:
       print("Additively surjective")
    elif result ==2:
       print("Did not explore full AR quiver; inconclusive; increase depth.")
    else:
       print("Not additively surjective")



def quiver_check_all(quiver):
    perm = generate_all_permutations(quiver[1])
    gap_list = convert_to_gap_format(perm)
    result = [check_add(quiver[0],item) for item in gap_list]
    AR_explore(result)
    return perm, result

def AR_explore(result):
   if(sum(result) > len(result)):
       print("Did not explore the full AR quiver; increase depth.")
   print("Fraction of additively realizable orientations: "+str(result.count(1))+"/"+str(len(result)))  

def typeE(n):
    #Works for n=6,7,8. When considering n=7, it first runs through n=6 to identify 
    #restricted representations that are not realizable. Same for n=8.
    edge_list = [
    [1, 2, "e1"],
    [2, 3, "e2"],
    [3, 4, "e3"],
    [3,5, "e4"],
    [5,6, "e5"],
    [6,7, "e6"],
    [7,8, "e7"]]

    permE6 = generate_all_permutations(edge_list[0:5])
    gap_listE6 = convert_to_gap_format(permE6)
    resE6 = [check_add(6,item) for item in gap_listE6]
    if n == 6:
        AR_explore(resE6)
        return permE6, resE6

    permE7 = generate_all_permutations(edge_list[0:6])
    permE7 = permE7
    forbidden = []
    gap_listE7 = convert_to_gap_format(permE7)
    FailedIndicesE6 = [i for i, x in enumerate(resE6) if x == 0]
    FailedOrientationsE6 = [permE6[index] for index in FailedIndicesE6]
    forbidden.extend(FailedOrientationsE6)
    skip_ind = [1 if item[:-1] not in forbidden else -10 for item in permE7]
    resE7 = [check_add(7,gap_listE7[i]) if skip_ind[i]==1  else 0 for i in range(0,len(permE7))]
    FailedIndicesE7 = [i for i, x in enumerate(resE7) if x == 0]
    FailedOrientationsE7 = [permE7[index] for index in FailedIndicesE7]
    forbidden.extend(FailedOrientationsE7)

    if n==7:
        AR_explore(resE7)
        return permE7, resE7
    permE8 = generate_all_permutations(edge_list)
    gap_listE8 = convert_to_gap_format(permE8)
    skip_ind2 = [1 if item[:-1] not in forbidden else -10 for item in permE8]
    resE8 = [check_add(8,gap_listE8[i]) if skip_ind2[i]==1  else 0 for i in range(0,len(permE8))]
    AR_explore(resE8)
    return permE8, resE8

      
#all_permutations, result = typeE(6) #Checks all orientations of E6; should run in a couple of minutes.
#with PdfPages("E6.pdf") as pdf:
#    [plot_graph(all_permutations[i], result[i]) for i in range(0,len(result))]

Q = [4,[[2,1, "e1"],[3,1, "e2"], [4,1, "e3"]]] # D4 quiver fixed inward orientations
quiver_check(Q)

all_permutations, result = quiver_check_all(Q) #Check all orientations of D4
with PdfPages("D4.pdf") as pdf:
    [plot_graph(all_permutations[i], result[i]) for i in range(0,len(result))]




