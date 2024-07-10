import os

def generate_nc_code(fname, z1, x2, y2, z3):
    """
    Generates NC code for moving between three points.

    Parameters:
        fname (str): The filename or identifier for the NC program.
        z1 (float): The Z coordinate for the first point.
        x2 (float): The X coordinate for the second point.
        y2 (float): The Y coordinate for the second point.
        z3 (float): The Z coordinate for the third point.

    Returns:
        str: The generated NC code.
    """
    # Generate NC code

    # ATTENTION: Coord need to be in float format "%2.2f"
    nc_code = [
        "%;",
        f"<{fname}>;",
        "G21;",         # Set units to millimeters (if needed)
        "G17;",                  # Select the XY plane
        "G90;",             # Absolute positioning
        f"G1 Z{z1} F90000;", # Move up to the first point in Z direction
        #f"G1 X{x1} Y{y1} F1000;", # Move to the first point in XY plane
        f"G1 X{x2} Y{y2};", # Move horizontally in XY plane to the second point
        f"G1 Z{z3};", # Move down to the Z coordinate of the second point
        "M30;",
        "%;"                    # End of program
    ]

    return "\n".join(nc_code)

def generate_save_nc_txt(fname, fpath, z1, x2, y2, z3):
    string = generate_nc_code(fname, z1, x2, y2, z3)
    with open(f"{fpath}/{fname}.txt", "w") as txt_file:
        txt_file.write(string)
    print(f"File {fname}.txt was saved.")

if __name__ == "__main__":
    # Example usage
    point1 = (0, 0, 10) # Example coordinates
    point2 = (10, 10, 10)
    point3 = (10, 10, 0)

    fname = "DIGITAL_TWIN_MOVE"

    nc_code = generate_nc_code(fname,point1, point2, point3)
    print(nc_code)

    
    file_path = os.getcwd()
    with open(f"{file_path}/{fname}.txt", "w") as txt_file:
        txt_file.write(nc_code)

    print(f"File {fname}.txt was saved.")