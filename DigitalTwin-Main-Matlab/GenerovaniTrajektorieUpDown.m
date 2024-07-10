function GenerovaniTrajektorieUpDown()
global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
global pocp endp pocp2 endp2
global xtraj ytraj ztraj natoceni konec_time

waypoints= [pocp(1) endp(1) ;pocp(2) endp(2) ;pocp(3) endp(3); 0 0 ];
vellim=[-vmax vmax; -vmax vmax; -vmax vmax; -vmax vmax];
accellim=[-amax amax; -amax amax; -amax amax; -amax amax];
[trajektorie,qd,qdd,t,solninfo] = contopptraj(waypoints,vellim,accellim);

xtraj = [[t]', [trajektorie(1,:)]'];
ytraj = [[t]', [trajektorie(2,:)]'];
ztraj = [[t]', [trajektorie(3,:)-robot.vyska_z]'];
natoceni = [[t]', [trajektorie(4,:)]'];

% hledani vetsiho rozdilu nez dve sekundy mezi dvemi po sobe jdoucimi
podmet_k_vymazani = find(diff(t) > 2);

% pripadne odstraneni nesmyslne hodnoty
t(podmet_k_vymazani + 1) = [];
xtraj(podmet_k_vymazani + 1, :) = [];
ytraj(podmet_k_vymazani + 1, :) = [];
ztraj(podmet_k_vymazani + 1, :) = [];
konec_time=max(t);
end