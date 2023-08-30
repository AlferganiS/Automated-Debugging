from debuggingbook.ChangeCounter import *
change_counter = ChangeCounter('https://github.com/cool-RR/PySnooper')
commits = change_counter.messages.get(('pysnooper\\tracer.py',), None)
size = change_counter.sizes.get(('pysnooper\\tracer.py',), None)
print(size)
