class Environment:
    def __init__(self):
        # Inicializa o grid com sujeira nos quadrados C, F, H, I, K, M e O
        self.grid = [
            ['clean', 'clean', 'dirty', 'clean'],  # A B C D
            ['clean', 'dirty', 'clean', 'dirty'],  # E F G H
            ['dirty', 'clean', 'dirty', 'clean'],  # I J K L
            ['dirty', 'clean', 'dirty', 'clean']   # M N O P
        ]
        self.agent_location = (0, 0)  # Localização inicial do agente
        self.dirt_bag = 0

    def is_clean(self):
        return all(cell == 'clean' for row in self.grid for cell in row)

    def print_grid(self):
        for row in self.grid:
            print(row)
        print()

class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.energy = 100
        self.unvisited_cells = {(i, j) for i in range(4) for j in range(4)}
        self.moves = 0  # Adiciona contador de movimentos

    def move(self, direction):
        x, y = self.environment.agent_location
        if direction == 'N':
            x -= 1
        elif direction == 'S':
            x += 1
        elif direction == 'E':
            y += 1
        elif direction == 'W':
            y -= 1
        self.environment.agent_location = (x, y)
        self.unvisited_cells.discard((x, y))
        self.energy -= 1
        self.moves += 1  # Incrementa contador de movimentos

    def suck_dirt(self):
        x, y = self.environment.agent_location
        self.environment.grid[x][y] = 'clean'
        self.environment.dirt_bag += 1
        self.energy -= 1
        self.moves += 1  # Incrementa contador de movimentos ao aspirar sujeira

    def empty_bag(self):
        self.environment.dirt_bag = 0

    def go_home(self):
        route = self.calculate_route_to_home()
        for move in route:
            self.move(move)

    def choose_direction(self):
        x, y = self.environment.agent_location
        possible_directions = []

        if x < 3 and (x + 1, y) in self.unvisited_cells:
            possible_directions.append('S')
        if y < 3 and (x, y + 1) in self.unvisited_cells:
            possible_directions.append('E')
        if x > 0 and (x - 1, y) in self.unvisited_cells:
            possible_directions.append('N')
        if y > 0 and (x, y - 1) in self.unvisited_cells:
            possible_directions.append('W')

        if possible_directions:
            return possible_directions[0]
        else:
            return 'N'  # Caso padrão, se todas as opções acima falharem

    def calculate_route_to_home(self):
        x, y = self.environment.agent_location
        route = []

        while x > 0:
            route.append('N')
            x -= 1
        while y > 0:
            route.append('W')
            y -= 1

        return route

    def act(self):
        actions = []
        visited_cells = set()

        while not self.environment.is_clean() and self.energy > 0:
            x, y = self.environment.agent_location

            if self.environment.grid[x][y] == 'dirty':
                self.suck_dirt()
                actions.append('suck_dirt')
            else:
                direction = self.choose_direction()
                self.move(direction)
                actions.append('move_' + direction)

            visited_cells.add((x, y))

            if self.environment.dirt_bag == 10:
                return_to_cleaning_position = self.environment.agent_location
                route_to_home = self.calculate_route_to_home()
                actions.extend(['move_' + move for move in route_to_home])
                self.go_home()
                self.empty_bag()
                visited_cells.clear()  # Limpa o conjunto de células visitadas
                self.environment.agent_location = return_to_cleaning_position

        # Se ainda houver sujeira, retorna para casa
        if not self.environment.is_clean():
            route_to_home = self.calculate_route_to_home()
            actions.extend(['move_' + move for move in route_to_home])
            self.go_home()

        # Retorna para a posição inicial após a limpeza
        route_to_home = self.calculate_route_to_home()
        actions.extend(['move_' + move for move in route_to_home])
        self.go_home()

        print(f"Lixo na sacola: {self.environment.dirt_bag}")  # Mostra quantidade de lixo na sacola
        print(f"Movimentos realizados: {self.moves}")  # Mostra quantidade de movimentos realizados
        print(f"Movimentos restantes: {self.energy}")  # Mostra quantidade de movimentos restantes

        return actions

# Exemplo de uso
env = Environment()
agent = Agent(env)
actions = agent.act()
print(actions)
