from Tree import Tree

class DirectoryTreeCreator:
    def __init__(self, tree = Tree()) -> None:
        self.tree = tree

    # TODO 1. figure out what format the crawler team will use for the crawl data
    # TODO 2. populate the tree from the given data
    def populate(self, crawl_data):
        pass

    def display_tree(self) -> None:
        for vertex in self.tree.dir_tree:
            print(f"{vertex} -> {self.tree.dir_tree[vertex]}")