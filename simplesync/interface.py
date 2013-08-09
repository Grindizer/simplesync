#!/usr/bin/python -O
# -*- coding: utf-8 -*-
#
# Id: $Id$
# URL: $URL$
# Module description:  $(description)

from zope.interface import Interface

class IHub(Interface):
    """ a Sasy IHUB allow to handle long processing task by switch them into asynchronous task.
    And is the central point for inquery task status. """
    def asynchrone(ICallable):
        """ add a ICallable object to the list of task handle by this hub and return a task ID."""

    def status(tid):
        """ return task status """

    def get(tid, timeout, remove):
        """ block until task return value or raise exception """

class IStorage(Interface):
    """ Interface dealing with storing and retrieving results. """
    def put(tid, data):
        """ """

    def get(tid):
        """ return result data for task tid """

    def delete(tid):
        """ delete the tid atsk result from storage """

class ICallable(Interface):
    """ a task """
    def __call__():
        """ """

