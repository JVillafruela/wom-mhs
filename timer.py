#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

class Timer(object):
    def __enter__(self):
        self.start()
        # __enter__ must return an instance bound with the "as" keyword
        return self

    # There are other arguments to __exit__ but we don't care here
    def __exit__(self, *args, **kwargs):
        self.stop()

    def start(self):
        if hasattr(self, 'interval'):
            del self.interval
        self.start_time = time.time()

    def stop(self):
        if hasattr(self, 'start_time'):
            self.interval = time.time() - self.start_time
            del self.start_time # Force timer reinit


class LoggerTimer(Timer):
    @staticmethod
    def default_logger(msg):
        print msg

    def __init__(self, prefix='', func=None)
        # Use func if not None else the default one
        self.f = func or LoggerTimer.default_logger
        # Format the prefix if not None or empty, else use empty string
        self.prefix = '{0}:'.format(prefix) if prefix else ''

    def stop(self):
        # Call the parent method
        super(LoggerTimer, self).stop()
        # Call the logging function with the message
        self.f('{0}{1}'.format(self.prefix, self.interval))

    def __call__(self, func):
        # Use self as context manager in a decorated function
        def decorated_func(*args, **kwargs):
            with self: return func(*args, **kwargs)
        return decorated_func
# See more at: http://saladtomatonion.com/blog/2014/12/16/mesurer-le-temps-dexecution-de-code-en-python/#sthash.aSPkWxVo.dpuf

'''
@LoggerTimer('The function', logger.debug)
def the_function(argument):
    content = server_call(argument)
    return process_data(content)
- See more at: http://saladtomatonion.com/blog/2014/12/16/mesurer-le-temps-dexecution-de-code-en-python/#sthash.aSPkWxVo.dpuf

'''
