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

from six import with_metaclass

__all__ = ['Q']

from datetime import datetime
from functools import partial

from moretools import cached

from modeled import mobject

from QtQuery import Q


DEFAULT_WIDGETS_AND_PROPERTIES = {
  int: (Q.SpinBox, 'value'),
  float: (Q.LineEdit, 'text'),
  str: (Q.LineEdit, 'text'),
  datetime: (Q.DateTimeEdit, 'dateTime'),
}


class QtMeta(mobject.type):
    @cached
    def __getitem__(cls, mclass):
        class Qt(cls, mclass):
            def __init__(self, **membervalues):
                mclass.__init__(self, **membervalues)

                def widget(member):
                    QClass, prop = DEFAULT_WIDGETS_AND_PROPERTIES[
                      member.mtype]
                    q = QClass()
                    qgetter = object.__getattribute__(q, prop)
                    qsetter = object.__getattribute__(
                      q, 'set' + prop[0].upper() + prop[1:])
                    msetter = partial(member.__set__, self)
                    getattr(q, prop + 'Changed').__add__(
                      lambda: msetter(qgetter()))
                    member.changed.append(
                      lambda mobj, value: qsetter(value))
                    qsetter(member.__get__(self))
                    return q

                for name, member in self.model.members:
                    setattr(self, name + 'Widget', widget(member))

        Qt.__module__ = cls.__module__
        Qt.__name__ = '%s[%s]' % (cls.__name__, mclass.__name__)
        return Qt


class Qt(with_metaclass(QtMeta, object)):
    pass
