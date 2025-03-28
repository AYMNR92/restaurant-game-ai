import os
lst_strat = ["A", "T", "S", "G", "F", "R", "W"]
for s1 in lst_strat:
    for s2 in lst_strat:
        os.system(f"python src/main2.py {s1} {s2}")

