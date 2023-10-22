function [] = FAST_Num_cells(FAST_output_path, write_directory)
%FAST_Num_cells Counts and records the number of cells at each time step.
%
% This function determines the number of bacterial cells present at each time step 
% from the provided SS output data. It then writes these counts to a CSV file.
%
% Inputs:
%   FAST_output_path: Directory path where the SS output data is located.
%   write_directory: Directory path where the results should be written.

% Load the cell features data from the given directory
load(strcat(FAST_output_path, '/CellFeatures.mat'), 'trackableData');

% Determine the number of time steps present in the data
Number_of_timesteps = size(trackableData.Centroid, 1);
number_of_cells_in_each_timesteps = zeros(1, Number_of_timesteps);

% Loop through each time step and count the number of cells present
for j = 1 : Number_of_timesteps
    number_of_cells = size(trackableData.Centroid{j, 1}, 1);
    number_of_cells_in_each_timesteps(j) = number_of_cells;
end  

% Organize the cell count data into a table for better representation
T2 = table(transpose(1:length(number_of_cells_in_each_timesteps)), transpose(number_of_cells_in_each_timesteps));
% Set the table column names
T2.Properties.VariableNames = {'StepNumber', 'NumberOfCells'};

% Save the table data to a CSV file in the specified directory
writetable(T2, strcat(write_directory, '/FAST_Num_cells_in_each_timeStep.csv'),...
    'Delimiter', ',', 'QuoteStrings', true);

end
