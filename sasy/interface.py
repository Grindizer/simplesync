#!/usr/bin/python -O
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 WALLIX, SARL. All rights reserved.
#
# Licensed computer software. Property of WALLIX.
# Product name: WALLIX Admin Bastion V 3.0
# Author(s): Nassim Babaci <nbabaci@wallix.com>
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

    def get(tid, timeout):
        """ block until task return value or raise exception """

class IStorage(Interface):
    """ Interface dealing with storing and retrieving results. """
    def put(tid, data):
        """ """

    def get(tid):
        """ return result data for task tid """

