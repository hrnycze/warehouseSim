function stdout = Matlab2PathfindingCallback()

    ScriptPath = "C:\Users\Jan-Lenovo\Documents\HoufekGJ\warehouseSim\Pathfinding-Python\PathfindingCallback.py";

    % Spustit Python skript z příkazové řádky
    commandLine = ['python ' + ScriptPath + ' "[6, 5], [2], [7, 3, 5], [5, 8, 1, 9, 3, 3, 1, 5]" "[1,2,3]" "[3,5,6]" '];
    [status, stdout] = system(commandLine);

    %disp(stdout)

end