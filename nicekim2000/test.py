stage_dir=[(1,0),(0,1),(-1,0),(0,-1)]
round_dir=[(0,1),(-1,0),(0,-1),(1,0)]
point_pos=[0,0]
n=3
for i in range(50):
    value = i % (4 * n)
    stage = value // n
    num = value % n
    if num!=0 :
        point_pos = [point_pos[0] + stage_dir[stage][0], point_pos[1] + stage_dir[stage][1]]
    print(point_pos)

