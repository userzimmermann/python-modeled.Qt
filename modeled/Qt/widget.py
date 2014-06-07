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

"""modeled.Qt.widget

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
__all__ = ['Widget', 'WidgetsDict', 'ismodeledwidgetclass', 'ismodeledwidget']

from collections import OrderedDict

from moretools import simpledict


class WidgetsDictStructBase(simpledict.structbase):
    """`basestructtype` for `simpledict()` to create MembersDict.struct class.
    """
    def __init__(self, model, widgets):
        def bases():
            for cls in model.__bases__:
                if cls is not object:
                    try:
                        yield cls.widgets
                    except AttributeError:
                        pass
        # Delegates widgets to SimpleDictType.__init__()
        simpledict.structbase.__init__( # First arg is struct __name__
          self, '%s.widgets' % repr(model), bases(), widgets)


WidgetsDict = simpledict(
  'WidgetsDict', structbase=WidgetsDictStructBase, dicttype=OrderedDict)


class Widget(object):
    def __init__(self, Q, name, *args, **kwargs):
        self.Q = Q
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.id = None

    def __call__(self):
        Q = self.Q
        if self.id:
            Q = Q.id[self.id]
        return getattr(Q, self.name)(*self.args, **self.kwargs)


def ismodeledwidgetclass(cls):
    """Checks if `cls` is a subclass of :class:`modeled.Qt.Widget`.
    """
    try:
        return issubclass(cls, Widget)
    except TypeError: # No class at all
        return False


def ismodeledwidget(obj):
    """Checks if `obj` is an instance of :class:`modeled.Qt.Widget`.
    """
    return isinstance(obj, Widget)
