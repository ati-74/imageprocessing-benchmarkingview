load('../../seg.mat','cellListN');

cell_Number_at_each_timestep=[cellListN(:)];

%add to table
T2=table(transpose(1:length(cell_Number_at_each_timestep)),cell_Number_at_each_timestep);
%add column name
T2.Properties.VariableNames={'StepNumber','NumberOfCells'};

% write to csv
writetable(T2,'../results/Oufti_TimeSteps_Analysis.csv','Delimiter',',','QuoteStrings',true)

