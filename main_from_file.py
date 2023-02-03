# CEGE0096: Point-in-Polygon Test
# Module Coordinator: Dr. Aldo Lipani
# The program solves a problem of determining whether a point lies inside or outside a polygon
# This part of the program works with predefined files

from plotter import Plotter


# Defining a class for Object-Oriented programming with methods for each main step of Point-in-Polygon Test
class Algorithm:
    # Defining global attributes
    def __init__(self):
        # List of exclusion points for classifying special cases
        self.sp_points = []
        # Dictionary of polygon vertexes, lists to operate with polygon vertexes
        self.dict_pol = {}
        self.x_pol_list = []
        self.y_pol_list = []
        self.id_pol_list = []
        self.pol_points = []
        # Dictionary of input points, lists to operate with input points
        self.dict_pt = {}
        self.x_pt_list = []
        self.y_pt_list = []
        self.id_pt_list = []
        # Spatial extent of a Minimum Bounding Rectangle
        self.x_max = 0
        self.x_min = 0
        self.y_max = 0
        self.y_min = 0
        # Dictionary for program output
        self.output_pt = {}

    # Reading a csv with input polygon vertexes coordinates
    def read_poly(self, in_poly):
        # For error handling a try / except construction is implemented
        try:
            # File opening for reading
            with open(in_poly, 'r') as pol:
                next(pol)
                # Formatting of input data, adding of formatted data into dictionary and lists
                for input_pol in pol:
                    input_pol = input_pol.replace('\n', '')
                    input_pol = input_pol.split(',')
                    id_pol = int(input_pol[0])
                    x_pol = float(input_pol[1])
                    y_pol = float(input_pol[2])
                    self.dict_pol[id_pol] = [x_pol, y_pol]
                    self.x_pol_list.append(x_pol)
                    self.y_pol_list.append(y_pol)
                    self.id_pol_list.append(id_pol)
                    self.pol_points.append([x_pol, y_pol])
        # Predefined file reading errors
        except OSError:
            print('Could not open or read file: ' + in_poly)
            return
        except ValueError:
            print('Input polygon data is not in appropriate format!')
            return
        except SyntaxError or NameError or PermissionError:
            print('Provide a correct path to a file!')
            return
        # Checking the object is a polygon (at least a triangle)
        if len(self.x_pol_list) < 4:
            print('This is not a polygon!')
            return
        # Checking the closure condition
        if self.pol_points[0] != self.pol_points[-1]:
            print('This is not a polygon (close the polygon)!')
            return
        # Checking the unique identifiers of points
        if len(self.id_pol_list) != len(set(self.id_pol_list)):
            print('IDs of points have to be unique!')
            return

    # Reading a csv with input point coordinates
    def read_poi(self, in_poi):
        # For error handling a try / except construction is implemented
        try:
            # File opening for reading
            with open(in_poi, 'r') as pt:
                next(pt)
                # Formatting of input data, adding of formatted data into dictionary and lists
                for input_pt in pt:
                    input_pt = input_pt.replace('\n', '')
                    input_pt = input_pt.split(',')
                    id_pt = int(input_pt[0])
                    x_pt = float(input_pt[1])
                    y_pt = float(input_pt[2])
                    self.dict_pt[id_pt] = {'coordinates': [x_pt, y_pt], 'category': ''}
                    self.x_pt_list.append(x_pt)
                    self.y_pt_list.append(y_pt)
                    self.id_pt_list.append(id_pt)
        # Predefined file reading errors
        except OSError:
            print('Could not open or read file: ' + in_poi)
            return
        except ValueError:
            print('Input point data is not in appropriate format!')
            return
        except SyntaxError or NameError or PermissionError:
            print('Provide a correct path to a file!')
            return
        # Checking the presence of at least one point
        if len(self.x_pt_list) < 1:
            print('File is empty!')
            return
        # Checking the unique identifiers of points
        if len(self.id_pt_list) != len(set(self.id_pt_list)):
            print('IDs of input points have to be unique!')
            return

    # Realization of a Minimum Bounding Rectangle Algorithm
    def mbr(self):
        # defining minimums and maximums according to lists of X and Y coordinates of a polygon vertexes
        self.x_max = max(self.x_pol_list)
        self.x_min = min(self.x_pol_list)
        self.y_max = max(self.y_pol_list)
        self.y_min = min(self.y_pol_list)

        # Iterating through points to exclude those lying outside the extent of a Minimum Bounding Rectangle
        for id in self.dict_pt.keys():
            x_pt = self.dict_pt[id]['coordinates'][0]
            y_pt = self.dict_pt[id]['coordinates'][1]
            if x_pt < self.x_min or x_pt > self.x_max or y_pt < self.y_min or y_pt > self.y_max:
                self.dict_pt[id]['category'] = 'outside'

    # Implementation of the algorithm for finding points belonging to the boundaries of the polygon
    def boundary(self, x, y, id_pt=1):
        for id_pol in self.dict_pol.keys():
            # Exception for the closure point
            if id_pol == len(self.dict_pol.keys()):
                break
            # Setting polygon segments
            segment_1 = [self.dict_pol[id_pol], self.dict_pol[id_pol + 1]]
            point = [x, y]
            x1 = segment_1[0][0]
            x2 = segment_1[1][0]
            y1 = segment_1[0][1]
            y2 = segment_1[1][1]
            # Processing a case when the denominator is equal to zero, comparison of Y values
            if x1 == x2 and point[0] != x1:
                continue
            if x1 == x2 and point[0] == x1:
                if y1 <= y2:
                    if y1 <= point[1] <= y2:
                        self.dict_pt[id_pt]['category'] = 'boundary'
                        continue
                    else:
                        continue
                elif y1 >= y2:
                    if y2 <= point[1] <= y1:
                        self.dict_pt[id_pt]['category'] = 'boundary'
                        continue
                    else:
                        continue
                else:
                    continue
            # Finding line coefficients
            a = (y1 - y2) / (x1 - x2)
            b = y1 - ((y1 - y2) / (x1 - x2)) * x1
            # Calculation of whether a point belongs to the border segments, recording the result
            if point[1] == a * point[0] + b:
                if x1 <= x2 and y1 <= y2:
                    if x1 <= point[0] <= x2 and y1 <= point[1] <= y2:
                        self.dict_pt[id_pt]['category'] = 'boundary'
                elif x1 >= x2 and y1 <= y2:
                    if x2 <= point[0] <= x1 and y1 <= point[1] <= y2:
                        self.dict_pt[id_pt]['category'] = 'boundary'
                elif x1 <= x2 and y1 >= y2:
                    if x1 <= point[0] <= x2 and y2 <= point[1] <= y1:
                        self.dict_pt[id_pt]['category'] = 'boundary'
                elif x1 >= x2 and y1 >= y2:
                    if x2 <= point[0] <= x1 and y2 <= point[1] <= y1:
                        self.dict_pt[id_pt]['category'] = 'boundary'
        return

    # Implementation of the Ray Casting Algorithm with regarding of special cases
    def intersect(self, segment_1, segment_2):
        # Setting rays from points
        x1 = segment_1[0][0]
        x2 = segment_1[1][0]
        y1 = segment_1[0][1]
        y2 = segment_1[1][1]
        # Finding line coefficients
        a = (y1 - y2) / (x1 - x2)
        b = y1 - ((y1 - y2) / (x1 - x2)) * x1
        # Setting polygon segments
        x3 = segment_2[0][0]
        x4 = segment_2[1][0]
        y3 = segment_2[0][1]
        y4 = segment_2[1][1]
        # Finding the intersection point for the case when the denominator is equal to zero
        if x3 == x4:
            x_int = x3
            y_int = a * x3 + b
        # Finding the intersection point for other cases
        else:
            c = (y3 - y4) / (x3 - x4)
            d = y3 - ((y3 - y4) / (x3 - x4)) * x3
            # Considering the case when the ray runs parallel to the segment of the polygon and not coincides with it
            if c == 0 and y1 != y3:
                return 0
            # Considering the case when the ray runs parallel to the segment of the polygon and coincides with it
            if c == 0 and y1 == y3:
                # Foresight the case when coincident polygon vertex has the first identifier
                id3 = self.pol_points.index([x3, y3])
                id4 = self.pol_points.index([x4, y4])
                prev_pt = self.pol_points[id3 - 1]
                next_pt = self.pol_points[id4 + 1]
                if id3 == 0:
                    prev_pt = self.pol_points[-2]
                elif id3 == len(self.pol_points) - 1:
                    next_pt = self.pol_points[1]
                # Both coincident vertexes are written to the list of exclusion points to avoid reconsideration
                if x3 > x1:
                    self.sp_points.append([x3, y3])
                    self.sp_points.append([x4, y4])
                    if (prev_pt[1] >= y1 and next_pt[1] >= y1) or (prev_pt[1] <= y1 and next_pt[1] <= y1):
                        return 0
                    else:
                        return 1
                else:
                    return 0
            # Finding the intersection point
            x_int = (d - b) / (a - c)
            y_int = a * ((d - b) / (a - c)) + b
        # Considering the case when an intersection point is not contained in the list of polygon vertexes
        # Standard counting case
        if not [x_int, y_int] in self.pol_points:
            if x3 <= x4 and y3 <= y4:
                if x3 <= x_int <= x4 and y3 <= y_int <= y4 and x1 <= x_int <= x2:
                    return 1
                else:
                    return 0
            elif x3 >= x4 and y3 <= y4:
                if x4 <= x_int <= x3 and y3 <= y_int <= y4 and x1 <= x_int <= x2:
                    return 1
                else:
                    return 0
            elif x3 <= x4 and y3 >= y4:
                if x3 <= x_int <= x4 and y4 <= y_int <= y3 and x1 <= x_int <= x2:
                    return 1
                else:
                    return 0
            elif x3 >= x4 and y3 >= y4:
                if x4 <= x_int <= x3 and y4 <= y_int <= y3 and x1 <= x_int <= x2:
                    return 1
                else:
                    return 0
            else:
                return 0
        # Considering the case when an intersection point is contained in the list of polygon vertexes
        # Counting with regarding of exceptions
        else:
            if [x_int, y_int] != [x3, y3] and [x_int, y_int] != [x4, y4]:
                return 0
            if [x_int, y_int] in self.sp_points:
                return 0
            sp_id = self.pol_points.index([x_int, y_int])
            sp_bef = self.pol_points[sp_id - 1]
            sp_af = self.pol_points[sp_id + 1]
            # Checking which side of the ray both polygon segments lie on
            if x1 <= x_int <= x2:
                if (sp_bef[1] >= y_int and sp_af[1] >= y_int) or (sp_bef[1] <= y_int and sp_af[1] <= y_int):
                    self.sp_points.append([x_int, y_int])
                    return 0
                else:
                    self.sp_points.append([x_int, y_int])
                    return 1
            else:
                return 0

    # Launching classification for each point in a dictionary
    def classify(self):
        for id_pt in self.dict_pt.keys():
            # Calling a boundary method
            self.boundary(self.dict_pt[id_pt]['coordinates'][0], self.dict_pt[id_pt]['coordinates'][1], id_pt)
            count = 0
            self.sp_points = []
            # Skipping points, which were already classified
            if self.dict_pt[id_pt]['category'] == 'outside' or self.dict_pt[id_pt]['category'] == 'boundary':
                continue
            # Setting rays from points
            segment_1 = [self.dict_pt[id_pt]['coordinates'], [self.x_max + 1, self.dict_pt[id_pt]['coordinates'][1]]]
            for id_pol in self.dict_pol.keys():
                # Exception for the closure point
                if id_pol == len(self.dict_pol.keys()):
                    break
                # Setting polygon segments
                segment_2 = [self.dict_pol[id_pol], self.dict_pol[id_pol + 1]]
                # Setting counter and performing an evenness and odd check (parity check)
                count += self.intersect(segment_1, segment_2)
                if count % 2 == 0:
                    self.dict_pt[id_pt]['category'] = 'outside'
                else:
                    self.dict_pt[id_pt]['category'] = 'inside'

    # Creating an output csv
    def write_output(self, out_path):
        # Creating an output dictionary
        for id in self.dict_pt.keys():
            self.output_pt[id] = self.dict_pt[id]['category']

        # For error handling a try / except construction is implemented
        try:
            # Writing an output csv file from a dictionary
            with open(out_path, 'w') as out:
                # Formatting the headings
                out.write('id,category\n')
                print('Results of Point-in-Polygon Algorithm:')
                # Formatting the output data and providing a print of results for input points
                for id in self.output_pt.keys():
                    out.write(str(id) + ',' + self.output_pt[id] + '\n')
                    print('Point ' + str(id) + ' is ' + self.output_pt[id])
        # Error handling to check a provided path to a file
        except SyntaxError or NameError or PermissionError:
            print('Provide a correct path to a file!')
            return

    # Visualization of all objects on the graph
    def plot(self):
        plotter = Plotter()
        # Plotting of a testing polygon
        plotter.add_polygon(self.x_pol_list, self.y_pol_list)
        # Plotting of a Minimum Bounding Rectangle
        plotter.add_mbr(self.x_max, self.x_min, self.y_max, self.y_min)
        for p in range(len(self.x_pt_list)):
            # Plotting of a Rays, build during the Ray Casing Algorithm implementation as arrows
            if self.x_min <= self.x_pt_list[p] <= self.x_max and self.y_min <= self.y_pt_list[p] <= self.y_max:
                plotter.add_arrow(self.x_pt_list[p], self.y_pt_list[p], self.x_max + 1 - self.x_pt_list[p], 0)
            # Plotting of classified points with their ID labels
            plotter.add_point(self.x_pt_list[p], self.y_pt_list[p], self.output_pt[p + 1], p + 1)
        plotter.show()


# Defining main function
def main(in_poly='polygon.csv', in_poi='input.csv', out_path='output.csv'):
    pip = Algorithm()

    # Referring to methods
    try:
        pip.read_poly(in_poly)
        pip.read_poi(in_poi)
        pip.mbr()
        pip.classify()
        pip.write_output(out_path)
        pip.plot()
    except Exception:
        return


if __name__ == '__main__':
    main()
