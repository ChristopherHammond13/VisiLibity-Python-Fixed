import visilibity as vis
import pylab as p
import math
from utils import parser
import sys
from io import open
import os.path
import getopt


#reverse a list to make it ccw
def rev(random = []):
    return random[::-1]

def checkCounterclockkwise(listThing = [], sum): #make sure you initialize sum to 0
    for i in range(0, len(listThing)):
        x = listThing[i+1][0] - listThing[i][0]
        y = listThing[i][1] + listThing[i+1][1]
        sum = sum + (x*y)
        if sum > 0: #if sum is positive, it is clockwise
            return False
        else: #if sum is negative, it is counter clockwise
            return True


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
        polygonsPlain = [] #polygon coordinates
        polygonsVis = [[]] #polygon coordinates with vis points already assigned
        #iterating over all the robots and making them vis point thingies
        for x in problemset.values():
            for y in x[0]: #first value in the tuple, which contains list of robots 
                robotsPlainList.append(y) #add this to a generic robots list just in case
                newThingy = vis.Point(y[0], y[1]) #hope dis works, because list contains tuples of coordinates
                robots.append(newThingy)
        
        #adding polygons to a random list just for bants
        for x in problemset.values():
            for y in x[1]:
                polygonsPlain.append(y)
        
        if(checkCounterclockkwise(polygonsPlain) == False): #reversing the list if the points aren't in counter-clockwise order
            rev(polygonsPlain)
        


        for x in polygonsPlain:
            i = -1
            i += 1
            for y in x:
                otherNewThingy = vis.Point(y[0], y[1])
                polygonsVis[i].append(otherNewThingy)
                

                
                


            

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

    robot1 = vis.Point(0, 1)
    robot2 = vis.Point(6, 2)

    obstacle = vis.Polygon([vis.Point(8,1),vis.Point(4,1),vis.Point(4,4),vis.Point(5,2), vis.Point(8,1)])
    obstacle_x = [8, 4, 4, 5, 8]
    obstacle_y = [1, 1, 4, 2, 1]

    obstacle2 = vis.Polygon([vis.Point(1,2), vis.Point(1,4), vis.Point(3,4), vis.Point(3,2), vis.Point(1,2)][::-1])
    obstacle2_x = [1, 1, 3, 3, 1][::-1]
    obstacle2_y = [2, 4, 4, 2, 2][::-1]

    env = vis.Environment([walls, obstacle, obstacle2])

    robot1.snap_to_boundary_of(env, epsilon)
    robot1.snap_to_vertices_of(env, epsilon)

    isovist = vis.Visibility_Polygon(robot1, env, epsilon)

    shortest_path = env.shortest_path(robot1, robot2, epsilon)

    point_x, point_y = save_print(isovist)

    point_x.append(isovist[0].x())
    point_y.append(isovist[0].y())

    p.title('Shortest (????) Path')

    p.xlabel('X Position')
    p.ylabel('Y Position')

    p.plot(wall_x, wall_y, 'black')

    p.plot([robot1.x()], [robot1.y()], 'go')

    p.plot([robot2.x()], [robot2.y()], 'go')

    p.plot(obstacle_x, obstacle_y, 'r')
    p.plot(obstacle2_x, obstacle2_y, 'r')
    
    print "Shortest Path length from observer to end: ", shortest_path.length()

    print "Number of options: ", shortest_path.size()
    polyline = []
    for x in range(0, shortest_path.size()):
        point = shortest_path.getVertex(x)
        print "(", point.x(), ", ", point.y(), ")"
        polyline.append(point)

    p.show()

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

if __name__ == "__main__":
    calculate_solution()