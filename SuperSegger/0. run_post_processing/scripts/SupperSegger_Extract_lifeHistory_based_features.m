function [AverageVelocity,AverageLength] = SupperSegger_Extract_lifeHistory_based_features(dataset,mode,intervalTime,num_time_steps,numcells)
%find .mat files in cell directory

directory=strcat('../../',dataset,'/',mode,'/xy1/cell/');
files=dir([strcat(directory,'*.mat')]);
load(strcat('../../',dataset,'/',mode,'/raw_im/cropbox.mat'),'crop_box_array');
%sorted files
sorted_files = natsortfiles(files);
%number of files
Num_files=length(sorted_files);

AverageVelocity=NaN(1,numcells);
AverageLength=NaN(1,numcells);

for i=1:Num_files
    file_name=sorted_files(i).name;
    % load `.mat` file
    load(strcat(directory,file_name));
    life_history=length(CellA);
    
    %store length and orientation of cell
    cell_length=[];
    
    for j=1:life_history
        cell_length(end+1)=CellA{1,j}.cellLength(1);
        %degree
        %cell_orientation(end+1)=CellA{1,j}.coord.orientation;
    end
    %mean length
    meanLength=mean(cell_length);
    %average velocity
    first_frame = birth;
    last_frame = min(birth + length(CellA)-1,num_time_steps);
    if first_frame == last_frame
        AverageVelocity(ID)=NaN;
        AverageLength(ID)=NaN;         
    else
        x_x1 = CellA{1,1}.coord.r_center(1)-crop_box_array{1, 1}(first_frame,2);
        y_x1 = CellA{1,1}.coord.r_center(1)-crop_box_array{1, 1}(first_frame,1);
        x1=sqrt(x_x1^2+y_x1^2);

        x_x2 = CellA{1,last_frame-first_frame+1}.coord.r_center(1)-crop_box_array{1, 1}(last_frame,2);
        y_x2 = CellA{1,last_frame-first_frame+1}.coord.r_center(2)-crop_box_array{1, 1}(last_frame,1);
        x2=sqrt(x_x2^2+y_x2^2);

        AverageVelocityValue=(x2-x1)/(life_history*intervalTime);
        AverageVelocity(ID)=AverageVelocityValue;
        AverageLength(ID)=meanLength;        
    end
end
