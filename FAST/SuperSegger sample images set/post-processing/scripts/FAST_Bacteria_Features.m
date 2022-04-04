
load('../../Tracks.mat','procTracks');

cellNumber=length(procTracks);

TimeStep = [];
cellNumber_value = [];
orientation=[];

for i=1:cellNumber
    Timesteps_num = size(procTracks(i).times);
    for j=1:Timesteps_num(2)
        TimeStep(end+1)=procTracks(i).times(j);
        cellNumber_value(end+1) = i;
        orientation (end+1) = procTracks(i).phi(j);  
    end
end


%add to sorted table
T = sortrows(table(transpose(TimeStep),transpose(cellNumber_value),transpose(orientation)));
%add column name
T.Properties.VariableNames={'TimeStep','CellNumber','Orientation'};

% write to csv
writetable(T,'../results/FAST_bacteria_feature_analysis.csv','Delimiter',',','QuoteStrings',true)
