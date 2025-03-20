# Import the DirectoryTreeCreator class from an external module
from DirectoryTreeCreator import DirectoryTreeCreator

# Define a hierarchical network map representing a tree structure of URLs
networkMap = [
    {
        'url': "www.google.com",
        'path': "/",
        'children': [
            {
                'url': "www.google.com/search",
                'path': "/search",
                'children': [
                    {
                        'url': "www.google.com/search/search",
                        'path': "/search/search",
                        'children': []  # No further children, marking this as a leaf node
                    }
                ]
            },
            {
                'url': "www.google.com/earth",
                'path': "/earth",
                'children': [
                    {
                        'url': "www.google.com/earth/search",
                        'path': "/earth/search",
                        'children': []  # Another leaf node
                    }
                ]
            }
        ]
    }
]

# Create an instance of DirectoryTreeCreator
treeCreator = DirectoryTreeCreator()

# Populate the tree with the predefined network map. Display = True is to show real time updates
treeCreator.populate(networkMap, display=True)

# Manually add edges between different nodes to represent additional connections
treeCreator.add_edge(('www.google.com', '/'), ('linked-in.com', '/l'))  # Connect Google root to LinkedIn
treeCreator.add_edge(('linked-in.com', '/l'), ('random.com', '/rnd'))   # Connect LinkedIn to Random site
treeCreator.add_edge(('www.google.com', '/'), ('random.com', '/rnd'))   # Directly connect Google root to Random site

# Display the tree structure in a formatted output
#,mtreeCreator.display_pretty(treeCreator.tree.root)

# Optionally, display raw data representation of the tree (currently commented out)
# treeCreator.display_data()