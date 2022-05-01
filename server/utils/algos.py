import osmnx as ox
import networkx as nx
import numpy as np
import copy
import json
import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming
from sklearn.cluster import SpectralClustering
from math import sin, cos, sqrt, radians, atan2


def Min(lst,myindex):
    return min(x for idx, x in enumerate(lst) if idx != myindex)

#функция удаления нужной строки и столбцах
def Delete(matrix,index1,index2):
    del matrix[index1]
    for i in matrix:
        del i[index2]
    return matrix


def get_dist(coos1, coors2):
    R = 6373.0
    lat1 = radians(coos1[0])
    lon1 = radians(coos1[1])
    lat2 = radians(coors2[0])
    lon2 = radians(coors2[1])
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance



def get_shortest_path(G, orig=[59.9454552627266, 30.265246173508295],
                      dest=[59.9280917384679, 30.290336197625937]):
    R = 6373.0

    # ox.config(use_cache=True, log_console=True)

    # define the place query
    # query = {'city': 'Saint-Petersburg'}

    # G = ox.graph_from_place(query, network_type='drive')

    orig_id = ox.distance.get_nearest_node(G, orig)
    dest_id = ox.distance.get_nearest_node(G, dest)

    shortest_path_ids = nx.shortest_path(G, orig_id, dest_id)
    shortest_path_coors = [orig]
    for node in shortest_path_ids:
        shortest_path_coors.append([G.nodes[node]['y'], G.nodes[node]['x']])
    shortest_path_coors.append(dest)
    distance = 0

    for i in range(len(shortest_path_coors)-1):
        distance += get_dist(shortest_path_coors[i], shortest_path_coors[i+1])

    return shortest_path_coors, distance


def clustering(coors:dict):  
    query = {'city': 'Saint-Petersburg'}

    G = ox.graph_from_place(query, network_type='drive')

    for c in coors:
        if 'clusters' in c.keys():
            clusters = c['clusters']

    points = {}
    for data in coors:
        if 'id' in sorted(data.keys()):
            points[data['id']] = [data['position']['x'], data['position']['y']]

    keys_of_points = sorted(points.keys())
    ln_points = len(keys_of_points)
    matrix_of_dist = np.zeros((ln_points, ln_points))
    for row in range(ln_points):
        for col in range(ln_points):
            if row == col:
                matrix_of_dist[row, col] = 0
            else:
                _, matrix_of_dist[row, col] = \
                    get_shortest_path(G, points[keys_of_points[row]], points[keys_of_points[col]])

    clustering = SpectralClustering(n_clusters=clusters,  assign_labels='discretize', \
                                          random_state=0).fit(matrix_of_dist)
    
    matching_c = {x: y for x, y in zip(keys_of_points[1:], clustering.labels_[1:])}
    result = []
    for c in range(clusters):
        result.append([])
        for k, v in matching_c.items():
            if v == c:
                result[c].append(k)

    return result, matrix_of_dist.tolist(), keys_of_points


def com(clusters:list, matrix:np.array, keys_of_points:list, coors:dict):
    final_result = []
    for cluster in clusters:
        matrix_cluster = copy.deepcopy(matrix)
        inds = []
        for point in cluster:
            inds.append(keys_of_points.index(point))
        # print(f'points index: {inds}')
        # print(f'cluser: {cluster}')

        # print(f'len: {len(keys_of_points)}')
        for i in range(len(keys_of_points)-1, 0, -1):
            # print(i)
            # print(keys_of_points[i])
            if keys_of_points[i] not in inds:
                # print('YEEEEP')
                matrix_cluster = Delete(matrix_cluster, keys_of_points[i], keys_of_points[i])

        # for i in range(len(matrix_cluster[0])): 
        #     matrix_cluster[i][i]=float('inf')
        permutation, distance = solve_tsp_dynamic_programming(np.asarray(matrix_cluster))
        final_result.append((inds, permutation))
    out_data = []
    for k in final_result:
        dict_out = {}
        for ind1, ind2 in zip(k[0], k[1]):
            dict_out[ind1] = ind2
        out_data.append(dict_out)
    return out_data


def algos(json_in):
    # json_in = json.load(open('dataset2.json'))
    clusters, matrix, keys = clustering(json_in)
    commi = com(clusters, matrix, keys, json_in)
    # print(commi)
    k = -1
    json_out = []
    for cl in commi:
        k += 1
        for key in cl:
            for d in json_in:
                if d['id'] == key:
                    d['numberOfClaster'] = k
                    d['numberInClaster'] = cl[key]
                    json_out.append(d)
                    break
    for d in json_in:
        if d['id'] == 0:
            json_out.append(d)
            break    
    return json_out