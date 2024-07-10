Simulační model automatické skladu je řízen skrze uživatelské rozhraní, které otevřeme zapnutím skriptu HlavniOkno.m. Není potřeba otevírat jakýkoliv jiný skript. Po spuštění skriptu HlavniOkno.m je nutné chvíli počkat, protože se načte poslední stav skladu a dojde k otevření Simulink prostředí. U pomalejších PC to může zabrat i více jak minutu. 

!!! Pokud se chceme připojit na externí databázi, je nutné ve skriptech getDesks.m, getStorage.m, setStorage.m vytvořit VLASTNÍ cestu do složky, kde se nám bude vytvářet dočasný python. Další nutností je mít nainstalovaný python, skrze který z databáze čtu a do databáze nahrávám. A také je nutné mít zprovozněnou databázi v prostředí Docker Desktop, což je problematická operace, kterou za mě vyřešil pan kolega Ing. Pavel Bastl Ph.D. Pokud chceme z databáze načíst aktuální stav skladu, musíme se přesvědčit, že poslední uložený stav v databázi je pro naší konfiguraci! Při náhodném generování desek se stav skladu do databáze neuloží, je potřeba zvolit naskladnění jako v reálném skladu. Tudíž například kombinace náhodné generování a následně naskladnění nám přepíše stav externí databáze. Jakýkoliv pohyb desek ve skladu nám též přepíše externí databázi! !!!

Po spuštění se objeví hlavní okno s nápisem Automatický chaotický sklad, níže budou popsány jednotlivé funkce.. je vhodné minimalizovat a "dát stranou" Simulink model, který musí zůstat otevřený, ale není potřeba do něj zasahovat. Není vhodné posouvat uživatelské rozhraní, protože je pevně nastavené, kde se bude otevírat.

1) Automatické přeskladnění - U automatického přeskladnění je potřeba vybrat platný soubor (blíže popsáno v diplomové práci), který obsahuje ID pozic (vstupní a výstupní záporné, skladové 0-n) - například sklad1.txt nebo sklad2.txt (ale je nutné zkontrolovat, že automatické přesuny odpovídají aktuální rozložení skladu!!!). Po vložení se objeví sekvence pohybů v tabulce a dále je možné vybrat stav skladu (aktuální, nově vygenerovaný, nagenerování dalších desek nebo načtení desek z ext. databáze - pokud je připojena).

2) Manuální přeskladnění - Manuální přeskladnění obsahuje tři možnosti. Vyskladnění dle ID, vyskladnění dle TYP_ID a přeskladnění dle ID. Na výběr jsou pouze ID desek, které jsou naskladněné ve skladu a pozice, které náleží aktuální konfiguraci skladu. Vyskladnění je možné pouze na vysklaďnovací pozice. Přeskladnění je možné z jakékoliv na jakoukoliv jinou pozici.

3) Generovat sklad - Tlačítko generovat sklad otevře nové okno, kde je na výběr "Náhodně generovat" nebo "Načíst z databáze", pokud jsme ale k externí databázi připojeni. 

4) Naskladnění desek - Naskladnit desky je možné jak na vstupní, tak na výstupní pozice. Je nutné specifikovat konkrétní ID dané pozice (pozn. specifikované od kolegy Ing. Jana Hrnčíře). Dále je potřeba zvolit počet typů desek, které budeme naskladňovat a počet desek od každého typu a typ. 

5) Konfigurace skladu - Slouží k vytvoření nového rozložení skladu a je potřeba přesně specifikovat hodnoty pro parametrický model. Prvně je potřeba zapsat počet vstupních a výstupních pozic (defaultně 1) a jejich ID (kolega Ing. Hrnčíř) (-2 -3 ... -n). Pro vstupní a výstupní polohy definovat souřadnice x a y. Je potřeba definovat sklad tak, aby "uvnitř" skladu byla souřadnice x=0 a y=0, protože zde jsou nastavené první počáteční podmínky. Dále je nutné nastavit počet skladovacích poloh a dopsat jejich souřadnice x a y. Například následovně ( vstupní polohy x=-3 y=-1.2, výstupní polohy x=-3 y=1.2, počet skladovacích poloh = 4, skladovací polohy x=0 y=-1.2, x=0 y=1.2, x=3, y=-1.2, x=3 y=1.2).

6) Aktuální stav - Zobrazí aktuálně naskladněné desky ve skladu dle ID a TYP_ID. 

7) Definovat typ desek - Pokud nejsme připojení na externí databázi, je možné si definovat vlastní desku. Případně odebrat již definované desky. Výška, délka a šířka jsou v metrech, hustota je v kg/m3 a materiál je označen jako integer od 1 do 10 (pro ostatní čísla není nastavená barva...). Pokud je sklad připojený na databáti, tak je možné do typů desek pouze nahlédnout!

8) Vymazání skladu - Spustí funkci vymazání skladu, která vymaže veškeré naskladněné desky ve skladu.

9) Ukončit program - zavře uživatelské rozhraní

10) Databáze OFF/ON. Pokud se chceme připojit na externí databázi, je potřeba mít databázi zprovozněnou v Dockeru. Nahrání databáze do dockeru ve Windows je problematické a vyřešil to za mě kolega Ing. Pavel Bastl Ph.D. Pokud nemáme spuštěnou externí databázi, není možné se připojit na databázi!


ŘEŠENÍ CHYB

Simulační model je odzkoušený a po vyladění jsem se nesetkal s žádnými chybami. Nejpravděpodobněji by ale chyba nastala v prostředí Simulink, kde je vytvořený Simscape model skladu. Mohlo by dojít k neúspěšnému "odpojení" desky, poté je potřeba od bloku pojmenovaného "Rigid" odstranit prázdné připojení zleva. Tato chyba se objevovala v předchozí verzi, ale podařilo se jí pravděpodobně úspěšně odstranit. 

