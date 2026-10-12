import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDD(self):
        for g in self._model.getGeneri():
            self._view._ddGenere.options.append(ft.dropdown.Option(g))
        for a in self._model.getAnni():
            self._view._ddAnno.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        genere = self._view._ddGenere.value
        anno = self._view._ddAnno.value
        if genere is None or anno is None:
            self._errore("Seleziona genere e anno!")
            return
        try:
            k = int(self._view._txtK.value)
        except (ValueError, TypeError):
            self._errore("K deve essere un intero!")
            return
        if k < 1:
            self._errore("K deve essere almeno 1!")
            return

        self._model.buildGraph(genere, int(anno), k)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {genere} {anno}, K = {k}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        self._view.txt_result.controls.append(ft.Text("I 5 archi di peso maggiore:"))
        for f1, f2, peso in self._model.getTop5():
            self._view.txt_result.controls.append(ft.Text(f"{f1} -> {f2}: {peso}"))

        self._view._ddFilm.options.clear()
        self._view._ddFilm.value = None
        for f in self._model.getNodiOrdinati():
            self._view._ddFilm.options.append(ft.dropdown.Option(key=f.id, text=f.title))
        self._view.update_page()

    def handleRaggiungibili(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return
        idFilm = self._view._ddFilm.value
        if idFilm is None:
            self._errore("Seleziona un film!")
            return
        film = self._model._idMap[idFilm]

        n = self._model.getNumRaggiungibili(film)
        self._view.txt_result.controls.append(ft.Text(f"Film raggiungibili da {film}: {n}"))
        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handlePercorso(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return
        idFilm = self._view._ddFilm.value
        if idFilm is None:
            self._errore("Seleziona un film!")
            return
        film = self._model._idMap[idFilm]

        percorso, peso = self._model.getPercorso(film)

        if len(percorso) == 1:
            self._view.txt_result.controls.append(
                ft.Text(f"{film} non ha archi uscenti: nessun percorso."))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(f"Percorso da {film}:"))
        for i in range(len(percorso) - 1):
            u = percorso[i]
            v = percorso[i + 1]
            self._view.txt_result.controls.append(
                ft.Text(f"{u} ({u.date_published}) --({self._model.getPesoArco(u, v)})--> {v}"))
        ultimo = percorso[-1]
        self._view.txt_result.controls.append(ft.Text(f"{ultimo} ({ultimo.date_published})"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di film: {len(percorso)}"))
        self._view.txt_result.controls.append(ft.Text(f"Peso totale: {peso:.2f}"))
        self._view.update_page()