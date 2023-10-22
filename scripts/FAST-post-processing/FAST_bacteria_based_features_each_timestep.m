function [AverageLength, AverageVelocity, AverageOrientation] = FAST_bacteria_based_features_each_timestep(FAST_output_directory, write_directory, bac_label, intervalTime)
%FAST_bacteria_based_features_each_timestep Extracts features for bacteria at each timestep.
%
% This function calculates and extracts various features of bacterial cells 
% at each time step from the FAST output. Features include length, velocity, 
% and orientation among others. The results are then written to a CSV file.
%
% Inputs:
%   FAST_output_directory: Directory containing the FAST output.
%   write_directory: Directory where results will be written.
%   bac_label: Label assigned to each bacterium.
%   intervalTime: Time interval between frames.
%
% Outputs:
%   AverageLength: Average length of bacteria over their lifespan.
%   AverageVelocity: Average velocity of bacteria.
%   AverageOrientation: Average orientation of bacteria.

% Load necessary data
load(strcat(FAST_output_directory,'/Tracks.mat'),'procTracks');
load(strcat(FAST_output_directory,'/Metadata.mat'), 'metaStore');

% Initialize arrays for storing various bacterial properties
% number of time steps
num_time_steps = max([procTracks(:).end]);
number_of_bacteria = size(procTracks, 2);

TimeStep_of_bacteria = zeros(1, sum([procTracks(:).length]));
cell_life_id_value = zeros(1, sum([procTracks(:).length]));
orientation =  zeros(1, sum([procTracks(:).length]));
Center_X = zeros(1, sum([procTracks(:).length]));
Center_Y =  zeros(1, sum([procTracks(:).length]));
major_axis = zeros(1, sum([procTracks(:).length]));
minor_axis = zeros(1, sum([procTracks(:).length]));
bacteria_label = zeros(1, sum([procTracks(:).length]));
% tracking information
parent = zeros(1, sum([procTracks(:).length]));
daughter1 = zeros(1, sum([procTracks(:).length]));
daughter2 = zeros(1, sum([procTracks(:).length]));

% average length of bacteria during its life history
AverageLength = NaN(1, number_of_bacteria);
% average velocity of bacteria
AverageVelocity = NaN(1, number_of_bacteria);
AverageOrientation = NaN(1, number_of_bacteria);

% cell index in all matrices
cell_index = 1;

% Process each bacterial track
for i = 1:number_of_bacteria
    
    life_history = procTracks(i).length;
    
    for j=1:life_history
        living_time_step = procTracks(i).times(j);
        % bacterium time step
        TimeStep_of_bacteria(cell_index)= living_time_step;
        cell_life_id_value(cell_index) = i;
        % each bacteria_label matrix cell shows the label of bacteria corresponding to one cell.mat file 
        bacteria_label(cell_index) = bac_label(i);
        if metaStore.dx ~= 0.5
            % center coordinate
            Center_X(cell_index) = procTracks(i).x(j) / (metaStore.dx * 2);
            Center_Y(cell_index) = procTracks(i).y(j) / (metaStore.dy * 2);
            % minor and major axis length
            major_axis(cell_index) = procTracks(i).majorLen(j) / (metaStore.dx * 2);
            minor_axis(cell_index) = procTracks(i).minorLen(j) / (metaStore.dy * 2);
        else
             % center coordinate
            Center_X(cell_index) = procTracks(i).x(j);
            Center_Y(cell_index) = procTracks(i).y(j);
            % minor and major axis length
            major_axis(cell_index) = procTracks(i).majorLen(j);
            minor_axis(cell_index) = procTracks(i).minorLen(j);           
        end
        % orientation (radian)
        orientation(cell_index) = procTracks(i).phi(j) * pi / -180;
        % tracking information
        if isempty(procTracks(i).M)
            parent(cell_index) = 0;
        else
            parent(cell_index) = procTracks(i).M;
        end
        if isempty(procTracks(i).D1)
            daughter1(cell_index) = 0;
        else
            daughter1(cell_index) = procTracks(i).D1;
        end
        if isempty(procTracks(i).D2)
            daughter2(cell_index) = 0;
        else
            daughter2(cell_index) = procTracks(i).D2;
        end
        cell_index = cell_index + 1;
        % cell length of bacteria during its life history
    end
    
    first_frame = procTracks(i).times(1);
    % last time step of bacterium life
    last_frame = procTracks(i).times(end);
    
    if life_history > 1
        if metaStore.dx ~= 0.5
            mean_length_of_bacterium = mean([procTracks(i).majorLen] / (metaStore.dx * 2) );
        else
           mean_length_of_bacterium = mean([procTracks(i).majorLen]);
        end
        AverageOrientationValue = mean([procTracks(i).phi] * pi / -180);
        
        % calculate velocity
        if metaStore.dx ~= 0.5
            x_x1 = procTracks(i).x(1)  / (metaStore.dx * 2);
            y_x1 = procTracks(i).y(1)  / (metaStore.dy * 2);

            x_x2 = procTracks(i).x(end)  / (metaStore.dx * 2);
            y_x2 = procTracks(i).y(end)  / (metaStore.dy * 2);            
            
        else
            x_x1 = procTracks(i).x(1);
            y_x1 = procTracks(i).y(1);

            x_x2 = procTracks(i).x(end);
            y_x2 = procTracks(i).y(end);
            
        end
        
        x1 = sqrt(x_x1^2 + y_x1^2);       
        x2 = sqrt(x_x2^2 + y_x2^2);
        AverageVelocityValue= (x2-x1) / (life_history * intervalTime);
        
    else
        mean_length_of_bacterium = NaN;
        AverageVelocityValue = NaN;
        AverageOrientationValue = NaN;
    end
    AverageLength(i) = mean_length_of_bacterium;
    AverageVelocity(i) = AverageVelocityValue;
    AverageOrientation(i) = AverageOrientationValue;
end

%add to sorted table
T = sortrows(table(transpose(TimeStep_of_bacteria), transpose(cell_life_id_value), transpose(bacteria_label),...
    transpose(orientation), transpose(Center_X), transpose(Center_Y), transpose(major_axis),...
    transpose(minor_axis), transpose(parent), transpose(daughter1), transpose(daughter2)));
%add column name
T.Properties.VariableNames={'TimeStep', 'CellLifeId', 'label', 'Orientation', 'Center_X', 'Center_Y', ...
    'Major_axis', 'Minor_axis', 'parent','daughter1', 'daughter2'};

% write to csv
%life history based features
writetable(T,strcat(write_directory, '/FAST_bacteria_feature_analysis.csv'), ...
    'Delimiter', ',', 'QuoteStrings', true);

