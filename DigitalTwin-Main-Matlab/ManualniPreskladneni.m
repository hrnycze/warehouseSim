function ManualniPreskladneni


global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
global pocp endp pocp2 endp2
global xtraj ytraj ztraj natoceni konec_time databaze
global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc Vysunuti natoceni_rad pozice_typ_ID mainFig ukazatelBehu
    


% Vytvoření okna pro manuální přeskladnění
manualniPreskladneniOkno = uifigure('Name', 'Manuální přeskladnění', 'Position', [700, 370, 300, 430]);
manualniPreskladneniOkno.Color = '#DAE6FA';

dataPozice=[];
zkoumanePozice=[1:length(vstupni_ID),1+length(vstupni_ID)+length(vystupni_ID):length(pozice_typ_ID)];
for j=zkoumanePozice
    dataPozice=[dataPozice, pozice{j}'];
end
dataPozice=sort(dataPozice);

dataPoziceTyp=[];

for j=zkoumanePozice
    dataPoziceTyp=[dataPoziceTyp, pozice_typ_ID{j}'];
end
dataPoziceTyp=sort(unique(dataPoziceTyp));

listData={};

index=1;
for i = 1:length(vstupni_ID)
  valuesText = sprintf(mat2str(pozice{i}));
  listData{index} = sprintf('Vstupní %d: %s', i);
  index = index + 1;
end
l=1;
for i = length(vstupni_ID)+1:length(vstupni_ID)+length(vystupni_ID)
  valuesText = sprintf(mat2str(pozice{i}));
  listData{index} = sprintf('Výstupní %d: %s', l);
  index = index + 1;
  l=l+1;
end
j = 0;
for i = length(vstupni_ID)+length(vystupni_ID):(length(pozice)-1)
   if isnumeric(pozice{i+1})
      % Převeďte číselné pole na textový řetězec:
      valuesText = sprintf(mat2str(pozice{i+1}));
      listData{index} = sprintf('Pozice %d: %s', j);
   else
   % Pokud prvek není maticí, zobrazí se jeho typ:
   listData{index} = sprintf('Pozice %d: %s', i, class(pozice{i+1}));
   end
   index = index + 1;
   j = j + 1;
end


TitleID=uilabel(manualniPreskladneniOkno, 'Text','Vykladnění dle ID', 'Position', [10, 400, 300, 30], FontWeight='bold', FontSize=16);

dropdownMenuIDTitle= uilabel (manualniPreskladneniOkno, 'Text', 'ID desky k vyskladnění:', 'Position', [20, 380, 150, 30]);
dropdownMenuID= uicontrol(manualniPreskladneniOkno,'Style', 'popupmenu', 'String', cellfun(@num2str, num2cell(dataPozice), 'UniformOutput', false), 'Position', [90, 350, 50, 30]);

dropdownMenuIDpTitle= uilabel (manualniPreskladneniOkno, 'Text', 'Vyskladňovací pozice:', 'Position', [170, 380 , 150, 30]);
dropdownMenuIDp = uicontrol(manualniPreskladneniOkno,'Style', 'popupmenu', 'String', cellfun(@num2str, num2cell(vystupni_ID), 'UniformOutput', false), 'Position', [230, 350 , 50, 30]);

buttonID = uibutton(manualniPreskladneniOkno, 'text', 'Manuální vyskladnění dle ID', 'Position', [90, 310, 190, 30]);
buttonID.ButtonPushedFcn= @(~,~) pozadovaneIDf();


TitleTypID=uilabel(manualniPreskladneniOkno, 'Text','Vykladnění dle TYP ID', 'Position', [10, 280, 300, 30], FontWeight='bold', FontSize=16);

dropdownMenuTypIDTitle= uilabel (manualniPreskladneniOkno, 'Text', 'TYP ID k vyskladnění:', 'Position', [20, 260, 150, 30]);
dropdownMenuTypID= uicontrol(manualniPreskladneniOkno,'Style', 'popupmenu', 'String', cellfun(@num2str, num2cell(dataPoziceTyp), 'UniformOutput', false), 'Position', [90, 230, 50, 30]);

dropdownMenuTypIDpTitle= uilabel (manualniPreskladneniOkno, 'Text', 'Vyskladňovací pozice:', 'Position', [170, 260 , 150, 30]);
dropdownMenuTypIDp = uicontrol(manualniPreskladneniOkno,'Style', 'popupmenu', 'String', cellfun(@num2str, num2cell(vystupni_ID), 'UniformOutput', false), 'Position', [230, 230 , 50, 30]);

buttonTypID = uibutton(manualniPreskladneniOkno, 'text', 'Manuální vyskladnění dle Typ ID', 'Position', [90, 190, 190, 30]);
buttonTypID.ButtonPushedFcn= @(~,~) pozadovaneTypID();


TitleManPreskladneniID=uilabel(manualniPreskladneniOkno, 'Text','Přeskladnění dle ID', 'Position', [10, 160, 300, 30], FontWeight='bold', FontSize=16);

dropdownMenuManPocPozTitle= uilabel (manualniPreskladneniOkno, 'Text', 'Výchozí pozice:', 'Position', [20, 130, 150, 30]);
dropdownMenuManPreskladneniPoc= uicontrol(manualniPreskladneniOkno,'Style', 'popupmenu', 'String', listData, 'Position', [50, 100, 90, 30]);

dropdownMenuManKonPozTitle= uilabel (manualniPreskladneniOkno, 'Text', 'Koncová pozice:', 'Position', [170, 130 , 150, 30]);
dropdownMenuManPreskladneniKon = uicontrol(manualniPreskladneniOkno,'Style', 'popupmenu', 'String', listData, 'Position', [190, 100 , 90, 30]);

buttonManPreskladneni = uibutton(manualniPreskladneniOkno, 'text', 'Manuální přeskladnění dle pozic', 'Position', [90, 60, 190, 30]);
buttonManPreskladneni.ButtonPushedFcn = @(~,~) preskladnenidesek();

% Přidává tlačítko pro zavření okna
buttonZpet = uibutton(manualniPreskladneniOkno, 'text', 'Zpět', 'Position', [20, 20, 80, 30]);
buttonZpet.ButtonPushedFcn = @(~,~) zavriOkno();
buttonZpet.FontColor = [1, 0, 0];

function zavriOkno
    % Zavření aktuálního okna
    close(manualniPreskladneniOkno);
end

function pozadovaneIDf
    set(ukazatelBehu, 'Color', [1, 0, 0]);
    drawnow;
    % Inicializace proměnných pro uchování nejlepší pozice
    id_man=[];
    indexd=[];

    pozadovaneIDpoz=dropdownMenuID.Value;
    pozadovaneID=str2double(dropdownMenuID.String(pozadovaneIDpoz));
    koncoveIDpoz=dropdownMenuIDp.Value;
    koncoveID=str2double(dropdownMenuIDp.String(koncoveIDpoz));

    for i = zkoumanePozice
        zkoumanePozice=[1:length(vstupni_ID),1+length(vstupni_ID)+length(vystupni_ID):length(pozice)];
        % Najdi index hledaného ID v aktuální pozici
        id_index = find(pozice{i} == pozadovaneID);

        % Pokud je ID v aktuální pozici nalezeno
        if ~isempty(id_index)
            % Vypočti vzdálenost od konce a aktualizuj nejlepší pozici
            id_man=id_index;
            indexd=i;
            poziceid=pozice{i};
        end
    end
    
    for k=1:length(poziceid)-id_man+1
        if indexd>length(IO_ID)
           A(1,1)=indexd-length(IO_ID)-1;
        else 
           A(1,1)=IO_ID(indexd);
        end

        if k==length(poziceid)-id_man+1
           A(1,2) = koncoveID;
        else
           poziceSklad=setdiff(0:(length(pozice) - length(IO_ID)-1), A(1,1))
           A(1,2)=poziceSklad(randi(length(poziceSklad)));
        end
        disp(A);
        param=A;
        spousteci(param);
    end
    set(ukazatelBehu, 'Color', [0, 1, 0]);
    delete(manualniPreskladneniOkno);
    ManualniPreskladneni();
end

function pozadovaneTypID
    set(ukazatelBehu, 'Color', [1, 0, 0]);
    drawnow;
    % Inicializace proměnných pro uchování nejlepší pozice
    nejlepsi_pozice = [];
    id_man=[];
    indexd=[];
    nejlepsi_vzdalenost = Inf;

    pozadovaneIDpoz=dropdownMenuTypID.Value;
    pozadovaneID=str2double(dropdownMenuTypID.String(pozadovaneIDpoz));
    koncoveIDpoz=dropdownMenuTypIDp.Value;
    koncoveID=str2double(dropdownMenuTypIDp.String(koncoveIDpoz));

    for i = zkoumanePozice
        zkoumanePozice=[1:length(vstupni_ID),1+length(vstupni_ID)+length(vystupni_ID):length(pozice)];
        id_index = find(pozice_typ_ID{i} == pozadovaneID);

        % Pokud je ID v aktuální pozici nalezeno
        if ~isempty(id_index)
            vzdalenost_od_konce = length(pozice_typ_ID{i}) - id_index + 1;
        
        if vzdalenost_od_konce < nejlepsi_vzdalenost
            nejlepsi_pozice = pozice_typ_ID{i};
            nejlepsi_vzdalenost = vzdalenost_od_konce;
            id_man=id_index;
            indexd=i;
        end
        end
    end
    
    for k=1:length(nejlepsi_pozice)-id_man+1
        if indexd>length(IO_ID)
           A(1,1)=indexd-length(IO_ID)-1;
        else 
           A(1,1)=IO_ID(indexd);
        end

        if k==length(nejlepsi_pozice)-id_man+1
           A(1,2) = koncoveID;
        else
           poziceSklad=setdiff(0:(length(pozice) - length(IO_ID)-1), A(1,1))
           A(1,2)=poziceSklad(randi(length(poziceSklad)));
        end
        disp(A);
        param=A;
        spousteci(param);
    end
    set(ukazatelBehu, 'Color', [0, 1, 0]);
    delete(manualniPreskladneniOkno);
    ManualniPreskladneni();
end
    function preskladnenidesek
    set(ukazatelBehu, 'Color', [1, 0, 0]);
    drawnow;
    pocatecni=dropdownMenuManPreskladneniPoc.Value;
    koncova=dropdownMenuManPreskladneniKon.Value;
    
    if pocatecni>length(IO_ID)
           A(1,1)=pocatecni-length(IO_ID)-1;
    else 
           A(1,1)=IO_ID(pocatecni);
    end
    
    if koncova>length(IO_ID)
           A(1,2)=koncova-length(IO_ID)-1;
    else 
           A(1,2)=IO_ID(koncova);
    end

    param=A;
    spousteci(param);
    set(ukazatelBehu, 'Color', [0, 1, 0]);
    delete(manualniPreskladneniOkno);
    ManualniPreskladneni();
    end
end
    
