%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%% Spouštění pohybu a přeskladnění ve skladu %%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function spousteci(A)
    global IO_ID  vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
    global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  pozice_typ_ID
    global pocp endp pocp2 endp2
    global xtraj ytraj ztraj natoceni konec_time databaze
    global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc var_rigid pozice_time
    global USE_REAL_FANUC_CNC

    
    % uložení vstupních hodnot
     pocatek=A(1,1);
     konec=A(1,2);
     var_rigid=0;
     
    %předpřipravení dat - začátek 
    if pocatek>=0
       pocatek=pocatek+length(IO_ID);
    else
     for o=1:length(IO_ID)
         if pocatek==IO_ID(o)
            pocatek=IO_ID(o)+abs(IO_ID(o))+o-1;
         else
            pocatek=pocatek;
         end
     end
    end

     %předpřipravení dat - konec
     if konec>=0
       konec=konec+length(IO_ID);
     else
        for o=1:length(IO_ID)
         if konec==IO_ID(o)
            konec=IO_ID(o)+abs(IO_ID(o))+o-1;
         else
            konec=konec;
         end
        end
     end
    pocatek=pocatek+1;
    konec=konec+1;
    
    % načtení hodnot ve stohu pro počáteční stoh (x,y,z,ID,tloušťka desky)
        if isempty(pozice{pocatek})
           vyska_poc=0;
           xy_poc=stoh_poloha(pocatek,:);
           pozice_poc=[];
           deska=0;
        else
            pozice_poc = pozice{pocatek};
            ID_deska_poc=pozice_poc(end);
            pz_ID_poc=ismember(matice_desek(:,1),ID_deska_poc);
            poz_ID_poc = find(pz_ID_poc == 1);
            vyska_poc=matice_desek(poz_ID_poc,4)+matice_desek(poz_ID_poc,5)/2;
            xy_poc=stoh_poloha(pocatek,:);
            deska=1;
        end
    % načtení hodnot ve stohu pro koncový stoh (x,y,z,ID,tloušťka desky)
        if isempty(pozice{konec})
            if isempty(matice_desek)
           vyska_end=0;
           vyska_end_set=0;
           xy_end=stoh_poloha(konec,:);  
           pozice_end=[];
            else
           vyska_end=matice_desek(poz_ID_poc,5);
           vyska_end_set=matice_desek(poz_ID_poc,5)/2;
           xy_end=stoh_poloha(konec,:);  
           pozice_end=[];
            end
        else
            pozice_end = pozice{konec};
            ID_deska_end=pozice_end(end);
            pz_ID_end=ismember(matice_desek(:,1),ID_deska_end);
            poz_ID_end = find(pz_ID_end == 1);
            vyska_end=matice_desek(poz_ID_end,4)+matice_desek(poz_ID_end,5)/2+matice_desek(poz_ID_poc,5);
            vyska_end_set=matice_desek(poz_ID_end,4)+matice_desek(poz_ID_end,5)/2+matice_desek(poz_ID_poc,5)/2;
            xy_end=[matice_desek(poz_ID_end,2), matice_desek(poz_ID_end,3)];
            if A(1,2)==A(1,1)
               vyska_end=matice_desek(poz_ID_poc,4)+matice_desek(poz_ID_poc,5)/2;
               vyska_end_set=matice_desek(poz_ID_poc,4);
            end
        end
     
 
       % zjištění aktuální polohy manipulátoru a vybrání následného pohybu
       if pocp(1,1:2)==stoh_poloha(pocatek,:)
            % pokud je náhodou manipulátor přímo na desce
            if  pocp(1,3)==(matice_desek(poz_ID_poc,4)+matice_desek(poz_ID_poc,5)/2)        
                
                % vstup pro generátor trajektorií 
                endp=[xy_end(1), xy_end(2), vyska_end];
                pocp2 = [pocp(1), pocp(2), svisle+max(matice_desek(:,4))];
                endp2 = [endp(1), endp(2), svisle+max(matice_desek(:,4))]; 
                
                % "přisátí" desky, pokud deska existuje.. (u testování
                % nemusí existovat)
                if deska==0
                elseif deska==1
                delete_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['R' num2str(ID_deska_poc) '/Rconn1']);
                add_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], 'Rigid/Rconn1');
                end
                
                % generování trajektorie a simulace pohybu
                disp("Path: přímo na desce A-->B")

                GenerovaniTrajektorie();
                if USE_REAL_FANUC_CNC
                    %TODO: RUN FANUC, WAIT END MOVE
                    [fanuc_state, simOut] = Matlab2FanucCallback();
                    if fanuc_state ~= 0
                        error("FAILED to finish move on FANUC!")
                    else
                        disp("FANUC: Move done.")
                    end
                else
                    simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(konec_time));
                    pause(konec_time-1.5);
                end

                %TODO: RUN FANUC, WAIT END MOVE
                
                % uložení koncových hodnot poloh pohonů
                pohon1=simOut.pohon1.signals.values(end);
                pohon2=simOut.pohon2.signals.values(end);
                nuzky1=simOut.nuzky1.signals.values(end);
                nuzky2=simOut.nuzky2.signals.values(end);
                nuzky3=simOut.nuzky3.signals.values(end);
                nuzky4=simOut.nuzky4.signals.values(end);
                
                % přepsání interní databáze
                if deska==0
                elseif deska==1
                pozice{konec}=[pozice{konec};ID_deska_poc];
                pozice_typ_ID{konec}=[pozice_typ_ID{konec};matice_desek(ID_deska_poc,7)];
                %pozice_time{konec}=[pozice_time{konec};matice_desek(ID_deska_poc,9)];
                
                if length(pozice{pocatek})>1
                  pozice{pocatek}=pozice{pocatek}(1:end-1,1);
                  pozice_typ_ID{pocatek}=pozice_typ_ID{pocatek}(1:end-1,1);
                  %pozice_time{pocatek}=pozice_time{pocatek}(1:end-1,1);
                else
                  pozice{pocatek} = [];
                  pozice_typ_ID{pocatek}=[];
                  %pozice_time{pocatek}=[];
                end
                
                % "puštění" desky a přepsání parametrů Rigid Transform
                delete_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], 'Rigid/Rconn1');
                add_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['R' num2str(ID_deska_poc) '/Rconn1']);
                matice_desek(ID_deska_poc,2:4)=[endp(1), endp(2), vyska_end_set];
                set_param([model_path '/R' num2str(ID_deska_poc)], 'TranslationCartesianOffset', sprintf('[%f %f %f]', matice_desek(ID_deska_poc,2), matice_desek(ID_deska_poc,3), -3+vyska_end_set) );
                end
            else % pokud je manipulátor přímo nad stohem, odkud máme brát desku..
                % vstup pro generátor trajektorií 
                endp=[xy_poc(1), xy_poc(2), vyska_poc];
                endp2=endp;
                pocp2=pocp;
                
                % generování trajektorie a simulace pohybu
                disp("Path: přímo nad stoh DOLU")

                GenerovaniTrajektorieUpDown()
                if USE_REAL_FANUC_CNC
                    %TODO: RUN FANUC, WAIT END MOVE
                    [fanuc_state, simOut] = Matlab2FanucCallback();
                    if fanuc_state ~= 0
                        error("FAILED to finish move on FANUC!")
                    else
                        disp("FANUC: Move done.")
                    end
                else
                    simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(konec_time));
                    pause(konec_time-1.5);
                end

                %TODO: RUN FANUC, WAIT END MOVE
                
                % uložení koncových hodnot poloh pohonů
                pohon1=simOut.pohon1.signals.values(end);
                pohon2=simOut.pohon2.signals.values(end);
                nuzky1=simOut.nuzky1.signals.values(end);
                nuzky2=simOut.nuzky2.signals.values(end);
                nuzky3=simOut.nuzky3.signals.values(end);
                nuzky4=simOut.nuzky4.signals.values(end);
               
                % počáteční a koncová poloha pro tvorbu trajektorie
                pocp=endp;
                pocp(3)=endp(3)+matice_desek(poz_ID_poc,5)/2;
                endp=[xy_end(1), xy_end(2), vyska_end];
                pocp2 = [pocp(1), pocp(2), svisle+max(matice_desek(:,4))];
                endp2 = [endp(1), endp(2), svisle+max(matice_desek(:,4))];
                var_rigid=-matice_desek(poz_ID_poc,5)/2;

                save('pohyb_data.mat', 'pohon1', 'pohon2', 'nuzky1','nuzky2','nuzky3','nuzky4', 'pocp');
                
                % "přisátí" desky, pokud deska existuje.. (u testování
                % nemusí existovat)
                if deska==0
                elseif deska==1
                delete_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['R' num2str(ID_deska_poc) '/Rconn1']);
                add_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['Rigid/Rconn1']);
                end
                
                % generování trajektorie a simulace pohybu
                disp("Path: přímo nad stoh A-->B")

                GenerovaniTrajektorie();
                if USE_REAL_FANUC_CNC
                    %TODO: RUN FANUC, WAIT END MOVE
                    [fanuc_state, simOut] = Matlab2FanucCallback();
                    if fanuc_state ~= 0
                        error("FAILED to finish move on FANUC!")
                    else
                        disp("FANUC: Move done.")
                    end
                else
                    simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(konec_time));
                    pause(konec_time-1.5);
                end

                %TODO: RUN FANUC, WAIT END MOVE
                
                % uložení koncových hodnot poloh pohonů
                pohon1=simOut.pohon1.signals.values(end);
                pohon2=simOut.pohon2.signals.values(end);
                nuzky1=simOut.nuzky1.signals.values(end);
                nuzky2=simOut.nuzky2.signals.values(end);
                nuzky3=simOut.nuzky3.signals.values(end);
                nuzky4=simOut.nuzky4.signals.values(end);
                
                % přepsání interní databáze
                if deska==0
                elseif deska==1
                pozice{konec}=[pozice{konec};ID_deska_poc];
                pozice_typ_ID{konec}=[pozice_typ_ID{konec};matice_desek(ID_deska_poc,7)];
                %pozice_time{konec}=[pozice_time{konec};matice_desek(ID_deska_poc,9)];
                
                if length(pozice{pocatek})>1
                  pozice{pocatek}=pozice{pocatek}(1:end-1,1);
                  pozice_typ_ID{pocatek}=pozice_typ_ID{pocatek}(1:end-1,1);
                  %pozice_time{pocatek}=pozice_time{pocatek}(1:end-1,1);
                else
                  pozice{pocatek} = [];
                  pozice_typ_ID{pocatek}=[];
                  %pozice_time{pocatek}=[];
                end
                     
                % "puštění" desky a přepsání parametrů Rigid Transform
                delete_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['Rigid/Rconn1']);
                add_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['R' num2str(ID_deska_poc) '/Rconn1']);
                matice_desek(ID_deska_poc,2:4)=[endp(1), endp(2), vyska_end_set];
                set_param([model_path '/R' num2str(ID_deska_poc)], 'TranslationCartesianOffset', sprintf('[%f %f %f]', matice_desek(ID_deska_poc,2), matice_desek(ID_deska_poc,3), -3+vyska_end_set) );
                end
           end
       else     % pokud je stoh kdekoliv jinde
                 % vstup pro generátor trajektorií 
                endp=[xy_poc(1), xy_poc(2), vyska_poc];
                if isempty(matice_desek)
                pocp2 = [pocp(1), pocp(2), svisle];
                endp2 = [endp(1), endp(2), svisle];
                else
                pocp2 = [pocp(1), pocp(2), svisle+max(matice_desek(:,4))];
                endp2 = [endp(1), endp(2), svisle+max(matice_desek(:,4))]; 
                end

                % generování trajektorie a simulace pohybu
                disp("Path: gripper anywhere A ---> B PICK")

                GenerovaniTrajektorie();
                if USE_REAL_FANUC_CNC
                    %TODO: RUN FANUC, WAIT END MOVE
                    [fanuc_state, simOut] = Matlab2FanucCallback();
                    if fanuc_state ~= 0
                        error("FAILED to finish move on FANUC!")
                    else
                        disp("FANUC: Move done.")
                    end
                else
                    simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(konec_time));
                    pause(konec_time-1.5);
                end



                %TODO: RUN FANUC, WAIT END MOVE
                % ret = Matlab2FanucCallback();
                % if ret ~= 0
                %     error("FAILED to finish move on FANUC!")
                % else
                %     disp("FANUC: Move done.")
                % end




                % uložení koncových hodnot poloh pohonů
                pohon1=simOut.pohon1.signals.values(end);
                pohon2=simOut.pohon2.signals.values(end);
                nuzky1=simOut.nuzky1.signals.values(end);
                nuzky2=simOut.nuzky2.signals.values(end);
                nuzky3=simOut.nuzky3.signals.values(end);
                nuzky4=simOut.nuzky4.signals.values(end);

                pocp=endp;

                % vstup pro generátor trajektorií 
                if isempty(matice_desek)
                pocp(3)=endp(3);
                endp=[xy_end(1), xy_end(2), vyska_end];
                pocp2 = [pocp(1), pocp(2), svisle];
                endp2 = [endp(1), endp(2), svisle];
                var_rigid=0;
                else
                pocp(3)=endp(3)+matice_desek(poz_ID_poc,5)/2;
                endp=[xy_end(1), xy_end(2), vyska_end];
                pocp2 = [pocp(1), pocp(2), svisle+max(matice_desek(:,4))];
                endp2 = [endp(1), endp(2), svisle+max(matice_desek(:,4))]; 
                var_rigid=-matice_desek(poz_ID_poc,5)/2;
                end
                save('pohyb_data.mat', 'pohon1', 'pohon2', 'nuzky1','nuzky2','nuzky3','nuzky4', 'pocp');
                
                % "přisátí" desky, pokud deska existuje.. (u testování
                % nemusí existovat)
                if deska==0
                elseif deska==1
                delete_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['R' num2str(ID_deska_poc) '/Rconn1']);
                add_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['Rigid/Rconn1']);
                end
                
                % generování trajektorie a simulace pohybu
                disp("Path: gripper anywhere A ---> B PLACE")

                GenerovaniTrajektorie();
                if USE_REAL_FANUC_CNC
                    %TODO: RUN FANUC, WAIT END MOVE
                    [fanuc_state, simOut] = Matlab2FanucCallback();
                    if fanuc_state ~= 0
                        error("FAILED to finish move on FANUC!")
                    else
                        disp("FANUC: Move done.")
                    end
                else
                    simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(konec_time));
                    pause(konec_time-1.5);
                end

                % GenerovaniTrajektorie();
                % simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(konec_time));
                %pause(konec_time-1.5);
 
                % uložení koncových hodnot poloh pohonů
                pohon1=simOut.pohon1.signals.values(end);
                pohon2=simOut.pohon2.signals.values(end);
                nuzky1=simOut.nuzky1.signals.values(end);
                nuzky2=simOut.nuzky2.signals.values(end);
                nuzky3=simOut.nuzky3.signals.values(end);
                nuzky4=simOut.nuzky4.signals.values(end);
                
                % přepsání interní databáze
                if deska==0
                elseif deska==1
                pozice{konec}=[pozice{konec};ID_deska_poc];
                pozice_typ_ID{konec}=[pozice_typ_ID{konec};matice_desek(ID_deska_poc,7)];
                %pozice_time{konec}=[pozice_time{konec};matice_desek(ID_deska_poc,9)];
                
                if length(pozice{pocatek})>1
                  pozice{pocatek}=pozice{pocatek}(1:end-1,1);
                  pozice_typ_ID{pocatek}=pozice_typ_ID{pocatek}(1:end-1,1);
                  %pozice_time{pocatek}=pozice_time{pocatek}(1:end-1,1);
                else
                  pozice{pocatek} = [];
                  pozice_typ_ID{pocatek}=[];
                  %pozice_time{pocatek}=[];
                end
                
                % "puštění" desky a přepsání parametrů Rigid Transform
                delete_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['Rigid/Rconn1']);
                add_line(model_path, ['S' num2str(ID_deska_poc) '/RConn1'], ['R' num2str(ID_deska_poc) '/Rconn1']);
                matice_desek(ID_deska_poc,2:4)=[endp(1), endp(2), vyska_end_set];
                set_param([model_path '/R' num2str(ID_deska_poc)], 'TranslationCartesianOffset', sprintf('[%f %f %f]', matice_desek(ID_deska_poc,2), matice_desek(ID_deska_poc,3), -3+vyska_end_set) );
                end
       end

       pocp=endp;
       if isempty(matice_desek)
       pocp(3)=endp(3);
       else
       pocp(3)=endp(3)+matice_desek(poz_ID_poc,5)/2;
       end
    
    % pokud jsme připojení na externí databázi.. tak uložení do ní
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
                        %skladData(n, 4) = pozice_time{i}(j);   
                end
            end
        end
        
        % Převedení matice na buňky obsahující řádky a kulaté závorky s čárkami
        skladCell = cellfun(@(row) ['(', num2str(row(1), '%d, '), num2str(row(2), '%d, '), num2str(row(3), '%d, '), num2str(row(4), '%d'), ')'], num2cell(skladData, 2), 'UniformOutput', false);
    
        % Spojení buněk do jednoho řetězce s mezerami a odstranění poslední čárky
        skladString = ['[', strjoin(skladCell, ', '), ']'];
        
        % uložení do databáze pomocí skriptu
        setStorage(skladString);
    else
    end
        
       %uložení polohových dat a externí databáze
       save('pohyb_data.mat', 'pohon1', 'pohon2', 'nuzky1','nuzky2','nuzky3','nuzky4', 'pocp');
       save('desky_data.mat', 'pozice', 'pozice_typ_ID', 'matice_desek', 'celkem_ID');
       save_system(model_path);
        
end