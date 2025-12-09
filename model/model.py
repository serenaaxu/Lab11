import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.id_map = {}

    def build_graph(self, year: int):
        """
        Costruisce il grafo (self.G) dei rifugi considerando solo le connessioni
        con campo `anno` <= year passato come argomento.
        Quindi il grafo avrà solo i nodi che appartengono almeno ad una connessione, non tutti quelli disponibili.
        :param year: anno limite fino al quale selezionare le connessioni da includere.
        """
        # TODO
        self.G.clear()

        # 1. Recupero tutti i rifugi e creo la mappa id -> Oggetto
        all_rifugi = DAO.get_all_rifugi()
        self.id_map = {r.id: r for r in all_rifugi}

        # 2. Recupero gli archi validi
        edges = DAO.get_edges_by_year(year)

        # 3. Aggiungo gli archi al grafo.
        # Aggiungo gli OGGETTI Rifugio.
        for id1, id2 in edges:
            if id1 in self.id_map and id2 in self.id_map:
                node_a = self.id_map[id1]
                node_b = self.id_map[id2]
                self.G.add_edge(node_a, node_b)

    def get_nodes(self):
        """
        Restituisce la lista dei rifugi presenti nel grafo.
        :return: lista dei rifugi presenti nel grafo.
        """
        # TODO
        return list(self.G.nodes())

    def get_num_neighbors(self, node):
        """
        Restituisce il grado (numero di vicini diretti) del nodo rifugio.
        :param node: un rifugio (cioè un nodo del grafo)
        :return: numero di vicini diretti del nodo indicato
        """
        # TODO
        return self.G.degree(node)

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse del grafo.
        :return: numero di componenti connesse
        """
        # TODO
        return nx.number_connected_components(self.G)

    def get_reachable(self, start):
        """
        Deve eseguire almeno 2 delle 3 tecniche indicate nella traccia:
        * Metodi NetworkX: `dfs_tree()`, `bfs_tree()`
        * Algoritmo ricorsivo DFS
        * Algoritmo iterativo
        per ottenere l'elenco di rifugi raggiungibili da `start` e deve restituire uno degli elenchi calcolati.
        :param start: nodo di partenza, da non considerare nell'elenco da restituire.

        ESEMPIO
        a = self.get_reachable_bfs_tree(start)
        b = self.get_reachable_iterative(start)
        b = self.get_reachable_recursive(start)

        return a
        """

        # TODO
        # Tecnica 1: NetworkX BFS Tree
        path_bfs = self._get_reachable_bfs(start)

        # Tecnica 2: Algoritmo Iterativo DFS (Stack)
        # path_dfs = self._get_reachable_iterative_dfs(start)

        return path_bfs

    def _get_reachable_bfs(self, start):
        # Restituisce un Digrafo (albero), prendiamo i nodi
        tree = nx.bfs_tree(self.G, start)
        nodes = list(tree.nodes)
        nodes.remove(start)  # Rimuovo il nodo di partenza
        return nodes

    def _get_reachable_iterative_dfs(self, start):
        """Algoritmo iterativo DFS usando una lista come Stack"""
        visited = []
        stack = [start]

        while stack:
            node = stack.pop()  # Prendo l'ultimo
            if node not in visited:
                visited.append(node)
                # Aggiungo i vicini non visitati
                # Inverto l'ordine dei vicini se voglio simulare l'ordine standard
                neighbors = list(self.G.neighbors(node))
                for n in neighbors:
                    if n not in visited:
                        stack.append(n)

        visited.remove(start)
        return visited
