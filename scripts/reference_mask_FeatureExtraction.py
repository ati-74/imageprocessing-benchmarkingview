import numpy as np
import pandas as pd
import cv2
import os


def coords_to_mask(coords, shape):
    """
    Converts given coordinates to a binary mask of specified shape.

    @param coords list of lists A list containing two lists - the x and y coordinates.
    @param shape tuple The desired shape of the mask, given as (height, width).

    Returns:
    mask np.array: A binary mask of given shape where specified coordinates are set to 255.
    """

    mask = np.zeros(shape, dtype=np.uint8)
    mask[coords[1], coords[0]] = 255
    return mask


def compute_iou(mask1, mask2):
    """
    Computes the Intersection over Union (IoU) between two binary masks (useful for tracking).

    @param mask1 np.array The first binary mask.
    @param mask2 np.array The second binary mask.

    Returns:
    - float: The IoU value between the two masks. Returns 0 if the union is zero.
    """

    # Calculating the pixel-wise logical intersection of the two masks
    intersection = np.logical_and(mask1, mask2).sum()

    # Calculating the pixel-wise logical union of the two masks
    union = np.logical_or(mask1, mask2).sum()

    # Returning the IoU
    return intersection / union if union != 0 else 0


def find_objects(values_dict, max_y, max_x):
    """
    Extracts object properties based on the provided dictionary of values
    and returns them in a pandas dataframe.

    @param values_dict dict A dictionary containing information about objects and their coordinates.
    @param max_y int The maximum y-coordinate value.
    @param max_x int The maximum x-coordinate value.

    Returns:
    - properties_df DataFrame containing properties of objects like orientation, center coordinates,
                    major and minor axis lengths, and more.
    """

    # Create an empty dataframe to store object properties.
    columns = ['TimeStep', 'ObjectNumber', 'Orientation', 'label', 'Center_X', 'Center_Y',
               'Major_axis', 'Minor_axis', 'ParentImageNumber', 'ParentObjectNumber']
    properties_df = pd.DataFrame(columns=columns)

    # Extract the list of time steps.
    time_steps_list = range(1, int(values_dict['interval'].split('],')[1].split(',')[-1]) + 2)

    all_masks = []

    for time_step in [time_steps_list[-1]]:
        print('time step:' + str(time_step))

        # Dictionary to store object coordinates for this timestep.
        coords_list_labels_dict = {}
        temp_masks = []

        # Extracting coordinates for each label.
        for label, coords_str in values_dict['labels'].items():
            x_coords, y_coords = [], []
            for coord_str in coords_str.split(']'):
                coord_str = coord_str.replace('[', '').strip()
                if coord_str:
                    x, y, t = map(int, [v for v in coord_str.split(',') if v != ''])
                    if t == time_step - 1:
                        x_coords.append(x)
                        y_coords.append(y)
            # Filters for removing objects with less than 5 points and on the image borders.
            if len(x_coords) > 4 and 0 not in x_coords and max_x not in x_coords and 0 not in y_coords and \
                    max_y not in y_coords:
                coords_list_labels_dict[label] = [x_coords, y_coords]
            else:
                print(x_coords)

        for label_name, coords in coords_list_labels_dict.items():
            # Convert coordinates to mask.
            current_mask = coords_to_mask(coords, (max_y + 1, max_x + 1))

            # Finding contours for the object mask.
            contours, _ = cv2.findContours(current_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filtering out small contours.
            min_contour_area = 10
            contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

            if len(contours) == 0 or len(contours[0]) < 5:
                # Log the properties of contours which are skipped.
                try:
                    print(len(contours))
                    print(len(contours[0]))
                    print(coords)
                    print(len(coords[0]))
                except:
                    print(len(contours))
                print('warning 1')
                continue
            else:
                temp_masks.append((current_mask, label_name))

            # Compute properties from the contour.
            ellipse = cv2.fitEllipse(contours[0])
            center_x, center_y = ellipse[0]
            major_axis = max(ellipse[1])
            minor_axis = min(ellipse[1])
            orientation = (ellipse[2] + 90) * np.pi / 180

            # Default values for parent image and object number.
            ParentImageNumber, ParentObjectNumber = 0, 0

            # Track objects based on overlap with previous time step.
            if time_step > 1:
                previous_masks_with_labels = all_masks[time_step - 2]
                ious = [compute_iou(current_mask, prev_mask[0]) for prev_mask in previous_masks_with_labels]
                max_iou_index = np.argmax(ious)

                if ious[max_iou_index] > 0:
                    ParentImageNumber = time_step - 1
                    ParentObjectNumber = int(previous_masks_with_labels[max_iou_index][1].split('Label ')[1])

            # Add the properties to the dataframe.
            new_row = {
                'TimeStep': time_step,
                'ObjectNumber': int(label_name.split('Label ')[1]),
                'Orientation': orientation,
                'label': 0,
                'Center_X': center_x,
                'Center_Y': center_y,
                'Major_axis': major_axis,
                'Minor_axis': minor_axis,
                'ParentImageNumber': ParentImageNumber,
                'ParentObjectNumber': ParentObjectNumber
            }
            properties_df = pd.concat([properties_df, pd.DataFrame([new_row])], ignore_index=True)

        all_masks.append(temp_masks)

    return properties_df


if __name__ == '__main__':

    # Define the path to the labeling file.
    label_file = 'EcoliK12.T000.labeling'

    # Read the labeling file.
    with open(label_file, 'r') as file:
        content = file.read()

    # Define keys for the dictionary to store extracted values.
    keys = ['interval', 'pixelSizes', 'labels', 'colors']

    # Parse content to extract 'interval' and 'pixelSizes'.
    values_dict = {
        'interval': content.split('interval')[1].split('pixelSizes')[0].replace('"', '').replace('{', '').replace('}',
                                                                                                                  '').strip(),
        'pixelSizes': content.split('pixelSizes')[1].split('labels')[0].replace('"', '').replace('[', '').replace(']',
                                                                                                                  '').strip()
    }

    # Extract labels and their corresponding coordinates.
    coordinates = content.split('labels')[1].split('colors')[0][3:-3]
    labels_coordinate_dict = {}
    for val in coordinates.split('"'):
        if val != '':
            if val.count('Label') > 0:
                current_label = val
            else:
                labels_coordinate_dict[current_label] = val[2:-2]

    values_dict['labels'] = labels_coordinate_dict

    # Parse interval to get the min and max values of x, y, and time steps.
    min_x, min_y, first_time_step = [int(v) for v in
                                     values_dict['interval'].split('min:')[1].split(',max')[0].replace(']', '').replace(
                                         '[', '').split(',')]
    max_x, max_y, last_time_step = [int(v) for v in
                                    values_dict['interval'].split('max:')[1].split(',n')[0].replace(']', '').replace(
                                        '[', '').split(',')]

    # Extract the list of time steps.
    max_time_step = int(values_dict['interval'].split('],')[1].split(',')[-1]) + 1
    time_steps_list = [i for i in range(1, max_time_step + 1)]
    num_digit = len(str(time_steps_list[-1]))

    # Call the function to extract object properties.
    properties_df = find_objects(values_dict, max_y, max_x)

    # Save the extracted properties to a CSV file.
    output_path = os.path.join(os.path.dirname(label_file), 'ref_mask_bacteria_feature_analysis.csv')
    properties_df.to_csv(output_path, index=False)
