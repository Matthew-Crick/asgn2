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

def calculateMaxDataFlow(adjMatrix, origin):
    # Initialize a variable to keep track of the total data that can be sent from the origin to all target data centres
    max_data_flow = 0

    while True:
        # Initialize a list to keep track of visited data centres
        visited = [False] * len(adjMatrix)

        # Perform a depth-first search to find a path from the origin to the super target node
        flow = dfs(origin, float('inf'), adjMatrix, visited)

        # If no path was found, break the loop
        # This means we have found all paths from the origin to the super target node
        if flow == 0:
            break

        # If a path was found, add its flow to the total flow
        # This flow represents the maximum data that can be sent from the origin to all target data centres via this path
        max_data_flow += flow

    return max_data_flow


# Example
connections = [(0, 1, 3000), (1, 2, 2000), (1, 3, 1000), (0, 3, 2000), (3, 4, 2000), (3, 2, 1000)]
maxIn = [5000, 3000, 3000, 3000, 2000]
maxOut = [5000, 3000, 3000, 2500, 1500]
origin = 0
targets = [4, 2]
# Your function should return the maximum possible data throughput from the
# data centre origin to the data centres specified in targets.
print(maxThroughput(connections, maxIn, maxOut, origin, targets))
#4500


connections1 = [(182, 235, 785), (2, 47, 629), (144, 210, 255), (82, 122, 420), (108, 215, 327), (116, 64, 531), (161, 37, 304), (189, 27, 614), (23, 25, 373), (4, 51, 671), (18, 23, 137), (208, 175, 317), (180, 109, 189), (67, 234, 315), (225, 49, 115), (4, 93, 405), (68, 0, 238), (123, 31, 596), (130, 19, 195), (158, 5, 438), (211, 67, 344), (235, 86, 635), (125, 28, 797), (230, 44, 501), (157, 67, 564), (181, 189, 688), (104, 68, 490), (39, 159, 688), (196, 144, 420), (229, 62, 166), (177, 48, 162), (34, 5, 557), (192, 207, 562), (70, 170, 89), (127, 57, 729), (60, 151, 383), (63, 41, 95), (10, 39, 383), (79, 80, 418), (217, 15, 789), (26, 88, 714), (2, 30, 657), (148, 136, 168), (122, 144, 194), (223, 105, 641), (205, 4, 349), (21, 152, 259), (188, 119, 611), (44, 71, 507), (184, 194, 176), (220, 162, 578), (189, 229, 679), (173, 99, 335), (105, 116, 574), (238, 17, 410), (55, 156, 572), (72, 13, 116), (154, 221, 472), (112, 23, 732), (22, 128, 582), (103, 28, 770), (62, 144, 638), (145, 43, 291), (207, 50, 409), (124, 208, 427), (166, 51, 146), (139, 156, 237), (162, 54, 707), (59, 1, 513), (146, 85, 241), (109, 26, 377), (150, 221, 231), (138, 46, 687), (35, 192, 676), (54, 110, 555), (26, 203, 117), (102, 115, 644), (233, 79, 105), (160, 39, 580), (191, 23, 371), (197, 36, 129), (121, 37, 246), (1, 172, 199), (80, 88, 104), (100, 185, 549), (28, 38, 799), (97, 134, 686), (174, 107, 618), (33, 73, 782), (155, 48, 734), (50, 62, 567), (84, 213, 376), (185, 30, 170), (57, 223, 339), (86, 104, 619), (126, 47, 643), (92, 23, 470), (165, 61, 669), (154, 218, 352), (185, 228, 170), (127, 152, 369), (45, 127, 112), (16, 190, 157), (207, 216, 671), (20, 200, 681), (192, 84, 662), (159, 47, 288), (110, 27, 768), (164, 92, 305), (194, 98, 448), (31, 208, 308), (201, 31, 648), (15, 226, 344), (132, 186, 137), (176, 190, 165), (12, 23, 102), (202, 201, 721), (12, 55, 292), (69, 99, 477), (134, 207, 543), (59, 227, 152), (156, 171, 707), (172, 73, 537), (227, 158, 454), (25, 190, 154), (81, 176, 581), (168, 187, 206), (83, 211, 241), (52, 41, 543), (87, 60, 486), (25, 19, 409), (136, 42, 331), (203, 78, 387), (237, 64, 108), (29, 96, 84), (120, 207, 256), (42, 65, 682), (193, 226, 538), (84, 175, 88), (163, 93, 537), (170, 39, 467), (221, 210, 567), (218, 50, 187), (40, 211, 334), (64, 42, 599), (74, 110, 169), (43, 56, 237), (182, 112, 619), (206, 84, 408), (67, 90, 329), (232, 41, 116), (88, 110, 394), (41, 16, 783), (48, 8, 799), (8, 72, 426), (108, 18, 642), (114, 68, 156), (37, 224, 474), (224, 113, 280), (95, 148, 791), (72, 3, 690), (177, 142, 258), (198, 58, 247), (91, 35, 774), (73, 224, 417), (107, 50, 234), (222, 148, 437), (236, 14, 750), (216, 132, 679), (40, 29, 716), (99, 91, 698), (100, 36, 169), (66, 44, 182), (119, 236, 318), (109, 223, 380), (140, 158, 323), (14, 184, 520), (27, 158, 436), (19, 221, 653), (219, 40, 128), (3, 106, 166), (214, 76, 113), (94, 234, 702), (13, 79, 697), (115, 221, 700), (7, 131, 411), (17, 56, 643), (90, 24, 679), (6, 57, 419), (133, 101, 433), (216, 215, 697), (137, 3, 233), (53, 28, 87), (49, 59, 784), (24, 238, 514), (93, 32, 780), (135, 70, 632), (187, 18, 245), (215, 170, 287), (147, 160, 309), (0, 206, 430), (30, 199, 702), (32, 25, 447), (89, 58, 96), (149, 104, 788), (143, 87, 755), (56, 120, 390), (209, 20, 465), (25, 185, 392), (11, 189, 778), (91, 53, 537), (183, 47, 577), (46, 85, 512), (65, 10, 142), (195, 133, 144), (20, 44, 240), (204, 40, 688), (234, 203, 269), (226, 89, 285), (212, 83, 584), (169, 124, 181), (167, 25, 440), (85, 81, 460), (75, 2, 523), (106, 159, 359), (142, 225, 639), (141, 32, 400), (186, 138, 749), (231, 139, 322), (128, 85, 367), (121, 59, 328), (178, 57, 131), (199, 19, 75), (153, 4, 80), (71, 133, 338), (131, 163, 93), (200, 23, 654), (101, 49, 107), (190, 119, 585), (78, 180, 180), (113, 176, 625), (96, 49, 451), (127, 51, 223), (51, 217, 160), (210, 107, 222), (118, 29, 716), (151, 102, 692), (58, 185, 778), (173, 56, 792), (117, 97, 217), (129, 81, 566), (174, 219, 675), (36, 227, 674), (77, 42, 252), (173, 94, 785), (137, 111, 648), (9, 229, 570), (61, 132, 705), (47, 212, 790), (171, 105, 629), (111, 81, 772), (5, 162, 558), (179, 174, 172), (167, 179, 365), (228, 200, 587), (76, 155, 526), (152, 216, 474), (38, 155, 482), (175, 215, 222), (166, 124, 607), (213, 204, 356), (216, 232, 445), (98, 210, 190), (55, 214, 95), (52, 153, 760)]
maxIn1 = [1197, 912, 1029, 1332, 826, 1935, 855, 1759, 1137, 2129, 1005, 1734, 1127, 1834, 1540, 1784, 1043, 1222, 819, 628, 2140, 1336, 2112, 1641, 810, 1466, 1919, 811, 512, 514, 1686, 1509, 1982, 1105, 1066, 504, 2036, 1353, 1332, 1428, 807, 1559, 1008, 762, 1279, 1975, 788, 1412, 754, 799, 555, 605, 1422, 1574, 1976, 1887, 1473, 2018, 1283, 1713, 1875, 1888, 1036, 1392, 592, 1244, 860, 1134, 826, 900, 1331, 1115, 760, 516, 1602, 816, 1299, 842, 582, 1225, 602, 2138, 1290, 1988, 961, 616, 1233, 1067, 1994, 777, 1164, 1561, 2112, 1533, 2078, 1390, 1901, 1421, 584, 1573, 1122, 1278, 1462, 1724, 1202, 710, 777, 649, 2016, 1255, 529, 1329, 1922, 748, 2013, 587, 1464, 650, 1167, 1623, 2115, 1595, 1007, 598, 1718, 1629, 1186, 1253, 1346, 1256, 1003, 977, 787, 663, 1158, 1068, 2160, 1859, 1193, 1190, 2059, 1929, 1831, 1919, 1233, 1733, 1184, 2097, 1997, 1032, 655, 891, 1068, 2129, 1929, 1212, 1079, 1602, 1254, 1884, 841, 803, 1368, 1613, 530, 903, 870, 1212, 1721, 1547, 1820, 1533, 600, 2019, 619, 2003, 723, 1440, 722, 1735, 2122, 1961, 730, 880, 1381, 1808, 1270, 802, 1841, 1966, 757, 2090, 1656, 1149, 1264, 1337, 736, 546, 1719, 917, 1801, 1378, 1998, 1587, 1213, 913, 669, 1444, 562, 2005, 1324, 1584, 1547, 935, 951, 1784, 2032, 1405, 1566, 926, 1870, 629, 1481, 607, 1396, 1673, 1497, 896, 2146, 1131, 640, 1211, 1921, 1154, 645, 1010, 1274, 1044, 1678]
maxOut1 = [597, 1225, 795, 1668, 1152, 521, 1391, 631, 561, 863, 1171, 1453, 1474, 660, 874, 1660, 906, 1400, 1278, 510, 1368, 1576, 1105, 951, 1359, 1238, 1598, 955, 918, 1575, 921, 795, 626, 703, 1433, 1512, 1612, 1616, 1760, 1675, 1596, 1119, 1395, 1537, 1407, 1133, 1463, 587, 1006, 1543, 1326, 1546, 1518, 668, 949, 899, 1339, 912, 569, 1710, 906, 680, 1435, 749, 1508, 547, 1009, 1327, 892, 1283, 1288, 1061, 826, 1660, 974, 1083, 1004, 1702, 1526, 1032, 751, 635, 1640, 770, 1525, 732, 1285, 1282, 1078, 656, 784, 1747, 913, 502, 775, 1132, 1211, 1500, 1640, 1732, 1579, 1430, 901, 1627, 935, 995, 1379, 1767, 762, 1758, 879, 1297, 1762, 618, 986, 1683, 1761, 870, 1745, 727, 708, 1735, 736, 826, 1522, 1556, 876, 1134, 737, 524, 1428, 874, 835, 692, 1315, 1489, 1279, 770, 644, 1734, 685, 1439, 1356, 1105, 1018, 777, 1379, 783, 763, 1227, 1667, 1320, 1284, 805, 902, 1366, 1257, 1081, 1173, 1700, 699, 739, 549, 1723, 1525, 1291, 1433, 575, 1097, 1570, 1487, 1318, 1419, 1681, 1316, 1728, 846, 1386, 877, 707, 899, 1721, 1619, 831, 1047, 1597, 738, 1217, 712, 876, 1644, 1274, 1577, 1547, 567, 1355, 1053, 671, 963, 593, 1685, 507, 933, 1458, 1182, 1280, 633, 1132, 1270, 710, 1031, 892, 1170, 1735, 1311, 962, 1729, 574, 1527, 988, 658, 1086, 1565, 986, 553, 1605, 1716, 812, 963, 1623, 1049, 1057, 1100, 937, 1554, 1163, 732, 1244, 1580]
origin1 = 112
targets1 = [42, 57]

#0
print(maxThroughput(connections1, maxIn1, maxOut1, origin1, targets))