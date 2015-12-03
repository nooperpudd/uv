# -*- coding: utf-8 -*-
#
# Copyright (C) 2015, Maximilian Köhl <mail@koehlma.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, unicode_literals, division

from .library import ffi, lib, detach, dummy_callback

from .error import UVError
from .handle import HandleType, Handle

__all__ = ['Prepare']


@ffi.callback('uv_prepare_cb')
def uv_prepare_cb(uv_prepare):
    prepare = detach(uv_prepare)
    with prepare.loop.callback_context:
        prepare.callback(prepare)


@HandleType.PREPARE
class Prepare(Handle):
    """
    Prepare handles will run the given callback once per loop
    iteration, right before polling for IO.
    """

    __slots__ = ['prepare', 'callback']

    def __init__(self, loop=None, callback=None):
        """
        :param callback: callback which should be called right before polling for IO
        :type callback: (Prepare) -> None
        """
        self.prepare = ffi.new('uv_prepare_t*')
        super(Prepare, self).__init__(self.prepare, loop)
        self.callback = callback or dummy_callback
        code = lib.uv_prepare_init(self.loop.uv_loop, self.prepare)
        if code < 0: raise UVError(code)

    def start(self, callback=None):
        self.callback = callback or self.callback
        code = lib.uv_prepare_start(self.prepare, uv_prepare_cb)
        if code < 0: raise UVError(code)

    def stop(self):
        code = lib.uv_prepare_stop(self.prepare)
        if code < 0: raise UVError(code)

    __call__ = start
