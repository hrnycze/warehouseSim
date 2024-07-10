function AktualniStav()
    global vstupni_ID vystupni_ID pozice pozice_typ_ID;

    aktualniStavOkno = uifigure('Name', 'Aktuální stav', 'Position', [700, 350, 300, 450]);
    aktualniStavOkno.Color = '#DAE6FA';

    poziceList = uilistbox(aktualniStavOkno, 'Position', [20, 100, 260, 300]);

    listData = cell(length(pozice), 1);

    % Přepínač pro vybrání mezi ID a TYP ID
    typSwitch = uiswitch(aktualniStavOkno, 'Position', [110, 410, 120, 30], 'Items', {'ID', 'TYP ID'}, 'ValueChangedFcn', @(src, event) toggleDisplay());
    typID = false;  % Původně zobrazovat ID

    function toggleDisplay()
        typID = ~typID;
        aktualizujSeznam();
    end

    function aktualizujSeznam()
        index = 1;

        switch typID
            case false
                % Vstupní ID
                for i = 1:length(vstupni_ID)
                    valuesText = sprintf(mat2str(pozice{i}));
                    listData{index} = sprintf('Vstupní %d: %s', i, valuesText);
                    index = index + 1;
                end

                % Výstupní ID
                l = 1;
                for i = length(vstupni_ID) + 1:length(vstupni_ID) + length(vystupni_ID)
                    valuesText = sprintf(mat2str(pozice{l}));
                    listData{index} = sprintf('Výstupní %d: %s', l, valuesText);
                    index = index + 1;
                    l = l + 1;
                end

                % Normální pozice
                j = 0;
                for i = length(vstupni_ID) + length(vystupni_ID):length(pozice)
                    if isnumeric(pozice{i})
                        valuesText = sprintf(mat2str(pozice{i}));
                        listData{index} = sprintf('Pozice %d: %s', j, valuesText);
                    else
                        listData{index} = sprintf('Pozice %d: %s', i, class(pozice{i}));
                    end
                    index = index + 1;
                    j = j + 1;
                end

            case true
                % Vstupní ID
                for i = 1:length(vstupni_ID)
                    valuesText = sprintf(mat2str(pozice_typ_ID{i}));
                    listData{index} = sprintf('Vstupní %d: %s', i, valuesText);
                    index = index + 1;
                end

                % Výstupní ID
                l = 1;
                for i = length(vstupni_ID) + 1:length(vstupni_ID) + length(vystupni_ID)
                    valuesText = sprintf(mat2str(pozice_typ_ID{l}));
                    listData{index} = sprintf('Výstupní %d: %s', l, valuesText);
                    index = index + 1;
                    l = l + 1;
                end

                % Normální pozice
                j = 0;
                for i = length(vstupni_ID) + length(vystupni_ID):length(pozice_typ_ID)
                    if isnumeric(pozice_typ_ID{i})
                        valuesText = sprintf(mat2str(pozice_typ_ID{i}));
                        listData{index} = sprintf('Pozice %d: %s', j, valuesText);
                    else
                        listData{index} = sprintf('Pozice %d: %s', i, class(pozice_typ_ID{i}));
                    end
                    index = index + 1;
                    j = j + 1;
                end
        end

        % Nastavení dat pro seznam:
        poziceList.Items = listData;
    end

    aktualizujSeznam();

    updateButton = uibutton(aktualniStavOkno, 'Text', 'Aktualizovat pozice', 'Position', [160, 20, 120, 30], 'ButtonPushedFcn', @(src, event) aktualizujSeznam());

    zpetButton = uibutton(aktualniStavOkno, 'Text', 'Zpět', 'Position', [20, 20, 80, 30], 'ButtonPushedFcn', @(src, event) zpet());
    zpetButton.FontColor = [1, 0, 0];

    function zpet
        close(aktualniStavOkno);
    end

    t = timer('TimerFcn', @aktualizujSeznam, 'Period', 5, 'ExecutionMode', 'fixedRate');
    start(t);
end
