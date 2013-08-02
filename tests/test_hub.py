import time
#!/usr/bin/python -O
# -*- coding: utf-8 -*-
#
# Author(s): Nassim Babaci <nbabaci@wallix.com>
# Id: $Id$
# URL: $URL$
# Module description:  $(description)

import unittest, time
from simplesync import ThreadedHub
from simplesync import excp
from simplesync import status



class TestIHub(object):

    def test_asynch_id(self):
        def fct():
            return "data"
        tid1 = self.obj.asynchrone(fct)
        tid2 = self.obj.asynchrone(fct)
        self.assertNotEqual(tid1, tid2, "2 registred task cannot have the same tid")


    def test_async_not_callable(self):
        not_callable = "123"
        self.assertRaises(excp.CannotRegisterObject, self.obj.asynchrone, (not_callable,))


    def test_status_sucess(self):
        def fct():
            return "data"

        tid = self.obj.asynchrone(fct)
        self.obj.get(tid, remove=False)
        self.assertEqual(status.SUCCESS, self.obj.status(tid))

    def test_status_fail(self):
        def fct():
            raise Exception, "an error"

        tid = self.obj.asynchrone(fct)
        self.assertRaises(Exception, self.obj.get, (tid,), {'remove': False})
        # perform a get on obj so we can be sure result is ready.
        try:
            self.obj.get(tid, remove=False)
        except:
            pass
        self.assertEqual(status.FAIL, self.obj.status(tid))

    def test_status_fail_after_remove_true(self):
        pass

    def test_status_success_after_remove_true(self):
        pass

    def test_status_running(self):
        stop = False
        def fct():
            while not stop:
                time.sleep(0.1)

        tid = self.obj.asynchrone(fct)
        st = self.obj.status(tid)
        stop = True
        self.assertEqual(status.RUNNING, st)

    def test_get(self):
        def fct():
            return "data"

        tid = self.obj.asynchrone(fct)
        d = self.obj.get(tid)
        self.assertEqual("data", d)

class TestThreadedHub(TestIHub, unittest.TestCase):
    def setUp(self):
        class MemDico(object):
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

        storage = MemDico()
        self.obj = ThreadedHub(storage)

if __name__ == '__main__':
    unittest.main()


