


cellNumber = size(procTracks,2);

cell_id = [];
cell_start = [];
cell_end = [];
cell_mother = [];
cell_d1 = [];
cell_d2 = [];


for i=1:cellNumber
    cell_id (end + 1) =i;
    cell_start (end+1) = procTracks(i).start;
    cell_end (end+1) = procTracks(i).end;
    if procTracks(i).M == []
        cell_mother (end+1) = 0;
    else
        cell_mother (end+1) = procTracks(i).M;
    end
    cell_d1 (end+1) = procTracks(i).D1;
    cell_d2 (end+1) = procTracks(i).D2;
end


%add to table
T = table(transpose(cell_id), transpose(cell_start),transpose(cell_end),transpose(cell_mother), transpose(cell_d1), transpose(cell_d2));
%add column name
% ,'NumberOfDivision'
T.Properties.VariableNames={'Cell_id','start','end', 'mother', 'd1', 'd2'};

% write to csv
writetable(T,'Analysis.csv','Delimiter',',','QuoteStrings',true)

