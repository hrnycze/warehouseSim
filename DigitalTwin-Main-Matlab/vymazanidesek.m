function vymazanidesek

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%% Vymazání desek %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
    global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
    global pocp endp pocp2 endp2
    global xtraj ytraj ztraj natoceni konec_time
    global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc pozice_typ_ID natoceni_rad pozice_time ukazatelBehu
    
    %nastavení ukazatele skladu na zaneprázdněný
    set(ukazatelBehu, 'Color', [1, 0, 0]);
    drawnow;

    %načtení dat v případě, že je nemáme ve workspace
    load desky_data.mat;
    % Nastavení cesty k modelu
    model_path = 'RobotickyManipulator_Simscape';
    % Otevření modelu
    open_system(model_path);
    
    %pokud zde žádné desky nemáme, tak aby zde nenastala chyba
    if length(matice_desek)==0
    %pokud nejsou zde desky, přeskočíme.. 
    else
        for i=1:length(matice_desek(:,1)) %pro každou desku uloženou v matice_desek
            %načtení hodnoty jednoznačného ID z matice_desek
            p=matice_desek(i,1);
            %vymazání propojení mezi S a R
            try
            delete_line(model_path, ['S' num2str(p) '/RConn1'], ['R' num2str(p) '/Rconn1']);
            catch
            end
            %pro případ chyby
            try
            delete_line(model_path, ['S' num2str(p) '/RConn1'], ['Rigid/Rconn1']);
            catch
            end
            %získání parametrů propojení z R, nešlo to zde napřímo jako výš
            h = get_param([model_path '/R' num2str(p)],'LineHandles');
            %vymázání propojení R a WorldFrame
            delete_line(h.LConn);
            %vymazání bloku S
            delete_block([model_path '/S' num2str(p)]);
            %vymazání bloku R
            delete_block([model_path '/R' num2str(p)]);
        end
    end
    
    %přepsání uložených dat databáze skladu
    matice_desek=[];
    celkem_ID=0;
    pozice={};
    pozice_typ_ID={};
    pozice_time={};
    for i = 1:(numel(stoh_poloha) / 2)
        pozice{i} = [];
        pozice_typ_ID{i} = [];
        pozice_time{i} = [];
    end
    
    % Uložení změn
    save_system(model_path);
    % Uložení databáze skladu
    save('desky_data.mat', 'pozice', 'pozice_typ_ID', 'pozice_time', 'matice_desek', 'celkem_ID');
    
    % Vykreslení aktuálního stavu skladu
    xtraj=[0 pocp(1); 0.0047 pocp(1)];
    ytraj=[0 pocp(2); 0.0047 pocp(2)];
    ztraj=[0 -3+pocp(3); 0.0047 -3+pocp(3)];
    natoceni=[0 0; 0.0047 0];
    var_rigid=0;
    simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(0.0047));
    set(ukazatelBehu, 'Color', [0, 1, 0]);
end