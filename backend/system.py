from frontend.globals import WIDTH, HEIGHT
from .eventhandler import EventHandler
from pygame import Rect


class System:
    number_of_nodes = 0

    type_mode = False
    area_nodos = Rect(0, 21, WIDTH // 5 * 4 + 25, HEIGHT // 5 * 4)
    MAIN_TB = None

    @classmethod
    def toggle_typemode(cls, typebox):
        cls.type_mode = not cls.type_mode
        EventHandler.trigger('ToggleTypeMode', 'System', {'instance': typebox, 'value': cls.type_mode})
