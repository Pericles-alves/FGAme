# -*- coding: utf8 -*-
'''
Re-define os objetos do módulo FGAme.physics e adiciona propriades extras de
renderização
'''


from FGAme import physics
from FGAme.events import EventDispatcherMeta, signal
from FGAme.core import conf
from FGAme.draw import Color, color
from FGAme.util import lazy
DEBUG = False

__all__ = ['AABB', 'Circle', 'Poly', 'RegularPoly', 'Rectangle']


@EventDispatcherMeta.decorate
class ObjectMixin(object):
    _is_mixin_ = True
    _mixin_args = ['color', 'line_color', 'line_width']

    long_press = signal('long-press', 'key', delegate_to='_input')
    key_up = signal('key-up', 'key', delegate_to='_input')
    key_down = signal('key-down', 'key', delegate_to='_input')
    mouse_motion = signal('mouse-motion', delegate_to='_input')
    mouse_button_up = signal(
        'mouse-button-up', 'button', delegate_to='_input')
    mouse_button_down = signal(
        'mouse-button-down', 'button', delegate_to='_input')
    mouse_long_press = signal(
        'mouse-long-press', 'button', delegate_to='_input')

    @lazy
    def _input(self):
        return conf.get_input()  # @UndefinedVariable

    def __init__(self, *args, **kwds):
        mixin_kwds = self._extract_mixin_kwargs(kwds)
        self._init_physics(*args, **kwds)
        self._init_visualization(**mixin_kwds)

    def _extract_mixin_kwargs(self, kwds):
        D = {}
        mixin_args = self._mixin_args
        for k in kwds:
            if k in mixin_args:
                D[k] = kwds[k]
        for k in D:
            del kwds[k]
        return D

    def _init_visualization(
            self, color='black', line_color=None, line_width=1):
        '''Init visualization parameters'''

        self._color = None
        self._line_color = None
        self._line_width = line_width
        self.color = color
        self.line_color = line_color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if value is None:
            self._color = None
        else:
            self._color = Color(value)

    @property
    def line_color(self):
        return self._line_color

    @line_color.setter
    def line_color(self, value):
        if value is None:
            self._line_color = None
        else:
            self._color = Color(value)

    @property
    def line_width(self):
        return self._line_width

    @line_width.setter
    def line_width(self, value):
        self._line_width = value


class AABB(ObjectMixin, physics.AABB):
    _init_physics = physics.AABB.__init__

    def draw(self, screen):
        if self._color is not None:
            color = self._color
            lw, lc = self._line_width, self._line_color
            screen.draw_aabb(self.aabb, True, color, lw, lc)


class Circle(ObjectMixin, physics.Circle):
    _init_physics = physics.Circle.__init__

    def draw(self, screen):
        if self._color is not None:
            color = self._color
            lw, lc = self._line_width, self._line_color
            screen.draw_circle(self.bounding_box, True, color, lw, lc)


class Poly(ObjectMixin, physics.Poly):
    _init_physics = physics.Poly.__init__

    def paint(self, screen):
        if self.color is not None:
            screen.paint_poly(self.vertices, self.color)
            self._debug(screen)


class Rectangle(ObjectMixin, Poly, physics.Rectangle):
    _init_physics = physics.Rectangle.__init__


class RegularPoly(ObjectMixin, Poly, physics.RegularPoly):
    _init_physics = physics.RegularPoly.__init__


if __name__ == '__main__':
    x = AABB(shape=(100, 200), world=set())
    type(x)
    print(x.mass)
