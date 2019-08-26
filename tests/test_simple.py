import unittest
import time

import redis

from simple import *


class DlockSimpleTest(unittest.TestCase):

    r = redis.Redis.from_url('redis://localhost:6379/0')

    def setUp(self):
        self.r.flushdb()
        self.ts = time.time()

    def tearDown(self):
        #print('{} cost: {}s'.format(self._testMethodName, time.time() - self.ts))
        self.r.flushdb()

    def test_normal_usage(self):
        '''
        正常使用锁
        '''

        for i in range(10):
            id = acquire_lock(self.r, 'lck')
            self.assertTrue(release_lock(self.r, 'lck', id))

    def test_repeatedly_release(self):
        '''
        重复释放
        '''

        id = acquire_lock(self.r, 'lck')
        self.assertTrue(release_lock(self.r, 'lck', id))
        self.assertFalse(release_lock(self.r, 'lck', id))
        self.assertFalse(release_lock(self.r, 'lck', id))

    @unittest.skip('time watsting case')
    def test_repeatedly_acquire(self):
        self.assertIsInstance(acquire_lock(self.r, 'lck'), str)
        self.assertFalse(acquire_lock(self.r, 'lck'))
        self.assertFalse(acquire_lock(self.r, 'lck'))

    def test_release_before_acquire(self):

        import uuid

        self.assertFalse(release_lock(self.r, 'lck', uuid.uuid4()))
