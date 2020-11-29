from backend.group import WidgetGroup
from .eventhandler import EventHandler


class Selected(WidgetGroup):
    def __init__(self):
        super().__init__()

    def sumar(self, sprites):
        super().add(*sprites)
        for sprite in sprites:
            EventHandler.trigger('select', self, {'target': sprite})

    def empty(self):
        for sprite in self.sprites():
            EventHandler.trigger('deselect', self, {'target': sprite})
        super().empty()
