from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooser
from kivytiledrpg.widgets.widgets import NumberInput
from kivy.graphics import Color, Rectangle, InstructionGroup, Line
from .widgets import EditorImage


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)


class CollisionEditor(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def show_save(self):
        if not self.tileset.source:
            return
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.3, 0.3))
        self._popup.open()

    def load(self, path, filename):
        try:
            self.tileset.source = filename[0]
        except Exception as e:
            print(e)

        self.dismiss_popup()

    def save(self):
        try:
            self.tileset.save_collisions()
        except Exception as e:
            print(e)
        self.dismiss_popup()


class EditorApp(App):
    def build(self):
        return CollisionEditor()


def main():
    EditorApp().run()

if __name__ == '__main__':
    main()

# Factory.register('CollisionEditor', cls=CollisionEditor)
# Factory.register('LoadDialog', cls=LoadDialog)
# Factory.register('SaveDialog', cls=SaveDialog)

