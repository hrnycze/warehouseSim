## TODO

# MATLAB - Main

- ZBYTKY !!!!!

- ERROR pri prenosu desky, objevuje se pri PLACE preraci
"FANUC: Move done.
Brace indexing is not supported for variables of this type.

Error in spousteci (line 240)
                pozice_time{konec}=[pozice_time{konec};matice_desek(ID_deska_poc,9)];

Error in ManualniPreskladneni/preskladnenidesek (line 224)
    spousteci(param);

Error in ManualniPreskladneni>@(~,~)preskladnenidesek() (line 93)
buttonManPreskladneni.ButtonPushedFcn = @(~,~) preskladnenidesek();
 
Error using appdesservices.internal.interfaces.model.AbstractModel/executeUserCallback (line 282)
Error while evaluating Button PrivateButtonPushedFcn."

-ERROR generovani a mazani skladu
"Brace indexing is not supported for variables of this type.

Error in GenerovaniDesek (line 197)
            pozice_time{pozicedesek(i)}=[pozice_time{pozicedesek(i)}; (matice_desek(find(matice_desek(:,1))==cisla_zamichej(i),9))];

Error in GenerovaniSkladu/nahodneSklad (line 38)
        GenerovaniDesek()

Error in GenerovaniSkladu>@(~,~)nahodneSklad() (line 19)
    nahodneSkladButton.ButtonPushedFcn = @(~,~) nahodneSklad();
 
Error using appdesservices.internal.interfaces.model.AbstractModel/executeUserCallback (line 282)
Error while evaluating Button PrivateButtonPushedFcn."
"Error using vymazanidesek (line 42)
Invalid Simulink object name: 'RobotickyManipulator_Simscape/R13'.

Error in HlavniOkno>HlavniMenu/VymazatSklad (line 238)
        vymazanidesek();

Error in HlavniOkno>@(~,~)VymazatSklad() (line 72)
    vymazatSkladButton.ButtonPushedFcn = @(~,~) VymazatSklad(); - Show complete stack trace
Caused by:
    Error using vymazanidesek (line 42)
    Unable to find block 'R13'. - Show complete stack trace
 
Error using appdesservices.internal.interfaces.model.AbstractModel/executeUserCallback (line 282)
Error while evaluating Button PrivateButtonPushedFcn."
- UI Aktualni stav -- NOT WORKING
- UI Naskladneni -- NOT WORKING

![alt text](sklad.png)
