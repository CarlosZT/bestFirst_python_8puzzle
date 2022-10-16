class Node():
    def __init__(self):
        self.up = None
        self.down = None
        self.right = None
        self.left = None
        self.value = None

    def set_right(self, node):
        self.right = node
        node.left = self

    def set_left(self, node):
        self.left = node
        node.right = self

    def set_up(self, node):
        self.up = node
        node.down = self

    def set_down(self, node):
        self.down = node
        node.up = self

class Grid():
    def __init__(self, order):
        self.order = order
        self.size = order * order
        self.node = []
        for i in range(0, self.size):
            self.node.append(Node())

        #Conexiones en horizontal
        self.node[0].set_right(self.node[1])
        self.node[1].set_right(self.node[2])
        self.node[3].set_right(self.node[4])
        self.node[4].set_right(self.node[5])
        self.node[6].set_right(self.node[7])
        self.node[7].set_right(self.node[8])

        #Conexiones en vertical
        self.node[0].set_down(self.node[3])
        self.node[3].set_down(self.node[6])
        self.node[1].set_down(self.node[4])
        self.node[4].set_down(self.node[7])
        self.node[2].set_down(self.node[5])
        self.node[5].set_down(self.node[8])
        

    def show_grid(self):
        print(f'------------------')
        for i in range(0, self.order):
            print(f'|{self.node[0 + (3 * i)].value}\t{self.node[1 + (3 * i)].value}\t{self.node[2 + (3 * i)].value}|')
        print(f'------------------')

    def assign_values(self, values):
        for v, n in zip(values, self.node):
            n.value = v

    def get_node_by_value(self, v):
        for n in self.node:
            if n.value == v:
                return n

    def grid_to_array(self):
        r = []
        for n in self.node:
            r.append(n.value)
        return r

    def move_value(self, value, dir):
        node = None
        for n in self.node:
            if n.value == value:
                node = n
                break

        if node == None:
            print(f'That value "{value}" does\'nt exists in the grid')
            return

        if dir == 'up' and node.up != None:
            aux = node.up.value
            node.up.value = node.value
            node.value = aux
            return         
            
        if dir == 'down'and node.down != None:
            aux = node.down.value
            node.down.value = node.value
            node.value = aux 
            return 

        if dir == 'left'and node.left != None:
            aux = node.left.value
            node.left.value = node.value
            node.value = aux  
            return

        if dir == 'right'and node.right != None:
            aux = node.right.value
            node.right.value = node.value
            node.value = aux
            return

        print(f'Error, this "{dir}" ain\'t a valid direction')