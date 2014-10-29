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

"""modeled.Qt.member

.. moduleauthor:: Stefan Zimmermann <zimmermann.code@gmail.com>
"""
from .widget import Widget


class MemberQ(object):
    __slots__ = ['Q', 'im', 'props', 'qlist']

    def __init__(self, Q, im):
        self.Q = Q
        self.im = im
        self.props = {}
        self.qlist = []

    def qwidget(self, Q):
        q = self.im.qwidget(Q, **self.props)
        self.qlist.append(q)
        return q

    # def __getitem__(self, index):
    #     return self.qlist[index]

    # def __iter__(self):
    #     return iter(self.qlist)

    # def __len__(self):
    #     return len(self.qlist)

    def __setattr__(self, name, value):
        if name in self.__slots__:
            object.__setattr__(self, name, value)
        else:
            self.props[name] = value
            for q in self.qlist:
                setattr(q, name, value)

    def __getattr__(self, name):
        Q = self.Q
        try:
            return getattr(Q(self.qlist), name)
        except KeyError:
            raise AttributeError(name)
