from pygame import event, KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT, K_ESCAPE, key, mouse
from pygame import KMOD_CTRL, KMOD_SHIFT, K_RETURN, K_s, K_d, K_c, K_a, K_F3, Rect
from backend import salir, EventHandler, System, Selected
from backend.group import WidgetGroup


class WidgetHandler:
    widgets = WidgetGroup()
    active_widget = None
    name = "WidgetHandler"
    selection = None
    on_selection = False
    selected = Selected()
    numerable = []
    active_area = Rect(0, 21, 537, 363)

    @classmethod
    def add_widget(cls, widget):
        cls.widgets.add(widget)
        if widget.numerable:
            cls.numerable.append(widget)
            System.number_of_nodes += 1

    @classmethod
    def del_widget(cls, widget):
        cls.widgets.remove(widget)
        if widget.numerable:
            cls.numerable.remove(widget)
            System.number_of_nodes -= 1

        cls.numerable.sort(key=lambda o: o.idx)

    @classmethod
    def set_active(cls, widget):
        cls.active_widget = widget

    @classmethod
    def enable_selection(cls, selection_object):
        cls.selection = selection_object
        cls.add_widget(selection_object)
        cls.on_selection = True
        cls.set_active(selection_object)

    @classmethod
    def toggle_selection(cls, evento):
        cls.on_selection = evento.data['value']

    @classmethod
    def update(cls):
        events = event.get([KEYDOWN, KEYUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, QUIT])
        event.clear()

        # esto es para que se pueda reemplazar un locutor sin tener que reseleccionarlo.
        cls.selected.add([i for i in cls.widgets.widgets() if i.is_selected and (i not in cls.selected)])

        for e in events:
            mods = key.get_mods()
            ctrl = mods & KMOD_CTRL
            shift = mods & KMOD_SHIFT
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                salir()

            elif e.type == KEYDOWN:
                widgets = cls.selected.widgets()
                if System.type_mode:
                    if e.key == K_F3:
                        System.toggle_typemode('MainTB')
                    else:
                        EventHandler.trigger('Key', cls.name, {'key': e.key, 'mod': e.mod})

                elif e.key == K_c:
                    if len(widgets) == 2 and all([o.numerable for o in widgets]):
                        widgets.sort(key=lambda o: o.idx)  # lower idx's go first
                        if not shift:
                            widgets[0].connect(widgets[1])
                        else:
                            widgets[0].disconnect(widgets[1])

                elif e.key == K_a and len(widgets) == 2:
                    base, other = widgets
                    EventHandler.trigger('AddMidPoint', 'System', {'base': base, 'other': other})

                elif e.key == K_RETURN:
                    EventHandler.trigger('CreateDialog', cls.name, {'nodes': cls.numerable})

                # elif e.key == K_F1:
                #     System.load_data()
                #     diff = len(cls.numerable) - System.lenght
                #     for i in range(diff):
                #         cls.numerable[-1].kill()
                #
                # elif e.key == K_F2:
                #     System.new_locutor()

                elif e.key == K_F3:
                    if any([o.order == 'b' for o in widgets]):
                        System.toggle_typemode('MainTB')
                    else:
                        for widget in widgets:
                            widget.on_keydown(e)

                elif e.key == K_s:
                    x, y = mouse.get_pos()
                    color = None
                    if any([o.order == 'a' for o in widgets]):
                        color = [i for i in widgets if i.order == 'a'][0].color

                    if System.area_nodos.collidepoint(x, y):
                        EventHandler.trigger('AddNode', cls.name, {'pos': [x, y], 'color': color})

                elif e.key == K_d and any([o.order == 'a' for o in widgets]):
                    widgets.sort(key=lambda o: o.order)
                    color_namer = widgets.pop(0)
                    for other in widgets:
                        other.colorize(color_namer)

                # elif e.key == K_F5:
                #     System.toggle_input_mode()

                elif len(cls.selected):
                    for widget in cls.selected.widgets():
                        widget.on_keydown(e)

            elif e.type == KEYUP:
                if len(cls.selected):
                    for widget in cls.selected.widgets():
                        widget.on_keyup(e)

            elif e.type == MOUSEBUTTONDOWN:  # pos, button
                widgets = [w for w in cls.widgets.widgets() if w.selectable and w.rect.collidepoint(e.pos)]
                if not len(widgets) and e.button == 1 and cls.active_area.collidepoint(e.pos):
                    if not shift and not System.type_mode:
                        cls.selected.empty()
                    if not ctrl:
                        EventHandler.trigger('AddSelection', cls.name, {"pos": e.pos, 'value': True})

                elif len(widgets) and not len(cls.selected):
                    cls.selected.sumar([w for w in widgets if w.selectable])

                elif not cls.selected.has(widgets) and e.button == 1 and len(widgets):
                    order_c = [i for i in widgets if i.order == 'c']
                    if not ctrl and not System.type_mode and not len(order_c):
                        cls.selected.empty()
                    cls.selected.sumar(widgets)

                if len(widgets):
                    for widget in cls.selected.widgets():
                        if widget is not cls.selection:
                            widget.on_mousedown(e)

                elif e.button != 1:
                    widgets = [w for w in cls.widgets.widgets() if w.numerable]
                    if ctrl and not shift:
                        dx, dy = 1, 0
                    elif shift and not ctrl:
                        dx, dy = 0, 5
                    elif ctrl and shift:
                        dx, dy = 5, 0
                    else:
                        dx, dy = 0, 1

                    for widget in widgets:
                        if e.button == 4:
                            dx *= -1
                            dy *= -1
                        elif e.button == 5:
                            dx *= 1
                            dy *= 1

                        widget.rect.move_ip(dx, dy)

            elif e.type == MOUSEBUTTONUP:  # pos, button
                if cls.on_selection and e.button == 1:
                    cls.selection.on_mouseup(e)
                    selected = [i for i in cls.widgets if cls.selection.rect.contains(i.rect)]
                    cls.selected.sumar(selected)

            elif e.type == MOUSEMOTION:  # pos, rel, buttons
                if e.buttons[0] and len(cls.selected) and not shift and not System.type_mode:
                    for widget in [i for i in cls.selected.widgets() if i.draggable is True]:
                        widget.on_mousemotion(e)

                elif cls.on_selection and e.buttons[0]:
                    cls.selection.on_mousemotion(e)

                elif ctrl and e.buttons[0]:
                    widgets = [w for w in cls.widgets.widgets() if w.selectable and w.draggable]
                    for widget in widgets:
                        widget.on_mousemotion(e)

        cls.widgets.update()

    @classmethod
    def __repr__(cls):
        return cls.name + " ({} widgets)".format(str(len(cls.widgets)))


EventHandler.register(WidgetHandler.toggle_selection, 'AddSelection', 'EndSelection')
