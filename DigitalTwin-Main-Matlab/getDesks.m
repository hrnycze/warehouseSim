function desky= getDesks()
try
    % Vytvořit dočasný Python skript
    %cesta !!!NUTNÉ PŘEPSAT!!!
    tempScriptPath = 'C:\Users\Marek\Desktop\diplomka_V2\temp_script.py';

    pythonCommands = [
        "import hfdb.StorageDesks as desks", ...
        "import json", ...
        "desks.connect()", ...
        "desky = desks.getAllDesks()",...
        "result = {'Desky': desky}", ...
        "print(json.dumps(result))", ...
    ];

    fid = fopen(tempScriptPath, 'w');
    fprintf(fid, '%s\n', pythonCommands{:});
    fclose(fid);

    % Spustit Python skript z příkazové řádky
    commandLine = ['python "', tempScriptPath, '"'];
    [status, result] = system(commandLine);

    % Zpracování výstupu do proměnných v MATLABu
    jsonData = jsondecode(result);

    desky_dat = jsonData.Desky;

    desky(:,1)=desky_dat(:,1);
    desky(:,2)=desky_dat(:,6)/1000;
    desky(:,3)=desky_dat(:,7);
    desky(:,4)=desky_dat(:,8);
    desky(:,5)=desky_dat(:,4)/1000;
    desky(:,6)=desky_dat(:,5)/1000;

    % Smazat dočasný soubor
    delete(tempScriptPath);

catch exception
    disp(getReport(exception));
end
end