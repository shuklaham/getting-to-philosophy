from wikipedia_philosophy import HopToPhilosophySimple

from wikipedia_philosophy_hashing import HopToPhilosophyHash

h1 = HopToPhilosophySimple()
print h1.getHops(url ="https://en.wikipedia.org/wiki/Design_pattern")

h2 = HopToPhilosophyHash()
print h2.getHops(url="https://en.wikipedia.org/wiki/Design_pattern")
