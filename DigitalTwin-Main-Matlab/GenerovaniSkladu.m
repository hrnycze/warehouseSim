function GenerovaniSkladu
    global databaze
    
    %vytvoření okna pro generování skladu
    fig = uifigure('Name', 'Definované desky');
    fig.Position(1) = 700;
    fig.Position(2) = 600;
    fig.Position(3) = 200;
    fig.Position(4) = 200;

    fig.Color = '#DAE6FA';
    
    zpetButton = uibutton(fig, 'Text', 'Zpět', 'Position', [20, 10, 80, 30], 'ButtonPushedFcn', @(src, event) zpet());
    zpetButton.FontColor=[1,0,0];

    % tlačítko generovat sklad
    nahodneSkladButton = uibutton(fig, 'Text', 'Náhodně generovat', 'Position', [25, 150, 150, 30]);
    % akce při stistknutí tlačítka
    nahodneSkladButton.ButtonPushedFcn = @(~,~) nahodneSklad();

    % tlačítko generovat sklad
    databazeSkladButton = uibutton(fig, 'Text', 'Načíst z databáze', 'Position', [25, 100, 150, 30]);
    % akce při stistknutí tlačítka
    databazeSkladButton.ButtonPushedFcn = @(~,~) databazeSklad();
    
    if databaze == 1
        % Pokud databaze == 1, tlačítko je viditelné a klikatelné
        databazeSkladButton.BackgroundColor = [1, 1, 1];
        databazeSkladButton.Enable = 'on';
        databazeSkladButton.ButtonPushedFcn = @(~,~) databazeSklad();
    else
        % Pokud databaze není 1, tlačítko je šedivé a neklikatelné
        databazeSkladButton.BackgroundColor = [0.8, 0.8, 0.8];
        databazeSkladButton.Enable = 'off';
    end
    
    function nahodneSklad()
        GenerovaniDesek()
    end

    function databazeSklad()
        vymazanidesek;
        NacteniZDatabaze;
    end

    function zpet()
        close(fig);
    end
end