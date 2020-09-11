clear all
clc
%%Get information about what's inside your Repo.
% %Specify where all your data is saved
Root_dir='D:/itl2/Documents/GitHub/matl-db/Non-charring/PMMA/';
PMMA_Repo = dir(fullfile(Root_dir,'**/*.*','*.csv'));   %get list of files and folders in any subfolder | fullfile gives you the full file location; **\*.* looks through all subfolders; '*.csv' only reads in .csv files

% % same dir command using different OS-specific file separators (/ \ :)
% if ismac
%     PMMA_Repo = dir(fullfile(Root_dir,'**:*.*','*.csv'));   
% elseif ispc
%     PMMA_Repo = dir(fullfile(Root_dir,'**\*.*','*.csv'));   %get list of files and folders in any subfolder | fullfile gives you the full file location; **\*.* looks through all subfolders; '*.csv' only reads in .csv files
% elseif isunix
%     PMMA_Repo = dir(fullfile(Root_dir,'**/*.*','*.csv'));  
% end

PMMA_Repo = PMMA_Repo(~[PMMA_Repo.isdir]);      %remove folders from list
%Get the filenames and folders of all files and folders inside your Root Directory
filenames={PMMA_Repo(:).name}';
filefolders={PMMA_Repo(:).folder}';

% %Get only those files that have a csv extension and their corresponding
% folders. [note, this 'endsWith' is case sensitive]
% csvfiles=filenames(endsWith(filenames,'.csv'));
% csvfolders=filefolders(endsWith(filenames,'.csv'));

%Make a cell array of strings containing the full file locations of the files.
files=fullfile(filefolders,filenames);
N_files=size(files,1);
% files=fullfile(csvfolders,csvfiles);

% Learn the names of each folder (lab institution) in your Repo
temp=struct2table(dir(Root_dir));
LabNames=table2array(temp(4:end,1));
% Create corresponding list of anonymous names for each institution
QMJHL={'Baie-Comeau' 'Blainville-Boisbriand' 'Cape-Breton' 'Charlottetown' 'Chicoutimi' 'Drummondville'...
    'Gatineau' 'Halifax' 'Moncton' 'Quebec' 'Rimouski' 'Rouyn-Noranda' 'Saint John' 'Shawinigan'...
    'Sherbrooke'  'Val dOr' 'Victoriaville'}';
% Create corresponding list of colors for each dataset submitted by a given institution
Colors={'Black' 'Gray' 'Red' 'OrangeRed' 'Gold' 'Green' 'Blue' 'DarkViolet' 'DeepSkyBlue' ...
    'Indigo' 'Lime' 'Navy' 'DeepPink' 'DarkRed' 'Cyan' 'Magenta' 'Khaki'}';
clear temp
N_Labs=size(LabNames,1);
Asurf=csvread('Asurf.txt');  % Note: DBI/LUND (LabNames{2}) has two different sample areas for CONE data (here atleast, HRR data is already normalized as [kW/m2])

%Define Types of Experimental data
Test_types={'CAPA_25kW';'CAPA_60kW';...
            'Cone_25kW';'Cone_50kW'; 'Cone_65kW';...
            'DSC_N2_1K';'DSC_N2_2K';'DSC_N2_3K';'DSC_N2_5K';'DSC_N2_10K';'DSC_N2_20K';...
            'DSC_O2-10_10K';'DSC_O2-21_10K';'DSC_Ar_1K'; 'DSC_Ar_10K'; 'DSC_Ar_50K';...
            'FPA_25kW';'FPA_50kW';'FPA_65kW';...
            'Gasification_25kW';'Gasification_50kW';'Gasification_65kW';...
            'MCC_N2_60K';...
            'TGA_N2_1K';'TGA_N2_2K';'TGA_N2_2-5K';'TGA_N2_5K';'TGA_N2_10K';'TGA_N2_15K';'TGA_N2_20K';'TGA_N2_50K';'TGA_N2_100K';...
            'TGA_O2-10_10K';'TGA_O2-21_10K'; 'TGA_Ar_1K'; 'TGA_Ar_10K'; 'TGA_Ar_50K'};
N_test_types=size(Test_types,1); 
%Initialize a counter to track the number of each test types submitted by each lab in the PMMA_Repo
Test_count=zeros(N_test_types,N_Labs+1);

% Read in all of your data  EXP_DATA is a 3D cell array of indexing {LabName, Test #, Test Type}   
% Inside of each cell is a 2D array of indexing [timestep, data type]
% Also, indexd the cell array files to now include 
% files = {filepath | Index_Test_type | Index_LabName | Index_Test_Count}
for i = 1:N_files % loop through all of your data sets
    for m=1:N_test_types 
        if contains(filenames{i},Test_types{m})==1      % [does the file name contain (name of test of interest) 
            Test_count(m,end)=Test_count(m,end)+1;      % if so, save it to that index counter
            files{i,2}=m;
            for k=1:N_Labs
                if contains(filenames{i},LabNames{k})==1    % [does the file name contain (name of lab of interest) %initialize a new counter 
                    files{i,3}=k;
                    Test_count(m,k)=Test_count(m,k)+1;  % if so, save it to a lab-specific index counter
                    EXP_DATA{k,(Test_count(m,k)),m}=csvread(files{i},3);
                    files{i,4}=Test_count(m,k);
                end
                
                                                           
            end
        end
    end
end

save EXP_DATA.mat

% filelist = dir(fullfile(rootdir, '**\*.*'));  %get list of files and folders in any subfolder
% filelist = filelist(~[filelist.isdir]);  %remove folders from list

