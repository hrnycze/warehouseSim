import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process three vec3 arguments.")
    
    parser.add_argument('vec1', type=str, help='First vec3 argument (format: x,y,z)')
    parser.add_argument('vec2', type=str, help='Second vec3 argument (format: x,y,z)')
    parser.add_argument('vec3', type=str, help='Third vec3 argument (format: x,y,z)')

    args = parser.parse_args()

    # Convert string inputs to 3D vector tuples
    vec1 = tuple(map(float, args.vec1.split(',')))
    vec2 = tuple(map(float, args.vec2.split(',')))
    vec3 = tuple(map(float, args.vec3.split(',')))

    return vec1, vec2, vec3

def main():
    arrgs = sys.argv[1].split(',')
    if len(arrgs) != 4:
        print("Wrong number of arrgs!")
        print("Format: Matlab2FocasCallback.py z1,x2,x2,z3")
        sys.exit(1)
    print(f"Arrgs: {arrgs}")

    # Process the vectors as needed
    # For example, generate NC code using these vectors
    nc_code = generate_nc_code(arrgs[0], arrgs[1],arrgs[2],arrgs[3])
    print(nc_code)

def generate_nc_code(z1, x2, y2, z3):
    """
    Generates NC code for moving between three points.

    Parameters:
        point1 (tuple): The first point (x1, y1, z1).
        point2 (tuple): The second point (x2, y2, z2).
        point3 (tuple): The third point (x3, y3, z3).

    Returns:
        str: The generated NC code.
    """

    # ATTENTION: Coord need to be in float format "%2.2f"
    nc_code = [
        "%;",
        "G21;",         # Set units to millimeters (if needed)
        "G17;",                  # Select the XY plane
        "G90;",             # Absolute positioning
        f"G1 Z{z1} F500;", # Move up to the first point in Z direction
        #f"G1 X{x1} Y{y1} F1000;", # Move to the first point in XY plane
        f"G1 X{x2} Y{y2} F1000;", # Move horizontally in XY plane to the second point
        f"G1 Z{z3} F500;", # Move down to the Z coordinate of the second point
        "M30;",
        "%;"                    # End of program
    ]

    return "\n".join(nc_code)

if __name__ == "__main__":
    main()