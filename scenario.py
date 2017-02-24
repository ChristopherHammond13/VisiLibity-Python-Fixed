from __future__ import division
from __future__ import absolute_import
import visilibity as vis
import pylab as p
import math
from utils import parser
import sys
from io import open
import os.path
import getopt
from collections import deque
from collections import OrderedDict

def main(argv):
    u'''
    Parses command line args and calls appropriate function
    '''
    input_file = u""
    output_file = u""
    help_string = u"Usage: main.py -n <number_to-run> -a <algorithm> -i <input_file> -o \
            <output_file>"
    
    try:
        opts, _ = getopt.getopt(argv, u"hn:a:i:o:", [u"number=", u"algorithm=",
                                                    u"ifile=", u"ofile="])
    except getopt.GetoptError:
        print help_string
        sys.exit(2)

    algorithm = default_schedule
    number = 30

    for opt, arg in opts:
        if opt == u"-h":
            print help_string
            sys.exit()
        elif opt in (u"-n", u"--number"):
            number = int(arg)
        elif opt in (u"-a", u"--algorithm"):
            if arg == u"greedy-claim":
                algorithm = greedy_claim_schedule
            elif arg == u"greedy-dynamic":
                algorithm = greedy_dynamic_schedule
            else:
                print u"Algorithm: " + unicode(arg) + u" does not exist, use \
                      greedy-claim, greedy-dynamic or omit the option \
                      for the default"
                sys.exit(1)
        elif opt in (u"-i", u"--ifile"):
            input_file = arg
        elif opt in (u"-o", u"--ofile"):
            output_file = arg

    if not os.path.isfile(input_file):
        print u"Input file does not exist"
        sys.exit(1)

    if output_file == u"":
        output_file = u"output.mat"

    if os.path.isfile(output_file):
        print u"Specified output file already exists"
        sys.exit(1)

    try:
        problemset_file = open(input_file)
        print u"Opened " + input_file
    except IOError:
        print u"Unable to open input file"
        sys.exit(1)

    calculate_solution(problemset_file, algorithm, number)


#reverse a list to make it ccw
def rev(random = []):
    return random[::-1]

def checkCounterclockwise(listThing): #make sure you initialize sum to 0
    sum = 0
    for i in range(0, len(listThing)):
        x = listThing[i+1][0] - listThing[i][0]
        y = listThing[i][1] + listThing[i+1][1]
        sum = sum + (x*y)
        if sum > 0: #if sum is positive, it is clockwise
            return False
        else: #if sum is negative, it is counter clockwise
            return True

def returnXtuples(listThing):
    newListThing = []
    for x in listThing:
        newListThing.append(x[0])
    return newListThing

def returnYtuples(listThing):
    newListThing = []
    for x in listThing:
        newListThing.append(x[1])
    return newListThing

def calculate_solution(problemset_file, algorithm, number):

    u"""
    Solves a problem given to it
    """
    _parser = parser.input_parser()
    parsed_string = u"Problems parsed: "
    u"""
    Our problems are stored in a map<int, (robots:[point],polygons:[[point]])>
    """
    problemset = {}

    for problem in problemset_file:
        _parser.parse(problem)
        parsed_string += unicode(_parser.index) + u";"
        problemset[_parser.index] = (_parser.robots, _parser.polygons)
        #robots is a list, and polygons in a list of list- which is stored in a tuple- wot

    robotsVis = [] #robots with vis points assigned already 
    robotsPlainList = [] #robot coordinates
    polygonsPlain = [] #polygon coordinates, nested list btw
    polygonsVis = [] #polygon coordinates with vis points already assigned
    #iterating over all the robots and making them vis point thingies
    for x in problemset.values():
        for y in x[0]: #first value in the tuple, which contains list of robots 
            robotsPlainList.append(y) #add this to a generic robots list just in case
            newThingy = vis.Point(y[0], y[1]) #hope dis works, because list contains tuples of coordinates
            robotsVis.append(newThingy)
        
    #adding polygons to a random list just for bants
    for x in problemset.values():
        for y in x[1]:
            polygonsPlain.append(y)
    
    for x in polygonsPlain:
        if checkCounterclockwise(x):
            rev(x)
    
    #function to convert polygon coordinates to vis thingies 
    for x in polygonsPlain:
        for y in x:
            otherNewThingy = vis.Point(y[0], y[1])
            row = []
            row.append(otherNewThingy)
            polygonsVis.append(row)
        
        
    #converting every polygon inside list to vis.Polygon 
    for x in polygonsVis:
        x = vis.Polygon(x)
    
    singularXcords = [] #contains list of individual x cords for obstacles
    singularYcords = [] #contains list of individual y cords for obstacles

    for x in polygonsPlain:
        temp = returnXtuples(x)
        temp2 = returnYtuples(x)
        tempList = []
        tempList2 = []
        tempList.append(temp)
        tempList2.append(temp2)
        singularXcords.append(tempList)
        singularYcords.append(tempList2)
    

    print parsed_string + u"\nStarting...\n"

    # The Ilya Constant (TM)
    epsilon = 0.000000001

    # Environment plot (500 x 500 should be enough, right?! *gulps with fear*)
    p1 = vis.Point(50, 50)
    p2 = vis.Point(-50, 50)
    p3 = vis.Point(-50, -50)
    p4 = vis.Point(50, -50)

    # Set up our walls (yay)
    wall_x = [p1.x(), p2.x(), p3.x(), p4.x(), p1.x()]
    wall_y = [p1.y(), p2.y(), p3.y(), p4.y(), p1.y()]

    walls = vis.Polygon([p1, p2, p3, p4])

    #robot1 = vis.Point(-1,-1)
    #robot2 = vis.Point(4,4)

    #obstacle = vis.Polygon([vis.Point(1,6),vis.Point(1,1),vis.Point(5,1),vis.Point(5,5),vis.Point(3,5),vis.Point(3,3),vis.Point(4,3),vis.Point(4,2),
    #            vis.Point(2,2),vis.Point(2,6),vis.Point(6,6),vis.Point(6,0),vis.Point(0,0),vis.Point(0,6),vis.Point(1,6)][::-1])

    #obstacle_x = [1, 1, 5, 5, 3, 3, 4, 4, 2, 2, 6, 6, 0, 0, 1][::-1]
    #obstacle_y = [6, 1, 1, 5, 5, 3, 3, 2, 2, 6, 6, 0, 0, 6, 6][::-1]

    #robot1 = vis.Point(0, 1)
    #robot2 = vis.Point(6, 2)

    #obstacle = vis.Polygon([vis.Point(8,1),vis.Point(4,1),vis.Point(4,4),vis.Point(5,2), vis.Point(8,1)])
    #obstacle_x = [8, 4, 4, 5, 8]
    #obstacle_y = [1, 1, 4, 2, 1]

    #obstacle2 = vis.Polygon([vis.Point(1,2), vis.Point(1,4), vis.Point(3,4), vis.Point(3,2), vis.Point(1,2)][::-1])
    #obstacle2_x = [1, 1, 3, 3, 1][::-1]
    #obstacle2_y = [2, 4, 4, 2, 2][::-1]

    """
    also awks that this doesn't work bc bloody C++ needs all da 
    parameters- need to fix it at some point 
    
    """
    
    envList = [walls]
    #adds individuals obstacles to list used for the environment
    for x in polygonsVis:
        envList.append(x)
    

    env = vis.Environment(envList)

    robot1.snap_to_boundary_of(env, epsilon)
    robot1.snap_to_vertices_of(env, epsilon)

    robot1 = robotsVis[0]

    isovist = vis.Visibility_Polygon(robot1, env, epsilon)

    #need to fix these 
    shortest_path = env.shortest_path(robot1, robot2, epsilon)

    point_x, point_y = save_print(isovist)

    point_x.append(isovist[0].x())
    point_y.append(isovist[0].y())

    p.title('Shortest (????) Path')

    p.xlabel('X Position')
    p.ylabel('Y Position')

    p.plot(wall_x, wall_y, 'black')

    #plots robots from the robotsVis list
    for x in robotsVis:
        p.plot([x.x()], [x.y()], 'go')

    #p.plot([robot1.x()], [robot1.y()], 'go')

    #p.plot([robot2.x()], [robot2.y()], 'go')

    #iterate through list of individual x and y coordinates and plot the obstacles
    for x,y in zip(singularXcords, singularYcords):
        p.plot(x , y , 'r')

    #p.plot(obstacle_x, obstacle_y, 'r')
    #p.plot(obstacle2_x, obstacle2_y, 'r')
    
    print "Shortest Path length from observer to end: ", shortest_path.length()

    print "Number of options: ", shortest_path.size()
    polyline = []
    for x in range(0, shortest_path.size()):
        point = shortest_path.getVertex(x)
        print "(", point.x(), ", ", point.y(), ")"
        polyline.append(point)

    p.show()

    """
    implementing other shortest path algorithms

    """

    for i in xrange(1, number):
        # reset these trackers
        global awake
        awake = {}
        global claimed
        claimed = {}
        global distance_to_travel
        distance_to_travel = {}
        global stopped
        stopped = set([])
        # a solution is our list of paths
        solution = []
        robot_paths = OrderedDict()
        problem = problemset[i] #why is dis here
        robots = robotsPlainList
        obstacles = polygonsPlain

        # get the wakeup order for the problem
        schedule = algorithm(problem) #marking this as may need changing
        first_robot = schedule.popleft() 
        awake[robots.index(first_robot)] = first_robot
        robot_paths[robots.index(first_robot)] = [first_robot]

        """ may need to get this checked
        # get the visibility graph
        try:
            _vis_graph = graph.vis_graph(i, robots, obstacles)
        except ValueError:
            _vis_graph = None
        """

        # perform simulation
        simulationRunning = True
        while simulationRunning:
            simulationRunning = False
            for robot in robots:
                if robots.index(robot) not in awake.keys(): #what is this index method? may be standard lib implementation
                    simulationRunning = True
                    break
        
            # update positions
            remaining_movement = 10.0
            while (remaining_movement > 0):
                # find distance to closest target
                next_robot_id = None
                min_distance = 9999

                for robot in robots:
                    robot_id = robots.index(robot)
                    if ((robot_id in awake.keys())
                        and (robot_id not in claimed.keys())
                        and (robot_id not in stopped)
                       and (len(schedule) == 0)):
                        stopped.add(robot_id)
                        # print("[ScheduleEmpty] Robots stopped: " + str(stopped))
                    if ((robot_id in awake.keys())
                        and (robot_id not in claimed.keys())
                        and (robot_id not in stopped)
                       and (len(schedule) > 0)):
                        try:
                            next_target = schedule.popleft()
                            claimed[robot_id] = next_target
                            if _vis_graph is not None: #need to change this as well, a lot of the method
                                min_len = _vis_graph.get_shortest_path_length(
                                    vg.Point(awake[robot_id][0], awake[robot_id][1]),
                                    vg.Point(next_target[0], next_target[1]))
                            else:
                                min_len = math.sqrt(
                                    math.pow(awake[robot_id][0]
                                             - claimed[robot_id][0], 2) +
                                    math.pow(awake[robot_id][1]
                                             - claimed[robot_id][1], 2))

                            # need to put robot in distance_to_travel with its
                            # distance
                            # print("Distance between " + str(robot) + " and " + str(next_target) + " is " + str(min_len))
                            distance_to_travel[robot_id] = min_len

                        except IndexError:
                            stopped.add(robot_id)
                            # print("[IndexError] Robots stopped: " + str(stopped))
                    if (robot_id in awake.keys()) and (robot_id not in stopped):
                        if distance_to_travel[robot_id] < min_distance:
                            min_distance = distance_to_travel[robot_id]
                            next_robot_id = robot_id
                
                 # if no robot close enough to awaken
                if min_distance > remaining_movement:
                    move_bots(remaining_movement)
                    remaining_movement = 0

                    # set target
                    wakeup_target = claimed[next_robot_id]
                    wakeup_id = robots.index(wakeup_target)
                    # wake target
                    awake[wakeup_id] = wakeup_target
                    # create path for woken up target
                    robot_paths[wakeup_id] = [wakeup_target]
                    # print("Woke up " + str(wakeup_id) + " with "
                         # + str(next_robot_id))

                    # add the point of the woken up robot to the path for
                    # the wakeup_target
                    # print(claimed[next_robot_id])
                    robot_paths[next_robot_id].append(claimed[next_robot_id])
                    # print("Path for " + str(next_robot_id) + ": " + str(robot_paths[next_robot_id]))
                    # free up the waker
                    del claimed[next_robot_id]

        
        #check this function again for visgraph thingies
        for visited in robot_paths.keys():
            if len(robot_paths[visited]) > 1:
                full_path = []
                if _vis_graph is not None:
                    for j in xrange(0, len(robot_paths[visited])-1):
                        point1 = vg.Point(robot_paths[visited][j][0],
                                          robot_paths[visited][j][1])
                        point2 = vg.Point(robot_paths[visited][j+1][0],
                                          robot_paths[visited][j+1][1])
                        path_to_add = _vis_graph.get_shortest_path(
                                        point1,
                                        point2)
                        for point in path_to_add:
                            full_path.append((point.x, point.y))
                else:
                    full_path = robot_paths[visited]

                solution.append(full_path)

        solution_string_list = []
        for path in solution:
            solution_string_list.append(u','.join(repr(e) for e in path).replace(u" ", u""))

        print unicode(i) + u": " + unicode(u';'.join(solution_string_list))


def move_bots(distance):
    u"""
    Moves the robots
    """
    # print("Move bots")
    for robot_id in awake.keys():
        if robot_id not in stopped:
            # Move robot to target along x axis
            new_x = awake[robot_id][0] + ((claimed[robot_id][0] -
                                          awake[robot_id][0]) * distance /
                                          distance_to_travel[robot_id])
            # Move robot to target along y axis
            new_y = awake[robot_id][1] + ((claimed[robot_id][1] -
                                          awake[robot_id][1]) * distance /
                                          distance_to_travel[robot_id])
            awake[robot_id] = (new_x, new_y)
            # print("New robot " + str(robot_id) + " position: " + str(awake[robot_id]))
            # Update distance left to travel
            distance_to_travel[robot_id] -= distance



def save_print(polygon):
    end_pos_x = []
    end_pos_y = []
    print
    'Points of Polygon: '
    for i in range(polygon.n()):
        x = polygon[i].x()
        y = polygon[i].y()

        end_pos_x.append(x)
        end_pos_y.append(y)

        print
        x, y

    return end_pos_x, end_pos_y

def default_schedule(problem):
    """
    Default schedule algorithm
    """
    _schedule = deque()
    # print(str(problem))
    for robot in problem[0]:
        # print("Adding " + str(robot))
        _schedule.append(robot)

    return _schedule

def greedy_claim_schedule(problem):
    u"""
    Greedy claim schedule algorithm
    """


def greedy_dynamic_schedule(problem):
    u"""
    Greedy dynamic schedule algorithm
    """

if __name__ == u"__main__":
    main(sys.argv[1:])