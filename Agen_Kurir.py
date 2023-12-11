import csv
import random
import sys
from queue import PriorityQueue
from colorama import init, Fore, Style

init(autoreset=True)
class Colors:
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    CBLACK = "\33[30m"
    CRED = "\33[31m"
    CGREEN = "\33[32m"
    CYELLOW = "\33[33m"
    CBLUE = "\33[34m"
    CVIOLET = "\33[35m"
    CBEIGE = "\33[36m"
    CWHITE = "\33[37m"
    CGREY = "\33[90m"
    CRED2 = "\33[91m"
    CGREEN2 = "\33[92m"
    CYELLOW2 = "\33[93m"
    CBLUE2 = "\33[94m"
    CVIOLET2 = "\33[95m"
    CBEIGE2 = "\33[96m"
    CWHITE = Fore.WHITE + Style.BRIGHT

class Stack:
    def __init__(self):
        self.data = ['*'] * 10
        self.top = -1

    def push(self, input_char):
        self.top += 1
        self.data[self.top] = input_char

    def pop(self):
        y = self.data[self.top]
        self.top -= 1
        return y

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top == 5

    def print_stack(self):
        for i in range(self.top + 1):
            print(self.data[i], end=" ")

def entry():
    x = """
   @@@       @@@@      @@@@@@@@@       @@@@@@@@@   @@@      @@@   @@@@@@@@@    @@@@@@@@@    @@@@@@@@@   @@@@@@@@   @@@@@@@@  
   @@@     @@@  @@@    @@@             @@@         @@@      @@@   @@@    @@@   @@@    @@@   @@@        @@         @@ 
   !@@     @@!  @!@    @@@             @@@         @@@      @@@   @@@    @@@   @@@    @@@   @@@        @@@        @@@
   !@@     @@!  @!@    @!@             @!@          @!!@  @!!@    @!@    @@    @!@    @@    @!@           @@!!@      @@!!@ 
   !!@     @!!  !@!    !@!!@!!@!       !@!!@!!@!       @!!@       !@!@@@!!     @!!@@@!!     !@!!@!!@!        !@@!       !@@!
   :!@     @!:  !:!    !@!             !@!          @!!@  @!!@    !@!          !@!   !!     !@!              !@@!       !@@!
!  :!      !!:  !:!    !!!             !!!         !!!      !!!   !!!          !!!    !!    !!!              !!!        !!!
:: ::      :::  :::    :::             :::         :::      :::   :::          :::    :::   :::              ::         ::
 :::       :::  :::    :::::::::       :::::::::   :::      :::   :::          :::    :::   :::::::::  :::::::    :::::::
    """
    for c in x:
        print(Colors.CBLUE + c, end='', flush=True)

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

    bold_start = Colors.BOLD
    bold_end = Colors.ENDC
    yellow_start = Colors.CYELLOW
    yellow_end = Colors.ENDC
    red_start = Colors.CRED
    red_end = Colors.ENDC

    print()
    print('-' * 45)
    print(f'{bold_start}Rute terbaik yang dilalui: {bold_end}')
    print()
    count = 0
    while count < (length - 2):
        km = city_to_neighbor(graph, route[count], route[count + 1])
        print(f'{yellow_start}{route[count]} -> {route[count + 1]} {yellow_end} jarak = {red_start}{km} KM{red_end}')
        count += 1

    print('-' * 45)
    print(f'{bold_start}Jarak total: {red_start}{distance} KM{red_end}')
    print('-' * 45)
    return

def main():
    entry()
    print("\n")

if __name__ == "__main__":
    main()
    
    while True:
        try:
            inputFile = input(f"{Colors.CWHITE}Isi nama file road map(csv): {Style.RESET_ALL}")
            test = open(inputFile, 'r').readlines()
        except FileNotFoundError:
            print(f"{Colors.CWHITE}Salah format file atau path file, coba lagi!{Style.RESET_ALL}")
        else:
            break

    graph = build_graph(inputFile)

    while True:
        try:
            start_agen = input(f"{Colors.CWHITE}Titik start kurir agen: {Style.RESET_ALL}")
            if start_agen not in graph:
                raise AgenKurirNotFound(start_agen)
            break
        except AgenKurirNotFound:
            print(f"{Colors.CWHITE}Titik start tersebut tidak terdapat pada map!{Style.RESET_ALL}")

    while True:
        try:
            tujuan_agen = input(f"{Colors.CWHITE}Titik tujuan kurir agen: {Style.RESET_ALL}")
            if tujuan_agen not in graph:
                raise AgenKurirNotFound(tujuan_agen)
            break
        except AgenKurirNotFound:
            print(f"{Colors.CWHITE}Titik tujuan tersebut tidak terdapat pada map!{Style.RESET_ALL}")

    uniform_cost_search(graph, start_agen, tujuan_agen)

