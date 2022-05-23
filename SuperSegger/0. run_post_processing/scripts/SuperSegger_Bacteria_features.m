function [] = SuperSegger_Bacteria_features(dataset,mode)

load(strcat('../../',dataset,'/',mode,'/xy1/clist.mat'),'data');
load(strcat('../../',dataset,'/',mode,'/xy1/clist.mat'),'def');
write_directory = strcat('../../',dataset,'/',mode,'/post-processing/results/');

% total information about cells
SuperSegger_Results=array2table([def;num2cell(data)]);

% write to csv
% write full data
writetable(SuperSegger_Results,strcat(write_directory,'SuperSegger_Bacteria_features.csv'),'Delimiter',',','QuoteStrings',true,'WriteVariableNames',0)

