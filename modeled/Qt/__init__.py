# modeled.Qt
#
# Qt GUI Adapter for modeled objects.
#
# Copyright (C) 2014 Stefan Zimmermann <zimmermann.code@gmail.com>
#
# modeled.Qt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# modeled.Qt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with modeled.Qt. If not, see <http://www.gnu.org/licenses/>.

"""modeled.Qt

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from six import with_metaclass, text_type as unicode

__all__ = ['Qt']

from inspect import getmembers
from datetime import datetime

from path import path as Path
from moretools import cached

from modeled import Adapter, ismodeledclass

from QtQuery import Q

from .widget import Widget, WidgetsDict, ismodeledwidgetclass, ismodeledwidget
from .member import MemberQt


class _QtMeta(Adapter.type):
    @staticmethod
    def DEFAULT_WIDGETS_AND_PROPERTIES(Q):
        return {
          int: (Q.SpinBox, 'value'),
          float: (Q.DoubleSpinBox, 'value'),
          str: (Q.LineEdit, 'text'),
          unicode: (Q.LineEdit, 'text'),
          Path: (Q.LineEdit, 'text'),
          datetime: (Q.DateTimeEdit, 'dateTime'),
          }

    def __init__(cls, clsname, bases, clsattrs):
        if not ismodeledclass(cls):
            return

        def widgets():
            for name, obj in getmembers(cls):
                if ismodeledwidgetclass(obj):
                    obj = obj()
                    obj.id = name
                    setattr(cls, name, obj)
                    yield name, obj
                elif ismodeledwidget(obj):
                    if not obj.id:
                        obj.id = name
                    yield name, obj

        cls.model.widgets = WidgetsDict.struct(cls.model, widgets())

    def __getattr__(cls, name):
        return lambda *args, **kwargs: Widget(cls.Q, name, *args, **kwargs)


class _Qt(with_metaclass(_QtMeta, Adapter)):
    def __init__(self, **membervalues):
        Qt = type(self)
        Q = self.Q
        self.q = Q.Object()
        object.__setattr__(self.q.emit, 'q', self)

        for name, im in self.model.members:
            class instancemember(im.__class__):
                @property
                @cached
                def Qt(self):
                    return MemberQt(Qt, self)

                def __getitem__(self, key):
                    im = super(instancemember, self).__getitem__(key)
                    im.__class__ = self.__class__
                    return im

            im.__class__ = instancemember

        for name, widget in self.model.widgets:
            setattr(self, name, widget())

    @property
    def emit(self):
        return self.q.emit


def Qt(qmodule):
    _Q = Q(qmodule)

    class QtMeta(_QtMeta):
        DEFAULT_WIDGETS_AND_PROPERTIES = (
          _QtMeta.DEFAULT_WIDGETS_AND_PROPERTIES(_Q))

    class Qt(with_metaclass(QtMeta, _Qt)):
        Q = _Q

    return Qt
