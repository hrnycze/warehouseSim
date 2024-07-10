function pridaninovedesky(dataZTabulky, poloha_naskladneni)

global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
global pocp endp pocp2 endp2
global xtraj ytraj ztraj natoceni_rad konec_time databaze
global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc var_rigid A pozice_typ_ID typ_ID mainFig Vysunuti pozice_time

     
    for row = 1:size(dataZTabulky, 1)
        dataZTabulky{row, 2} = str2double(dataZTabulky{row, 2});
    end
    
    dataZTabulky=cell2mat(dataZTabulky);
    poloha_naskladneni=str2num(poloha_naskladneni);
    pocetdesek = sum(dataZTabulky(:, 1));


    if poloha_naskladneni>=0
       poloha_naskladneni=poloha_naskladneni+length(IO_ID);
    else
        for o=1:length(IO_ID)
            if poloha_naskladneni==IO_ID(o)
            poloha_naskladneni=IO_ID(o)+abs(IO_ID(o))+o-1;
            else
            poloha_naskladneni=poloha_naskladneni;
            end
        end
    end
    % Nastavení cesty k modelu
    model_path = 'RobotickyManipulator_Simscape';
    % Otevření modelu
    open_system(model_path);

if celkem_ID==0
            
            % Vytvoření matice
            matice_desek = zeros(pocetdesek, 11);
            
            % Vložení čísel od 1 do pocetdesek do prvního sloupce
            matice_desek(:, 1) = 1:pocetdesek;
            
            deska_teziste=0;
            sizetab=size(dataZTabulky);
            for i=1:sizetab(1)
                for j=1:dataZTabulky(i,1)
                    celkem_ID=celkem_ID+1;
                    matice_desek(celkem_ID,7)=dataZTabulky(i,2);
                    matice_desek(celkem_ID,5)=dataZTabulky(i,3);
                    matice_desek(celkem_ID,6)=dataZTabulky(i,5);
                    matice_desek(celkem_ID,8)=dataZTabulky(i,4);
                    matice_desek(celkem_ID,10)=dataZTabulky(i,6);
                    matice_desek(celkem_ID,11)=dataZTabulky(i,7);
                    matice_desek(celkem_ID,9)=posixtime(datetime('now'));
                    matice_desek(celkem_ID,2)=stoh_poloha(poloha_naskladneni+1,1);
                    matice_desek(celkem_ID,3)=stoh_poloha(poloha_naskladneni+1,2);
                    deska_teziste=deska_teziste+dataZTabulky(i,3)/2;
                    matice_desek(celkem_ID,4)=deska_teziste;
                    deska_teziste=deska_teziste+dataZTabulky(i,3)/2;
                    pozice{poloha_naskladneni+1} = [pozice{poloha_naskladneni+1}; matice_desek(celkem_ID,1)];
                    pozice_typ_ID{poloha_naskladneni+1}=[pozice_typ_ID{poloha_naskladneni+1}; matice_desek(celkem_ID,7)];
                    pozice_time{poloha_naskladneni+1}=[pozice_time{poloha_naskladneni+1}; posixtime(datetime('now'))];

                    if matice_desek(celkem_ID,6) == 1
                            brick_colour = [0 0.4470 0.7410];
                      elseif matice_desek(celkem_ID,6) == 2
                            brick_colour = [0.4500 0.3250 0.0980];
                      elseif matice_desek(celkem_ID,6) == 3
                            brick_colour = [0.9290 0.6940 0.1250];
                      elseif matice_desek(celkem_ID,6) == 4
                            brick_colour = [0.4940 0.1840 0.5560];
                      elseif matice_desek(celkem_ID,6) == 5
                            brick_colour = [0.4660 0.6740 0.1880];
                      elseif matice_desek(celkem_ID,6) == 6
                             brick_colour = [0.3010 0.7450 0.9330];
                      elseif matice_desek(celkem_ID,6) == 7
                             brick_colour = [0.6350 0.0780 0.1840];
                      elseif matice_desek(celkem_ID,6) == 8
                             brick_colour = [0.54 0.1 0.1];
                      elseif matice_desek(celkem_ID,6) == 9
                             brick_colour = [0.1 0.54 0.1];
                      elseif matice_desek(celkem_ID,6) == 10
                             brick_colour = [0.1 0.1 0.54];
                    end

                    ID=matice_desek(celkem_ID,1);
                    add_block("sm_lib/Body Elements/Brick Solid", [model_path '/S' num2str(ID)]);
                    set_param([model_path '/S' num2str(ID)], 'BrickDimensions', sprintf('[%f %f %f]', matice_desek(ID,10), matice_desek(ID,11), matice_desek(ID,5)), 'position',  [560  -125+65*ID   580   -85+65*ID], 'GraphicDiffuseColor', sprintf('[%f %f %f]', brick_colour(1,1), brick_colour(1,2), brick_colour(1,3)), "Orientation", "left",'Density', num2str(matice_desek(ID,8)) );
                    add_block("sm_lib/Frames and Transforms/Rigid Transform", [model_path '/R' num2str(ID)]);
                    set_param([model_path '/R' num2str(ID)], 'Translationmethod', 'Cartesian', 'TranslationCartesianOffset', sprintf('[%f %f %f]', matice_desek(ID,2), matice_desek(ID,3), -3+matice_desek(ID,4)), 'position',  [400  -125+65*ID   440   -85+65*ID], "Orientation", "right");
                    add_line(model_path, ['S' num2str(ID) '/RConn1'], ['R' num2str(ID) '/Rconn1']);
                    add_line(model_path, ['R' num2str(ID) '/Lconn1'], 'World Frame/Rconn1', 'autorouting', "on");
                    
                end
            end     
else        
            delka_mat=length(matice_desek(:,1));

                pozice_l=pozice{poloha_naskladneni+1};
                if isempty(pozice_l)
                vyska_n=0;
                tloustka_n=0;
                pozice_n=length(pozice_l);
                else
                vyska_n=matice_desek(find(matice_desek(:,1)==(pozice{poloha_naskladneni+1}(end))),4);
                tloustka_n=matice_desek(find(matice_desek(:,1)==(pozice{poloha_naskladneni+1}(end))),5);
                pozice_n=length(pozice{poloha_naskladneni+1});
                end

            % Vytvoření matice
            matice_desek = vertcat(matice_desek,zeros(pocetdesek, 11));
            
            % Vložení čísel od 1 do pocetdesek do prvního sloupce
            matice_desek(delka_mat+1:pocetdesek+delka_mat, 1) = celkem_ID+1:pocetdesek+celkem_ID;
            
            deska_teziste=vyska_n+tloustka_n/2;
            sizetab=size(dataZTabulky);
            for i=1:sizetab(1)
                for j=1:dataZTabulky(i,1)
                    celkem_ID=celkem_ID+1;
                    delka_mat=delka_mat+1;
                    matice_desek(delka_mat,7)=dataZTabulky(i,2);
                    matice_desek(delka_mat,5)=dataZTabulky(i,3);
                    matice_desek(delka_mat,6)=dataZTabulky(i,5);
                    matice_desek(delka_mat,8)=dataZTabulky(i,4);
                    matice_desek(delka_mat,10)=dataZTabulky(i,6);
                    matice_desek(delka_mat,11)=dataZTabulky(i,7);
                    matice_desek(delka_mat,9)=posixtime(datetime('now'));
                    matice_desek(delka_mat,2)=stoh_poloha(poloha_naskladneni+1,1);
                    matice_desek(delka_mat,3)=stoh_poloha(poloha_naskladneni+1,2);
                    deska_teziste=deska_teziste+dataZTabulky(i,3)/2;
                    matice_desek(delka_mat,4)=deska_teziste;
                    deska_teziste=deska_teziste+dataZTabulky(i,3)/2;
                    pozice{poloha_naskladneni+1} = [pozice{poloha_naskladneni+1}; matice_desek(delka_mat,1)];
                    pozice_typ_ID{poloha_naskladneni+1}=[pozice_typ_ID{poloha_naskladneni+1}; matice_desek(delka_mat,7)];
                    pozice_time{poloha_naskladneni+1}=[pozice_time{poloha_naskladneni+1}; posixtime(datetime('now'))];

                    if matice_desek(delka_mat,6) == 1
                            brick_colour = [0 0.4470 0.7410];
                      elseif matice_desek(delka_mat,6) == 2
                            brick_colour = [0.4500 0.3250 0.0980];
                      elseif matice_desek(delka_mat,6) == 3
                            brick_colour = [0.9290 0.6940 0.1250];
                      elseif matice_desek(delka_mat,6) == 4
                            brick_colour = [0.4940 0.1840 0.5560];
                      elseif matice_desek(delka_mat,6) == 5
                            brick_colour = [0.4660 0.6740 0.1880];
                      elseif matice_desek(delka_mat,6) == 6
                             brick_colour = [0.3010 0.7450 0.9330];
                      elseif matice_desek(delka_mat,6) == 7
                             brick_colour = [0.6350 0.0780 0.1840];
                      elseif matice_desek(delka_mat,6) == 8
                             brick_colour = [0.54 0.1 0.1];
                      elseif matice_desek(delka_mat,6) == 9
                             brick_colour = [0.1 0.54 0.1];
                      elseif matice_desek(delka_mat,6) == 10
                             brick_colour = [0.1 0.1 0.54];
                    end

                    ID=matice_desek(delka_mat,1);
                    add_block("sm_lib/Body Elements/Brick Solid", [model_path '/S' num2str(ID)]);
                    set_param([model_path '/S' num2str(ID)], 'BrickDimensions', sprintf('[%f %f %f]', matice_desek(delka_mat,10), matice_desek(delka_mat,11), matice_desek(delka_mat,5)), 'position',  [560  -125+65*ID   580   -85+65*ID], 'GraphicDiffuseColor', sprintf('[%f %f %f]', brick_colour(1,1), brick_colour(1,2), brick_colour(1,3)), "Orientation", "left",'Density', num2str(matice_desek(delka_mat,8)) );
                    add_block("sm_lib/Frames and Transforms/Rigid Transform", [model_path '/R' num2str(ID)]);
                    set_param([model_path '/R' num2str(ID)], 'Translationmethod', 'Cartesian', 'TranslationCartesianOffset', sprintf('[%f %f %f]', matice_desek(delka_mat,2), matice_desek(delka_mat,3), -3+matice_desek(delka_mat,4)), 'position',  [400  -125+65*ID   440   -85+65*ID], "Orientation", "right");
                    add_line(model_path, ['S' num2str(ID) '/RConn1'], ['R' num2str(ID) '/Rconn1']);
                    add_line(model_path, ['R' num2str(ID) '/Lconn1'], 'World Frame/Rconn1', 'autorouting', "on"); 
                end
   
            end

            
end

  save('desky_data.mat', 'pozice', 'pozice_typ_ID', 'pozice_time', 'matice_desek', 'celkem_ID');
  save_system(model_path); %%%%%%%%%%%%%%%%%%%%%%%
  
      if databaze==1
        length(matice_desek(:,1));
        skladData=zeros(length(matice_desek(:,1)),4);
        n=0;
        for i=1:length(pozice)
            if length(pozice{i})==0
            else
                for j=1:length(pozice{i})
                    n=n+1;
                     if length(IO_ID) >= i
                        skladData(n, 1) = IO_ID(i);
                     else
                        skladData(n, 1) = i-length(IO_ID)-1;
                     end
                        skladData(n, 2) = pozice{i}(j);
                        skladData(n, 3) = pozice_typ_ID{i}(j);
                        skladData(n, 4) = pozice_time{i}(j);   
                end
            end
        end
        
        % Převedení matice na buňky obsahující řádky a kulaté závorky s čárkami
        skladCell = cellfun(@(row) ['(', num2str(row(1), '%d, '), num2str(row(2), '%d, '), num2str(row(3), '%d, '), num2str(row(4), '%d'), ')'], num2cell(skladData, 2), 'UniformOutput', false);
    
        % Spojení buněk do jednoho řetězce s mezerami a odstranění poslední čárky
        skladString = ['[', strjoin(skladCell, ', '), ']'];
    
        setStorage(skladString);
    else
    end

  xtraj=[0 pocp(1); 0.0047 pocp(1)];
  ytraj=[0 pocp(2); 0.0047 pocp(2)];
  ztraj=[0 -3+pocp(3); 0.0047 -3+pocp(3)];
  natoceni=[0 natoceni_rad; 0.0047 natoceni_rad];
  var_rigid=0;
  simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(0.0047));

end