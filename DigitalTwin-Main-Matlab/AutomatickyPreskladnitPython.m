function AutomatickyPreskladnit
    
    global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
    global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
    global pocp endp pocp2 endp2
    global xtraj ytraj ztraj natoceni konec_time
    global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc A ukazatelBehu mainFig
    global typ_ID pozice_typ_ID

    vybranySoubor = ''; % Globální proměnná pro uchování cesty k vybranému souboru

    % Vytvoření nového okna pro automatické přeskladnění
    automatickePreskladneniOkno = uifigure('Name', 'Aut. přeskladnění', 'Position', [700, 350, 550, 500]);
    automatickePreskladneniOkno.Color = '#DAE6FA';

    tabulka_desky_pocet = uitable(automatickePreskladneniOkno, 'Position', [290, 345, 260, 140], 'ColumnName', {'Typ Desky', 'Pocet ve skladu'}, 'ColumnEditable', [false false],'ColumnWidth', { 100, 100},'RowName', []);
    
    % % Popisek pro výběr souboru
    % popisekText = uilabel(automatickePreskladneniOkno, 'Text', 'Vyberte sekvenci přeskladnění', 'Position', [150, 400, 140, 30]);
    % 
    % % Tlačítko pro výběr souboru
    % vyberSouborButton = uibutton(automatickePreskladneniOkno, 'Text', 'Vybrat soubor', 'Position', [20, 400, 120, 30], 'ButtonPushedFcn', @vyberSouborCallback);
    pathfindingButton = uibutton(automatickePreskladneniOkno, 'Text', 'Pathfinding', 'Position', [20, 400, 120, 30], 'ButtonPushedFcn', @PathfindingCallback);
    % 
    % Tabulka pro zobrazení načtených hodnot
    tabulka = uitable(automatickePreskladneniOkno, 'Position', [290, 100, 260, 250], 'ColumnName', {'Počáteční pozice', 'Koncová pozice'}, 'ColumnEditable', [false false],'ColumnWidth', { 120, 120},'RowName', []);
    
    
    % tabulka2 = uitable(automatickePreskladneniOkno, 'Position', [280, 100, 260, 250], 'ColumnName', {'Počáteční pozice', 'Koncová pozice'}, 'ColumnEditable', [false false],'ColumnWidth', { 120, 120},'RowName', []);
    % 
    % % Textové pole pro zobrazení vybraného souboru
    % vybranySouborText = uitextarea(automatickePreskladneniOkno, 'Value', vybranySoubor, 'Position', [20, 360, 260, 30]);

    % Tlačítko pro spuštění automatického přeskladnění
    preskladneniButton = uibutton(automatickePreskladneniOkno, 'Text', 'Aut. přeskladnit', 'Position', [180, 10, 100, 30], 'ButtonPushedFcn', @spustitPreskladneni);
    preskladneniButton.FontColor = [0.5, 0.8, 0.5];
    % Tlačítko pro zavření okna
    zpetButton = uibutton(automatickePreskladneniOkno, 'Text', 'Zpět', 'Position', [20, 10, 80, 30], 'ButtonPushedFcn', @zpetButtonCallback);
    zpetButton.FontColor = [1, 0, 0];

    panelMoznosti = uipanel(automatickePreskladneniOkno, 'Position', [20, 50, 260, 40]);

    % Rozbalovací seznam s možnostmi
    moznosti = {'Aktuální stav skladu', 'Vymazat a generovat desky', 'Generovat nové desky', 'Načíst desky z databáze'};
    vyberMoznosti = uicontrol(panelMoznosti, 'Style', 'popupmenu', 'String', moznosti, 'Position', [0, 0, 260, 40]);

    % Callback funkce pro tlačítko vybrat soubor
    function vyberSouborCallback(~, ~)
        % Zobrazit dialog pro výběr souboru
        [soubor, cesta] = uigetfile('*.txt', 'Vyberte soubor pro automatické přeskladnění (*.txt)');
        
        % Aktualizovat globální proměnnou s cestou k vybranému souboru
        vybranySoubor = fullfile(cesta, soubor);
        
        % Aktualizovat textové pole pro zobrazení vybraného souboru
        vybranySouborText.Value = vybranySoubor;
        
        % Kontrola a načtení souboru do matice A
        try
            fileID = fopen(vybranySoubor, 'r');
            formatSpec = '%d %f';
            sizeA = [2 inf];
            A = fscanf(fileID, formatSpec, sizeA);
            A = A';
            UpdateTabulky();
            catch
            warndlg('Chyba při načítání souboru, vybrán špatný soubor.', 'Chyba');
            UpdateTabulky();
        end
    end
    function PathfindingCallback(~,~)
        %% Define set of action of manipulator store in matrix A
        %disp(size(tabulka2.Data))
        out_order = zeros(size(tabulka2.Data,1),1);
        for i=1 : size(tabulka2.Data,1)
             %disp(tabulka2.Data{i,2})
             out_order(i) = str2double(tabulka2.Data{i,2});
        end
       

        str = Matlab2PathfindingCallback({out_order});
        
        % Remove the brackets and parentheses
        str = strrep(str, '[', '');
        str = strrep(str, ']', '');
        str = strrep(str, '(', '');
        str = strrep(str, ')', '');
        
        % Split the string by comma and space
        parts = split(str, ', ');
        
        % Initialize an array to hold the numeric values
        values = zeros(1, length(parts));
        
        % Convert each part to a numeric value
        for i = 1:length(parts)
            values(i) = str2double(parts{i});
        end
        
        % Reshape the values into a 2xN matrix
        A = reshape(values, 2, [])';
        
        % Display the matrix
        disp(A);

        UpdateTabulky();
    end
    function UpdateTabulky()
            tabulka.Data = {};
            for i = 1:size(A, 1)
                

                vstupniPozice = A(i, 1);
                vystupniPozice = A(i, 2);

                % Pravidla pro vstupní pozici
                if vstupniPozice < 0
                    if any(vstupniPozice == vstupni_ID)
                        vstupniPoziceText = sprintf('Vstupní %d', find(vstupniPozice == vstupni_ID));
                    elseif any(vstupniPozice == vystupni_ID)
                        vstupniPoziceText = sprintf('Výstupní %d', find(vstupniPozice == vystupni_ID));
                    else
                        vstupniPoziceText = 'CHYBA';
                    end
                else
                    vstupniPoziceText = sprintf('Pozice %d', vstupniPozice);
                end

                % Pravidla pro výstupní pozici
                if vystupniPozice < 0
                    if any(vystupniPozice == vstupni_ID)
                        vystupniPoziceText = sprintf('Vstupní %d', find(vystupniPozice == vstupni_ID));
                    elseif any(vystupniPozice == vystupni_ID)
                        vystupniPoziceText = sprintf('Výstupní %d', find(vystupniPozice == vystupni_ID));
                    else
                        vystupniPoziceText = 'CHYBA';
                    end
                else
                
                    vystupniPoziceText = sprintf('Pozice %d', vystupniPozice);
                end

                % Aktualizace hodnot v tabulce
                tabulka.Data{i, 1} = vstupniPoziceText;
                tabulka.Data{i, 2} = vystupniPoziceText;
            end
    
    end

    % Callback funkce pro tlačítko Zpět
    function zpetButtonCallback(~, ~)
        % Zavřít okno
        close(automatickePreskladneniOkno);
    end

    % Callback funkce pro tlačítko Aut. přeskladnění
    function spustitPreskladneni(~, ~)
         set(ukazatelBehu, 'Color', [1, 0, 0]);
         drawnow;
        vybranaMoznost = moznosti{get(vyberMoznosti, 'Value')};

        % Implementujte kód na základě vybrané možnosti
        switch vybranaMoznost
            case 'Načíst desky z databáze'
                %...
            case 'Vymazat a generovat desky'
                % vymazat celý sklad a poté vygenerovat náhodně desky 
                vymazanidesek();
                GenerovaniDesek();
                spustitAutomat();
            case 'Generovat nové desky'
                % nevymazá desky, pouze přidá další náhodně vygenerované
                GenerovaniDesek();
                pause(1);
                spustitAutomat();
            case 'Aktuální stav skladu'
                % Žádné generování neproběhne
                spustitAutomat();
        end
         set(ukazatelBehu, 'Color', [0, 1, 0]);
    end
    function spustitAutomat()
        for i=1:length(A(:,1))
            spustitOperaci()
        end
    end
    
    function spustitOperaci()
        param=A(1,:);
        spousteci(param);
        A=A(2:end,:);
        UpdateTabulky();
    end

    %% volba vystupni fronta desek

    %% najdi dostupne desky ve skladu
    
    
    dostupne_desky = [];
    dostupne_desky_pocet = [];
    
    typ_ID_copy = typ_ID;

    temp = pozice_typ_ID((IO_pocet+1):length(pozice_typ_ID));
    for i = 1: length(temp)
        dostupne_desky = [dostupne_desky; temp{i}];
    end
    % disp(dostupne_desky')

    unique_desky = unique(dostupne_desky);

    counts = zeros(size(unique_desky));

    for i=1 : length(counts)
        counts(i) = sum(dostupne_desky == unique_desky(i)); 
    end
    
    % disp(unique_desky')
    % disp(counts')

    row_to_remove = false(size(typ_ID,1),1);

    for i=1 : size(unique_desky,1)
        if any(ismember(typ_ID(:,1), unique_desky(i)))
            row_to_remove(unique_desky(i)) = true;
        end
    end

    typ_ID_copy = typ_ID_copy(row_to_remove,:);

    for i=1 : length(counts)
        tabulka_desky_pocet.Data{i,1} = unique_desky(i);%sprintf("%d",unique_desky(i));
        tabulka_desky_pocet.Data{i,2} = counts(i);%sprintf("%d",counts(i));
    end

    % disp(typ_ID_copy)

    % konvertování..
    typ_ID_strings = arrayfun(@(x) num2str(x, '%.0f'), typ_ID_copy(:,1)', 'UniformOutput', false);
     % Vytvoření tabulky se sedmi sloupci a nulovým počtem řádků
        
   
    
    % Ueditfield pro počet desek na vystup
    uilabel(automatickePreskladneniOkno, 'Text', 'Počet desek k vyskladneni:', 'Position', [10, 450, 300, 22]);
    poctyDesekEditField = uieditfield(automatickePreskladneniOkno, 'Position', [170, 450, 40, 22]);
    % Nastavení callback funkce pro aktualizaci tabulky
    poctyDesekEditField.ValueChangedFcn = @UpdateTabulka;

    data = cell(0, 7);
    columnNames = {'Počet','Typ', 'Tloušťka','Hustota','Materiál','Délka', 'Šířka' };
    columnFormats = {'numeric', typ_ID_strings, 'numeric', 'numeric', 'numeric','numeric', 'numeric'};

    tabulka2 = uitable(automatickePreskladneniOkno, 'Data', data, 'ColumnName', columnNames, 'ColumnFormat', columnFormats, 'Position', [20, 100, 260, 250], 'ColumnEditable',[true true false false false], 'RowName', []);
    tabulka2.ColumnWidth={47, 45, 70,60,60,47,45};
    tabulka2.CellEditCallback = @UpdateTableRow;

    % Funkce pro aktualizaci tabulky na základě zadaného počtu desek
   function UpdateTabulka(~, ~)
    poctyDesek = str2double(poctyDesekEditField.Value);

    % Aktualizace počtu řádků v tabulce
    if ~isnan(poctyDesek)
        data = cell(poctyDesek, 7);
        tabulka2.Data = data;
        tabulka2.ColumnWidth={47, 45, 70,60,60,47,45};
    else
        % Pokud zadaný počet desek není platný, nastavte tabulku na prázdnou
        tabulka2.Data = cell(0, 7);
        tabulka2.ColumnWidth={47, 45, 70,60,60,47,45};
    end
   end
    
function UpdateTableRow(src, event)
    editedRow = event.Indices(1);
    editedCol = event.Indices(2);

    if editedCol == 2 % Zkontrolujte, zda byla změněna hodnota v prvním sloupci
        selectedValue = event.EditData;

        % Vyhledejte odpovídající řádek v typ_ID_strings
        idx = find(strcmp(typ_ID_strings, selectedValue));

        % Aktualizujte zbylé sloupce v daném řádku
        if ~isempty(idx)
            tabulka2.Data{editedRow, 3} = typ_ID(idx, 2); % Tloušťka
            tabulka2.Data{editedRow, 4} = typ_ID(idx, 3); % Hustota
            tabulka2.Data{editedRow, 5} = typ_ID(idx, 4); % Materiál
            tabulka2.Data{editedRow, 6} = typ_ID(idx, 5); % Délka
            tabulka2.Data{editedRow, 7} = typ_ID(idx, 6); % Šířka

        else
            % Pokud hodnota není nalezena v typ_ID_strings, vynulujte zbylé sloupce
            tabulka2.Data{editedRow, 3} = [];
            tabulka2.Data{editedRow, 4} = [];
            tabulka2.Data{editedRow, 5} = [];
            tabulka2.Data{editedRow, 6} = [];
            tabulka2.Data{editedRow, 7} = [];
        end
    end
end
end
