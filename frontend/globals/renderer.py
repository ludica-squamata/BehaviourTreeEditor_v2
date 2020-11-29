from frontend.globals import WIDTH, HEIGHT, COLOR_TEXT
from pygame import display, font, Surface, draw
from pygame.sprite import LayeredUpdates
from backend import EventHandler, System
from .constants import COLOR_BG


class Renderer:
    widgets = None
    on_selection = False
    selection = None
    typemode_label = None
    typemode_mark = None

    @classmethod
    def init(cls):
        display.set_caption('BehaviourTreeEditor v2')
        # display.set_icon(image.load('frontend/favicon.png'))
        display.set_mode((WIDTH, HEIGHT))

        f = font.SysFont('Verdana', 14)
        cls.typemode_label = f.render('TypeMode (F3):', 1, COLOR_TEXT, COLOR_BG)
        cls.typemode_mark = Surface((19, 19))
        cls.widgets = LayeredUpdates()

    @classmethod
    def enable_selection(cls, selection_object):
        cls.selection = selection_object
        cls.on_selection = True

    @classmethod
    def add_widget(cls, widget):
        cls.widgets.add(widget)

    @classmethod
    def del_widget(cls, widget):
        cls.widgets.remove(widget)

    @classmethod
    def update(cls):
        fondo = display.get_surface()
        rect = [fondo.fill(COLOR_BG)]
        if System.type_mode:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)

        r = fondo.blit(cls.typemode_label, (505, 360))
        cls.typemode_mark.fill(color)
        fondo.blit(cls.typemode_mark, (r.right+3, r.y))

        rect.extend(cls.widgets.draw(fondo))
        if cls.on_selection:
            corners = [cls.selection.rect.topleft,
                       cls.selection.rect.topright,
                       cls.selection.rect.bottomright,
                       cls.selection.rect.bottomleft]
            draw.aalines(fondo, cls.selection.color, 1, corners)
        display.update(rect)

    @classmethod
    def toggle_selection(cls, evento):
        cls.on_selection = evento.data['value']


EventHandler.register(Renderer.toggle_selection, 'EndSelection')
