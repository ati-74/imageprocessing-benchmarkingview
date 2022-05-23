function [] = SuperSegger_bacteria_based_features_each_timestep(dataset,mode,num_time_steps,bac_lable)
%find .mat files in cell directory
directory=strcat('../../',dataset,'/',mode,'/xy1/cell/');
write_directory = strcat('../../',dataset,'/',mode,'/post-processing/results/');
files=dir([strcat(directory,'*.mat')]);
load(strcat('../../',dataset,'/',mode,'/raw_im/cropbox.mat'),'crop_box_array');
%sorted files
sorted_files = natsortfiles(files);
%number of files
Num_files=length(sorted_files);

TimeStep = [];
cell_life_id_value = [];
orientation=[];
Center_X=[];
Center_Y=[];
major_axis = [];
minor_axis = [];
bacteria_lable = [];

for i=1:Num_files
    file_name=sorted_files(i).name;
    % load `.mat` file
    load(strcat(directory,file_name));
    life_history=length(CellA);
    
    for j=1:life_history
        if birth+j-1 <= num_time_steps
            time_step = birth+j-1;
            TimeStep(end+1)=birth+j-1;
            cell_life_id_value(end+1) = i;
            bacteria_lable(end+1) = bac_lable(i);
            orientation (end+1) = CellA{1,j}.coord.orientation;
            Center_X (end+1) = CellA{1,j}.coord.r_center(1)-crop_box_array{1, 1}(time_step,2);
            Center_Y (end+1) = CellA{1,j}.coord.r_center(2)-crop_box_array{1, 1}(time_step,1);
            major_axis (end+1) = CellA{1,j}.cellLength(1);
            minor_axis (end+1) = CellA{1,j}.cellLength(2);
        end
    end
end
% cellLength
%add to sorted table
T = sortrows(table(transpose(TimeStep),transpose(cell_life_id_value),transpose(bacteria_lable),transpose(orientation),transpose(Center_X),transpose(Center_Y),transpose(major_axis),transpose(minor_axis)));
%add column name
T.Properties.VariableNames={'TimeStep','CellLifeId','lable','Orientation','Center_X','Center_Y','Major_axis','Minor_axis'};

% write to csv
%life history based features
writetable(T,strcat(write_directory,'SuperSegger_bacteria_feature_analysis.csv'),'Delimiter',',','QuoteStrings',true);
