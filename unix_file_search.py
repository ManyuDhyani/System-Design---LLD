"""
You are asked to search files in a Unix-style system based on multiple filters, like:

    File extension (.txt, .log, .pdf)

    File name (e.g. "report")

    File size (e.g. larger than 10000 bytes)

You should also be able to combine these filters using AND or OR logic.
"""
class File:
    #Ex file: File("file1", "txt", 1000)
    def __init__(self, name, extension, size):
        self.name = name
        self.extension = extension
        self.size = size # in bytes

from abc import ABC, abstractmethod
# This is the parent class for all filters
class BaseFilter(ABC):
    @abstractmethod
    def is_match(self, file):
        pass
    

# === Concrete Filters (Simple Single-Purpose Filters) ===

# Match files with a specific extension

class ExtensionFilter(BaseFilter):
    def __init__(self, extension):
        self.extension = extension
    
    def is_match(self, file):
        return self.extension == file.extension

# Match files with an exact name
class NameFilter(BaseFilter):
    def __init__(self, name):
        self.name = name
    
    def is_match(self, file):
        return self.name == file.name

# Match files where name contains a substring
# Match files where name contains a substring
class NameContainsFilter(BaseFilter):
    def __init__(self, substring):
        self.substring = substring

    def is_match(self, file):
        return self.substring in file.name


# Match files larger than a given size
class SizeGreaterThanFilter(BaseFilter):
    def __init__(self, min_size):
        self.min_size = min_size

    def is_match(self, file):
        return file.size > self.min_size


# Match files smaller than a given size
class SizeLessThanFilter(BaseFilter):
    def __init__(self, max_size):
        self.max_size = max_size

    def is_match(self, file):
        return file.size < self.max_size
    

# This is the parent class for all combination filters like AND / OR
class CombinationFilter(BaseFilter):
    # Accepts a list of filter objects
    def __init__(self, filters):
        self.filters = filters

# All filters must match (AND logic)
class AndFilter(CombinationFilter):
    def is_match(self, file):
        for f in self.filters:
            if not f.is_match(file):
                return False
        return True

class OrFilter(CombinationFilter):
    def is_match(self, file):
        for f in self.filters:
            if f.is_match(file):
                return True
        return False

# === Utility Function to Search === 
def search_files(files, files_obj):
    result = []
    for file in files:
        if files_obj.is_match(file):
            result.append(file.name)
    return result


files = [
        File("report", "pdf", 100000),
        File("file1", "txt", 1000),
        File("data_backup", "txt", 50000),
        File("notes", "log", 20000),
        File("summary", "txt", 15000),
]

# Example 1: Find .txt files with size > 10KB
f1 = ExtensionFilter("txt")
f2 = SizeGreaterThanFilter(10000)
combined_and = AndFilter([f1, f2])
print("Files with .txt AND size > 10KB:")
print(search_files(files, combined_and))  # Output: ['data_backup', 'summary']

# Example 2: Find files where name contains "data" OR size > 10KB
f3 = NameContainsFilter("data")
combined_or = OrFilter([f2, f3])
print("\nFiles with name contains 'data' OR size > 10KB:")
print(search_files(files, combined_or))  # Output: ['report', 'data_backup', 'notes', 'summary']

# Example 3: Combine 3 filters: .txt AND >10KB AND <30KB
f4 = SizeLessThanFilter(30000)
combo_all = AndFilter([f1, f2, f4])
print("\nFiles with .txt AND size between 10KB and 30KB:")
print(search_files(files, combo_all))  # Output: ['summary']


    

    