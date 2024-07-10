function NaskladneniDesek

global typ_ID IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek pozice_time mainFig ukazatelBehu;

% Vytvoření nového okna pro aplikaci
    fig = uifigure('Name', 'Aplikace pro naskladnění desek');
    fig.Position(1) = 700;
    fig.Position(2) = 200;
    fig.Position(3) = 400;
    fig.Position(4) = 600; 

    % Nastavení barvy pozadí
    fig.Color = '#DAE6FA'; % Světle modrá barva pozadí 
    
    % konvertování..
    typ_ID_strings = arrayfun(@(x) num2str(x, '%.3f'), typ_ID(:,1)', 'UniformOutput', false);

    typ_ID_s=arrayfun(@(x) num2str(x, '%.3f'), typ_ID', 'UniformOutput', false);
    
    % konvertování
    typ_desek_strings = arrayfun(@num2str, typ_desek, 'UniformOutput', false);

    % Seznamy pro výběr s názvy
    prvniVolba = {'Vstupní', 'Výstupní'};
    
    uilabel(fig, 'Text', 'Naskladnění desek', 'Position', [100, 565, 250, 30], 'FontSize', 25);

    % První dropdown s popiskem
    prvniDropDown = uidropdown(fig, 'Items', prvniVolba, 'Position', [10, 520, 150, 22]);
    uilabel(fig, 'Text', 'Vstupní/Výstupní poloha:', 'Position', [12, 540, 150, 22]);
    
    % Druhý dropdown s popiskem
    druhaDropDown = uidropdown(fig, 'Items', {}, 'Position', [10, 480, 150, 22]);
    uilabel(fig, 'Text', 'Zvol konkrétní vstup/výstup:', 'Position', [10, 500, 150, 22]);

    % Ueditfield pro počet desek
    uilabel(fig, 'Text', 'Počet typů desek:', 'Position', [10, 450, 100, 22]);
    poctyDesekEditField = uieditfield(fig, 'Position', [120, 450, 40, 22]);

    % Funkce pro aktualizaci seznamu druhé volby na základě první volby
    function UpdateDruhaDropDown(~, ~)
        prvni = prvniDropDown.Value;
        if strcmp(prvni, 'Vstupní')
            druhaItems = arrayfun(@(x) num2str(x, '%d'), vstupni_ID, 'UniformOutput', false);
        elseif strcmp(prvni, 'Výstupní')
            druhaItems = arrayfun(@(x) num2str(x, '%d'), vystupni_ID, 'UniformOutput', false);
        else
            druhaItems = {}; % Prázdný seznam, pokud není vybrána žádná možnost
        end
        druhaDropDown.Items = druhaItems;
    end

    % Nastavení callback funkce pro aktualizaci seznamu druhé volby
    prvniDropDown.ValueChangedFcn = @UpdateDruhaDropDown;

    % Vytvoření tabulky se sedmi sloupci a nulovým počtem řádků
    data = cell(0, 7);
    columnNames = {'Počet','Typ', 'Tloušťka','Hustota','Materiál','Délka', 'Šířka' };
    columnFormats = {'numeric', typ_ID_strings, 'numeric', 'numeric', 'numeric','numeric', 'numeric'};
    % Nastavení počáteční hodnoty v prvním sloupci
    initialData = {1, [], [],[],[],[],[]}; % Zde 1 je počáteční číslo, které chcete

    tabulka = uitable(fig, 'Data', data, 'ColumnName', columnNames, 'ColumnFormat', columnFormats, 'Position', [10, 150, 380, 280], 'ColumnEditable',[true true false false false], 'RowName', []);
    tabulka.ColumnWidth={47, 45, 70,60,60,47,45};
    % Funkce pro aktualizaci tabulky na základě zadaného počtu desek
   function UpdateTabulka(~, ~)
    poctyDesek = str2double(poctyDesekEditField.Value);

    % Aktualizace počtu řádků v tabulce
    if ~isnan(poctyDesek)
        data = cell(poctyDesek, 7);
        tabulka.Data = data;
        tabulka.ColumnWidth={47, 45, 70,60,60,47,45};
    else
        % Pokud zadaný počet desek není platný, nastavte tabulku na prázdnou
        tabulka.Data = cell(0, 7);
        tabulka.ColumnWidth={47, 45, 70,60,60,47,45};
    end
   end
    
    
    tabulka.CellEditCallback = @UpdateTableRow;

    function UpdateTableRow(src, event)
    editedRow = event.Indices(1);
    editedCol = event.Indices(2);

    if editedCol == 2 % Zkontrolujte, zda byla změněna hodnota v prvním sloupci
        selectedValue = event.EditData;

        % Vyhledejte odpovídající řádek v typ_ID_strings
        idx = find(strcmp(typ_ID_strings, selectedValue));

        % Aktualizujte zbylé sloupce v daném řádku
        if ~isempty(idx)
            tabulka.Data{editedRow, 3} = typ_ID(idx, 2); % Tloušťka
            tabulka.Data{editedRow, 4} = typ_ID(idx, 3); % Hustota
            tabulka.Data{editedRow, 5} = typ_ID(idx, 4); % Materiál
            tabulka.Data{editedRow, 6} = typ_ID(idx, 5); % Délka
            tabulka.Data{editedRow, 7} = typ_ID(idx, 6); % Šířka

        else
            % Pokud hodnota není nalezena v typ_ID_strings, vynulujte zbylé sloupce
            tabulka.Data{editedRow, 3} = [];
            tabulka.Data{editedRow, 4} = [];
            tabulka.Data{editedRow, 5} = [];
            tabulka.Data{editedRow, 6} = [];
            tabulka.Data{editedRow, 7} = [];
        end
    end
end
    
% Vytvoření tlačítka "Zpět"
zpetButton = uibutton(fig, 'Text', 'Zpět', 'Position', [10, 10, 60, 30]);
zpetButton.FontColor = [1, 0, 0];

% Nastavení funkce pro tlačítko "Zpět"
zpetButton.ButtonPushedFcn = @(~,~) Zpet();

% Funkce pro zavření okna
function Zpet()
    % Zavření aktuálního okna
    delete(fig);
end
% Vytvoření tlačítka pro aplikaci
    aplikovatButton = uibutton(fig, 'Text', 'Aplikovat', 'Position', [fig.Position(3) - 110, 10, 100, 30]);
    
    % Nastavení funkce pro tlačítko "Aplikovat"
    aplikovatButton.ButtonPushedFcn = @(~,~) AplikovatFunkci();

    % Funkce pro aplikaci zvolených možností
    function AplikovatFunkci()
        set(ukazatelBehu, 'Color', [1, 0, 0]);
        drawnow;
    % Získání dat z tabulky
    tabulkaData = tabulka.Data;

    % Získání dat z druhého dropdownu
    druha = druhaDropDown.Value;

    
    % Volání skriptu pridaninovedesky s daty jako argumenty
    PridaniNoveDesky(tabulkaData, druha);   
    set(ukazatelBehu, 'Color', [0, 1, 0]);
    end
    
    % Nastavení callback funkce pro aktualizaci tabulky
    poctyDesekEditField.ValueChangedFcn = @UpdateTabulka;

    % Spuštění aktualizace seznamu druhé volby při spuštění aplikace
    UpdateDruhaDropDown([]);
end
