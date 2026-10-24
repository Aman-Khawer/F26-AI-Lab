
# Lab 5: Minimax and Alpha-Beta Pruning

scores = [3, 5, 2, 9, 0, 7, 0, 0]
treeDepth = 3

min_count = 0
ab_count = 0


# Task 1: Minimax
def minimax(currDepth, nodeIndex, isMaxTurn):
    global min_count

    if currDepth == treeDepth:
        min_count += 1
        return scores[nodeIndex]

    if isMaxTurn:
        return max(
            minimax(currDepth+1, nodeIndex*2, False),
            minimax(currDepth+1, nodeIndex*2+1, False)
        )
    else:
        return min(
            minimax(currDepth+1, nodeIndex*2, True),
            minimax(currDepth+1, nodeIndex*2+1, True)
        )


# Task 2: Alpha-Beta Pruning
def alphabeta(currDepth, nodeIndex, isMaxTurn, alpha, beta):
    global ab_count

    if currDepth == treeDepth:
        ab_count += 1
        return scores[nodeIndex]

    if isMaxTurn:
        value = float('-inf')

        for i in range(2):
            value = max(value, alphabeta(currDepth+1, nodeIndex*2+i, False, alpha, beta))
            alpha = max(alpha, value)

            if alpha >= beta:
                break
        return value

    else:
        value = float('inf')

        for i in range(2):
            value = min(value, alphabeta(currDepth+1, nodeIndex*2+i, True, alpha, beta))
            beta = min(beta, value)

            if alpha >= beta:
                break
        return value


# Task 1: Minimax Result
print("TASK 1: MINIMAX")
print("Optimal Value:", minimax(0, 0, True))


# Task 2: Leaf Counter
print("\nTASK 2: LEAF COUNTER")
print("Minimax Leaves:", min_count)

print("Alpha-Beta Value:", alphabeta(0, 0, True, float('-inf'), float('inf')))
print("Alpha-Beta Leaves:", ab_count)


# Task 3: Branch Ordering
print("\nTASK 3: BRANCH ORDERING")

scores = [0, 0, 0, 7, 2, 9, 3, 5]

min_count = 0
ab_count = 0

print("Reordered Minimax Value:", minimax(0, 0, True))
print("Reordered Minimax Leaves:", min_count)

print("Reordered Alpha-Beta Value:", alphabeta(0, 0, True, float('-inf'), float('inf')))
print("Reordered Alpha-Beta Leaves:", ab_count)
