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

from interface import IHub, IStorage, ICallable
from excp import CannotRegisterObject
from zope.component import adapts
from zope.interface import implements
from threading import Thread, current_thread

class HubBase(object):
    def __init__(self, storage):
        self.storage = storage
        
    def asynchrone(self, task):
        if not callable(task):
            raise CannotRegisterObject, "Object {0} is not callable".format(task)

class ThreadedHub(HubBase):
    implements(IHub)
    adapts(IStorage)
    
    def __init__(self, storage):
        super(ThreadedHub, self).__init__(storage)
        self._tasks = {}
        self._thread = {}
    
    def asynchrone(self, task):
        """ run task in a thread and return an Id for that task""" 
        super(ThreadedHub, self).asynchrone(task)
        
        def MyThread():
            _id = current_thread().ident
            try:
                result = task()
            except Exception, e:
                self.storage.put(_id, e)
            else:
                self.storage.put(_id, result)
        
        task_thread = Thread(target=MyThread)
        task_thread.start()
        
        ident = task_thread.ident
        self._thread[ident] = task_thread
        
        return task_thread.ident
    
    def get(self, task, timeout=5, remove=False):
        self._thread[task].join(timeout)
        if self._tasks[task]['status'] == 0: #still running:
            # TODO: replace this with an exception from excp.
            raise Exception, "timeout"
        
        # TODO: handle errors here:
        # task does not exists
        # result not ready yet because MyThread return between self._task[_id] =, and self.storage.put ... 
        # may be remove _task, and use only self.storage.
        return self.storage.get(task)
    
    def status(self, task):
        if self._thread.get(task, None) is None:
            #TODO: replace this with a excp exception.
            raise Exception, "Task not registered"
        # ... time to go bed ! grrr
        
            