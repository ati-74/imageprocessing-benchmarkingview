
%find .mat files in cell directory
directory='../../xy1/cell/';
files=dir([strcat(directory,'*.mat')]);
%sorted files
sorted_files = natsortfiles(files);
%number of files
Num_files=length(sorted_files);

TimeStep = [];
cellNumber_value = [];
orientation=[];

for i=1:Num_files
    file_name=sorted_files(i).name;
    % load `.mat` file
    load(strcat(directory,file_name));
    life_history=length(CellA);
    
    for j=1:life_history
        TimeStep(end+1)=birth+j-1;
        cellNumber_value(end+1) = i;
        orientation (end+1) = CellA{1,j}.coord.orientation;  
    end
end

%add to sorted table
T = sortrows(table(transpose(TimeStep),transpose(cellNumber_value),transpose(orientation)));
%add column name
T.Properties.VariableNames={'TimeStep','CellNumber','Orientation'};

% write to csv
%life history based features
writetable(T,'../results/SuperSegger_bacteria_based_features_each_timestep.csv','Delimiter',',','QuoteStrings',true)

