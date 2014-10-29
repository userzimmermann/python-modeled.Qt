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
from six import (
  PY3, with_metaclass, create_bound_method, text_type as unicode)

__all__ = ['Qt']

from inspect import getmembers
from datetime import datetime
from functools import partial

from path import path as Path

from modeled import MemberError, Adapter, ismodeledclass

from QtQuery import Q

from .widget import Widget, WidgetsDict, ismodeledwidgetclass, ismodeledwidget


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
        Q = self.Q
        self.q = Q.Object()
        object.__setattr__(self.q.emit, 'q', self)

        def widget(im):
            member = im.m
            if PY3 and member.mtype is bytes:
                return None
            try:
                label = member.options.qt.label
            except AttributeError:
                label = False
            if label:
                q = Q.Label()
                if member.format:
                    def qsetter(value):
                        q.text = format(value, member.format)
                else:
                    def qsetter(value):
                        q.text = str(value)
            else:
                try:
                    QClass, prop = type(self) \
                      .DEFAULT_WIDGETS_AND_PROPERTIES[member.mtype]
                except KeyError:
                    return None
                q = QClass()
                ## qgetter = object.__getattribute__(q, prop)
                msetter = partial(member.__set__, self)
                getattr(q, prop + 'Changed').__add__(
                  ## lambda value: msetter(qgetter()))
                  lambda value: msetter(value))
                qsetter = object.__getattribute__(
                  q, 'set' + prop[0].upper() + prop[1:])
            im.changed.append(qsetter)
              # lambda mobj, value: qsetter(value))
            try:
                qsetter(member.__get__(self))
            except MemberError: # No assigned/default value
                pass
            return q

        for name, im in self.model.members:
            im.qwidget = create_bound_method(widget, im)
            # setattr(self, name + 'Widget', widget(member.m))

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
