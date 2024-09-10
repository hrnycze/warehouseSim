# PREREQUISITIES
* MATLAB - Optimalization Toolbox, Parallel Toolbox ... etc.
* Fanuc - Focus (32 bits /or if lucky 64bits/) + CNC Guide 2 
* Python 3.10 (32 bits /or if lucky 64bits/)
* Python Packages: Numpy
* ! It's needed to have Python 32-bit /or if lucky 64bits/ in PATH !
* (Docker :P) 

## Repořitář modulů vytvořených vrámci diplomové práce Optimální řízení toku materiálu v chaotickém skladu s výrobními stroji

![alt text](sklad.png)


# Architektura plánované aplikace s vytvořenými moduly

Komunikace mezi vytvořenými moduly je následující. Nejdříve musí být
vytvořena požadovaná fronta z dostupných desek z databáze skladu rozvrhovacím modulem
nebo případně ručně operátorem skladu. Fronta je dále zpracována A–Star
algoritmem, který potřebuje simulátor skladu. Proto musí být do simulátoru nahrán aktuální
stav skladu z databáze. Po získání posloupností akcí od A–Star jsou akce
provedeny reálným skladem a současně aplikovány na simulátor. Nakonec je
aktualizována databáze podle simulátoru a celý proces se může opakovat.

![alt text](Pathfinding-Python/arch.png)

# Vytvořené moduly:

- warehouse.py Simulátor formální reprezentace skladu
- astar.py Algoritmus pro optimální pohyb materiálu ve skladu
- ilpScheduleSolver.py Program pro rozvrhování výroby na identických
- ilpScheduleTypeOfMachinesSolver.py a na dedikovaných strojích
- schedule-plus-astar.py Ukázka spojení astar.py s rozvrhováním výroby
- ilp-model.py ILP model pro rozvrhování s deadliny
- cp-model.py CP model pro rozvrhování s deadliny

# Ukázka běhu A-Star algoritmu skladu:

```
Searching path: [[1, 2, 6, 3], [8, 7, 5], [4, 9]] 
Input: (12, 14, 15) Output: [] Orders: (2, 3, 7, 8) Done: False -> for order (2, 3, 7, 8)
Found a path (length=10): 
[(1, -2), (1, -2), (0, 1), (-3, 1), (-3, 1), (-3, 1), (0, 1), (0, 2), (0, -2), (1, -2)]
How it goes: 
[[1, 2, 6, 3], [8, 7, 5], [4, 9]] 
Input: (12, 14, 15) Output: [] Orders: (2, 3, 7, 8) Done: False

                    |1|        
  |12|        |8|   |2|        
  |14|  |4|   |7|   |6|        
  |15|  |9|   |5|   |3|        
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (1, -2) ----------

                    |1|        
  |12|              |2|        
  |14|  |4|   |7|   |6|        
  |15|  |9|   |5|   |3|   |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (1, -2) ----------

                    |1|        
  |12|              |2|        
  |14|  |4|         |6|   |7|
  |15|  |9|   |5|   |3|   |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (0, 1) ----------

  |12|              |2|        
  |14|  |4|   |1|   |6|   |7|
  |15|  |9|   |5|   |3|   |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (-3, 1) ----------

              |12|  |2|        
  |14|  |4|   |1|   |6|   |7|
  |15|  |9|   |5|   |3|   |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (-3, 1) ----------

              |14|             
              |12|  |2|        
        |4|   |1|   |6|   |7|
  |15|  |9|   |5|   |3|   |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (-3, 1) ----------

              |15|             
              |14|             
              |12|  |2|        
        |4|   |1|   |6|   |7|
        |9|   |5|   |3|   |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (0, 1) ----------

              |2|              
              |15|             
              |14|             
              |12|             
        |4|   |1|   |6|   |7|
        |9|   |5|   |3|   |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (0, 2) ----------

              |2|              
              |15|             
              |14|             
        |6|   |12|             
        |4|   |1|         |7|
        |9|   |5|   |3|   |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (0, -2) ----------

              |2|              
              |15|             
              |14|             
        |6|   |12|        |3|
        |4|   |1|         |7|
        |9|   |5|         |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
------------ Action: (1, -2) ----------

              |15|             
              |14|        |2|
        |6|   |12|        |3|
        |4|   |1|         |7|
        |9|   |5|         |8|
''####''^^^^''^^^^''^^^^''****''
[input]  #2    #1    #0  [output]
[[], [15, 14, 12, 1, 5], [6, 4, 9]] 
Input: [] Output: [2 3 7 8] Orders: (2, 3, 7, 8) Done: True
Total expanded nodes: 10 Time: 0.01

```

## TODO

# MATLAB - Main

- ZBYTKY !!!!!

- ERROR pri prenosu desky, objevuje se pri PLACE preraci, NEJSPI SPATNE ULOZENO var "pozice_time" 
```
FANUC: Move done.
Brace indexing is not supported for variables of this type.

Error in spousteci (line 240)
                pozice_time{konec}=[pozice_time{konec};matice_desek(ID_deska_poc,9)];

Error in ManualniPreskladneni/preskladnenidesek (line 224)
    spousteci(param);

Error in ManualniPreskladneni>@(~,~)preskladnenidesek() (line 93)
buttonManPreskladneni.ButtonPushedFcn = @(~,~) preskladnenidesek();
 
Error using appdesservices.internal.interfaces.model.AbstractModel/executeUserCallback (line 282)
Error while evaluating Button PrivateButtonPushedFcn."
```
- ERROR generovani a mazani skladu
``` 
Brace indexing is not supported for variables of this type.

Error in GenerovaniDesek (line 197)
            pozice_time{pozicedesek(i)}=[pozice_time{pozicedesek(i)}; (matice_desek(find(matice_desek(:,1))==cisla_zamichej(i),9))];

Error in GenerovaniSkladu/nahodneSklad (line 38)
        GenerovaniDesek()

Error in GenerovaniSkladu>@(~,~)nahodneSklad() (line 19)
    nahodneSkladButton.ButtonPushedFcn = @(~,~) nahodneSklad();
 
Error using appdesservices.internal.interfaces.model.AbstractModel/executeUserCallback (line 282)
Error while evaluating Button PrivateButtonPushedFcn.
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
Error while evaluating Button PrivateButtonPushedFcn.
```
- UI Aktualni stav -- NOT WORKING
- UI Naskladneni -- NOT WORKING

![alt text](sklad.png)
