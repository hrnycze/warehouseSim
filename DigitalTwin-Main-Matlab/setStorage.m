function setStorage(data)
try
    % Příprava dat pro zápis
    dataString = data;

    % Vytvoření dočasného Python skriptu
    tempScriptPath = 'C:\Users\Marek\Desktop\diplomka_V2\temp_script.py';
    
    % to co budeme zapisovat do pythonu...
    pythonCommands = [
        "import hfdb.StorageData as storage",
        "import json",
        "from time import time",  
        "storage.connect()",
        "data = " + dataString,
        "aktualni_cas = int(time())", 
        "storage.setStorage(aktualni_cas, data)",
        "storage.close()",
    ];

    fid = fopen(tempScriptPath, 'w');
    fprintf(fid, '%s\n', pythonCommands{:});
    fclose(fid);

    % Spustit Python skript z příkazové řádky
    commandLine = ['python "', tempScriptPath, '"'];
    [status, result] = system(commandLine);

    % Smazat dočasný soubor
    delete(tempScriptPath);

catch exception
    disp(getReport(exception));
end
end
