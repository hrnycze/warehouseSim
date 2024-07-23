function stdout = Matlab2PathfindingCallback(out_order, inner_state)
    global IO_pocet pozice_typ_ID

    %root = "D:\Dropbox\Houfek Upload\TREND 2020\2024\3_Warehouse\warehouseSim" ;
    Root = fullfile(pwd, '..');
    ScriptPath = Root + "\Pathfinding-Python\PathfindingCallback.py";
    
    %inner_state = pozice_typ_ID(IO_pocet+1:length(pozice_typ_ID));
    
    % mat to str
    % Define the cell array
    cellArray = inner_state;
    
    % Initialize the final string
    inner_state_str = "";
    
    % Loop through each cell
    for i = 1:length(cellArray)
        % Convert the cell contents to a string
        cellContent = cellArray{i};
        % needed reverse vector % ING. VLcek totally ingnored Ing. hrncir's work !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        cellString = sprintf('%d,', flipud(cellContent)); 
        % Remove the trailing comma
        cellString = cellString(1:end-1);
        % Add brackets
        cellString = ['[' cellString ']'];
        
        % Concatenate to the final string
        if i == 1
            inner_state_str = cellString;
        else
            inner_state_str = [inner_state_str ', ' cellString];
        end
    end
    
        
    %mat to str
    in_order = pozice_typ_ID(1);

    % needed reverse vector % ING. VLcek totally ingnored Ing. hrncir's work !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cellString = sprintf('%d,', flipud(in_order{1}));

    % Remove the trailing comma
    cellString = cellString(1:end-1);
    % Add brackets
    cellString = ['[' cellString ']'];
    in_order_str = cellString;

    

    %mat to str
    %out_order = {[2;3]};%pozice_typ_ID(1);

    % needed reverse vector % ING. VLcek totally ingnored Ing. hrncir's work !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    cellString = sprintf('%d,', flipud(out_order{1})); % ING. VLcek totally ingnored Ing. hrncir's work !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    % Remove the trailing comma
    cellString = cellString(1:end-1);
    % Add brackets
    cellString = ['[' cellString ']'];
    out_order_str = cellString;

    
    
   

    % Display the final string
    disp(inner_state_str);
    disp(in_order_str)
    disp(out_order_str)


    % Spustit Python skript z příkazové řádky
    %commandLine = ['python ' + ScriptPath + ' "[14], [4,15,1,1], [2,6,15], [4,10,12]" "[2,3]" "[1,1]" '];

    commandLine = ['python ' + ScriptPath + ' "' + inner_state_str + '" "' + in_order_str + '" "' + out_order_str + '"'];
    
    %disp(commandLine)

    [status, stdout] = system(commandLine);

    %disp(stdout)

end