def generate_nc_code(point1, point2, point3):
    """
    Generates NC code for moving between three points.

    Parameters:
        point1 (tuple): The first point (x1, y1, z1).
        point2 (tuple): The second point (x2, y2, z2).
        point3 (tuple): The third point (x3, y3, z3).

    Returns:
        str: The generated NC code.
    """
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    x3, y3, z3 = point3

    # Generate NC code
    nc_code = [
        "G21 ; Set units to millimeters",         # Set units to millimeters (if needed)
        "G17 ; Select XY plane",                  # Select the XY plane
        "G90 ; Absolute positioning",             # Absolute positioning
        f"G0 Z{z1} ; Move up to the first point", # Move up to the first point in Z direction
        f"G0 X{x1} Y{y1} ; Move to the first point in XY plane", # Move to the first point in XY plane
        f"G1 X{x2} Y{y2} F1000 ; Linear move to the second point in XY plane", # Move horizontally in XY plane to the second point
        f"G1 Z{z2} F500 ; Move down to the Z coordinate of the second point", # Move down to the Z coordinate of the second point
        f"G1 X{x3} Y{y3} F1000 ; Linear move to the third point in XY plane", # Move horizontally in XY plane to the third point
        f"G1 Z{z3} F500 ; Move down to the third point", # Move down to the third point
        "M30 ; End of program"                    # End of program
    ]

    return "\n".join(nc_code)

if __name__ == "__main__":
    # Example usage
    point1 = (0, 0, 10) # Example coordinates
    point2 = (10, 10, 10)
    point3 = (10, 10, 0)

    nc_code = generate_nc_code(point1, point2, point3)
    print(nc_code)