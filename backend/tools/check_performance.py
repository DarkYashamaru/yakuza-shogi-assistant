import pstats

p = pstats.Stats(r"D:\Repositories\yakuza-shogi-assistant\backend\profile.out")
p.sort_stats("cumtime").print_stats(30)