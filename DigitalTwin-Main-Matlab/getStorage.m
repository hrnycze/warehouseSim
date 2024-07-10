function sklad= getStorage()
try
    % vytvoreni docasneho python skriptu
    tempScriptPath = 'C:\Users\Marek\Desktop\diplomka_V2\temp_script.py';
    
    % importovani vystupu do pythonu, pripojeni na databazi, ziskani info
    pythonCommands = [
        "import hfdb.StorageData as storage", ...
        "import json", ...
        "storage.connect()", ...
        "sklad = storage.getStorage()", ...
        "result = {'Sklad': sklad}", ...
        "print(json.dumps(result))", ...
    ];

    fid = fopen(tempScriptPath, 'w');
    fprintf(fid, '%s\n', pythonCommands{:});
    fclose(fid);

    % spusteni pythonu z prikazoveho radku
    commandLine = ['python "', tempScriptPath, '"'];
    [status, result] = system(commandLine);

    % zpracovani vystupu do matlabu
    jsonData = jsondecode(result);
    % uprava a vybrani potrebnych dat
    sklad=jsonData.Sklad;
    sklad=sklad(:,3:end);
    
    % smazani docasneho souboru
    delete(tempScriptPath);

catch exception
    disp(getReport(exception));
end
end