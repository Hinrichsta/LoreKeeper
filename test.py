from Database.Parse import *

active_party = get_active_party()
for act in active_party:
    print(act[1])