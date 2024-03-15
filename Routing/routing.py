import osmnx as ox
import networkx as nx


def Min(lst, myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)


def Delete(matrix, index1, index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix


def find_path(graph, nodes_list, optimizer):
    n = len(nodes_list)
    my_graph = nx.Graph()
    matrix = []
    path_matrix = []
    H = 0
    PathLenght = 0
    Str = []
    Stb = []
    res = []
    result = []
    StartMatrix = []

    for i in range(n):
        Str.append(i)
        Stb.append(i)
        matrix.append([float('inf') for x in range(n)])
        path_matrix.append(['' for x in range(n)])

    for i in range(n - 1):
        for j in range(n - 1, i, -1):
            cur_shortest_path = nx.shortest_path(graph, nodes_list[i], nodes_list[j], weight=optimizer)
            cur_shortest_length = nx.path_weight(graph, cur_shortest_path,  weight=optimizer)
            my_graph.add_edge(nodes_list[i], nodes_list[j], weight=float(cur_shortest_length))
            matrix[i][j] = cur_shortest_length
            matrix[j][i] = cur_shortest_length
            path_matrix[i][j] = cur_shortest_path
            path_matrix[j][i] = list(reversed(cur_shortest_path))

    for i in range(n):
        StartMatrix.append(matrix[i].copy())

    while True:
        for i in range(len(matrix)):
            temp = min(matrix[i])
            H += temp
            for j in range(len(matrix)):
                matrix[i][j] -= temp

        for i in range(len(matrix)):
            temp = min(row[i] for row in matrix)
            H += temp
            for j in range(len(matrix)):
                matrix[j][i] -= temp

        NullMax = 0
        index1 = 0
        index2 = 0
        tmp = 0
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if matrix[i][j] == 0:
                    tmp = Min(matrix[i], j) + Min((row[j] for row in matrix), i)
                    if tmp >= NullMax:
                        NullMax = tmp
                        index1 = i
                        index2 = j

        res.append(Str[index1] + 1)
        res.append(Stb[index2] + 1)

        oldIndex1 = Str[index1]
        oldIndex2 = Stb[index2]
        if oldIndex2 in Str and oldIndex1 in Stb:
            NewIndex1 = Str.index(oldIndex2)
            NewIndex2 = Stb.index(oldIndex1)
            matrix[NewIndex1][NewIndex2] = float('inf')
        del Str[index1]
        del Stb[index2]
        matrix = Delete(matrix, index1, index2)
        if len(matrix) == 1:
            break

    for i in range(0, len(res) - 1, 2):
        if res.count(res[i]) < 2:
            result.append(res[i])
            result.append(res[i + 1])

    for i in range(0, len(res) - 1, 2):
        for j in range(0, len(res) - 1, 2):
            if result[len(result) - 1] == res[j]:
                result.append(res[j])
                result.append(res[j + 1])

    for i in range(0, len(result) - 1, 2):
        if i == len(result) - 2:
            PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]
            PathLenght += StartMatrix[result[i + 1] - 1][result[0] - 1]
        else:
            PathLenght += StartMatrix[result[i] - 1][result[i + 1] - 1]

    result.append(result[-1])
    result.append(result[0])

    result_path = []
    for i in range(0, len(result) - 1, 2):
        start_index = int(result[i])
        end_index = int(result[i + 1])
        new_path = path_matrix[start_index - 1][end_index - 1]
        deleted_element = new_path.pop(len(new_path) - 1)
        result_path += new_path
    return result_path
