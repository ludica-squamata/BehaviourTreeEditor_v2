from pygame import init as py_init, time
from frontend.globals.widgethandler import WidgetHandler
from frontend.globals.renderer import Renderer
from backend.eventhandler import EventHandler

py_init()
fps = time.Clock()
Renderer.init()

EventHandler.trigger('Init', 'System', {})

while True:
    fps.tick(60)
    Renderer.update()
    WidgetHandler.update()
    EventHandler.process()
