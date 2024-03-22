import osmnx as ox
import networkx as nx


def matrix_min(lst, myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)


def delete(matrix, index1, index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix


def print_matrix(matrix):
    print("---------------")
    for i in range(len(matrix)):
        temp = ''
        for j in range(len(matrix)):
            if matrix[i][j] != float('inf'):
                temp += '\t' + str(int(matrix[i][j]))
            else:
                temp += '\t' + str(matrix[i][j])
        print(temp)
    print("---------------")


def find_existing_paths(new_point, existing_paths):
    start_list = [cur_path[0] for cur_path in existing_paths]
    end_list = [cur_path[1] for cur_path in existing_paths]
    if (new_point[1] in start_list) and (new_point[0] in end_list):
        cur_start_index = end_list.index(new_point[0])
        cur_end_index = start_list.index(new_point[1])
        existing_paths[cur_start_index] = (existing_paths[cur_start_index][0], existing_paths[cur_end_index][1])
        del existing_paths[cur_end_index]
    elif (new_point[1] in start_list) and (new_point[0] not in end_list):
        cur_index = start_list.index(new_point[1])
        existing_paths[cur_index] = (new_point[0], end_list[cur_index])
    elif (new_point[1] not in start_list) and (new_point[0] in end_list):
        cur_index = end_list.index(new_point[0])
        existing_paths[cur_index] = (start_list[cur_index], new_point[1])
    else:
        existing_paths.append((new_point[0], new_point[1]))
    return existing_paths

def set_inf_values(matrix, row_numbers, col_numbers, existing_paths):
    for cur_path in existing_paths:
        row_point = cur_path[0]-1
        col_point = cur_path[1]-1
        if (row_point in col_numbers) and (col_point in row_numbers):
            NewIndex1 = row_numbers.index(col_point)
            NewIndex2 = col_numbers.index(row_point)
            matrix[NewIndex1][NewIndex2] = float('inf')
    return matrix


def find_path(graph, nodes_list, optimizer):
    n = len(nodes_list)
    my_graph = nx.Graph()
    matrix = []
    path_matrix = []
    H = 0
    path_lenght = 0
    row_numbers = []
    col_numbers = []
    res = []
    result = []
    start_matrix = []
    existing_paths = []

    for i in range(n):
        row_numbers.append(i)
        col_numbers.append(i)
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
        start_matrix.append(matrix[i].copy())

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
                    tmp = matrix_min(matrix[i], j) + matrix_min((row[j] for row in matrix), i)
                    if tmp >= NullMax:
                        NullMax = tmp
                        index1 = i
                        index2 = j

        new_point = (row_numbers[index1] + 1, col_numbers[index2] + 1)
        existing_paths = find_existing_paths(new_point, existing_paths)
        matrix = set_inf_values(matrix, row_numbers, col_numbers, existing_paths)
        res.append(row_numbers[index1] + 1)
        res.append(col_numbers[index2] + 1)

        del row_numbers[index1]
        del col_numbers[index2]
        matrix = delete(matrix, index1, index2)
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
            path_lenght += start_matrix[result[i] - 1][result[i + 1] - 1]
            path_lenght += start_matrix[result[i + 1] - 1][result[0] - 1]
        else:
            path_lenght += start_matrix[result[i] - 1][result[i + 1] - 1]

    result.append(result[-1])
    result.append(result[0])

    result_path = []
    for i in range(0, len(result) - 1, 2):
        start_index = int(result[i])
        end_index = int(result[i + 1])
        new_path = path_matrix[start_index - 1][end_index - 1]
        deleted_element = new_path.pop(len(new_path) - 1)
        result_path += new_path
    print(result_path)
    return result_path
