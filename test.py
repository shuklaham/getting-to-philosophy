from wikipedia_philosophy import HopToPhilosophySimple
import sys
from wikipedia_philosophy_hashing import HopToPhilosophyHash

inp = sys.argv
url = inp[1]

h1 = HopToPhilosophySimple()
op = h1.getHops(url =url)
if op:
    print op
else:
    print 'Its a deadend'


h2 = HopToPhilosophyHash()
op = h2.getHops(url=url)
if op:
    print op
else:
    print 'Its a deadend'