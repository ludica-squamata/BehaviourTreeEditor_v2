from frontend.globals import WIDTH, HEIGHT
from .eventhandler import EventHandler
from pygame import Rect
# from .util import abrir_json
# from random import randint


class System:
    # data = abrir_json('data/input.json')
    # lenght = len(data)
    number_of_nodes = 0
    # generated_colors = []

    type_mode = False
    area_nodos = Rect(0, 21, WIDTH // 5 * 4 + 25, HEIGHT // 5 * 4)
    MAIN_TB = None

    # limit_input = True
    # replacing_locutor = False

    @classmethod
    def toggle_typemode(cls, typebox):
        cls.type_mode = not cls.type_mode
        EventHandler.trigger('ToggleTypeMode', 'System', {'instance': typebox, 'value': cls.type_mode})

    # @classmethod
    # def toggle_input_mode(cls):
    #     cls.limit_input = not cls.limit_input

    # @classmethod
    # def get_lenght(cls):
    #     return len(cls.data) - cls.number_of_nodes
    #
    # @classmethod
    # def get_extra(cls):
    #     return cls.number_of_nodes - len(cls.data)

    # @classmethod
    # def load_data(cls):
    #     cls.data = abrir_json('data/input.json')
    #     cls.lenght = len(cls.data)

    # @classmethod
    # def generate_color(cls):
    #     h = randint(0, 360)
    #     a = Color('white')
    #     a.hsla = h, 100, 50, 100
    #     return '%02x%02x%02x' % (a.r, a.g, a.b)
    #
    # @classmethod
    # def new_locutor(cls):
    #     name = cls.generate_color()
    #     cls.generated_colors.append(name)
    #     idx = cls.generated_colors.index(name)
    #     if idx < 20:
    #         EventHandler.trigger('NewLocutor', 'System', {'idx': idx, 'name': name, 'replace': False})

    # @classmethod
    # def replace_locutor(cls, idx):
    #     name = cls.generate_color()
    #     cls.generated_colors[idx] = name
    #     cls.replacing_locutor = True
    #     EventHandler.trigger('NewLocutor', 'System', {'idx': idx, 'name': name, 'replace': True})
    #
    # @classmethod
    # def modify_data(cls, data):
    #     idx = data['idx']
    #     text = data['text']
    #     cls.data[idx] = text


# EventHandler.register(lambda o: System.modify_data(o.data), 'WriteNode')
