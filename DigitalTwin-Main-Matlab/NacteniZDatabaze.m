function NacteniZDatabaze()
    global  IO_pocet stoh_poloha celkem_ID pozice sirka_desky delka_desky matice_desek model_path
    global natoceni 
    global pocp 
    global xtraj ytraj ztraj natoceni 
    global var_rigid  pozice_typ_ID typ_ID natoceni_rad pozice_time mainFig ukazatelBehu IO_ID databaze
    
    sklad=getStorage();
    
    %ukazatel..
    set(ukazatelBehu, 'Color', [1, 0, 0]);
    drawnow;
    
    % zavedení rozměrů matice
    pocetdesek = length(sklad(:,1));  %počet desek, které se budou generovat
    n = 11; % počet sloupců interní databáze matice_desek
    
    %vytvoření matice
    matice_desek=zeros(pocetdesek,n);
   
    model_path = 'RobotickyManipulator_Simscape'; % Nastavení cesty k simscape modelu
    open_system(model_path); % Otevření simscape modelu
    
    % zavedení a uložení parametrů desek do matice.. 
    matice_desek(:,1)=sklad(:,2);
    matice_desek(:,7)=sklad(:,3);
    matice_desek(:,9)=sklad(:,4);

    for i=1:length(sklad(:,1))
        
        if sklad(i,1)<0
            n=find(sklad(i,1)==IO_ID);
            matice_desek(i,2)=stoh_poloha(n,1);
            matice_desek(i,3)=stoh_poloha(n,2);
            pozice{n} = [pozice{n}; sklad(i,2)]; 
            pozice_typ_ID{n} = [pozice_typ_ID{n}; sklad(i,3)]; 
            pozice_time{n} = [pozice_time{n}; sklad(i,4)]; 
        else
            n=length(IO_ID)+sklad(i,1)+1;
            matice_desek(i,2)=stoh_poloha(n,1);
            matice_desek(i,3)=stoh_poloha(n,2);
            pozice{n} = [pozice{n}; sklad(i,2)]; 
            pozice_typ_ID{n} = [pozice_typ_ID{n}; sklad(i,3)]; 
            pozice_time{n} = [pozice_time{n}; sklad(i,4)]; 
        end

            par=find(sklad(i,3)==typ_ID(:,1));
            matice_desek(i,5)=typ_ID(par,2);
            matice_desek(i,6)=typ_ID(par,4);
            matice_desek(i,8)=typ_ID(par,3);
            matice_desek(i,10)=typ_ID(par,5);
            matice_desek(i,11)=typ_ID(par,6);  
    end
    z=1;
    for j=1:length(pozice)
        if isempty(pozice{j})  
        else
            for k=1:length(pozice{j})
                if k==1
                vyska_teziste= matice_desek(find(matice_desek(:,1)==pozice{j}(k)),5)/2
                else
                vyska_teziste=vyska_teziste+matice_desek(find(matice_desek(:,1)==pozice{j}(k)),5)/2
                end
                matice_desek(z,4)=vyska_teziste;
                vyska_teziste=vyska_teziste+matice_desek(find(matice_desek(:,1)==pozice{j}(k)),5)/2
                z=z+1;
            end
        end
    end   
    
    for i=1:length(matice_desek(:,1))
                  %nastavení různých barev dle materiálu pro každou desku
                  if matice_desek(i,6) == 1
                        brick_colour = [0 0.4470 0.7410];
                  elseif matice_desek(i,6) == 2
                        brick_colour = [0.4500 0.3250 0.0980];
                  elseif matice_desek(i,6) == 3
                        brick_colour = [0.9290 0.6940 0.1250];
                  elseif matice_desek(i,6) == 4
                        brick_colour = [0.4940 0.1840 0.5560];
                  elseif matice_desek(i,6) == 5
                        brick_colour = [0.4660 0.6740 0.1880];
                  elseif matice_desek(i,6) == 6
                         brick_colour = [0.3010 0.7450 0.9330];
                  elseif matice_desek(i,6) == 7
                         brick_colour = [0.6350 0.0780 0.1840];
                  elseif matice_desek(i,6) == 8
                         brick_colour = [0.54 0.1 0.1];
                  elseif matice_desek(i,6) == 9
                         brick_colour = [0.1 0.54 0.1];
                  elseif matice_desek(i,6) == 10
                         brick_colour = [0.1 0.1 0.54];
                  end
           ID=matice_desek(i,1);
           %přidání Brick Solid pojmenovaného dle jednoznačného SID (S1, S3...)
           add_block("sm_lib/Body Elements/Brick Solid", [model_path '/S' num2str(ID)]);
           %nastavení parametrů Brick Solid, rozměry, hustota, barva, umístění
           set_param([model_path '/S' num2str(ID)], 'BrickDimensions', sprintf('[%f %f %f]', matice_desek(i,10), matice_desek(i,11), matice_desek(i,5)), 'position',  [560  -125+65*i   580   -85+65*i], 'GraphicDiffuseColor', sprintf('[%f %f %f]', brick_colour(1), brick_colour(2), brick_colour(3)), "Orientation", "left" ,'Density', num2str(matice_desek(i,8)));
           %přidání Rigid Transform pojmenovaného dle jednoznačného RID (R1, R3...)
           add_block("sm_lib/Frames and Transforms/Rigid Transform", [model_path '/R' num2str(ID)]);
           %nastavení parametrů polohy x,y,z
           set_param([model_path '/R' num2str(ID)], 'Translationmethod', 'Cartesian', 'TranslationCartesianOffset', sprintf('[%f %f %f]', matice_desek(i,2), matice_desek(i,3), -3+matice_desek(i,4)), 'position',  [400  -125+65*i   440   -85+65*i], "Orientation", "right");
           %propojení Solid a Rigid
           add_line(model_path, ['S' num2str(ID) '/RConn1'], ['R' num2str(ID) '/Rconn1']);
           %propojení s WorldFrame
           add_line(model_path, ['R' num2str(ID) '/Lconn1'], 'World Frame/Rconn1', 'autorouting', "on");     
   end
    %update celkem_ID;
    celkem_ID = max(matice_desek(:, 1));
    %uložení důležitých hodnot int. a ext. databáze skladu 
    save('desky_data.mat', 'pozice', 'pozice_typ_ID', 'pozice_time', 'matice_desek', 'celkem_ID');
    
    % Uložení změn
    save_system(model_path);

    %rychlé vykreslení aktuálního stavu skladu
    xtraj=[0 pocp(1); 0.0047 pocp(1)];
    ytraj=[0 pocp(2); 0.0047 pocp(2)];
    ztraj=[0 -3+pocp(3); 0.0047 -3+pocp(3)];
    natoceni=[0 natoceni_rad; 0.0047 natoceni_rad];
    var_rigid=0;
    simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(0.0047));
    
    set(ukazatelBehu, 'Color', [0, 1, 0]);

end
  