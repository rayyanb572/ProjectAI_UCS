import csv
from queue import PriorityQueue

class AgenKurirNotFound(Exception):
    def __init__(self, agen):
        print("%s tidak ada pada map" % agen)


def build_graph(path):

    file = open(path, 'r')
    routes = {}
    next(file)
    for row in file:
        row = row.split(',')
        routes.setdefault(row[0], []).append((row[1], row[2]))
        routes.setdefault(row[1], []).append((row[0], row[2]))

    file.close()
    return routes


def uniform_cost_search(graph, start_agen, tujuan_agen):

    visited = set()
    route = []
    priority_queue = PriorityQueue()
    priority_queue.put((0, [start_agen]))

    while priority_queue:

        if priority_queue.empty():
            print('distance: infinity \nroute: \nnone')
            break

        distance, route = priority_queue.get()
        agen = route[len(route) - 1]

        if agen not in visited:
            visited.add(agen)

            if agen == tujuan_agen:
                route.append(distance)
                display_route(graph, route)
                return route

        childs = graph[agen]
        neighbor = [i[0] for i in childs]

        for i in neighbor:
            if i not in visited:

                totaldistance = distance + float(city_to_neighbor(graph, agen, i))
                temp = route[:]
                temp.append(i)
                priority_queue.put((totaldistance, temp))

    return priority_queue


def city_to_neighbor(graph, current, neighbor):
    index = [i[0] for i in graph[current]].index(neighbor)
    return float(graph[current][index][1].replace(',', ''))


def display_route(graph, route):
    length = len(route)
    distance = route[-1]

    bold_start = "\033[1m"
    bold_end = "\033[0m"
    
    print()
    print('-' * 45) 
    print(f'{bold_start}Rute terbaik yang dilalui: {bold_end}')
    print()
    count = 0
    while count < (length - 2):
        km = city_to_neighbor(graph, route[count], route[count + 1])
        print('%s -> %s %s KM' % (route[count], route[count + 1], km))
        count += 1

    print('-' * 45)
    print(f'{bold_start}Jarak total: {distance} KM{bold_end}')
    print('-' * 45)
    return


if __name__ == "__main__":

    while True:
        try:
            inputFile = input("Isi nama file road map(csv): ")
            test = open(inputFile, 'r').readlines()
        except FileNotFoundError:
            print("Salah format file atau path file , coba lagi!")
        else:
            break

    graph = build_graph(inputFile)

    while True:
        try:
            start_agen = input("Titik start kurir agen: ")
            if start_agen not in graph:
                raise AgenKurirNotFound(start_agen)
            break
        except AgenKurirNotFound:
            print("Titik start tersebut tidak terdapat pada map!")

    while True:
        try:
            tujuan_agen = input("Titik tujuan kurir agen: ")
            if tujuan_agen not in graph:
                raise AgenKurirNotFound(tujuan_agen)
            break
        except AgenKurirNotFound:
            print("Titik tujuan tersebut tidak terdapat pada map!")

    uniform_cost_search(graph, start_agen, tujuan_agen)
