
load('../../2. results/Position000000.mat','res');

cellNumber=length(res{1}.lineage);

TimeStep=[];
cell_lable=[];
Orientation=[];


for i=1:cellNumber
    lifeHistoryValue=length(res{1}.lineage{i}.frames);
    for j=1:lifeHistoryValue
        TimeStep(end+1) = res{1}.lineage{i}.frames(j);
        cell_lable(end+1)=i;
        %Orientation(end+1)=res{1}.lineage{i}.orientation(j);
        Orientation(end+1)=0;
    end   
end

%add to table
T = sortrows(table(transpose(TimeStep),transpose(cell_lable),transpose(Orientation)));
%add column name
T.Properties.VariableNames={'TimeStep','Cell_lable','Orientation'};

% write to csv
writetable(T,'../results/DeLTA_bacteria_feature_analysis.csv','Delimiter',',','QuoteStrings',true)
