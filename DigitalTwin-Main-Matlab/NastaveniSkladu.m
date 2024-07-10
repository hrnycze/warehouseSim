%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%% Funkce pro nastavení skladu %%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function NastaveniSkladu
global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
global pocp endp pocp2 endp2
global xtraj ytraj ztraj natoceni konec_time
global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc var_rigid A pozice_typ_ID typ_ID mainFig ukazatelBehu
global databaze

    % Vytvoření nového okna pro aplikaci
    fig = uifigure('Name', 'Naskladnění desek');
    fig.Position(1) = 700;
    fig.Position(2) = 200;
    fig.Position(3) = 400;
    fig.Position(4) = 600;

    % Nastavení barvy pozadí
    fig.Color = '#DAE6FA'; % Světle modrá barva pozadí

    uilabel(fig, 'Text', 'Konfigurace skladu', 'Position', [100, 570, 250, 30], 'FontSize', 25);

    % Popisek pro vstupní polohy
    uilabel(fig, 'Text', 'Vstupní polohy', 'Position', [12, 460, 180, 22], 'FontSize', 14);

    druhyEditField = uieditfield(fig, 'numeric', 'Value', 1, 'Position', [342, 540, 25, 22]);
    uilabel(fig, 'Text', 'Počet výstupních poloh:', 'Position', [212, 540, 140, 22]);

    prvniEditField = uieditfield(fig, 'numeric', 'Value', 1, 'Position', [136, 540, 25, 22]);
    uilabel(fig, 'Text', 'Počet vstupních poloh:', 'Position', [12, 540, 140, 22]);
    
    % Tlačítko pro konfiguraci skladu
    configureButton = uibutton(fig, 'push', 'Text', 'Konfigurovat sklad', 'Position', [260, 20, 120, 30]);
    configureButton.ButtonPushedFcn = @(~, ~) ConfigureSklad();
    
    % Tlačítko pro návrat z konfigurace skladu
    backButton = uibutton(fig, 'push', 'Text', 'Zpět', 'Position', [20, 20, 70, 30]);
    backButton.ButtonPushedFcn = @(~, ~) BackFromConfiguration();
    backButton.FontColor=[1,0,0];

    vstupni_polohy_size = 1;
    vstupni_polohy = zeros(vstupni_polohy_size, 2); % Initialize vstupni_polohy
    vystupni_polohy_size = 1;
    vystupni_polohy = zeros(vystupni_polohy_size, 2); % Initialize vystupni_polohy
    stohy_polohy_size = vstupni_polohy_size+vystupni_polohy_size;
    stohy_polohy = zeros(stohy_polohy_size, 2);

    % vytvoření tabulky pro editování vstupni_polohy
    vstupni_table = uitable(fig, 'Data', vstupni_polohy, 'Position', [10, 330, 180, 122], 'ColumnName', {'X', 'Y'}, 'ColumnEditable', [true, true]);
    vstupni_table.ColumnWidth = {60, 60};

    % Popisek pro výstupní polohy
    uilabel(fig, 'Text', 'Výstupní polohy', 'Position', [212, 460, 180, 22], 'FontSize', 14);
    
    table=uitable(fig,'Data', stohy_polohy, 'Position', [95, 70, 210, 212], 'ColumnName', {'X', 'Y'}, 'ColumnEditable', [true, true]);
    table.ColumnWidth = {60, 60};

    % vytvoření tabulky pro editování vystupni_polohy
    vystupni_table = uitable(fig, 'Data', vystupni_polohy, 'Position', [210, 330, 180, 122], 'ColumnName', {'X', 'Y'}, 'ColumnEditable', [true, true]);
    vystupni_table.ColumnWidth = {60, 60};

    skladovaciPocetEditField = uieditfield(fig, 'numeric', 'Value', stohy_polohy_size, 'Position', [155, 290, 35, 22]);
    uilabel(fig, 'Text', 'Počet skladovacích poloh:', 'Position', [10, 290, 150, 22]);
    
    % pokud se něco změní...
    prvniEditField.ValueChangedFcn = @(~, ~) UpdateVstupniPolohySize(); 
    druhyEditField.ValueChangedFcn = @(~, ~) UpdateVystupniPolohySize();
    vstupni_table.CellEditCallback = @(~, ~) UpdateTabulka();
    vystupni_table.CellEditCallback = @(~, ~) UpdateTabulka();
    skladovaciPocetEditField.ValueChangedFcn = @(~, ~) UpdateTabulka();
    
    vstupniEditField = uieditfield(fig, 'text', 'Value', '', 'Position', [10, 490, 140, 22]);
    uilabel(fig, 'Text', 'Vstupní ID (ID s mezerou):', 'Position', [12, 510, 230, 22]);

    vystupniEditField = uieditfield(fig, 'text', 'Value', '', 'Position', [210, 490, 140, 22]);
    uilabel(fig, 'Text', 'Výstupní ID (ID s mezerou):', 'Position', [212, 510, 230, 22]);
    
    % tlačítko pro ověření vstupu
    confirmButtonInput = uibutton(fig, 'push', 'Text', 'OK', 'Position', [155, 490, 30, 22]);
    confirmButtonInput.ButtonPushedFcn = @(~, ~) ValidateInput('input', confirmButtonInput);
    
    % tlačítko pro ověření výstupu
    confirmButtonOutput = uibutton(fig, 'push', 'Text', 'OK', 'Position', [355, 490, 30, 22]);
    confirmButtonOutput.ButtonPushedFcn = @(~, ~) ValidateInput('output', confirmButtonOutput);
    

    % Validace vstupních nebo výstupních ID
    function ValidateInput(type, confirmButton)
        if strcmp(type, 'input')
            inputField = vstupniEditField;
            countField = prvniEditField;
        else
            inputField = vystupniEditField;
            countField = druhyEditField;
        end
        
        inputText = inputField.Value;
        inputValues = str2num(inputText);
        inputCount = countField.Value;
        
        if ~isempty(inputValues) && numel(inputValues) == inputCount
            if strcmp(type, 'input')
                vstupni_ID = inputValues;
            else
                vystupni_ID = inputValues;
            end
            % Změna barvy tlačítka na zelenou
            confirmButton.BackgroundColor = [0, 1, 0];
        else
            % vyhození chyby... 
            errordlg(['Neplatné ', type, ' ID. Zadávejte prosím čísla oddělená mezerou a počet čísel musí být stejný jako počet ', type, '.'], 'Chyba', 'modal');
            % Vrácení barvy tlačítka na původní hodnotu
            confirmButton.BackgroundColor = [0.94, 0.94, 0.94];
        end
    end

    function UpdateVstupniPolohySize()
        % aktualizace
        vstupni_polohy_size = prvniEditField.Value;
        vstupni_table.Position = [10, 330, 180, 122];
        data = zeros(vstupni_polohy_size, 2);
        vstupni_table.Data = data;
        vstupni_polohy = data; % Update vstupni_polohy
        UpdateTabulka();
    end

    function UpdateVystupniPolohySize()
        % aktualizace
        vystupni_polohy_size = druhyEditField.Value;
        vystupni_table.Position = [210, 330, 180, 122];
        data = zeros(vystupni_polohy_size, 2);
        vystupni_table.Data = data;
        vystupni_polohy = data; % Update vystupni_polohy
        UpdateTabulka();
    end

   function UpdateTabulka()
    % Získání celkového počtu poloh ze vstupu
    stohy_polohy_size = skladovaciPocetEditField.Value+prvniEditField.Value+druhyEditField.Value;

    % Změna velikosti tabulky a vytvoření nových dat
    table.Position = [95, 70, 210, 212];
    data = zeros(stohy_polohy_size, 2);
    
    % Vytvoření indexů pro vstupní a výstupní řádky
    input_indices = 1:min(prvniEditField.Value, size(vstupni_table.Data, 1));
    output_indices = (min(prvniEditField.Value, size(vstupni_table.Data, 1)) + 1):(min(prvniEditField.Value, size(vstupni_table.Data, 1)) + min(druhyEditField.Value, size(vystupni_table.Data, 1)));
    
    % Získání dat vstupních a výstupních poloh
    input_data = vstupni_table.Data;
    output_data = vystupni_table.Data;
    
    % Kopírování dat z tabulky vstupních poloh do nových dat pro vstupní
    data(input_indices, :) = input_data;
    
    % Kopírování dat z tabulky výstupních poloh do nových dat pro výstupní
    data(output_indices, :) = output_data;
    
    % Vytvoření pole s názvy řádků v tabulce
    row_names = cell(1, prvniEditField.Value + druhyEditField.Value);
    row_names(input_indices) = cellstr(arrayfun(@(x) sprintf('vstupní %d', x), 1:length(input_indices), 'UniformOutput', false));
    row_names(output_indices) = cellstr(arrayfun(@(x) sprintf('výstupní %d', x), 1:length(output_indices), 'UniformOutput', false));
    
    % Nastavení názvů řádků do tabulky
    table.RowName = row_names;
    
       % Pojmenujte řádky pro pozice0 až pozicen
    for i = 1:stohy_polohy_size-druhyEditField.Value-prvniEditField.Value
        row_names(output_indices(end) + i) = {sprintf('pozice%d', i - 1)};
    end

    % Nastavení názvů řádků do tabulky
    table.RowName = row_names;
    
    % Aktualizace dat v tabulce
    table.Data = data;
    stohy_polohy = data;
   end
% Funkce pro přechod na konfiguraci skladu a uložení dat do souboru
    function ConfigureSklad()
        set(ukazatelBehu, 'Color', [1, 0, 0]);
        drawnow;
        vymazanidesek();
        % Uložení dat do proměnných
        vstupni_ID = str2double(strsplit(vstupniEditField.Value));
        vystupni_ID = str2double(strsplit(vystupniEditField.Value));
        vstupni_polohy = vstupni_table.Data;
        vystupni_polohy = vystupni_table.Data;
        stoh_poloha = table.Data;
        IO_pocet=numel(vstupni_polohy)/2+numel(vystupni_polohy)/2;
        IO_ID=[vstupni_ID vystupni_ID];
        
        % Uložení dat do souboru
        save('sklad_data.mat', 'vstupni_ID', 'vystupni_ID', 'vstupni_polohy', 'vystupni_polohy', 'stoh_poloha', 'IO_ID','IO_pocet');

        % Získání seznamu bloků s názvem 'Zebrovani' v modelu
        blockList = find_system('RobotickyManipulator_Simscape', 'Name', 'Zebrovani');
        
        if ~isempty(blockList)
            delete_line(model_path, 'Zebrovani/Lconn1', 'pricny_nosnik/Rconn1');
            delete_block(blockList{1});
        else
        end
        
        blockList2 = find_system('RobotickyManipulator_Simscape', 'Name', 'Stojny');
        
        if ~isempty(blockList2)
            delete_line(model_path, 'Stojny/Lconn1', 'Rigid Stojny/Rconn1');
            delete_block(blockList2{1});
        else
        end

        mainFig = getappdata(gcbf, 'MainFig');
        % delete(mainFig)
        ZavedeniSkladu();
        delete(fig);
        HlavniOkno; 
        set(ukazatelBehu, 'Color', [0, 1, 0]);
    end

    function BackFromConfiguration()
        delete(fig);
    end
  
    
end
