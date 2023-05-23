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
    #  TODO:  Create
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
