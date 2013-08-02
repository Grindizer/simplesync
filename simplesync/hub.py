import threading
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
import status
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
        self._active_threads = {}
    
    def asynchrone(self, task):
        """ run task in a thread and return an Id for that task""" 
        super(ThreadedHub, self).asynchrone(task)

        _in_active_threads = threading.Event()
        def MyThread():
            _id = current_thread().ident
            _in_active_threads.wait()
            try:
                result = task()
            except Exception, e:
                self.storage.put(_id, e)
            else:
                self.storage.put(_id, result)
            finally:
                # remove _id from active thread.
                del self._active_threads[_id]
        
        task_thread = Thread(target=MyThread)
        # starting thread.
        task_thread.start()

        ident = task_thread.ident
        # register thread in dict
        self._active_threads[ident] = task_thread
        _in_active_threads.set()

        
        
        return task_thread.ident
    
    def get(self, task, timeout=5, remove=True):
        self._active_threads[task].join(timeout)
        if self.status(task) == status.RUNNING:  #still running:
            # TODO: replace this with an exception from excp.
            raise Exception, "timeout"
        
        # TODO: handle errors here:
        # task does not exists
        # result not ready yet because MyThread return between self._task[_id] =, and self.storage.put ... 
        # may be remove _task, and use only self.storage.
        result = self.storage.get(task)
        if remove:
            self.storage.delete(task)
        if not isinstance(result, Exception):
            return result
        
        raise result
    
    def status(self, task):
        task_thread = self._active_threads.get(task, None)
        if task_thread and task_thread.is_alive():
            return status.RUNNING

        result = self.storage.get(task)
        if result:
            if not isinstance(result, Exception):
                return status.SUCCESS
            else:
                return status.FAIL

        #TODO replace this with a better exception.
        raise Exception, "Task not registered"

        
            