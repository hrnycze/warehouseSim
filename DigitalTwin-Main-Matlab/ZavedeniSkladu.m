function ZavedeniSkladu()
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%% Funkce pro zavedení skladu %%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;
close all;
clc;

% zpřístupnění globálních proměnných
global IO_ID IO_pocet vstupni_polohy vystupni_polohy vystupni_ID vstupni_ID stoh_poloha num_list typ_desek celkem_ID pozice sirka_desky delka_desky matice_desek model_path;
global nejvyssi_x nejnizsi_x nejvyssi_y nejnizsi_y rozdil_x rozdil_y robot natoceni uhel uhelrad svisle svisle2 amax vmax h  
global pocp endp pocp2 endp2
global xtraj ytraj ztraj natoceni konec_time
global pohon1 pohon2 nuzky1 nuzky2 nuzky3 nuzky4 poz_ID_poc var_rigid A pozice_typ_ID typ_ID mainFig Vysunuti pozice_time
global databaze

% Nastavení cesty k modelu
model_path = 'RobotickyManipulator_Simscape';
% Otevření modelu
open_system(model_path);

%načtení skladových dat uložených z GUI
load sklad_data.mat;

% vynulování matice desek
matice_desek=[];

%zavedení skladových konstant
IO_pocet=numel(vstupni_polohy)/2+numel(vystupni_polohy)/2;
IO_ID=[vstupni_ID vystupni_ID];

nejvyssi_x = max(stoh_poloha(:, 1));
nejnizsi_x = min(stoh_poloha(:, 1));
nejvyssi_y = max(stoh_poloha(:, 2));
nejnizsi_y = min(stoh_poloha(:, 2));

rozdil_x = abs(nejvyssi_x - nejnizsi_x);
rozdil_y = abs(nejvyssi_y - nejnizsi_y);

celkem_ID=0;

robot.sirka_y = rozdil_y+3.6; %m
robot.delka_x = rozdil_x+4; %m
robot.vyska_z = 3; %m

robot.rigid_x=max(stoh_poloha(:,1))+3.6/2;
robot.rigid_y=max(stoh_poloha(:,2))+4/2;
robot.rigid_y2=max(stoh_poloha(:,2))+4/2-robot.sirka_y;

sirka_desky=2.00; %m 
delka_desky=2.75; %m
    
robot.delkaNuzek = 1.6; %m
robot.prisavkySirka = 2.55;%m
robot.prisavkyDelka = 1.8; %m

natoceni=0*pi/180;
uhel = [30; 150; 210; 330];
uhelrad = [uhel(1)*pi/180; uhel(2)*pi/180; uhel(3)*pi/180; uhel(4)*pi/180];
% výška minimálního svislého posunu při konečném polohování desky
svisle = 0.2; % [m]před vodorovnym posunem vyjede efektor svisle nahoru o xx [m]
svisle2 = 0.2; %  [m]svisle před koncem

% Diskretizační krok při numerickém výpočtu
h = 0.01; % [s]...krok

Vysunuti=0.2;

% Maximální rychlosti a zrychlení
vmax = 1.5; % [m/s] 
amax = 0.5; % [m/s^2] 

num_list = [0.01 0.015 0.020 0.025 0.030]; %tloušťky desek

typ_desek = [1 2 3 4 5 6 7 8 9 10]; %typ desek

pozice={};
pozice_typ_ID={};
pozice_time={};
for i = 1:(numel(stoh_poloha) / 2)
    pozice{i} = [];
    pozice_typ_ID{i} = [];
    pozice_time{i} = [];
end

pocp = [0, 0, 1];


nuzky1=0.4374;
nuzky2=1.1334;
nuzky3=1.1334;
nuzky4=0.4374;
pohon1=0.5;
pohon2=0.5;


% Nastavení cesty k modelu
  model_path = 'RobotickyManipulator_Simscape';
% Otevření modelu
  open_system(model_path);

  % přidání subsystémů do parametrického modelu
  add_block('simulink/Commonly Used Blocks/Subsystem', [model_path '/Zebrovani']);
  set_param( [model_path '/Zebrovani'], 'position', [160  -356   260  -314]);
  delete_line([model_path '/Zebrovani'], ['In1/1'], ['Out1/1']);
  delete_block([model_path '/' 'Zebrovani' '/In1'])
  delete_block([model_path '/' 'Zebrovani' '/Out1'])
  add_block('simulink/Signal Routing/Connection Port', [model_path '/' 'Zebrovani' '/In1']);
  add_line(model_path, ['Zebrovani/Lconn1'], 'pricny_nosnik/Rconn1', 'autorouting', "on"); 

  l=1;
  for k=1:round((robot.sirka_y-0.3)/0.85) 
        add_block("sm_lib/Body Elements/Brick Solid", [model_path '/' 'Zebrovani'  '/Zebro' num2str(k)]);
        set_param([model_path '/' 'Zebrovani'  '/Zebro' num2str(k)], 'BrickDimensions', '[1.4 0.05 0.05]', 'position',   [560  -125+65*l   600   -85+65*l], 'GraphicDiffuseColor', '[0.4 0.4 0.4]', "Orientation", "left" );
        add_block("sm_lib/Frames and Transforms/Rigid Transform", [model_path '/' 'Zebrovani'  '/Transform' num2str(k)]);
        set_param([model_path '/' 'Zebrovani'  '/Transform' num2str(k)], 'Translationmethod', 'Cartesian', 'TranslationCartesianOffset', sprintf('[%f %f %f]',0.7000, 0.3+0.85*(k-1), -0.025), 'position',  [480  -125+65*l   520   -85+65*l], "Orientation", "right");
        add_line([model_path '/' 'Zebrovani'], ['Zebro' num2str(k) '/RConn1'], ['Transform' num2str(k) '/Rconn1']);
        add_line([model_path '/' 'Zebrovani'], ['Transform' num2str(k) '/Lconn1'], 'In1/Rconn1', 'autorouting', "on");  
        l=l+1;
  end
  for k=1:round((robot.sirka_y-0.725)/1.7)
        j=k+99;
        add_block("sm_lib/Body Elements/Brick Solid", [model_path '/' 'Zebrovani'  '/Zebro' num2str(j)]);
        set_param([model_path '/' 'Zebrovani'  '/Zebro' num2str(j)], 'BrickDimensions', '[1.6 0.05 0.05]', 'position',   [560  -125+65*l   600   -85+65*l], 'GraphicDiffuseColor', '[0.4 0.4 0.4]', "Orientation", "left" );
        add_block("sm_lib/Frames and Transforms/Rigid Transform", [model_path '/' 'Zebrovani'  '/Transform' num2str(j)]);
        set_param([model_path '/' 'Zebrovani'  '/Transform' num2str(j)],'RotationMethod', 'StandardAxis', 'RotationStandardAxis', '+Z', 'RotationAngle', '30', 'Translationmethod', 'Cartesian', 'TranslationCartesianOffset', sprintf('[%f %f %f]',0.7000, 0.7250+1.7000*(k-1), -0.025), 'position',  [480  -125+65*l   520   -85+65*l], "Orientation", "right");
        add_line([model_path '/' 'Zebrovani'], ['Zebro' num2str(j) '/RConn1'], ['Transform' num2str(j) '/Rconn1']);
        add_line([model_path '/' 'Zebrovani'], ['Transform' num2str(j) '/Lconn1'], 'In1/Rconn1', 'autorouting', "on");   
        l=l+1;
  end
  for k=1:round((robot.sirka_y-1.575)/1.7)
        i=k+999;
        add_block("sm_lib/Body Elements/Brick Solid", [model_path '/' 'Zebrovani'  '/Zebro' num2str(i)]);
        set_param([model_path '/' 'Zebrovani'  '/Zebro' num2str(i)], 'BrickDimensions', '[1.6 0.05 0.05]', 'position',   [560  -125+65*l   600   -85+65*l], 'GraphicDiffuseColor', '[0.4 0.4 0.4]', "Orientation", "left" );
        add_block("sm_lib/Frames and Transforms/Rigid Transform", [model_path '/' 'Zebrovani'  '/Transform' num2str(i)]);
        set_param([model_path '/' 'Zebrovani'  '/Transform' num2str(i)],'RotationMethod', 'StandardAxis', 'RotationStandardAxis', '-Z', 'RotationAngle', '30', 'Translationmethod', 'Cartesian', 'TranslationCartesianOffset', sprintf('[%f %f %f]',0.7000, 1.5750+1.7000*(k-1), -0.025), 'position',  [480  -125+65*l   520   -85+65*l], "Orientation", "right");
        add_line([model_path '/' 'Zebrovani'], ['Zebro' num2str(i) '/RConn1'], ['Transform' num2str(i) '/Rconn1']);
        add_line([model_path '/' 'Zebrovani'], ['Transform' num2str(i) '/Lconn1'], 'In1/Rconn1', 'autorouting', "on");   
        l=l+1;  
  end

  add_block('simulink/Commonly Used Blocks/Subsystem', [model_path '/Stojny']);
  set_param( [model_path '/Stojny'], 'position', [-280  -660  -240  -620]);
  delete_line([model_path '/Stojny'], ['In1/1'], ['Out1/1']);
  delete_block([model_path '/' 'Stojny' '/In1'])
  delete_block([model_path '/' 'Stojny' '/Out1'])
  add_block('simulink/Signal Routing/Connection Port', [model_path '/' 'Stojny' '/In1']);
  add_line(model_path, ['Stojny/Lconn1'], 'Rigid Stojny/Rconn1', 'autorouting', "on"); 
  
  l=1;
  pozicky=linspace(robot.rigid_x, robot.rigid_x-robot.delka_x, 2+round(rozdil_x/3));
  for k=1:round(rozdil_x/3);
        linspace(robot.rigid_x, robot.rigid_x-robot.delka_x, round(rozdil_x/3) )
        add_block("sm_lib/Body Elements/Brick Solid", [model_path '/' 'Stojny'  '/Stojna' num2str(k)]);
        set_param([model_path '/' 'Stojny'  '/Stojna' num2str(k)], 'BrickDimensions', sprintf('[%f %f %f]', 0.1, 0.1, robot.vyska_z), 'position',   [560  -125+65*l   600   -85+65*l], 'GraphicDiffuseColor', '[0.4 0.4 0.4]', "Orientation", "left" );
        add_block("sm_lib/Frames and Transforms/Rigid Transform", [model_path '/' 'Stojny'  '/TransformS' num2str(k)]);
        set_param([model_path '/' 'Stojny'  '/TransformS' num2str(k)], 'Translationmethod', 'Cartesian', 'TranslationCartesianOffset', sprintf('[%f %f %f]',pozicky(k+1), robot.rigid_y, 0), 'position',  [480  -125+65*l   520   -85+65*l], "Orientation", "right");
        add_line([model_path '/' 'Stojny'], ['Stojna' num2str(k) '/RConn1'], ['TransformS' num2str(k) '/Rconn1']);
        add_line([model_path '/' 'Stojny'], ['TransformS' num2str(k) '/Lconn1'], 'In1/Rconn1', 'autorouting', "on"); 

        add_block("sm_lib/Body Elements/Brick Solid", [model_path '/' 'Stojny'  '/StojnaL' num2str(k)]);
        set_param([model_path '/' 'Stojny'  '/StojnaL' num2str(k)], 'BrickDimensions', sprintf('[%f %f %f]', 0.1, 0.1, robot.vyska_z), 'position',   [560  -125+65*l   600   -85+65*l], 'GraphicDiffuseColor', '[0.4 0.4 0.4]', "Orientation", "left" );
        add_block("sm_lib/Frames and Transforms/Rigid Transform", [model_path '/' 'Stojny'  '/TransformSL' num2str(k)]);
        set_param([model_path '/' 'Stojny'  '/TransformSL' num2str(k)], 'Translationmethod', 'Cartesian', 'TranslationCartesianOffset', sprintf('[%f %f %f]',pozicky(k+1), robot.rigid_y2, 0), 'position',  [480  -125+65*l   520   -85+65*l], "Orientation", "right");
        add_line([model_path '/' 'Stojny'], ['StojnaL' num2str(k) '/RConn1'], ['TransformSL' num2str(k) '/Rconn1']);
        add_line([model_path '/' 'Stojny'], ['TransformSL' num2str(k) '/Lconn1'], 'In1/Rconn1', 'autorouting', "on");  
        l=l+1;
  end
    
  % odsimulování trajektorie...
  save_system(model_path);
  xtraj=[0 0; 0.0047 0];
  ytraj=[0 0; 0.0047 0];
  ztraj=[0	-2;0.0047 -2.0];
  natoceni=[0	0;0.0047 0];
  var_rigid=0;
  simOut = sim('RobotickyManipulator_Simscape', 'StartTime', num2str(0), 'StopTime', num2str(xtraj(end,1)));

  % uložení poloh pohonů...
  pohon1=simOut.pohon1.signals.values(end);
  pohon2=simOut.pohon2.signals.values(end);
  nuzky1=simOut.nuzky1.signals.values(end);
  nuzky2=simOut.nuzky2.signals.values(end);
  nuzky3=simOut.nuzky3.signals.values(end);
  nuzky4=simOut.nuzky4.signals.values(end);

  % uložení dat
  save('pohyb_data.mat', 'pohon1', 'pohon2', 'nuzky1','nuzky2','nuzky3','nuzky4', 'pocp');
  save('desky_data.mat', 'pozice', 'pozice_typ_ID', 'pozice_time', 'matice_desek', 'celkem_ID');
end