from typing import Any, List
from dataclasses import dataclass

TYPE_TO_EMOJI = {
    'dir': '📂',
    'file': '🚩'
}

@dataclass
class Node:
    name: str
    parent: Any  # node
    children: List  # List of children nodes
    filetype: str
    size: int

    def add_children(self, data: str, children_name: str):
        filetype = get_filetype(data)
        size = get_size_based_on_filetype(filetype, data)
        new_child = Node(
            name=children_name,
            parent=self,
            children=[],
            filetype=filetype,
            size=size,
        )
        self.children.append(new_child)

    def print_tree_given_starting_node(self, indent=''):  # recursive
        print(f'{indent}{TYPE_TO_EMOJI[self.filetype]}', self.name, self.size)
        indent += '  '
        for child in self.children:
            child.print_tree_given_starting_node(indent)

    def update_folder_sizes_recursively(self) -> int:  # recursive
        if self.filetype == 'file':
            return self.size

        size_of_children = 0
        for child in self.children:
            size_of_children += child.update_folder_sizes_recursively()
        self.size = size_of_children  # a folder size is equal to the sum of their children
        return size_of_children

    def get_list_of_all_folder_sizes(self) -> List[int]:  # recursive
        if self.filetype == 'file':
            return []
        size_of_down_folders = []
        for child in self.children:
            size_of_down_folders += child.get_list_of_all_folder_sizes()
        size_of_down_folders.append(self.size)
        return sorted(list(size_of_down_folders))


def find_folder_size_with_smallest_positve_difference(
    folder_sizes: List[int], target_size: int
) -> int:
    for folder_size in folder_sizes:
        if folder_size > target_size:
            return folder_size
    return 0


def sum_folder_sizes_smaller_than(folder_sizes: List[int], target_size: int) -> int:
    folders_smaller = [f for f in folder_sizes if f < target_size]
    return sum(folders_smaller)


def read_input_as_lines(input_path: str) -> List[str]:
    with open(input_path) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


def find_node_in_list(list_of_nodes: List[Node], node_name: str):
    for node in list_of_nodes:
        if node.name == node_name:
            return node
    raise Exception(f'Node {node_name} not found in {list_of_nodes}')


def execute_cd_command(node: Node, argument: str):
    if argument == '..':
        return node.parent
    return find_node_in_list(node.children, argument)


def get_filetype(data: str) -> str:
    if data == 'dir':
        return 'dir'
    return 'file'


def get_size_based_on_filetype(filetype: str, data: str):
    if filetype == 'file':
        return int(data)
    return 0


def get_root(node: Node):
    while True:
        node = node.parent
        if node.parent == None:
            return node


def initialize_tree_node_given_commands(input: List[str]):
    input.pop(0)
    node = Node('/', None, [], 'dir', 0)
    for line in input:
        line = line.split(' ')
        if line[0] == '$':
            if line[1] == 'cd':
                node = execute_cd_command(node, line[2])
                continue
            elif line[1] == 'ls':
                continue
        # line is a `ls` statement if it reaches this part
        node.add_children(line[0], line[1])
    node = get_root(node)
    return node


def main():
    input = read_input_as_lines('easy_input.txt')
    node = initialize_tree_node_given_commands(input)
    node.update_folder_sizes_recursively()  # folders have no size, update based on folder contents
    node.print_tree_given_starting_node()

    folder_sizes = node.get_list_of_all_folder_sizes()
    combined_sum = sum_folder_sizes_smaller_than(folder_sizes, 100_000)
    target_size_to_delete = node.size - 40_000_000  # the size should be 40million (30 million free for update)
    folder_size_to_delete = find_folder_size_with_smallest_positve_difference(
        folder_sizes, target_size_to_delete
    )
    print(f'Combined sum {combined_sum}')
    print(f'Size of folder to delete {folder_size_to_delete}')


if __name__ == '__main__':
    main()
