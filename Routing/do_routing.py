import osmnx as ox
import networkx as nx
from Routing.routing import find_path


def parse_coordinates(graph, coordinates_list):
    nodes_list = []
    for point in coordinates_list:
        if point is not None:
            nearest_node = ox.distance.nearest_nodes(graph, point[1], point[0])
            nodes_list.append(nearest_node)
    return nodes_list


def get_map(city, coordinates):
    place = f'{city}, Россия'
    mode = 'walk'
    optimizer = 'length'
    graph = ox.graph_from_place(place, network_type=mode)
    nodes_list = parse_coordinates(graph, coordinates)
    result_path = find_path(graph, nodes_list, optimizer)
    shortest_route_map = ox.plot_route_folium(graph, result_path)
