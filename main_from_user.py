# CEGE0096: Point-in-Polygon Test
# Module Coordinator: Dr. Aldo Lipani
# The program solves a problem of determining whether a point lies inside or outside a polygon
# This part of the program works with user input

from main_from_file import main as algorithm


# Defining main function
def main():
    # Dialogue with a User for choosing point entering from csv file or from a keyboard (as a pair of coordinates)
    answer = 0
    while answer != str(1) and answer != str(2):
        answer = str(input('How do you want to provide points? Type 1 for csv / Type 2 for keyboard input: '))
        if answer == str(1):
            in_poi = input('Insert a path to points file: ')
        elif answer == str(2):
            x_user = input('Insert X coordinate: ')
            y_user = input('Insert Y coordinate: ')
            with open('input_user.csv', 'w') as out:
                out.write('id,x,y\n')
                out.write('1,' + str(x_user) + ',' + str(y_user))
                in_poi = 'input_user.csv'
        else:
            print('Provide an answer as 1 / 2! ')

    # Entering the path to the csv file with polygon vertexes
    in_poly = input('Insert a path to polygon file: ')

    # Entering the path to the output algorithm results
    out_path = input('Insert where to write the output: ')

    # Launching the main algorithm
    algorithm(in_poly=in_poly, in_poi=in_poi, out_path=out_path)


if __name__ == '__main__':
    main()
