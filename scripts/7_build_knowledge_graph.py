import re
from collections import Counter
import sys

# Attempt to import networkx and provide a helpful error message if it's not installed.
try:
    import networkx as nx
except ImportError:
    print("Error: The 'networkx' library is not installed.")
    print("Please install it by running: pip install networkx")
    sys.exit(1)

def load_roots(filename="roots.txt"):
    """
    Loads roots from a text file, cleaning comments and parsing morphemes.
    """
    roots = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or '===' in line or not line.strip():
                    continue
                morpheme = line.split('|')[0].strip()
                if morpheme:
                    roots.append(morpheme)
        return roots
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        sys.exit(1)

def load_and_segment_corpus(filename="voynich_super_clean_with_pages.txt"):
    """
    Loads the corpus and segments it into a dictionary based on folio markers.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{filename}' not found.")
        sys.exit(1)
    
    segments = re.split(r'(<f[0-9a-zA-Zvr]+>)', content)
    
    segmented_corpus = {}
    if len(segments) > 1:
        for i in range(1, len(segments), 2):
            folio_id = segments[i].strip('<>')
            text = segments[i+1].strip()
            if text:
                segmented_corpus[folio_id] = text
            
    return segmented_corpus

def find_longest_root_in_word(word, sorted_roots):
    """
    Finds the longest root from the pre-sorted list that is a substring of the word.
    """
    for root in sorted_roots:
        if root in word:
            return root
    return None

def tag_corpus_to_sequence(segmented_corpus, roots):
    """
    Converts the entire word-based corpus into a single flat list of roots.
    """
    print("Tagging corpus and creating a flat root sequence...")
    sorted_roots = sorted(roots, key=len, reverse=True)
    full_sequence = []
    for folio_id in sorted(segmented_corpus.keys()):
        text = segmented_corpus[folio_id]
        words = text.split()
        tagged_roots = [root for word in words if (root := find_longest_root_in_word(word, sorted_roots)) is not None]
        full_sequence.extend(tagged_roots)
    print("Tagging complete.\n")
    return full_sequence

def build_graph_from_sequence(sequence, connectors):
    """
    Builds a directed graph from the sequence of roots based on syntactic patterns.
    """
    print("Building the knowledge graph...")
    G = nx.DiGraph()
    edge_count = 0
    
    # Iterate through all possible trigrams
    for i in range(len(sequence) - 2):
        source, connector, target = sequence[i], sequence[i+1], sequence[i+2]
        
        # Check if the middle element is a known connector
        if connector in connectors:
            # Add the concepts as nodes and the connector as an edge
            G.add_node(source)
            G.add_node(target)
            G.add_edge(source, target, label=connector)
            edge_count += 1
            
    print(f"Graph built successfully: {G.number_of_nodes()} nodes and {edge_count} edges created.")
    return G

def save_graph_to_gexf(graph, filename="voynich_knowledge_graph.gexf"):
    """
    Saves the graph to a GEXF file, which is ideal for visualization in Gephi.
    """
    try:
        nx.write_gexf(graph, filename)
        print(f"\nSuccessfully saved the knowledge graph to '{filename}'.")
    except Exception as e:
        print(f"An error occurred while saving the graph: {e}")

if __name__ == "__main__":
    CORPUS_FILE = "voynich_super_clean_with_pages.txt"
    ROOTS_FILE = "roots.txt"
    OUTPUT_FILE = "voynich_knowledge_graph.gexf"
    
    # Define ALL the connectors that represent relationships (edges) in our graph
    TARGET_CONNECTORS = ['s', 'r', 'l', 'd', 'f']
    
    print("===== Knowledge Graph Engine: Building the Voynich Conceptual Map =====\n")
    
    # 1. Load data and create the root sequence
    print("1. Loading and tagging corpus...")
    roots = load_roots(ROOTS_FILE)
    segmented_corpus = load_and_segment_corpus(CORPUS_FILE)
    full_root_sequence = tag_corpus_to_sequence(segmented_corpus, roots)
    
    # 2. Build the graph from the sequence
    knowledge_graph = build_graph_from_sequence(full_root_sequence, TARGET_CONNECTORS)
    
    # 3. Save the graph to a file
    print(f"3. Saving graph to '{OUTPUT_FILE}' for visualization...")
    save_graph_to_gexf(knowledge_graph, OUTPUT_FILE)

    print("\n===== Process complete. =====")
    print("You can now open the .gexf file in a graph visualization tool like Gephi.")