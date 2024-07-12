

function NacteniParametru()

global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
global pocp endp pocp2 endp2
global xtraj ytraj ztraj natoceni konec_time
global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc Vysunuti natoceni_rad pozice_typ_ID databaze pozice_time
global USE_REAL_FANUC_CNC

USE_REAL_FANUC_CNC = false;

% Nastavení cesty k modelu
model_path = 'RobotickyManipulator_Simscape';
% Otevření modelu
open_system(model_path);


load sklad_data.mat;
load desky_data.mat;
load typy_desek.mat;
load pohyb_data.mat;



nejvyssi_x = max(stoh_poloha(:, 1));
nejnizsi_x = min(stoh_poloha(:, 1));
nejvyssi_y = max(stoh_poloha(:, 2));
nejnizsi_y = min(stoh_poloha(:, 2));

% Vypočtěte rozdíl mezi nejvyšším a nejnižším x
rozdil_x = abs(nejvyssi_x - nejnizsi_x);
rozdil_y = abs(nejvyssi_y - nejnizsi_y);

robot.sirka_y = rozdil_y+3.6; %m6
robot.delka_x = rozdil_x+4; %m10
robot.vyska_z = 3; %m

robot.rigid_x=max(stoh_poloha(:,1))+3.6/2;
robot.rigid_y=max(stoh_poloha(:,2))+4/2;
robot.rigid_y2=max(stoh_poloha(:,2))+4/2-robot.sirka_y;

sirka_desky=2.00; %m 
delka_desky=2.75; %m
    
robot.delkaNuzek = 1.6; %m
robot.prisavkySirka = 2.55;%m
robot.prisavkyDelka = 1.8; %m

natoceni_rad=0*pi/180;
% Přidání proměnné do workspace
assignin('base', 'natoceni_rad', natoceni_rad);
natoceni = 0;
uhel = [30; 150; 210; 330];
uhelrad = [uhel(1)*pi/180; uhel(2)*pi/180; uhel(3)*pi/180; uhel(4)*pi/180];

% výška minimálního svislého posunu při konečném polohování desky
svisle = 0.2; % [m]před vodorovnym posunem vyjede efektor svisle nahoru o xx [m]
svisle2 = 0.2; %  [m]svisle před koncem

% Diskretizační krok při numerickém výpočtu
h = 0.01; % [s]...krok

% Maximální rychlosti a zrychlení
vmax = 1.5; % [m/s] 
amax = 0.5; % [m/s^2] 

Vysunuti=0.2;
% Přidání proměnné do workspace
assignin('base', 'Vysunuti', Vysunuti);

num_list = [0.01 0.015 0.020 0.025 0.030]; %tloušťky desek

typ_desek = [1 2 3 4 5 6 7 8 9 10]; %typ desek
end