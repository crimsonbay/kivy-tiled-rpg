from kivy.properties import NumericProperty, DictProperty, ListProperty
from kivy.graphics import Color, InstructionGroup, Line
from kivytiledrpg.widgets.widgets import SharpLazyImage
from kivytiledrpg.utils.files import load_col_file, save_col_file

class EditorImage(SharpLazyImage):

    __collisions_count = 2
    __instructions = dict()
    canvas_tile_size = (16, 16)

    collisions = DictProperty({})
    scale = NumericProperty(1)
    line_width = NumericProperty(1)
    half_line_width = NumericProperty(0.5)
    canvas_tile_size = ListProperty((16, 16))
    tilesize = ListProperty((16, 16))

    def __init__(self, *args, **kwargs):

        super().__init__(self, *args, **kwargs)

    def on_source(self, obj, value):
        collision_filename = value[:-3] + 'col'
        collisions_data = load_col_file(collision_filename)
        if collisions_data:
            self.tilesize = collisions_data['tilesize']
            self.collisions = collisions_data['collisions']
            self.__collisions_count = collisions_data['collisions_count']
            # self.root = self.get_root_window()
            if self.col_count.text != str(self.__collisions_count):
                self.col_count.text = str(self.__collisions_count)
    def do_instructions(self):
        self.repaint_instructions()

    @property
    def collisions_count(self):
        return self.__collisions_count

    def save_collisions(self):
        collision_filename = self.source[:-3] + 'col'
        save_col_file(self.collisions, self.collisions_count, self.tilesize, collision_filename)

    def change_collisions_count(self, obj, value):
        self.__collisions_count = int(value)

    def change_tile_size(self, size_type, value):
        if not value or (value[0] == '0' and len(value) > 1):
            return
        self.tilesize[size_type] = int(value)
        self.clear_collisions()
        self.recalculate_scale()

    def recalculate_scale(self):
        if self.texture_size[0] and self.texture_size[0]:
            self.scale = self.norm_image_size[0] / self.texture_size[0]
            self.canvas_tile_size[0], self.canvas_tile_size[1] = self.tilesize[0] * self.scale - self.line_width, self.tilesize[1] * self.scale - self.line_width

    def tile_coordinates(self, touch):
        if not self.tilesize[0]:
            return (0, 0)
        return (touch.pos[0] // (self.scale * self.tilesize[0]),
                (self.norm_image_size[1] - touch.pos[1]) // (self.scale * self.tilesize[1]))

    def collision_change(self, coordinates):
        if coordinates not in self.collisions:
            self.collisions[coordinates] = 0
        collision_type = self.collisions[coordinates]
        if collision_type + 1 < self.collisions_count:
            self.collisions[coordinates] += 1
        else:
            self.collisions[coordinates] = 0

    def repaint_instructions(self):
        self.recalculate_scale()
        self.make_instructions(self.collisions)

    def clear_collisions(self):
        for coordinates in self.collisions:
            old_instruction = self.__instructions.get(coordinates, None)
            if old_instruction:
                old_instruction.clear()
        self.collisions.clear()

    def make_instructions(self, collisions):
        for coordinates in collisions:
            old_instruction = self.__instructions.get(coordinates, None)
            if old_instruction:
                old_instruction.clear()
                new_instruction = old_instruction
            else:
                new_instruction = InstructionGroup()
            if self.collisions[coordinates] == 0:
                new_instruction.clear()
                return
            elif self.collisions[coordinates] == 1:
                new_instruction.add(Color(1, 0, 0))
            elif self.collisions[coordinates] == 2:
                new_instruction.add(Color(0, 0, 1,))
            elif self.collisions[coordinates] == 3:
                new_instruction.add(Color(0, 1, 0))
            elif self.collisions[coordinates] == 4:
                new_instruction.add(Color(1, 1, 0))
            elif self.collisions[coordinates] == 5:
                new_instruction.add(Color(0, 1, 1))
            elif self.collisions[coordinates] == 6:
                new_instruction.add(Color(1, 0, 1))
            elif self.collisions[coordinates] == 7:
                new_instruction.add(Color(1, 1, 1))
            new_instruction.add(
                Line(width=self.line_width,
                     rectangle=(coordinates[0] * self.tilesize[0] * self.scale + self.half_line_width,
                                (self.norm_image_size[1] - (coordinates[1] + 1) * self.tilesize[1] * self.scale - self.half_line_width),
                                *self.canvas_tile_size)
                     )
            )
            if not old_instruction:
                self.__instructions[coordinates] = new_instruction
                self.canvas.add(new_instruction)

    def on_touch_down(self, touch):
        coordinates = self.tile_coordinates(touch)
        self.collision_change(coordinates)
        self.make_instructions([coordinates])
