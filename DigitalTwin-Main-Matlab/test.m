    % najdi dostupne desky ve skladu
    dostupne_desky = [];
    dostupne_desky_pocet = [];
    
    typ_ID_copy = typ_ID;

    temp = pozice_typ_ID((IO_pocet+1):length(pozice_typ_ID));
    for i = 1: length(temp)
        dostupne_desky = [dostupne_desky; temp{i}];
    end
    % disp(dostupne_desky')

    unique_desky = unique(dostupne_desky);

    counts = zeros(size(unique_desky));

    for i=1 : length(counts)
        counts(i) = sum(dostupne_desky == unique_desky(i)); 
    end
    
    % disp(unique_desky')
    % disp(counts')

    row_to_remove = false(size(typ_ID,1),1);

    for i=1 : size(unique_desky,1)
        if any(ismember(typ_ID(:,1), unique_desky(i)))
            row_to_remove(unique_desky(i)) = true;
        end
    end

    typ_ID_copy = typ_ID_copy(row_to_remove,:);

    % disp(typ_ID_copy)

    %%

    % Define the input string
str = "[(-2, 1), (-2, 1), (-2, 1), (0, -3), (0, -3), (1, -3)]";

% Remove the brackets and parentheses
str = strrep(str, '[', '');
str = strrep(str, ']', '');
str = strrep(str, '(', '');
str = strrep(str, ')', '');

% Split the string by comma and space
parts = split(str, ', ');

% Initialize an array to hold the numeric values
values = zeros(1, length(parts));

% Convert each part to a numeric value
for i = 1:length(parts)
    values(i) = str2double(parts{i});
end

% Reshape the values into a 2xN matrix
matrix = reshape(values, 2, [])';

% Display the matrix
disp(matrix);