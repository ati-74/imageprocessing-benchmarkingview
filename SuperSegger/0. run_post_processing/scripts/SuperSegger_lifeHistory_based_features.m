function [] = SuperSegger_lifeHistory_based_features(dataset,mode,intervalTime,num_time_steps)

load(strcat('../../',dataset,'/',mode,'/xy1/clist.mat'),'data');
write_directory = strcat('../../',dataset,'/',mode,'/post-processing/results/');

cellNumber=size(data,1);
cell_life_id_value = [];
growth_rate = [];
for i=1:cellNumber
    %append to list
    cell_life_id_value(end+1) = i;
    growth_rate(end+1)=(log(data(i,11))-log(data(i,10)))/((data(i,6)+1)*intervalTime);
end

birthLength=data(:,10);
lifeHistory=data(:,6)+1;


%calculation of average length and average velocity
[AverageVelocity,AverageLength] = SupperSegger_Extract_lifeHistory_based_features(dataset,mode,intervalTime,num_time_steps,cellNumber);

%add to table
T = table(transpose(cell_life_id_value),transpose(growth_rate),birthLength,lifeHistory,transpose(AverageVelocity),transpose(AverageLength));
%add column name
T.Properties.VariableNames={'CellLifeId','GrowthRate','birthLength','LifeHistory','AverageVelocity','AverageLength'};

% write to csv
%life history based features
writetable(T,strcat(write_directory,'SuperSegger_LifeHistory_based_Analysis.csv'),'Delimiter',',','QuoteStrings',true)

