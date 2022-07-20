class Node:
    def __init__(self, state, parent, actions):
        self.state = state
        self.parent = parent
        self.actions = actions


class Frontier:
    def __init__(self, start):
        self.frontier = [start]

    def add(self, node):
        self.frontier.append(node)

    def remove(self):
        removed_node = self.frontier.pop(-1)
        return removed_node


class Maze:
    def __init__(self, maze_file):
        self.maze = []
        self.solve_path = []
        self.maze_file_name = maze_file

        with open(maze_file) as f:
            for line in f.readlines():
                line = line.strip('\n')
                self.maze.append(line)

    def neighbours(self, location):
        x = location[0]
        y = location[1]
        moves = set()

        if x < 1 or x >= len(self.maze[0]) - 1:
            raise Exception('Invalid X')
        if y < 1 or y >= len(self.maze) - 1:
            raise Exception('Invalid Y')

        up = self.maze[y-1][x]
        if up == ' ' or up == 'F':
            moves.add((x, y - 1))
        down = self.maze[y+1][x]
        if down == ' ' or down == 'F':
            moves.add((x, y + 1))
        left = self.maze[y][x-1]
        if left == ' ' or left == 'F':
            moves.add((x - 1, y))
        right = self.maze[y][x+1]
        if right == ' ' or right == 'F':
            moves.add((x + 1, y))

        return moves

    def find_start(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == 'S':
                    return x, y

    def find_goal(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == 'F':
                    return x, y

    def expand(self, node):
        for move in self.neighbours(node.state):
            node.actions.append(move)

    def solve(self):
        explored_set = set()
        removed_nodes = []
        initial_node = Node(self.find_start(), None, [])
        goal = self.find_goal()
        frontier = Frontier(initial_node)

        while True:
            if len(frontier.frontier) == 0:
                raise Exception('No solution.')
            else:
                # Add neighbors to node's actions
                self.expand(frontier.frontier[-1])

                # Remove node & add to explored set
                removed_node = frontier.remove()
                removed_nodes.append(removed_node)

                if removed_node.state == goal:
                    removed_nodes = removed_nodes[::-1]
                    current_node = removed_nodes[0]

                    while True:
                        parent_node = current_node.parent
                        for search_node in removed_nodes:
                            if search_node.state == parent_node:
                                current_node = search_node
                                self.solve_path.append(current_node.state)

                        if current_node.state == self.find_start():
                            self.solve_path = self.solve_path[::-1]
                            self.solve_path.pop(0)
                            break
                    break

                explored_set.add(removed_node.state)
                # Add resulting nodes to frontier
                for action in removed_node.actions:
                    if action not in explored_set:
                        frontier.add(Node(action, removed_node.state, []))

    def output_solution(self):
        new_maze = []
        for i in range(len(self.maze)):
            row = []
            for j in range(len(self.maze[i])):
                if (j, i) in self.solve_path:
                    row.append('*')
                else:
                    row.append(self.maze[i][j])
            row.append('\n')
            new_maze.append(''.join(row))

        f = open(f'{self.maze_file_name.split(".")[0]}_SOLVED.txt', 'w')
        for line in new_maze:
            f.write(line)


maze = Maze('maze2.txt')
maze.solve()
maze.output_solution()
