fin = open("input.txt", "r")

N, T = map(lambda x: int(x), fin.readline().split())
timeline = [list(map(lambda x: int(x), fin.readline().split())) for x in range(N)]
result = [0 for i in range(10)]

fin.close()

for i in range(N):
    if timeline[i][3]:
        participants = []
        gank = True
        victim = timeline[i][2]
        participants.append(timeline[i][1])
        j = i - 1
        
        while timeline[i][0] - timeline[j][0] < T:
            if victim == timeline[j][2]:
                if timeline[j][1] not in participants:
                    participants.append(timeline[j][1])
            elif victim == timeline[j][1]:
                if timeline[j][2] not in participants:
                    gank = False
                    break
            j -= 1
        
        if gank:
            for p in participants:
                result[p] += 1
