class Test(object):

    def __repr__(self):
        return 'Hello World'

    __str__ = __repr__
t = Test()
print(t)
import datetime
postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))

print(postdate)