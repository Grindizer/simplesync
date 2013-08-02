#!/usr/bin/python -O
# -*- coding: utf-8 -*-
#
#
# Licensed computer software. Property of WALLIX.
# Author(s): Nassim Babaci <nbabaci@wallix.com>
# Id: $Id$
# URL: $URL$
# Module description:  $(description)

from interface import IStorage
from zope.interface import implements

class MemDico(object):
    implements(IStorage)
    """ a dummy and no efficient implementatioàn of IStorage, used mainly
        for testing purpouse """
    def __init__(self):
        self._s = {}

    def put(self, tid, data):
        self._s[tid] = data

    def get(self, tid):
        r = self._s.get(tid, None)
        return r

    def delete(self, tid):
        if tid in self._s:
            del self._s[tid]
