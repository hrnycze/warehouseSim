def gcode_fce_short(name, comment, x1, y1, z1, x2, y2, z2):
#     """
#     GCODE_FCE_SHORT Summary of this function goes here
#     This function is for easy trajectory planner
#     """
#     # Inputs
    # filename = output_file + "\\" + name + ".txt"  # Generation of file .txt
    filename = name + ".txt"  # Generation of file .txt
#     # Constants
    z_max = 3000
    F0 = 60
    F1 = 2000
    F2 = 10000
    F3 = 2000


    with open(filename, "w+") as fileID:
        # Gcode generation
        # Header
        fileID.write('%;\n')
        fileID.write('<' + name + '>(' + comment + ')(000H01M54S);\n') # (TOOL=D12FEM)
        fileID.write('N00 T1 M06;\n')
        fileID.write('N10G92X' + str(x1) + 'Y' + str(y1) + 'Z' + str(z1) + ';\n')
        fileID.write('N20G01X' + str(x1) + 'Y' + str(y1) + 'Z' + str(z1 + 10) + 'F' + str(F0) + ';\n')
        fileID.write('N30G01X' + str(x1) + 'Y' + str(y1) + 'Z' + str(z_max) + 'F' + str(F1) + ';\n')
        fileID.write('N40G01X' + str(x2) + 'Y' + str(y2) + 'Z' + str(z_max) + 'F' + str(F2) + ';\n')
        fileID.write('N50G01X' + str(x2) + 'Y' + str(y2) + 'Z' + str(z2 + 10) + 'F' + str(F3) + ';\n')
        fileID.write('N60G01X' + str(x2) + 'Y' + str(y2) + 'Z' + str(z2) + 'F' + str(F0) + ';\n')
        # Main code
        # Foot
        fileID.write('M30;\n')
        fileID.write('%;\n')


gcode_fce_short("name", "comment", 40, 80, 120, 400, 5000, 30)

