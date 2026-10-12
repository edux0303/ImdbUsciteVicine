import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Uscite Vicine"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self._title = None
        self._ddGenere = None
        self._ddAnno = None
        self._txtK = None
        self._btnCreaGrafo = None
        self._ddFilm = None
        self._btnRaggiungibili = None
        self._btnPercorso = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Film usciti a pochi giorni di distanza", color="blue", size=24)
        self._page.controls.append(self._title)

        # PUNTO 1
        self._ddGenere = ft.Dropdown(label="Genere", width=200)
        self._ddAnno = ft.Dropdown(label="Anno", width=130)
        self._txtK = ft.TextField(label="Max giorni K", width=130, value="7")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([self._ddGenere, self._ddAnno, self._txtK, self._btnCreaGrafo],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # PUNTO 1d e PUNTO 2
        self._ddFilm = ft.Dropdown(label="Film", width=400)
        self._btnRaggiungibili = ft.ElevatedButton(text="Film raggiungibili",
                                                   on_click=self._controller.handleRaggiungibili)
        self._btnPercorso = ft.ElevatedButton(text="Percorso",
                                              on_click=self._controller.handlePercorso)
        row2 = ft.Row([self._ddFilm, self._btnRaggiungibili, self._btnPercorso],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

        # generi e anni si possono caricare subito, i film solo dopo "Crea Grafo"
        self._controller.fillDD()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()