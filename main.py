'''
Your company has D data centres represented by 0, 1, . . . , |D| − 1. And you have a list
connections of the direct communication channels between the data centres. connections is
a list of tuples (a, b, t) where:
• a ∈ {0, 1, . . . , |D|−1} is the ID of the data centre from which the communication channel
departs.
• b ∈ {0, 1, . . . , |D| − 1} is the ID of the data centre to which the communication channel
arrives.
• t is a positive integer representing the maximum throughput of that channel.
Regarding connections:
• You cannot assume that the communication channels are bidirectional.
• You can assume that for each pair of data centers there will be at most one direct communication channel in each direction between them.
• You can assume that for every data centre {0, 1, . . . , |D| − 1} there is at least one communication channel departing or arriving at that data centre.
• You cannot assume that the list of tuples connections is given to you in any specific
order.
• The number of communication channels |C| might be significantly less than |D|
2
, therefore
you should not assume that |C| = Θ(|D|
2
).
'''

def maxThroughput(connections, maxIn, maxOut, origin, targets):
    # Determine the number of data centres
    num_data_centres = len(maxIn)

    # Initialize adjacency matrix representing data flow between data centres
    # Each cell in the matrix represents maximum possible data that can be sent from one data centre to another
    adjMatrix = initializeAdjMatrix(num_data_centres, connections, maxIn, maxOut)

    # Add a super target node (an extra node) in the network that connects all target data centres
    # This extra node will help us compute the maximum flow to all target data centres in a single run of Ford-Fulkerson
    connectTargetsToExtraNode(adjMatrix, targets, maxIn, maxOut)

    # Determine the maximum possible data flow from the origin to all target data centres using the Ford-Fulkerson algorithm
    #  TODO:  Create
    max_data_throughput = calculateMaxDataFlow(adjMatrix, origin)

    return max_data_throughput


def initializeAdjMatrix(num_data_centres, connections, maxIn, maxOut):
    # Create an empty matrix of zeros
    adjMatrix = [[0] * num_data_centres for _ in range(num_data_centres)]

    # Populate the matrix with the maximum possible data flow for each connection
    for from_data_centre, to_data_centre, throughput in connections:
        adjMatrix[from_data_centre][to_data_centre] = min(throughput, maxOut[from_data_centre], maxIn[to_data_centre])

    return adjMatrix

'''
The backup request that you receive has the following format: it specifies the integer ID origin
∈ {0, 1, . . . , |D| − 1} of the data centre where the data to be backed up is located and a list
targets of data centres that are deemed appropriate locations for the backup data to be stored.
targets is a list of integers such that each integer i in it is such that i ∈ {0, 1, . . . , |D| − 1}
and indicates that backing up data to server i is fine. Regarding those inputs:
• You can assume that origin is not contained in the list targets.
• You cannot assume that the list of integers targets is given to you in any specific order,
but you can assume that it contains no duplicated integers.
• The data to be backed up can be arbitrarily split among the data centres specified in
targets and each part of the data only needs to be stored in one of those data centres.
'''
def connectTargetsToExtraNode(adjMatrix, targets, maxIn, maxOut):
    # Append a new row to the matrix to represent the super target node
    adjMatrix.append([0] * len(adjMatrix[0]))

    # Connect each target data centre to the super target node
    for target_data_centre in targets:
        adjMatrix[target_data_centre].append(min(maxIn[target_data_centre], maxOut[target_data_centre]))
        adjMatrix[-1].append(0)

def dfs(data_centre, curr_flow, adjMatrix, visited):
    # Mark the current data centre as visited
    visited[data_centre] = True

    # If the current data centre is the super target node, return the current flow
    # This means we have found a path from the origin to the super target node
    if data_centre == len(adjMatrix) - 1:
        return curr_flow

    # Iterate over all data centres connected to the current data centre
    for neighbour, capacity in enumerate(adjMatrix[data_centre]):
        if capacity > 0 and not visited[neighbour]:
            # Perform a depth-first search from the neighbouring data centre to find a path to the super target node
            flow = dfs(neighbour, min(curr_flow, capacity), adjMatrix, visited)

            # If this path leads to the super target node, update the flow along this path
            if flow > 0:
                adjMatrix[data_centre][neighbour] -= flow
                adjMatrix[neighbour][data_centre] += flow
                return flow

    return 0