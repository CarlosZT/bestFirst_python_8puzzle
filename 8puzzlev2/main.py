from vertex import *
from puzzle import *

def verify(a, b):
        match = 0
        for _a, _b in zip(a,b):
            if _a == _b:
                match +=1
        return (9-match)

def insort(h, states, seeds):
    for j in range(1, len(h)):
        key = h[j]
        st_key = states[j]
        se_key = seeds[j]

        i = j - 1
        while i >= 0 and h[i] > key:
            h[i + 1] = h[i]
            states[i + 1] = states[i]
            seeds[i + 1] = seeds[i]
            i -= 1
        h[i + 1] = key
        states[i + 1] = st_key
        seeds[i + 1] = se_key
    return h, states, seeds

def format_state(state):
    result = ''
    for i in range(3):
        result += f'{state[i * 3: (i + 1) * 3]}\n'
    return result 

############################################################################
p = Puzzle()
test = Puzzle()
logs = False

pending = []
checked = []
steps = []

x0 = ['2', '8', '3',
      '1', '6', '4',
      '7', '#', '5']

x1 = ['2', '1', '6',
      '4', '#', '8',
      '7', '5', '3']

t = ['1', '2', '3',
     '8', '#', '4',
     '7', '6', '5']

p.assign_values(x1)
test.assign_values(p.grid_to_array())

r = Vertex()
r.value = p.grid_to_array()
r.seed = 'root'
r.depth = 0
r.score = verify(r.value, t)
current_vertex = r
second_best = None

max_iterations = 7500


print('Searching...')
for i in range(max_iterations):
      #Se verifica que el nodo actual no es el estado terminal
      if verify(current_vertex.value, t)==0:
            print('_______________________________________________')
            print(f'---Terminal---')
            print(f'Depth: {current_vertex.depth}, Score: {current_vertex.score}')
            print(format_state(current_vertex.value))

            #Para calcular el agoritmo que soluciona el puzzle, basta con preguntarle al nodo actual el movimiento que lo produjo (su 'seed')
            #Y repetir el proceso con su nodo padre hasta llegar a la raiz del arbol.
            steps = []
            while(current_vertex.parent):
                  steps.append(current_vertex.seed)
                  current_vertex = current_vertex.parent
            print('---Algorithm---')
            print(f'From: \n{format_state(r.value)}\n')

            #Ya obtenido el conjunto de pasos, solo le damos la vuelta para que estén en el orden para solucionar el puzzle partiendo del nodo raiz
            steps.reverse()
            j = 1
            for s in steps:
                  print(f'{j}. {s}')
                  j+=1
            print('---end---')
            break
      else:
            #Se calculan los estados sucesores (Se expande el vertice actual)
            p.assign_values(current_vertex.value)
            states, seeds = p.create_states()
            childs = []
            if logs:
                  print('_______________________________________________')
                  print(f'----- ST Calculated - Depth: {current_vertex.depth+1} -----')
                  for st, se in zip(states, seeds):
                        print(f'Seed: {se}\n{format_state(st)}')

            # Se verifica si alguno de los estados ya existe en pending o checked y se agregan a la cola de eliminación si es el caso.
            st_to_delete = []
            se_to_delete = []

            for st, se in zip(states, seeds):
                  if st in pending or st in checked:
                        st_to_delete.append(st)
                        se_to_delete.append(se)

            for st, se in zip(st_to_delete, se_to_delete):
                  states.remove(st)
                  seeds.remove(se)

            if len(states)==0:
                  last = pending.pop()
                  current_vertex = r.search_by_value(last)
                  second_best = r.search_by_value(pending[-1])
                  if logs:
                        print('--- Out of states---')
                        print(f'Getting from pending:')
                        print(f'Seed: {current_vertex.seed}, Score: {current_vertex.score}')
                        print(format_state(current_vertex.value))
                  continue

            

            #ya filtrados, se calcula la heuristica de cada estado candidato y se ordenan
            heuristics = []
            for st in states:
                  h = verify(st, t) + current_vertex.depth + 1
                  heuristics.append(h)

            heuristics, states, seeds = insort(heuristics, states, seeds)
            heuristics.reverse()
            states.reverse()
            seeds.reverse()

            #Se toma el mejor de todos los estados para continuar con la expansion y los demás se almacenan en pending
            #Ademas, el nodo actual se va al arreglo de checked y el mejor de esta iteracion toma su lugar
            
            # if logs: print('-----------------------------')
            for st, se, h in zip(states, seeds, heuristics):
                  current_vertex.childs.append(Vertex())
                  current_vertex.childs[-1].depth = current_vertex.depth + 1
                  current_vertex.childs[-1].value = st
                  current_vertex.childs[-1].seed = se
                  current_vertex.childs[-1].score = h
                  current_vertex.childs[-1].parent = current_vertex
                  
                #   if logs: print(f'---Added to the tree: \n{format_state(current_vertex.childs[-1].value)}')
            if logs:
                  print('-----------------------------')            
                  print(f'\n---- ST Available ----')
                  for c in current_vertex.childs:
                        print(f'Seed: {c.seed}, Score: {c.score}\n{format_state(c.value)}')

            checked.append(current_vertex.value)

            states.pop()
            
            if len(current_vertex.childs)>1:
                  second = current_vertex.childs[-2]
            current_vertex = current_vertex.childs[-1]
            

            for st in states:
                  pending.append(st)
            
            # if logs:
            #       print(f'--- Pending: {len(pending)}')
            #       print(f'Last: \n{format_state(pending[-1])}')

            #Nos aseguramos que este nodo sea un buen candidato respecto a la iteración anterior.
            if second_best:
                  if current_vertex.score > second_best.score:
                        if logs: print('--- Not the best candidate. Selecting second best...')
                        checked.append(current_vertex.value)
                        current_vertex = second_best
                        second_best = None
                        if current_vertex.value in pending:
                              pending.remove(current_vertex.value)
                            #   if logs:
                            #         print(f'--- Pending: {len(pending)}')
                            #         print(f'Last: \n{format_state(pending[-1])}')
                              
            else:
                  second_best = second
                  if logs:
                        print('--- Second best ---')
                        print(f'Seed: {second_best.seed}, Score: {second_best.score}')
                        print(format_state(second_best.value))
                        
            if logs:
                  print(f'\n---- ST Selected ----')
                  print(f'Seed: {current_vertex.seed}, Score: {current_vertex.score}\n{format_state(current_vertex.value)}')

if len(steps)==0:
      print('Not founded') 
else:
    
    #Si los pasos encontrados permiten llegar al estado marcado, entonces la solución es válida
    print('_____________________________')
    print('\nTesting solution...\n')

    for s in steps:
        test.move_value('#', s)
        if logs:
            print(f'Seed: {s}')
            print(format_state(test.grid_to_array()))
        
    if verify(test.grid_to_array(), t)==0:
        print('\n---Solution verified---')
    else:
        print('Invalid solution!')