# Import the Tree class and utility functions
from Tree import Tree
from utils import getURL, getPath  # Helper functions that assist with URL and path extraction

"""
# Expected format for crawler data:
let networkMap = [
    {
        url: "www.google.com",
        path: "/",
        children: [
            {
                url: "www.google.com/search",
                path: "/search",
                children: [
                    {
                        url: "www.google.com/search/search",
                        path: "/search/search",
                        children: []
                    }
                ]
            }
        ]
    }
];
"""

class DirectoryTreeCreator:
    def __init__(self, tree=Tree()) -> None:
        # Initializes the DirectoryTreeCreator with a tree structure.
        # By default, it creates a new Tree instance.
        self.tree = tree

    def get_tree(self) -> Tree:
        # Returns the current tree structure.
        return self.tree

    def reset(self) -> None:
        # Resets the tree by reinitializing it as a new Tree instance.
        self.tree = Tree()

    def populate(self, crawl_data: dict, display=False, indent="") -> None:
        # Recursively populates the tree using the provided crawl data.
        # Args:
        # - crawl_data (dict): The hierarchical network map of URLs.
        # - display (bool): If True, prints the tree structure as it's being built.
        # - indent (str): Used for formatting hierarchical levels in printed output.

        for node in crawl_data:
            url = node['url']
            path = node['path']
            children = node['children']
            vertex = (url, path)

            # Print the node being added (if display is enabled)
            if display:
                print(f"{indent}Adding node: {getURL(vertex)}")

            for child_node in children:
                child_url = child_node['url']
                child_path = child_node['path']
                child_vertex = (child_url, child_path)

                # Add an edge between parent and child
                self.tree.add_edge(vertex, child_vertex)

                # Print the connection (if display is enabled)
                if display:
                    print(f"{indent} ├─> {getURL(child_vertex)}")

            # Recursively process children with increased indentation
            self.populate(children, display, indent + "  ")

            
    def add_edge(self, src: tuple[str, str], dst: tuple[str, str], display=False) -> None:
        # Adds an edge (connection) between two nodes in the tree.
        # Args:
        # - src (tuple): The source node (url, path).
        # - dst (tuple): The destination node (url, path).
        # - display (bool): (TODO) Option to display the tree after adding an edge.

        # Validate that both source and destination are properly formatted tuples
        if not isinstance(src, tuple) or len(src) != 2:
            raise ValueError(f"Vertex {src} is not properly formatted! Expected (url, path).")
        if not isinstance(dst, tuple) or len(dst) != 2:
            raise ValueError(f"Vertex {dst} is not properly formatted! Expected (url, path).")

        self.tree.add_edge(src, dst)  # Add the edge (connection) to the tree

        if display:
            pass  # (TODO) Implement functionality to display the tree after adding an edge
            print(f"Added edge: {getURL(src)} ──> {getURL(dst)}")

    def display_data(self) -> None:
        # Displays all the data currently stored in the tree.
        # Iterates through the tree's dictionary structure and prints each vertex and its connections.

        for vertex in self.tree.dir_tree:
            print(f"{getURL(vertex)} -> {self.tree.dir_tree[vertex]}")  # Print each node and its children

    def display_pretty(self, root, indent="") -> None:
        # Displays the tree structure in a readable, hierarchical format.
        # Args:
        # - root: The root node from where to start displaying.
        # - indent (str): Used for formatting hierarchical levels.

        children = self.tree.dir_tree[root]  # Get the children of the current root node

        # Print the current node
        if children:
            print(f"{indent}{getURL(root)} --> ")  # If the node has children, show an arrow
        else:
            print(f"{indent}{getURL(root)}")  # If it's a leaf node, just print it

        # Recursively print child nodes with indentation to show hierarchy
        for child in children:
            if child in self.tree.dir_tree:
                self.display_pretty(child, f"{indent}\t")  # Increase indentation for child nodes
            else:
                raise ValueError(f"Vertex {child} was found as a child of {root}, but does not exist in the graph!")
