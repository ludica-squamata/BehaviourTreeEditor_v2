from pygame.sprite import Sprite
from pygame import K_DELETE


class BaseWidget(Sprite):
    rect = None
    is_selected = False
    on_focus = False
    selectable = False
    numerable = False
    editable = False
    draggable = True
    order = None

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__()
        if self.parent is not None:
            self.layer = self.parent.layer + 1
        else:
            self.layer = 1

    @property
    def center(self):
        return self.rect.center

    def __getitem__(self, item):
        return self.rect.center[item]

    # event catcher functions
    def on_keydown(self, event):
        if event.key == K_DELETE:
            self.kill()
            return True
        return False

    def on_keyup(self, event):
        pass

    def on_mousedown(self, event):
        pass

    def on_mouseup(self, event):
        pass

    def on_mousemotion(self, event):
        self.rect.move_ip(event.rel)

    def toggle_selection(self, event):
        if event.data['target'] is self:
            if event.tipo == 'select':
                self.select()
            elif event.tipo == 'deselect':
                self.deselect()

    # state functions
    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False
