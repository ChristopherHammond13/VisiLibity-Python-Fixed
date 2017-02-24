import visilibity as vis
import pylab as p
import math

def calculate_solution():
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