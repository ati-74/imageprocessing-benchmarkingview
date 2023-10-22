% Rename raw image files to use as input for SuperSegger

% Define the directory path where the raw files are stored
directory = 'baby20/raw/';
% Define the directory path where the output files will be stored
output_dir = 'baby20/SuperSegger';

% Find all .tif files in the specified directory
files = dir([strcat(directory, '/*.tif')]);

% Sort the files in natural order (e.g., img1, img2,..., img10, img11,...)
sorted_files = natsortfiles(files);

% Calculate the total number of files
Num_files = length(sorted_files);

% Loop through each file
for i = 1:Num_files
    % Get the name of the file
    file_name = sorted_files(i).name;

    % Read the image from the file
    raw_img = imread(strcat(directory, file_name));

    % Determine the number of digits in the file index
    num_digit = numel(num2str(i));

    % Generate the output image name based on the file index
    if num_digit == 1
        img_name = strcat(output_dir, '/baby20_t00', int2str(i), 'xy1c1.tif');
    elseif num_digit == 2
        img_name = strcat(output_dir, '/baby20_t0', int2str(i), 'xy1c1.tif');
    else
        img_name = strcat(output_dir, '/baby20_t', int2str(i), 'xy1c1.tif');
    end

    % Write the image to the specified output directory with the generated name
    imwrite(raw_img, img_name);
end
