from frontend.globals import WidgetHandler, Renderer, COLOR_UNSELECTED, COLOR_SELECTED
from pygame import Surface, font, transform, draw
from backend.eventhandler import EventHandler
from .connection import toggle_connection
from .basewidget import BaseWidget


class Node(BaseWidget):
    idx = 0
    order = 'b'
    tamanio = 16

    named = False
    color_base = COLOR_UNSELECTED
    color_font = COLOR_SELECTED
    color_box = COLOR_SELECTED

    numerable = True
    selectable = True
    editable = True

    def __init__(self, data):
        super().__init__()
        self.children = []
        self.fuente = font.SysFont('Verdana', 10)
        self.layer = 1
        self.tipo = data['text'] if data['text'] != '' else 'leaf'
        WidgetHandler.add_widget(self)
        Renderer.add_widget(self)
        self.image = self.create()
        if data['color'] is not None:
            self.colorize(data['color'])
            self.text = data['text']

        self.rect = self.image.get_rect(center=data['pos'])
        EventHandler.register(self.toggle_selection, 'select', 'deselect')

    def connect(self, other):
        if self.tipo == 'leaf' and other.tipo == 'leaf':
            raise TypeError('Two leaves cannot conect to each other')

        if other not in self.children:
            toggle_connection(self, other)
            self.children.append(other)

        for child in self.children:
            child.parent = self

    def disconnect(self, other):
        if other in self.children:
            toggle_connection(self, other, value=False)
            self.children.remove(other)

    def get_idx(self):
        return [w for w in WidgetHandler.widgets.sprites() if w.numerable].index(self)

    def colorize(self, color_namer):
        a = color_namer.color if hasattr(color_namer, 'color') else color_namer
        self.named = True if hasattr(color_namer, 'name') else False
        self.color_base = a
        if (0.2126 * a.r + 0.7152 * a.g + 0.0722 * a.b) < 50:
            color_b = COLOR_SELECTED
        else:
            color_b = COLOR_UNSELECTED
        self.color_font = color_b
        self.color_box = color_b
        self.image.fill(self.color_base)

    def create(self):
        return Surface((self.size, self.size))

    @property
    def size(self):
        len_idx = len(str(self.get_idx()))
        size = self.tamanio
        if len_idx == 2:
            size = 20
        elif len_idx == 3:
            size = 25
        return size

    def update(self, *args):
        self.idx = self.get_idx()
        render_uns = self.fuente.render(str(self.idx), 1, self.color_font, self.color_base)
        size = self.size if self.tamanio < self.size else self.tamanio
        self.image = transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.blit(render_uns, render_uns.get_rect(center=self.image.get_rect().center))

    def __repr__(self):
        return self.tipo + ' #' + str(self.idx)

    def __int__(self):
        return self.idx

    def __str__(self):
        return str(self.idx)

    def kill(self):
        WidgetHandler.del_widget(self)
        Renderer.del_widget(self)
        super().kill()

    @property
    def lead(self):
        lenght = len(self.children)
        if lenght > 1:
            return [int(i) for i in self.children]
        elif lenght == 1:
            return int(self.children[0])

    def select(self):
        super().select()
        r = self.rect.copy()
        draw.rect(self.image, self.color_box, [0, 0, r.w, r.h], 1)

    def deselect(self):
        super().deselect()
        self.image.fill(self.color_base)


EventHandler.register(lambda e: Node(e.data), 'AddNode')
