import osmnx as ox
import networkx as nx
from Routing.routing import find_path


print('Загружаю карту')
place = f'Москва, Россия'
mode = 'walk'
optimizer = 'length'
#graph = ox.graph_from_place(place, network_type=mode)
print('Карта загружена')


def parse_coordinates(coordinates_list):
    global graph
    nodes_list = []
    for point in coordinates_list:
        if point is not None:
            nearest_node = ox.distance.nearest_nodes(graph, point[1], point[0])
            nodes_list.append(nearest_node)
    return nodes_list


def get_map(coordinates):
    global graph
    nodes_list = parse_coordinates(coordinates)
    result_path = find_path(graph, nodes_list, optimizer)
    shortest_route_map = ox.plot_route_folium(graph, result_path)
    return shortest_route_map
