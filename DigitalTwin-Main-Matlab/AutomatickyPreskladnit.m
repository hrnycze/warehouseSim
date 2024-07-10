function AutomatickyPreskladnit
    
    global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
    global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
    global pocp endp pocp2 endp2
    global xtraj ytraj ztraj natoceni konec_time
    global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc A ukazatelBehu mainFig

    vybranySoubor = ''; % Globální proměnná pro uchování cesty k vybranému souboru

    % Vytvoření nového okna pro automatické přeskladnění
    automatickePreskladneniOkno = uifigure('Name', 'Aut. přeskladnění', 'Position', [700, 350, 300, 450]);
    automatickePreskladneniOkno.Color = '#DAE6FA';
    
    % Popisek pro výběr souboru
    popisekText = uilabel(automatickePreskladneniOkno, 'Text', 'Vyberte sekvenci přeskladnění', 'Position', [150, 400, 140, 30]);

    % Tlačítko pro výběr souboru
    vyberSouborButton = uibutton(automatickePreskladneniOkno, 'Text', 'Vybrat soubor', 'Position', [20, 400, 120, 30], 'ButtonPushedFcn', @vyberSouborCallback);

    % Tabulka pro zobrazení načtených hodnot
    tabulka = uitable(automatickePreskladneniOkno, 'Position', [20, 100, 260, 250], 'ColumnName', {'Počáteční pozice', 'Koncová pozice'}, 'ColumnEditable', [false false],'ColumnWidth', { 120, 120},'RowName', []);

    % Textové pole pro zobrazení vybraného souboru
    vybranySouborText = uitextarea(automatickePreskladneniOkno, 'Value', vybranySoubor, 'Position', [20, 360, 260, 30]);

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
end
