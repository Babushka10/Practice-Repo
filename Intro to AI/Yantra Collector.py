# Filename: l1.py

class YantraCollector:
    """
    YantraCollector class to solve the yantra collection puzzle.
    The player must collect all yantras sequentially and reach the exit.
    """
    
    def __init__(self, grid):
        """
        Initializes the game with the provided grid.

        Args:
            grid (list of list of str): The grid representing the puzzle.
        """
        self.grid = grid
        self.n = len(grid)
        self.start = self.find_position('P')
        self.exit = None
        self.yantras = self.find_all_yantras()
        self.revealed_yantra = self.find_position('Y1')
        self.collected_yantras = 0
        self.total_frontier_kids = 0
        self.total_explored_kids = 0
        
    def find_position(self, symbol):
        """
        Finds the position of a given symbol in the grid.

        Args:
            symbol (str): The symbol to locate.

        Returns:
            tuple or None: The position of the symbol, or None if not found.
        """
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j] == symbol:
                    return (i, j)
        return None

    def find_all_yantras(self):
        """
        Finds and stores the positions of all yantras in the grid.

        Returns:
            dict: A dictionary mapping yantra numbers to their positions.
        """
        positions = {}
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i][j].startswith('Y'):
                    positions[int(self.grid[i][j][1:])] = (i, j)
                elif self.grid[i][j] == 'E':
                    self.exit = (i, j)
        return positions

    def reveal_next_yantra_or_exit(self):
        """
        Reveals the next yantra in sequence or the exit when all yantras are collected.
        """
        self.collected_yantras += 1
        if self.collected_yantras + 1 in self.yantras:
            self.revealed_yantra = self.yantras[self.collected_yantras + 1]
        elif self.collected_yantras == len(self.yantras):
            self.revealed_yantra = self.exit
        else:
            self.revealed_yantra = None

    def goal_test(self, position):
        """
        Checks if the given position matches the currently revealed yantra or exit.

        Args:
            position (tuple): The current position to check.
        """
        return position==self.revealed_yantra

    def get_neighbors(self, position):
        """
        Generates valid neighboring positions for the given position.

        Args:
            position (tuple): The current position of the player.
        """
        #creating a list to store number 
        neighbors=[]
        #assigning coordinates to variables
        x=position[0]
        y=position[1]
        #assigning South East West North
        dir=[(-1,0),(0,1),(1,0),(0,-1)]
        
        #searching for other coordinates
        for dx,dy in dir:
            nx=dx+x
            ny=dy+y
            #applying boundary conditions and skipping trap and walls
            if 0<=nx<self.n and 0<=ny<self.n:
                if self.grid[nx][ny] not in ['#',"T"]:
                    neighbors.append((nx,ny))
        return neighbors


    def bfs(self, start, goal):
        """
        Performs Breadth-First Search (BFS) to find the shortest path to the goal.

        Args:
            start (tuple): The starting position.
            goal (tuple): The goal position.

        Returns:
            tuple: (optimal path, total frontier kids, total explored kids)
        """
        #creating list to store the nodes
        frontier = [start]
        visited = []
        ancestor = [(start, None)]
        #taking elements for search
        while frontier:
            current = frontier.pop(0)#taking the first element added for BFS
            visited.append(current)
            #backtracking once you reach the goal
            if current == goal:
                path = [current]
                while current != start:
                    for kid, par in ancestor:
                        if kid == current:
                            current = par
                            path.append(current)
                            break
                path.reverse()
                return path, len(frontier), len(visited)
            #finding neighbors
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and neighbor not in frontier:
                    frontier.append(neighbor)
                    ancestor.append((neighbor, current))
        #return none if no solution is found
        return None, len(frontier), len(visited)


    
    def dfs(self, start, goal):
        """
        Performs Depth-First Search (DFS) to find the shortest path to the goal.

        Args:
            start (tuple): The starting position.
            goal (tuple): The goal position.

        Returns:
            tuple: (optimal path, total frontier kids, total explored kids)
        """
         #creating list to store the nodes
        frontier = [start]
        visited = []
        ancestor = [(start, None)]
        #taking elements for search
        while frontier:
            current = frontier.pop(0) 
            #to avoid repetitions
            if current in visited:
                continue
            visited.append(current)
            #backtracking the path once goal is reached
            if current == goal:
                path = [current]
                while current != start:
                    for kid, par in ancestor:
                        if kid == current:
                            current = par
                            path.insert(0,current)#inserting the elements to the first for DFS
                            break
                return path, len(frontier), len(visited)
            
            #searching for neighbours
            tempn=self.get_neighbors(current)
            for neighbor in tempn[::-1]:  
                if neighbor not in visited and neighbor not in frontier:
                    frontier.insert(0,neighbor)#inserting the elements to the first for DFS
                    ancestor.append((neighbor, current))
        #return none if no solution is found
        return None, len(frontier), len(visited)




    def solve(self, strategy):
            """
            Solves the yantra collection puzzle using the specified strategy.

            Args:
                strategy (str): The search strategy (BFS or DFS).
            """
            #lists for storing position,count,no of nodes
            finale_path=[self.start]
            starting_position=self.start
            target=self.revealed_yantra
            no_in_frontier=0
            no_in_explored=0
            temp_path=[]
            #exception error
            if strategy not in ["BFS","DFS"]:
                raise ValueError("Correct Strategy use karo bhai, ye sab mujhe pata nahi")
            #various strategy cases
            while target is not None:
                if strategy == "BFS":
                    temp_path, no_in_frontier, no_in_explored = self.bfs(starting_position, target)
                else: 
                    temp_path, no_in_frontier, no_in_explored = self.dfs(starting_position, target)
                #when no solution is found
                if temp_path is None:
                    return None, self.total_frontier_kids, self.total_explored_kids
                
                #taking path without repetitions
                finale_path+=temp_path[1:]
                self.total_explored_kids+=no_in_explored
                self.total_frontier_kids+=no_in_frontier
                #changing positions to next state and searching yantra
                starting_position=target
                self.reveal_next_yantra_or_exit()
                target=self.revealed_yantra
            
            #return all the final attributes
            return finale_path,self.total_frontier_kids,self.total_explored_kids    

            

if __name__ == "__main__":
    grid = [
        ['P', '.', '.', '#', 'Y2'],
        ['#', 'T', '.', '#', '.'],
        ['.', '.', 'Y1', '.', '.'],
        ['#', '.', '.', 'T', '.'],
        ['.', '.', '.', '.', 'E']
    ]

    game = YantraCollector(grid)
    strategy = "BFS"  
    solution, total_frontier, total_explored = game.solve(strategy)
    if solution:
        print("Solution Path:", solution)
        print("Total Frontier kids:", total_frontier)
        print("Total Explored kids:", total_explored)
    else:
        print("No solution found.")
