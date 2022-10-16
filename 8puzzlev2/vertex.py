from re import search


class Vertex():
    def __init__(self) -> None:
        self.childs = []
        self.value = None
        self.score = 0
        self.parent = None
        self.seed = None
        self.depth = None
        
    def add_child(self, v):
        self.childs.append(v)

    def search_by_value(self, v):
        node = None
        # print('------------------------------------------------------')
        # print(f'value:  {self.value}')
        # print(f'target: {v}')
        # print('------------------------------------------------------')
        match = 0
        for v0, v1 in zip(self.value, v):
            if v0==v1:
                match+=1

        if match==9:
            # print('Founded')
            node = self
            return node
        else:
            for c in self.childs:
                node = c.search_by_value(v)
                if node:
                    return node


    def visit_childs(self):
        for v in self.childs:
            print(f"---------------------------\nChild (Seed: {v.seed}):\n{v.value} \nParent: (Seed: {self.seed})\n{self.value}")
            v.visit_childs()
