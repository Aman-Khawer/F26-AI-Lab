graph={
    "A":["B","C"],
    "B":["D","E"],
    "C":["F"],
    "D":[],
    "E":["G"],
    "F":[],
    "G":[]
}

def dls(node,limit):
    stack=[(node,0,[node])]
    while stack:
        temp,depth,path=stack.pop()
        if temp=="G":
            return "found",path
        if depth<limit:
            for child in reversed(graph[temp]):
                if child not in path:
                    stack.append((child,depth+1,path+[child]))
    return "cutoff",None

def iddfs(node,max_depth):
    for limit in range(1,max_depth+1):
        status,result=dls(node,limit)
        if status=="found":
            return status,result
    return "cutoff",None

for limit in [1,2,3,4]:
    status,result=iddfs("A",limit)
    print(status,result)