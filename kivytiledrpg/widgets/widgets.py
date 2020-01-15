import re

from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.textinput import TextInput


class SharpImage(Image):
    '''
    Image with nearest mag_filter, true pixelated, not smooth
    '''

    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.bind(texture=self._update_texture_filters)

    def _update_texture_filters(self, image, texture):
        texture.mag_filter = 'nearest'


class SharpLazyImage(SharpImage):

    '''
    Lazy SharpImage
    '''

    do_layout_event = ObjectProperty(None, allownone=True)

    layout_delay_s = NumericProperty(0.2)

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.bind(size=self.do_layout, pos=self.do_layout)

    def do_instructions(self):
        pass

    def do_layout(self, *args, **kwargs):
        if self.do_layout_event is not None:
            self.do_layout_event.cancel()
        real_do_layout = self.do_instructions
        self.do_layout_event = Clock.schedule_once(
            lambda dt: real_do_layout(),
            self.layout_delay_s)


class NumberInput(TextInput):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = pat.sub('', substring)
        super().insert_text(s, from_undo=from_undo)
        if self.text[0] == '0' and len(self.text) > 1:
            self.text = self.text[1:]
        return
