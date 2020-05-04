def shortest_path(dist, n, orig):
    BIG_VALUE = 1000
    result = {i: BIG_VALUE for i in range(1,n+1)}
    result[orig] = 0
    visited = {}
    
    current = orig
    visited[orig] = 0
    while (len(visited) <= n):
        print("visited", visited, "result", result)
        if current in dist:
            direct_path = dist[current]
        else:
            direct_path = {}
        if (len(visited) == 1):
            base = 0
        else:
            base = result[current]
        for k in direct_path:
            if (base + direct_path[k]) < result[k]:
                result[k] = base + direct_path[k]
        
        #find the next node to process
        min_value = BIG_VALUE
        min_idx = -1
        for k in result:
            if k not in visited:
                if result[k] < min_value:
                    min_value = result[k]
                    min_idx = k
        if (min_idx == -1):
            max_dist = max(result.values())
            max_dist = max_dist if max_dist != BIG_VALUE else -1
            return max_dist, result            
        else:
            current = min_idx
            visited[current] = 0 
    max_dist = max(result.values())
    max_dist = max_dist if max_dist != BIG_VALUE else -1
    return max_dist, result

cities = ["Atlanta", "Boston", "Chicago", "Denver", "El Paso"]
times = [[1,2,100],[1,4,160], [2,4,180],[2,3,120], [3,5,80], [4,3,40],[4,5,140], [5,2,100]]

def conv_to_ditn(times):
    d = {}
    for a in times:
        if a[0] in d:
            d0 = d[a[0]]
            d0[a[1]] = a[2]
            d[a[0]] = d0
        else:
            d0 = {}
            d0[a[1]] = a[2]
            d[a[0]] = d0
    return d

n = len(cities)
for orig in range(1,n+1):
    print("\n")
    print(shortest_path(conv_to_ditn(times), n, orig))

times = [[2,1,1],[2,3,1],[3,4,1]]
n = 4
orig = 2
shortest_path(conv_to_ditn(times), n, orig)
