import pstats

p = pstats.Stats('restats')

p.sort_stats('time', 'cumulative')
p.print_stats(20)
