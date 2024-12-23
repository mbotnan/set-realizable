import itertools
import json
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
from matplotlib.backends.backend_pdf import PdfPages

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
    """
    Runs TestQuiet from set-real-routines.g on the given quiver given by gap_list.
    """

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
            raise ValueError("Something went wrong. Too few verticeS? Is the algebra finite-dimensional?")

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



def quiver_check_all(quiver, prnt=False):
    """
    Checks all orientations of a quiver for additively realizability. 
    prnt=True outputs current orientation of total number of orientations
    """

    perm = generate_all_permutations(quiver[1]) 
    gap_list = convert_to_gap_format(perm)
    result = [-1]*len(perm)
    known_fails = []
    known_wins = []
    reachable = [reflections(graph) for graph in perm]
    index_bw = [list(i for i, graph in enumerate(reachable) if x in graph) for x in perm]
    for i in range(0, len(perm)):
        if(prnt):
            print("Permutation index: "+str(i+1)+"/"+str(len(perm)))
        if(result[i] > -1):
            continue
        k = 0
        resx=1
        while(k<len(perm[i]) and resx==1):
            if perm[i][:k+1] in known_fails:
                resx=0
            elif perm[i][:k+1] in known_wins:
                k = k+1
            else:
                list_to_use = convert_to_gap_format([perm[i][:k+1]])
                resx = check_add(quiver[0], list_to_use[0])
                if resx == 1:
                    known_wins.append(perm[i][:k+1])
                else:
                    known_fails.append(perm[i][:k+1])
                k = k+1
        result[i] = resx
        if(resx == 1):
            found_reflections = reachable[i]
            indices_to_skip = [j for j, x in enumerate(perm) if x in found_reflections]
            for k in indices_to_skip:
                result[k] = resx
        else:
            for k in index_bw[i]:
                result[k] = resx
 
    AR_explore(result)
    return perm, result

def AR_explore(result):
   if(sum(result) > len(result)):
       print("Did not explore the full AR quiver; increase depth.")
   print("Fraction of additively realizable orientations: "+str(result.count(1))+"/"+str(len(result)))  


def reflections(edge_list):
    """
    Generate all possible quivers one can reach from a given quiver (edge list) by 
    iteratively reversing sources of out-degree at most 2.
    """
    from collections import defaultdict

    def get_degrees(edges):
        """Compute the in-degree and out-degree of each vertex."""
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        for u, v, _ in edges:
            out_degree[u] += 1
            in_degree[v] += 1
        return in_degree, out_degree

    def reverse_edges(edges, source):
        """Reverse all outgoing edges of the given source."""
        new_edges = []
        for u, v, label in edges:
            if u == source:
                new_edges.append([v, u, label])  # Reverse outgoing edge
            else:
                new_edges.append([u, v, label])  # Keep other edges unchanged
        return new_edges

    def find_sources(in_degree, out_degree):
        """Find all vertices with in-degree 0 (sources) and out-degree at most 2."""
        return [node for node in out_degree if in_degree[node] == 0 and out_degree[node] <= 2]

    results = []
    queue = [edge_list]
    seen = set()

    while queue:
        current_edges = queue.pop(0)
        edge_tuple = tuple(tuple(edge) for edge in current_edges)  # Convert to hashable type

        if edge_tuple in seen:
            continue

        seen.add(edge_tuple)
        results.append(current_edges)

        in_degree, out_degree = get_degrees(current_edges)
        sources = find_sources(in_degree, out_degree)

        for source in sources:
            new_edges = reverse_edges(current_edges, source)
            queue.append(new_edges)

    return results[1:]

depth = 20 #How far into the AR quiver one departs from a projective. 
field = "GF(2)" # Replace with GF(n)"
    
QD4 = [4,[[2,1, "e1"],[3,1, "e2"], [4,1, "e3"]]] # D4 quiver fixed inward orientations
#QE8 = [8, [[2, 3, "e2"], [3, 4, "e3"], [3,5, "e4"], [5,6, "e5"], [1,2, "e1"], [6,7, "e6"], [7,8, "e7"] ]]
#QE6 = [6, [[2, 3, "e2"], [3, 4, "e3"], [3,5, "e4"], [5,6, "e5"], [1,2, "e1"]]]
#QE7 = [7, [[2, 3, "e2"], [3, 4, "e3"], [3,5, "e4"], [5,6, "e5"], [1,2, "e1"], [6,7, "e6"]]]
QD4T = [5, [[1,5, "e1"],[4,1, "e2"], [3,1, "e3"], [2,1, "e4"]]] #Not finite rep. type. 

#Check fixed orientation
quiver_check(QD4T) 

#Check all orientations of the quiver
all_permutations, result = quiver_check_all(QD4, prnt=True) 

#Produce graphs
with PdfPages("Quiver.pdf") as pdf:
    [plot_graph(all_permutations[i], result[i]) for i in range(0,len(result))]





