
datasets = ["E.coli_mono_agarose_skipTimeSteps","E.coli_chamber","E.coli_mono_agarose",...
    "E.coli_mono_agarose_noisy","Pseudomonas_agarose","Pseudomonas_chamber",...
"SuperSegger sample images set","Xanthomonase_agarose","Xanthomonase_chamber"];

modes = ["1. Raw Images","2. Ilastik Output"];

interval_time = [15 1.5 1.5 1.5 1.5 1.5 1 1.5 1.5];

num_timesteps = [12 314 112 112 176 156 60 279 203];

num_datasets = length(datasets);
num_modes = length(modes);

for i=1:num_datasets
    for j=1:num_modes
       dataset = datasets (i);
       dataset
       mode = modes (j);
       mode
       if mode == '2. Ilastik Output'
               if dataset ~= 'E.coli_mono_agarose_noisy' && dataset ~= "E.coli_chamber"
                    ExtractCellFeatures(dataset,mode)
               end
       else
           if dataset ~= 'E.coli_mono_agarose_skipTimeSteps'
               ExtractCellFeatures(dataset,mode)
           end
       end       
       
    end
end
