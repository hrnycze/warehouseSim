function DefinovatDesky()
    % Globální proměnná pro uchování dat o deskách
    global typ_ID databaze
    fig = uifigure('Name', 'Definované desky');
    fig.Position(1) = 700;
    fig.Position(2) = 200;
    fig.Position(3) = 500;
    fig.Position(4) = 600;
    fig.Color = '#DAE6FA';
    
    if databaze==0 
    % Matica pro uchování dat
    if isempty(typ_ID)
        deskData = zeros(0, 7);
    else
        deskData = typ_ID;
    end

    % Vytvoření tabulky v GUI
    tableUI = uitable(fig, 'Data', deskData, 'ColumnName', {'typ_ID', 'výška', 'hustota', 'materiál', 'délka', 'šířka','typ_zbytek'}, 'ColumnEditable', [true, true, true, true, true, true,true], 'ColumnFormat', {'numeric', 'numeric', 'numeric', 'numeric', 'numeric','numeric','numeric'}, 'Position', [20, 90, 460, 470], 'RowName', [], 'CellEditCallback', @aktualizovatData);
    
    tableUI.ColumnWidth = {50, 60, 60, 50, 60, 60,100};

    % Tlačítko pro přidání nového řádku
    addButton = uibutton(fig, 'push', 'Text', 'Přidat řádek', 'Position', [20, 55, 100, 25], 'ButtonPushedFcn', @pridatRadek);

    % Tlačítko pro uložení typů desek
    saveButton = uibutton(fig, 'push', 'Text', 'Uložit typy desek', 'Position', [260, 55, 120, 25], 'ButtonPushedFcn', @ulozitTypyDesek);

    % Tlačítko pro odebrání vybraného řádku
    removeButton = uibutton(fig, 'push', 'Text', 'Odebrat řádek', 'Position', [120, 55, 100, 25], 'ButtonPushedFcn', @odebratRadek);
    

    zpetButton = uibutton(fig, 'Text', 'Zpět', 'Position', [20, 10, 80, 30], 'ButtonPushedFcn', @(src, event) zpet());
    zpetButton.FontColor=[1,0,0];
    
    elseif databaze==1;
    
     % Matica pro uchování dat
    if isempty(typ_ID)
        deskData = zeros(0, 7);
    else
        deskData = typ_ID;
    end

    % Vytvoření tabulky v GUI
    tableUI = uitable(fig, 'Data', deskData, 'ColumnName', {'typ_ID', 'výška', 'hustota', 'materiál', 'délka', 'šířka', 'typ_zbytek'}, 'ColumnEditable', [false, false, false, false, false, false, false], 'ColumnFormat', {'numeric', 'numeric', 'numeric', 'numeric', 'numeric','numeric','numeric'}, 'Position', [20, 90, 360, 470], 'RowName', [], 'CellEditCallback', @aktualizovatData);
    
    tableUI.ColumnWidth = {50, 60, 60, 50, 60, 60, 100};


    zpetButton = uibutton(fig, 'Text', 'Zpět', 'Position', [20, 10, 80, 30], 'ButtonPushedFcn', @(src, event) zpet());
    zpetButton.FontColor=[1,0,0];
    end

    function zpet()
        close(fig);
    end

    % Funkce pro přidání nového řádku do tabulky
    function pridatRadek(~, ~)
        % Získání nejbližšího volného typ_ID
        if isempty(typ_ID)
            noveTypID = 1;
        else
            typIDs = deskData(:, 1);
            noveTypID = find(~ismember(1:max(typIDs+1), typIDs), 1, 'first');
            if isempty(noveTypID)
                noveTypID = max(typIDs) + 1;
            end
        end

        newRow = [noveTypID, 0.02, 700, 1, 2.700, 2.000, 0]; % Výchozí hodnoty pro nový řádek
        deskData = [deskData; newRow];
        tableUI.Data = deskData;

        % Aktualizace globální proměnné typ_ID
        typ_ID = deskData;
    end

    % Funkce pro aktualizaci dat po editaci buňky
    function aktualizovatData(~, eventdata)
        if ~isempty(eventdata) && ~isempty(eventdata.Indices)
            editovanyRadek = eventdata.Indices(1);
            editovanySloupec = eventdata.Indices(2);
            deskData(editovanyRadek, editovanySloupec) = eventdata.NewData;
            typ_ID = deskData;
        end
    end

    % Funkce pro uložení typů desek
    function ulozitTypyDesek(~, ~)
        save('typy_desek.mat', 'typ_ID');
    end

    % Funkce pro odebrání vybraného řádku
    function odebratRadek(~, ~)
        vybraneRozsahy = tableUI.Selection;
        if ~isempty(vybraneRozsahy)
            vybraneRadek = unique(vybraneRozsahy(:, 1));
            deskData(vybraneRadek, :) = [];
            tableUI.Data = deskData;
            typ_ID = deskData;
        end
    end
end
