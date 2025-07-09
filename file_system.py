#You need to implement the following methods:

#1. ls(path: str) -> List[str]
#If path is a file: return a list containing only the file name.


#If path is a directory: return a list of all files and directories in lexicographic order in that directory.

#2. mkdir(path: str) -> None
#Creates a directory structure along the specified path.

#Any intermediate directories that do not exist should also be created.

#3. addContentToFile(filePath: str, content: str) -> None
#If the file does not exist, it is created with the given content.

#If the file already exists, the new content is appended to the existing content.

#4. readContentFromFile(filePath: str) -> str
#Returns the entire content of the file at the specified path.

class TrieNode:
    def __init__(self):
        self.children = {} # Maps name -> TrieNode (file or directory)
        self.is_file = False # True if this node is a file
        self.content = "" # Used only if this node is a file

class FileSystem:
    def __init__(self):
        self.root = TrieNode()

    
    def traverse(self, path, create=False):
        node = self.root

        # If the path is just the root ("/"), return the root node immediately.
        if path == "/":
            return node

        for part in path.strip("/").split("/"):
            if part not in node.children:
                if not create:
                    return None
                node.children[part] = TrieNode()
            node = node.children[part]
        #Once all parts are processed, return the final node (could be a file or folder)
        return node
    

    #Just the file name, if the path points to a file.
    #All directory entries (files and subdirectories), if the path is a folder — in sorted order.
    def ls(self, path):
        node = self.traverse(path)
        if node.is_file:
            return [path.split("/")[-1]]
        return sorted(node.children.keys())

    def mkdir(self, path):
        self.traverse(path, create=True)
    
    def addContentToFile(self, path, content):
        node = self.traverse(path, create=True)
        node.is_file = True
        node.content += content
    
    def readContentFromFile(self, path):
        node = self.traverse(path)
        return node.content if node and node.is_file else ""

fs = FileSystem()

fs.mkdir("/a/b/c")
fs.addContentToFile("/a/b/c/d", "hello")
fs.ls("/")                        # returns ['a']
fs.readContentFromFile("/a/b/c/d")  # returns 'hello'

"""
Explanation:

mkdir("/a/b/c") creates the directory path step by step.

addContentToFile(...) creates file d and stores content "hello".

ls("/") shows ['a'] because a is the only top-level directory.

readContentFromFile(...) returns the content of the file.

"""

"""
 Design Considerations:
Use a Trie-like tree structure where each node represents a file or directory.

Track:

children (dict of subdirectories/files)

is_file (to distinguish files from directories)

content (only for file nodes)
"""