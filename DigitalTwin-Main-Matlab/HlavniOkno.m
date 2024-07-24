close all force;
clc;
warning("off","all");

%načtení parametrů do workspace důležité kvůli simscape
Workspace_param; 

%otevření hlavního menu
HlavniMenu;

% funkce spouštící GUI
function HlavniMenu
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% GUI Hlavní menu %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % nastavení viditelnosti proměnných 
    global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
    global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
    global pocp endp pocp2 endp2
    global xtraj ytraj ztraj natoceni_rad konec_time
    global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc var_rigid A pozice_typ_ID typ_ID mainFig Vysunuti ukazatelBehu pozice_time databaze
    
    % načtení parametrů..
    NacteniParametru();
    evalin('base', 'databaze = 0;');
    
    % vykreslení aktuálního stavu skladu
    xtraj=[0 pocp(1); 0.0047 pocp(1)];
    ytraj=[0 pocp(2); 0.0047 pocp(2)];
    ztraj=[0 -3+pocp(3); 0.0047 -3+pocp(3)];
    natoceni=[0 natoceni_rad; 0.0047 natoceni_rad];
    var_rigid=0;
    simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(0.0047));
    
    %Vytvoreni noveho okna pro hlavni menu, pojmenovaneho Automaticky sklad
    mainFig = uifigure('Name', 'Automatický sklad');
    % Nastaveni pozice x,y a velikost okna
    mainFig.Position(1) = 100;
    mainFig.Position(2) = 200;
    mainFig.Position(3) = 800;
    mainFig.Position(4) = 600;
    % barva pozadi
    mainFig.Color = '#DAE6FA';
    
    % Nadpis automatický chaot. sklad, jeho pozice a velikost písma
    uilabel(mainFig, 'Text', 'Automatický chaotický sklad', 'Position', [110, 540, 400, 40], 'FontSize', 30);
    
    % ukazal stavu skladu
    ukazatelBehu= uilamp(mainFig, 'position',  [500, 535, 400, 40]);

    % tlačítko naskladnění desek
    naskladneniDesekButton = uibutton(mainFig, 'Text', 'Naskladnění desek', 'Position', [50, 330, 200, 30]);
    % akce při stistknutí tlačítka
    naskladneniDesekButton.ButtonPushedFcn = @(~,~) OtevritNaskladneniDesek();
    
    % tlačítko nastaveni skladu
    nastaveniSkladuButton = uibutton(mainFig, 'Text', 'Konfigurace skladu', 'Position', [50, 280, 200, 30]);
    % akce při stistknutí tlačítka
    nastaveniSkladuButton.ButtonPushedFcn = @(~,~) OtevritKonfiguraciSkladu();
    
    % tlačítko generovat sklad
    generovatSkladButton = uibutton(mainFig, 'Text', 'Generovat sklad', 'Position', [50, 380, 200, 30]);
    % akce při stistknutí tlačítka
    generovatSkladButton.ButtonPushedFcn = @(~,~) GenerovatSklad();
    
    % tlačítko vymazat sklad
    vymazatSkladButton = uibutton(mainFig, 'Text', 'Vymazání skladu', 'Position', [50, 130, 200, 30]);
    % nastavení červené barvy fondu
    vymazatSkladButton.FontColor = [1, 0, 0];
    % akce při stistknutí tlačítka
    vymazatSkladButton.ButtonPushedFcn = @(~,~) VymazatSklad();

    % tlačitko automatický réžim
    automatickyRezimButton = uibutton(mainFig, 'Text', 'Auto vyskladnění - cele desky', 'Position', [50, 480, 200, 30]);
    % akce při stistknutí tlačítka
    automatickyRezimButton.ButtonPushedFcn = @(~,~) AutomatickePreskladneni();

    automatickyRezimHalfButton = uibutton(mainFig, 'Text', 'Auto vyskladnění - pul desky', 'Position', [260, 480, 200, 30]);
    % akce při stistknutí tlačítka
    automatickyRezimHalfButton.ButtonPushedFcn = @(~,~) AutomatickeHalfPreskladneni();

    automatickyRezimQuaterButton = uibutton(mainFig, 'Text', 'Auto vyskladnění - ctvrt desky', 'Position', [470, 480, 200, 30]);
    % akce při stistknutí tlačítka
    automatickyRezimQuaterButton.ButtonPushedFcn = @(~,~) AutomatickeQuaterPreskladneni();

    %tlačítko manuální réžim
    manualniRezimButton = uibutton(mainFig, 'Text', 'Manuální přeskladnění', 'Position', [50, 430, 200, 30]);
    % akce při stistknutí tlačítka
    manualniRezimButton.ButtonPushedFcn = @(~,~) ManualneSpustit();

    % tlačítko aktuální stav
    aktualniStavButton = uibutton(mainFig, 'Text', 'Aktuální stav', 'Position', [50, 230, 200, 30]);
    % akce při stistknutí tlačítka
    aktualniStavButton.ButtonPushedFcn = @(~,~) AktualizujStav();
    
    % tlačítko definovat typ desek
    definovatDeskyButton = uibutton(mainFig, 'Text', 'Definovat typ desek', 'Position', [50, 180, 200, 30]);
    % akce při stistknutí tlačítka
    definovatDeskyButton.ButtonPushedFcn = @(~,~) DefinujDesky();

    % Vytvoření přepínače s dvěma polohami
    databazovyPrepinac = uiswitch(mainFig, 'Position', [110, 30, 200, 30], 'Items', {'Databáze OFF', 'Databáze ON'});
    
    % Nastavení akce při změně stavu přepínače
    databazovyPrepinac.ValueChangedFcn = @(src, event) ZmenaDatabazovehoRezimu(src);    
    
    % tlačítko ukončit program
    ukoncitProgramButton = uibutton(mainFig, 'Text', 'Ukončit program', 'Position', [50, 80, 200, 30]);
    % nastavení barvy fondu na červenou
    ukoncitProgramButton.FontColor = [1, 0, 0];
    % nastavení akce při stisknutí tlačítka
    ukoncitProgramButton.ButtonPushedFcn = @(~,~) UkoncitProgram();
    
    % textové pole pro aktuální čas
    messageText = uilabel(mainFig, 'Text', '', 'Position', [400, 10, 300, 30]);
    
    %funkce pro aktualizaci času
    function AktualizovatCas()
        % získání aktuálního času
        aktualniCas = datetime('now', 'Format', 'dd.MM.yyyy, HH:mm:ss');
        % zobrazení aktuálního času v textovém poli
        messageText.Text = ['Aktuální čas: ', char(aktualniCas)];
    end

    % volání funkce pro aktualizaci času.. každou sekundu
    timerObj = timer('ExecutionMode', 'fixedRate', 'Period', 1, 'TimerFcn', @(~,~) AktualizovatCas());
    % spuštění timeru
    start(timerObj);
   
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%0%% Vykreslení aktuálního rozložení skladu %%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % vytvoření grafu, definice pozice a rozměrů 
    deskyAxis = uiaxes(mainFig, 'Position', [275, 255, 300, 300]);
        
    % nastavení stejného měřítka pro osu x a y (1:1)
    deskyAxis.DataAspectRatioMode = 'manual';
    deskyAxis.DataAspectRatio = [1 1 1];
    % nastavení barvy "pozadí"
    deskyAxis.Color='#DAE6FA';
        
    % načtení x a y těžiště jednotlivých pozic
    x_teziste = stoh_poloha(:, 1); 
    y_teziste = stoh_poloha(:, 2); 
        
    % vykreslení desek na ose x a y na základě těžišť 
    for i = 1:length(x_teziste)
        x_desky = x_teziste(i) - delka_desky / 2; 
        y_desky = y_teziste(i) - sirka_desky / 2; 
        
        % nastavení barvy jednotlivých pozic
        if i <= length(vstupni_ID) %pokud je to vstupní
            faceColor = '#6B8E23'; % vstupní zeleně
        elseif i <= length(vstupni_ID) + length(vystupni_ID) %pokud je to výstupní
            faceColor = '#CD5C5C'; % výstupní červeně
        else
            faceColor = '#6495ED'; % skladovací pozice modře
        end
        
        % vykreslení desek
        rectangle(deskyAxis, 'Position', [x_desky, y_desky, delka_desky, sirka_desky], 'FaceColor', faceColor, 'EdgeColor', 'k');
        
        % popsání jednotlivých pozic
        if i <= length(vstupni_ID)   
           text(deskyAxis, x_teziste(i), y_teziste(i), ['In', num2str(i)], 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Color', 'k');
        elseif i <= length(vstupni_ID) + length(vystupni_ID)    
           text(deskyAxis, x_teziste(i), y_teziste(i), ['Out', num2str(i - length(vstupni_ID))], 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Color', 'k');
        else 
           text(deskyAxis, x_teziste(i), y_teziste(i), ['Poz', num2str(i -1- (length(vstupni_ID) + length(vystupni_ID)))], 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Color', 'k');
        end
    end
        
    % nastavení rozsahu osy v závislosti na velikosti skladu
    deskyAxis.XLim = [min(x_teziste) - delka_desky / 2, max(x_teziste) + delka_desky / 2];
    deskyAxis.YLim = [min(y_teziste) - sirka_desky / 2, max(y_teziste) + sirka_desky / 2];
    
    %popisky os
    xlabel(deskyAxis, 'Poloha X (metry)');
    ylabel(deskyAxis, 'Poloha Y (metry)');

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%% Nastavení proměnných parametrů v modelu %%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    % popisek slideru
    uilabel(mainFig, 'Text', 'Nastavení vysunutí přísavek', 'Position', [355, 240, 200, 20]);
    % vytvoření posuvného pole (slideru), nastavení jména, pozice..
    slider = uislider(mainFig, 'Position', [330, 230, 200, 3]);
    % nastavení rozsahu
    slider.Limits = [0 0.2]; 
    % nastavení počáteční hodnoty slideru
    slider.Value = 0.2; 
    slider.MajorTicks = 0:0.05:0.2; 
    % akce v případě změny hodnoty na slideru
    slider.ValueChangedFcn = @(~, event) UlozitDoWorkspace('Vysunuti', event.Value);
        
        
    % definice slideru pro změnu úhlu
    uhlyStred = [30, 150, 210, 330];
    uhelRozsah = 20;
    
    % vytvoření 4 sliderů pro 4 úhly.. 
    for i = 1:4
        %nastavení x pozice slideru
        xPosition = 340 + mod(i - 1, 2) * 120;
        %nastavení y pozice slideru
        yPosition = 230 - ceil(i / 2) * 60;    

        %popisky jednotlivých sliderů
        uilabel(mainFig, 'Text', sprintf('Úhel %d', i), 'Position', [xPosition+10 , yPosition + 8, 200, 20]);
        %vytvoření slideru
        sliderUhly(i) = uislider(mainFig, 'Position', [xPosition, yPosition, 50, 3]); 
        %rozsahy jednotlivých sliderů
        sliderUhly(i).Limits = [uhlyStred(i) - uhelRozsah, uhlyStred(i) + uhelRozsah];
        %počáteční hodnota
        sliderUhly(i).Value = uhlyStred(i);
        sliderUhly(i).MajorTicks = uhlyStred(i) - uhelRozsah:20:uhlyStred(i) + uhelRozsah;
        % akce při změně úhlu
        sliderUhly(i).ValueChangedFcn = @(~, event) UlozitDoWorkspaceUhel(i, event.Value);

    end
    

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%% DEFINICE FUNKCÍ PO KLIKNUTÍ NA TLAČÍTKA %%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    % funkce při kliknutí na tlačítko naskladnění desek
    function OtevritNaskladneniDesek()
        % spusti naskladneni desek
        NaskladneniDesek();
    end

    function OtevritKonfiguraciSkladu()
        NastaveniSkladu();
    end
    
    function GenerovatSklad()
        GenerovaniSkladu()
    end
    
    % Funkce pro vymazání skladu
    function VymazatSklad()
        vymazanidesek();
    end 

    % funkce, která uloží hodnotu do workspace
    function UlozitDoWorkspace(nazev, hodnota)
        assignin('base', nazev, hodnota);
    end

    % funkce, která uloží konkrétní úhel do workspace
    function UlozitDoWorkspaceUhel(index, hodnota)
        uhel(index) = hodnota;
        assignin('base', 'uhel', uhel);
        uhelrad(index) = hodnota*pi()/180;
    end
    
    function UkoncitProgram()
        close(mainFig);
    end

    function AutomatickePreskladneni()
        %AutomatickyPreskladnit();
        AutomatickyVyskladnitCeleDesky;
    end

    function AutomatickeHalfPreskladneni()
        %AutomatickyPreskladnit();
        AutomatickyVyskladnitPulDesky;
    end

    function AutomatickeQuaterPreskladneni()
        AutomatickyVyskladnitCtvrtDesky;
    end

    function ManualneSpustit()
        ManualniPreskladneni();
    end

    function AktualizujStav()
        AktualniStav();
    end

    function ZmenaDatabazovehoRezimu(src)
    % Funkce, která se spustí při změně stavu přepínače
    switch src.Value
        case 'Databáze ON' %pokud databáze zapnutá..
            evalin('base', 'databaze = 1;');
            typ_ID=getDesks();
            vymazanidesek;
        case 'Databáze OFF' %pokud databáze vypnutá..
            evalin('base', 'databaze = 0;');   
            load typy_desek;
            vymazanidesek;
    end
    end
    function DefinujDesky()
        DefinovatDesky();
    end
end
