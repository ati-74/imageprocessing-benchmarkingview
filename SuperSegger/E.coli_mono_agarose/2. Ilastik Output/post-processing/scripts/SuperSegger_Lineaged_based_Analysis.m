
load('../../xy1/clist.mat','data');

mat_size = size(data);
cellNumber=mat_size(1);
lable=[];
last_lable_value=0;
num_division = [];
lable_for_final_table = [];
cell_id = [];

for i=1:cellNumber
    cell_id (end + 1) = data(i,1);
    if data(i,61)==0
        last_lable_value=last_lable_value+1;
        lable_value=last_lable_value;
    else
        parent_id=data(i,61);
        lable_indx = find(cell_id==parent_id);
        lable_value=lable(lable_indx);
    end
    %save Results
    %append to list
    lable(end+1)=lable_value;
    
end

%add to table
T = table(data(:,1),transpose(lable),data(:,61));
%add column name
% ,'NumberOfDivision'
T.Properties.VariableNames={'Cell_id','Cell_lable','mother_id'};

unique_lable = unique(lable);
for element_indx = 1 : length(unique_lable)
    
    Table = T(T.Cell_lable == unique_lable(element_indx), :);
    num_division_val = length(unique(Table.mother_id))-1;
    num_division (end + 1) = num_division_val;
    lable_for_final_table (end+1) = unique_lable(element_indx);
end

%add to table
T2 = table(transpose(lable_for_final_table),transpose(num_division));
%add column name
T2.Properties.VariableNames={'Cell_lable','NumberOfDivision'};

% write to csv
writetable(T2,'../results/SuperSegger_Lineage_based_Analysis.csv','Delimiter',',','QuoteStrings',true)
