function GenerovaniTrajektorie()
    global  robot natoceni amax vmax pocp endp pocp2 endp2 xtraj ytraj ztraj natoceni konec_time
    
    % vypocitani trajektorie
    waypoints= [pocp(1) pocp2(1) ;pocp(2) pocp2(2) ;pocp(3) pocp2(3); 0 0 ];
    vellim=[-vmax vmax; -vmax vmax; -vmax vmax; -vmax vmax];
    accellim=[-amax amax; -amax amax; -amax amax; -amax amax];
    [trajektorie,qd,qdd,t] = contopptraj(waypoints,vellim,accellim);
    waypoints= [pocp2(1) endp2(1) ;pocp2(2) endp2(2) ;pocp2(3) endp2(3); 0 0];
    [trajektorie2,qd2,qdd2,t2] = contopptraj(waypoints,vellim,accellim);
    waypoints= [endp2(1) endp(1) ;endp2(2) endp(2) ;endp2(3) endp(3); 0 0 ];
    [trajektorie3,qd3,qdd3,t3] = contopptraj(waypoints,vellim,accellim);
    
    % prepocitani casu
    t2=max(t)+t2;
    t3=max(t2)+t3;
    
    % spojeni dilcich trajektorii
    xtraj = [[t t2 t3]', [trajektorie(1,:) trajektorie2(1,:) trajektorie3(1,:)]'];
    ytraj = [[t t2 t3]', [trajektorie(2,:) trajektorie2(2,:) trajektorie3(2,:)]'];
    ztraj = [[t t2 t3]', [trajektorie(3,:)-robot.vyska_z trajektorie2(3,:)-robot.vyska_z trajektorie3(3,:)-robot.vyska_z]'];
    natoceni = [[t t2 t3]', [trajektorie(4,:) trajektorie2(4,:) trajektorie3(4,:)]'];
    
    % hledani vetsiho rozdilu nez dve sekundy mezi dvemi po sobe jdoucimi
    podmet_k_vymazani = find(diff([t t2 t3]) > 2);
    
    % pripadne odstraneni nesmyslne hodnoty
    t(podmet_k_vymazani + 1) = [];
    xtraj(podmet_k_vymazani + 1, :) = [];
    ytraj(podmet_k_vymazani + 1, :) = [];
    ztraj(podmet_k_vymazani + 1, :) = [];
    konec_time=max(t);

    %cas delky simulace
    konec_time=max(t3);
end