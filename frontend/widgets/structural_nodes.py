from frontend.globals import COLOR_BOX, COLOR_TEXT, COLOR_SELECTED, WIDTH, HEIGHT, node_colors
from pygame import font, Surface, Rect, Color
from backend import EventHandler, render_textrect, WidgetGroup
from frontend.globals import WidgetHandler, Renderer
from .basewidget import BaseWidget


class StructureNodes(BaseWidget):

    def __init__(self):
        super().__init__()
        self.fa = font.SysFont('Verdana', 15)
        self.fb = font.SysFont('Verdana', 12)
        self.fa.set_underline(1)
        self.properties = WidgetGroup()

        self.image = Surface((WIDTH // 5 - 25, (HEIGHT // 3) * 2 - 10))
        self.image.fill(COLOR_BOX)
        self.rect = self.image.get_rect(topright=(WIDTH, 0))
        self.clear_area = self.rect.copy()
        self.clear_area.centerx = self.rect.width // 2
        self.clear_area.height -= 21
        self.clear_area.top += 21

        render = self.fa.render('Structure', 1, COLOR_TEXT, COLOR_BOX)
        renderect = render.get_rect(centerx=self.rect.width // 2)
        self.image.blit(render, renderect)

        standard = ['Sequence', 'Selector', 'Repeater', 'UntilFail', 'Inverter', 'Succeder']
        for i, name in enumerate(standard):
            y = self.rect.y + 21 + + i * 21
            color = node_colors[name]
            n = StandardNode(self, name, y, color)
            Renderer.add_widget(n)
            WidgetHandler.add_widget(n)
            self.properties.add(n)

        n = StandardNode(self, 'Leaf', self.rect.y + 25 + + (len(standard)) * 21, COLOR_BOX)
        Renderer.add_widget(n)
        WidgetHandler.add_widget(n)
        self.properties.add(n)

        Renderer.add_widget(self)

    def deselect_all(self):
        for n in self.properties.widgets():
            n.deselect()


EventHandler.register(lambda e: StructureNodes(), 'Init')


class StandardNode(BaseWidget):
    selectable = True
    editable = True
    draggable = False
    order = 'a'

    def __init__(self, parent, name, y, color):
        super().__init__(parent)
        self.name = name
        if self.name != 'Leaf':
            self.text = name
            self.color = color
        else:
            self.text = ''
            self.color = Color('black')
        self.f = font.SysFont('Verdana', 13)
        self.rect = r = Rect(parent.rect.x, y, parent.rect.w, 21)
        self.img_uns = render_textrect(self.name, self.f, r, COLOR_TEXT, color, 1)
        self.img_sel = render_textrect(self.name, self.f, r, COLOR_SELECTED, color, 1)
        self.image = self.img_uns
        WidgetHandler.add_widget(self)
        EventHandler.register(self.toggle_selection, 'select', 'deselect')

    def show(self):
        Renderer.add_widget(self)
        WidgetHandler.add_widget(self)

    def hide(self):
        Renderer.del_widget(self)
        WidgetHandler.del_widget(self)

    def select(self):
        super().select()
        self.parent.deselect_all()
        self.image = self.img_sel

    def deselect(self):
        super().deselect()
        self.image = self.img_uns

    def __repr__(self):
        return 'LocName ' + self.name
