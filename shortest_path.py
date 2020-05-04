def shortest_path(dist, n, orig):
    result = {i: 1000 for i in range(1,6)}
    visited = {}
    
    current = orig
    visited[orig] = 0
    while (len(visited) <= n):
        print("visited", visited, "result", result)
        direct_path = dist[current]
        if (len(visited) == 1):
            base = 0
        else:
            base = result[current]
        for k in direct_path:
            if (base + direct_path[k]) < result[k]:
                result[k] = base + direct_path[k]
        
        #find the next node to process
        min_value = 1000
        min_idx = -1
        for k in result:
            if k not in visited:
                if result[k] < min_value:
                    min_value = result[k]
                    min_idx = k
        if (min_idx == -1):
            return result
        else:
            current = min_idx
            visited[current] = 0 
    return result

Cities = ["Atlanta", "Boston", "Chicago", "Denver", "El Paso"]
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

for orig in range(1,6):
    print("\n")
    shortest_path(conv_to_ditn(times), 5, orig)
