import osmnx as ox
import networkx as nx
import folium
from Routing.routing import find_path
from WebSite.models import Attractions


print('Загружаю карту')
place = f'Москва, Россия'
mode = 'walk'
optimizer = 'length'
#graph = ox.graph_from_place(place, network_type=mode)
graph = ox.load_graphml('mos.graphml')
print('Карта загружена')


def parse_coordinates(coordinates_list):
    global graph
    nodes_list = []
    for point in coordinates_list:
        print(point)
        nearest_node = ox.distance.nearest_nodes(graph, float(point['longitude']), float(point['latitude']))
        nodes_list.append(nearest_node)
    return nodes_list


def get_nearest_node(longitude, latitude):
    nearest_node = ox.distance.nearest_nodes(graph, float(longitude), float(latitude))
    return nearest_node


def set_nodes():
    object_list = Attractions.objects.filter()
    list_len = len(object_list)
    for i in range(list_len):
        cur_id = object_list[i].id
        if object_list[i].nearest_node is None:
            attraction = Attractions.objects.get(id=cur_id)
            attraction.nearest_node = get_nearest_node(attraction.longitude, attraction.latitude)
            attraction.save()


def get_map(nodes_list, object_list):
    global graph
    result_path = find_path(graph, nodes_list, optimizer)
    shortest_route_map = ox.plot_route_folium(graph, result_path,
                                              tiles='openstreetmap')
    for cur_object in object_list:
        iframe = folium.IFrame(html=f"<p>{cur_object['short_description']}</p>", width=200, height=200)
        folium.Marker(
            location=[cur_object['latitude'], cur_object['longitude']],
            popup=folium.Popup(iframe, max_width=2650),
            tooltip=cur_object['name']).add_to(shortest_route_map)
    return shortest_route_map


def update_map(object_list):
    global graph
    map_all = folium.Map(location=[55.7535926, 37.6214893], zoom_start=14, tiles="openstreetmap")
    for cur_object in object_list:
        iframe = folium.IFrame(html=f"<p>{cur_object['short_description']}</p>", width=200, height=200)
        folium.Marker(
            location=[cur_object['latitude'], cur_object['longitude']],
            popup=folium.Popup(iframe, max_width=2650),
            tooltip=cur_object['name']).add_to(map_all)
    return map_all
