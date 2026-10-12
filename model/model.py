import networkx as nx
from itertools import combinations

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._nodes = []
        self._idMap = {}
        self._solBest = []
        self._pesoBest = 0

    def getGeneri(self):
        # restituisce i generi dal DAO
        return DAO.getGeneri()

    def getAnni(self):
        return DAO.getAnni()

    # -------------------- PUNTO 1 --------------------

    def buildGraph(self, genere, anno, k):
        self._grafo.clear()
        self._idMap = {}
        self._nodes = DAO.getNodi(genere,anno)
        for n in self._nodes:
            self._idMap[n.id] = n
        self._grafo.add_nodes_from(self._nodes)


        for m1,m2 in combinations(self._nodes, 2):
            giorni = abs((m1.date_published-m2.date_published).days)
            if 1<=giorni<=k:
                peso = round((m1.avg_rating + m2.avg_rating) / giorni, 2)
                if m1.date_published < m2.date_published:
                    self._grafo.add_edge(m1,m2,weight=peso)
                if m1.date_published > m2.date_published:
                    self._grafo.add_edge(m2, m1, weight=peso)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

    def getTop5(self):
        # i 5 archi di peso maggiore come (film1, film2, peso),
        # ordinati per peso decrescente, poi titolo partenza, poi titolo arrivo
        archi = [(u,v,dati["weight"]) for u,v,dati in self._grafo.edges(data=True)]
        archi.sort(key=lambda x: (-x[2],x[0].title,x[1].title))
        return archi[:5]




    def getNodiOrdinati(self):
        # nodi in ordine alfabetico di titolo, per ddFilm
        nodi = [n for n in self._grafo.nodes()]
        nodi.sort(key=lambda x: (x.title, x.id))
        return nodi

    def getNumRaggiungibili(self, film):
        """
        La consegna chiede tutti i film raggiungibili
        seguendo gli archi, con un cammino di lunghezza
        qualsiasi: anche i successori dei successori, e così via.
        """
        return len(nx.descendants(self._grafo, film))


    def getPesoArco(self, u, v):
        # peso dell'arco u -> v, serve al controller per stampare
        return self._grafo[u][v]["weight"]

    """
    PUNTO 2
    a. Bottone "Percorso": con un algoritmo RICORSIVO trovare il cammino di PESO MASSIMO che
       - parte dal film selezionato in ddFilm;
       - segue il VERSO degli archi (da un film a uno uscito dopo);
       - ha i pesi degli archi STRETTAMENTE DECRESCENTI (ogni arco pesa meno del precedente);
       - non passa due volte per lo stesso film.

    b. Stampare:
       - il cammino: ogni film con la sua data di uscita e il peso dell'arco verso il successivo;
       - il numero di film;
       - il peso totale (2 decimali).
       Se il film non ha archi uscenti: messaggio.
    """

    def getPercorso(self, film):
        self._solBest = []
        self._pesoBest = -1
        self._ricorsione([film], 0, float("inf"))
        return self._solBest, self._pesoBest


    def _ricorsione(self,parziale,peso,ultimoPeso):
        if peso > self._pesoBest:
            self._solBest = list(parziale)
            self._pesoBest = peso

        ultimo = parziale[-1]

        for v in self._grafo.successors(ultimo):
            pesoArco = self._grafo[ultimo][v]["weight"]
            if pesoArco < ultimoPeso and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale,peso+pesoArco,pesoArco)
                parziale.pop()
