clear all
close all

load EXP_DATA.mat% This uses the related script 'Import_Data.m'

% QMJHL={'Baie-Comeau' 'Blainville-Boisbriand' 'Cape-Breton' 'Charlottetown' 'Chicoutimi' 'Drummondville'...
%     'Gatineau' 'Halifax' 'Moncton' 'Quebec' 'Rimouski' 'Rouyn-Noranda' 'Saint_John' 'Shawinigan'...
%     'Sherbrooke'  'Val-dOr' 'Victoriaville'}';


%% Information about the size of your datasets
N_files;    %total number of experiments
N_Labs;     %total number of labs
N_test_types;%number of different types of experiments
N_rows_i=zeros(184,1);
N_rows_all=NaN*ones(N_Labs,max(max(Test_count(:,1:end-1))),N_test_types);    %Initialize a matrix to hold the number of rows (e.g., timesteps) in each dataset
EVAL_DATA=cell(N_Labs,max(max(Test_count(:,1:(end-1)))),N_test_types);      %Initialize your cell array to hold (N_labs, N_repeat_exps
TAB_DATA=cell(N_test_types,5);                                              %Tabulated data of discrete values (e.g., t_ignition, heat of combustion, Peak HRR) # discrete values =5 (i.e., we can define up to 5 Tab values for each test type
% Recall, you have the following Types of Experimental data
% Test_types={'CAPA_25kW';'CAPA_60kW';...
%             'Cone_25kW';'Cone_50kW'; 'Cone_65kW';...
%             'DSC_N2_1K';'DSC_N2_2K';'DSC_N2_3K';'DSC_N2_5K';'DSC_N2_10K';'DSC_N2_20K';...
%             'DSC_O2-10_10K';'DSC_O2-21_10K';'DSC_Ar_1K'; 'DSC_Ar_10K'; 'DSC_Ar_50K';...
%             'FPA_25kW';'FPA_50kW';'FPA_65kW';...
%             'Gasification_25kW';'Gasification_50kW';'Gasification_65kW';...
%             'MCC_N2_60K';...
%             'TGA_N2_1K';'TGA_N2_2K';'TGA_N2_2.5K';'TGA_N2_5K';'TGA_N2_10K';'TGA_N2_15K';'TGA_N2_20K';'TGA_N2_50K';'TGA_N2_100K';...
%             'TGA_O2-10_10K';'TGA_O2-21_10K'; 'TGA_Ar_1K'; 'TGA_Ar_10K'; 'TGA_Ar_50K'};

%% CREATE EVAL_DATA, smooth Mass, calculate dm/dt
%Read in all of your data  EXP_DATA is a 3D cell array of indexing {LabName,k | Test #, L | Test Type,m}
%Inside of each cell is a 2D array of indexing [timestep, data type]

% Create EVAL_DATA= [ t | T | heat flow | Total Heat flow | dT/dt] (all values interpolated to 0.5 K intervals)
figure
for i =1:N_files   % Loop through all of your data sets
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m>=6 && m<=16        % Just DSC Tests

        T_start=ceil(min(EXP_DATA{k,L,m}(:,2)));            %find first timestep (rounded to nearest integer)
        T_end=floor(max(EXP_DATA{k,L,m}(:,2)));             %find last timestep (rounded to nearest integer)
        delta_T=0.5;
        EVAL_DATA{k,L,m}(:,2)=[T_start:delta_T:T_end-1]';   % generate uniform T from Tmin to Tmin at 0.5K intervals
%Thursday AM
        [T,sortidx_T]=unique(EXP_DATA{k,L,m}(:,2));         % Find all of your unique Temps
        T_idx=[T sortidx_T];
        T_idx=sortrows(T_idx,'ascend');
        heatflow=EXP_DATA{k,L,m}(:,3);
        heatflow=heatflow(sortidx_T);                       % Find all of the heatflow values asssociated with these unique temperatures
        time=EXP_DATA{k,L,m}(:,1);
        time=time(sortidx_T);
        EVAL_DATA{k,L,m}(:,1)=interp1(T,time,EVAL_DATA{k,L,m}(:,2));         % interpolate time (to T)
        EVAL_DATA{k,L,m}(:,3)=interp1(T,heatflow,EVAL_DATA{k,L,m}(:,2));     % interpolate masses (to T)
%         x_eval=EVAL_DATA{k,L,m};
%         x_exp=EXP_DATA{k,L,m};
        p_end=size(EVAL_DATA{k,L,m},1);
        for p=1:p_end                 %Calculate [4] total heat flow and [5] dT/dt (+/- one time step, delta_T=1k]
            if p==1
            EVAL_DATA{k,L,m}(p,5)=0;
            EVAL_DATA{k,L,m}(p,4)=0;
            elseif p<p_end
            EVAL_DATA{k,L,m}(p,5)=(EVAL_DATA{k,L,m}(p-1,2)-EVAL_DATA{k,L,m}(p+1,2))/(EVAL_DATA{k,L,m}(p+1,1)-EVAL_DATA{k,L,m}(p-1,1));  %dT/dt
            EVAL_DATA{k,L,m}(p,4)=EVAL_DATA{k,L,m}(p-1,4)+0.5*(EVAL_DATA{k,L,m}(p-1,3)+EVAL_DATA{k,L,m}(p,3))*(EVAL_DATA{k,L,m}(p,1)-EVAL_DATA{k,L,m}(p-1,1));  %Integral heat flow
            else
            EVAL_DATA{k,L,m}(p,4)=EVAL_DATA{k,L,m}(p-1,4)+0.5*(EVAL_DATA{k,L,m}(p-1,3)+EVAL_DATA{k,L,m}(p,3))*(EVAL_DATA{k,L,m}(p,1)-EVAL_DATA{k,L,m}(p-1,1));  %Integral heat flow
            end
        end
        clear p_end

        clear time heatflow sortidx_T T_idx T_start T_end

        clf
        hold on
        yyaxis left
        ylabel('Normalized Heat Flow [W g^{-1}]');
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,3),'-','MarkerSize',2);   %Heat Flow
        axis([300 900 -inf inf]);

        yyaxis right
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,4),'r');      %Integral heat flow
        axis([300 900 -inf inf]);
        title(filenames{i}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        xlabel('Temperature [K]');
        ylabel('Integral Heat Flow [J g^{-1}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, filenames{i}(1:end-4)]));
        print(fig_filename,'-dpdf')
    end
end
close

%% Quick code to determine minimum temperature reported in ALL DSC datasets
min_T=300;  %initialize minimum temperature reported in TGA data
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m>=6 && m<=16        % Just DSC Tests
    temp=min(EVAL_DATA{k,L,m}(:,2));
    if temp>min_T
        min_T=temp;
    end
    if temp==0
        i
    end
    end
end
clear temp
%% Check: Why is min_T failing?
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m>=6 && m<=16 && k~=14       % Just DSC Tests // UMET data has unique /\/\/\ temperature program
        T_check(i,1)=min(EVAL_DATA{k,L,m}(:,2)); %min_T
        T_check(i,2)=max(EVAL_DATA{k,L,m}(:,2)); %max_T
        T_check(i,3)=k;
        T_check(i,4)=L;
        T_check(i,5)=m;
    end
end
save('T_check.mat','T_check')

%% Analyze Temperature-Resolved DSC heat flow Data
DSC_heatflow=NaN*ones(1021,max(max(Test_count(6:16,1:15)))+4,N_Labs,37);
DSC_int_heatflow=NaN*ones(1021,max(max(Test_count(6:16,1:15)))+4,N_Labs,37);
DSC_Temperature=[295:0.5:805]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m>=6 && m<=16 && k~=14       % Just DSC Tests // UMET data has unique /\/\/\ temperature program

        last = min(min(N_rows_all(k,:,m)-1,1021));

        max_T =max(EVAL_DATA{k,L,m}(:,2));
        max_T_idx=min((max_T-295)*2+1,1021);    %we pull in all data up to 1021 rows of data (~up to 800K)

        min_T=min(EVAL_DATA{k,L,m}(:,2));
        min_T_idx=(min_T-295)*2+1;

%         DSC_Mass//DSC_MLR(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 1021 rows/timesteps of Mass and MLR data
            DSC_int_heatflow(min_T_idx:max_T_idx,L,k,m)=EVAL_DATA{k,L,m}(1:(max_T_idx+1-min_T_idx),4);
            DSC_heatflow(min_T_idx:max_T_idx,L,k,m)=EVAL_DATA{k,L,m}(1:(max_T_idx+1-min_T_idx),3);

        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp_MLR=DSC_heatflow(:,:,k,m);
            temp_MLR(temp_MLR==0)=NaN;
            DSC_heatflow(1:last,:,k,m)=temp_MLR;

            temp_Mass=DSC_int_heatflow(:,:,k,m);
            temp_Mass(temp_Mass==0)=NaN;
            DSC_int_heatflow(1:last,:,k,m)=temp_Mass;

            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
                DSC_heatflow(ix,5,k,m)=nnz(DSC_heatflow((ix-2:ix+2),(1:L),k,m));
                DSC_heatflow(ix,6,k,m)=mean_nonan(DSC_heatflow((ix-2:ix+2),(1:L),k,m));
                DSC_heatflow(ix,7,k,m)=std_nonan(DSC_heatflow((ix-2:ix+2),(1:L),k,m));
                DSC_heatflow(ix,8,k,m)=DSC_heatflow(ix,7,k,m)/sqrt(DSC_heatflow(ix,5,k,m));

                DSC_int_heatflow(ix,5,k,m)=nnz(DSC_int_heatflow((ix-2:ix+2),(1:L),k,m));
                DSC_int_heatflow(ix,6,k,m)=mean_nonan(DSC_int_heatflow((ix-2:ix+2),(1:L),k,m));
                DSC_int_heatflow(ix,7,k,m)=std_nonan(DSC_int_heatflow((ix-2:ix+2),(1:L),k,m));
                DSC_int_heatflow(ix,8,k,m)=DSC_int_heatflow(ix,7,k,m)/sqrt(DSC_int_heatflow(ix,5,k,m));
            end
%             HRR25(1:last,L+2,k)=sgolayfilt(HRR25(1:last,L+2,k),3,15);,
            clear temp_MLR temp_Mass

            if k==13    % plot UMD with their own error bars
                shadedErrorBar(EXP_DATA{k,L,m}(:,2),EXP_DATA{k,L,m}(:,3),[EXP_DATA{k,L,m}(:,4) EXP_DATA{k,L,m}(:,4)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
                axis([300 800 -inf inf]);
                title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
                xlabel('Temperature [K]');
                ylabel('Heat Flow [W g^{-1}]');
                clear ix
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{m} '_heatflow_avg']));
            print(fig_filename,'-dpdf')
                clf
            else    %plot everyone else's data with my errorbars
                hold on
                for ix=1:L
                    plot(DSC_Temperature(1:last),DSC_heatflow(1:last,ix,k,m),'.','MarkerSize',3);
                end
                shadedErrorBar(DSC_Temperature(1:last),DSC_heatflow(1:last,6,k,m),[2*DSC_heatflow(1:last,8,k,m) 2*DSC_heatflow(1:last,8,k,m)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
                axis([300 800 -inf inf]);
                title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
                xlabel('Temperature [K]');
                ylabel('Heat Flow [W g^{-1}]');
                clear ix
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{m} '_heatflow_avg']));
            print(fig_filename,'-dpdf')
                clf
            end

            hold on
            for ix=1:L
                plot(DSC_Temperature(1:last),DSC_int_heatflow(1:last,ix,k,m),'.','MarkerSize',3);
            end
            shadedErrorBar(DSC_Temperature(1:last),DSC_int_heatflow(1:last,6,k,m),[2*DSC_int_heatflow(1:last,8,k,m) 2*DSC_int_heatflow(1:last,8,k,m)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            axis([300 800 -inf inf]);
            title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            ylabel('Integral Heat Flow [J g^{-1}]');
            clear ix
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{m} '_int_heatflow_avg']));
            print(fig_filename,'-dpdf')
            clf
        end
    end
    clear min_T last fig_filename
end
clear last
close all


%% Estimate Heat of Reaction for STA tests in N2 or Argon

% ----------- TGA DATA = Determine dm+rxn = Mass loss around peak reaction ---------

%Read in all of your data  EXP_DATA is a 3D cell array of indexing {LabName,k | Test #, L | Test Type,m}
%Inside of each cell is a 2D array of indexing [timestep, data type]
% Create EVAL_DATA= [ t | T | m/m0_smoothed | dm*/dt | dT/dt] (all values interpolated to 0.5 K intervals)
figure
for i =1:N_files   % Loop through all of your data sets
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m== 28 | m== 30| m>=35
        T_start=ceil(min(EXP_DATA{k,L,m}(:,2)));   %find first timestep (rounded to nearest integer)
        T_end=floor(max(EXP_DATA{k,L,m}(:,2)));     %find last timestep (rounded to nearest integer)
        m0=mean(EXP_DATA{k,L,m}(1:5,3));            % define m0 as average m from first five timesteps
        delta_T=0.5;
        EVAL_DATA{k,L,m}(:,2)=[T_start:delta_T:T_end-1]';                   % generate uniform T from Tmin to Tmin at 0.5K intervals
%Thursday AM
        [T,sortidx_T]=unique(EXP_DATA{k,L,m}(:,2));    % Find all of your unique Temps
        T_idx=[T sortidx_T];
        T_idx=sortrows(T_idx,'ascend');
        mass=EXP_DATA{k,L,m}(:,3);
        mass=mass(sortidx_T);                                          % Find all of the masses asssociated with these unique temperatures
        time=EXP_DATA{k,L,m}(:,1);
        time=time(sortidx_T);
        EVAL_DATA{k,L,m}(:,1)=interp1(T,time,EVAL_DATA{k,L,m}(:,2));        % interpolate time (to T)
        EVAL_DATA{k,L,m}(:,3)=(1/m0)*interp1(T,mass,EVAL_DATA{k,L,m}(:,2));        % interpolate masses (to T)
%         x_eval=EVAL_DATA{k,L,m};
%         x_exp=EXP_DATA{k,L,m};
         for p=1:size(EVAL_DATA{k,L,m},1)-1
            if p==1
            EVAL_DATA{k,L,m}(p,4)=0;
            EVAL_DATA{k,L,m}(p,5)=0;
            else
            EVAL_DATA{k,L,m}(p,4)=(EVAL_DATA{k,L,m}(p-1,3)-EVAL_DATA{k,L,m}(p+1,3))/(EVAL_DATA{k,L,m}(p+1,1)-EVAL_DATA{k,L,m}(p-1,1));
            EVAL_DATA{k,L,m}(p,5)=60*(EVAL_DATA{k,L,m}(p+1,2)-EVAL_DATA{k,L,m}(p-1,2))/(EVAL_DATA{k,L,m}(p+1,1)-EVAL_DATA{k,L,m}(p-1,1));
            end
        end

        clear time mass sortidx_T T_idx T_start T_end

% smooth dm*/dt with a svgolayfilter
        frames=31;
        order=3;
        EVAL_DATA{k,L,m}(:,3)=sgolayfilt(EVAL_DATA{k,L,m}(:,3),order,frames);

        for p=1:size(EVAL_DATA{k,L,m},1)-1
            if p==1
            EVAL_DATA{k,L,m}(p,4)=0;
            else
            EVAL_DATA{k,L,m}(p,4)=(EVAL_DATA{k,L,m}(p-1,3)-EVAL_DATA{k,L,m}(p+1,3))/(EVAL_DATA{k,L,m}(p+1,1)-EVAL_DATA{k,L,m}(p-1,1));
            end
        end

        TAB_DATA{m,1}(k,L)=max(EVAL_DATA{k,L,m}(:,4));%            %Calculate dm/dt max maximum dm/dt [g/g-s]
        T_max=find((EVAL_DATA{k,L,m}(:,4))==max(EVAL_DATA{k,L,m}(:,4)));
        T_onset=find((EVAL_DATA{k,L,m}(:,4))>0.1*max(EVAL_DATA{k,L,m}(:,4)),1);
        T_endset=find((EVAL_DATA{k,L,m}(:,4))>0.1*max(EVAL_DATA{k,L,m}(:,4)),1,'last');
        TAB_DATA{m,2}(k,L)=EVAL_DATA{k,L,m}(T_max,2);   %         %Calculate T_Max as the first Temperature when dm/dt = dm/dt max
        TAB_DATA{m,3}(k,L)=EVAL_DATA{k,L,m}(T_onset,2); %         %Calculate T_onset as the first Temperature when dm/dt > 0.1*dm/dt max
        TAB_DATA{m,4}(k,L)=EVAL_DATA{k,L,m}(T_endset,2);%         %Calculate T_endset as the first Temperature when dm/dt > 0.1*dm/dt max
        TAB_DATA{m,5}(k,L)=(EVAL_DATA{k,L,m}(T_onset,3)-EVAL_DATA{k,L,m}(T_endset,3));%         %Calculate dm_rxn [g/g]as the mass loss during between T_onset and T_endset
        clear T_max T_onset T_endset m0
    end

end

for i =1:N_files   % Loop through all of your data sets
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m== 10 && (k==5 || k==10 || k==13)   %N2_10K
        T_onset=TAB_DATA{28,3}(k,L);
        T_endset=TAB_DATA{28,4}(k,L);
        i_onset=find((EVAL_DATA{k,L,m}(:,2))==T_onset,1);
        i_endset=find((EVAL_DATA{k,L,m}(:,2))==T_endset,1,'last');
        baseline=0.5*(EVAL_DATA{k,L,m}(i_onset,3)+EVAL_DATA{k,L,m}(i_endset,3))*((EVAL_DATA{k,L,m}(i_endset,1)-EVAL_DATA{k,L,m}(i_onset,1)));
        int_heat_rxn=(EVAL_DATA{k,L,m}(i_endset,4)-EVAL_DATA{k,L,m}(i_onset,4));
        TAB_DATA{m,1}(k,L)=(int_heat_rxn-baseline)/TAB_DATA{28,5}(k,L);
        clear   T_onset  T_endset i_onset i_endset baseline int_heat_rxn

    elseif m== 11 && k==2   %N2_20K
        T_onset=TAB_DATA{30,3}(k,L);
        T_endset=TAB_DATA{30,4}(k,L);
        i_onset=find((EVAL_DATA{k,L,m}(:,2))==T_onset,1);
        i_endset=find((EVAL_DATA{k,L,m}(:,2))==T_endset,1,'last');
        baseline=0.5*(EVAL_DATA{k,L,m}(i_onset,3)+EVAL_DATA{k,L,m}(i_endset,3))*((EVAL_DATA{k,L,m}(i_endset,1)-EVAL_DATA{k,L,m}(i_onset,1)));
        int_heat_rxn=(EVAL_DATA{k,L,m}(i_endset,4)-EVAL_DATA{k,L,m}(i_onset,4));
        TAB_DATA{m,1}(k,L)=(int_heat_rxn-baseline)/TAB_DATA{30,5}(k,L);
        clear   T_onset  T_endset i_onset i_endset baseline int_heat_rxn

    elseif m>=14 && m<=16 && k==9   %Ar_1,10,50K
        T_onset=TAB_DATA{m+21,3}(k,L);
        T_endset=TAB_DATA{m+21,4}(k,L);
        i_onset=find((EVAL_DATA{k,L,m}(:,2))==T_onset,1);
        i_endset=find((EVAL_DATA{k,L,m}(:,2))==T_endset,1,'last');
        baseline=0.5*(EVAL_DATA{k,L,m}(i_onset,3)+EVAL_DATA{k,L,m}(i_endset,3))*((EVAL_DATA{k,L,m}(i_endset,1)-EVAL_DATA{k,L,m}(i_onset,1)));
        int_heat_rxn=(EVAL_DATA{k,L,m}(i_endset,4)-EVAL_DATA{k,L,m}(i_onset,4));
        TAB_DATA{m,1}(k,L)=(int_heat_rxn-baseline)/TAB_DATA{m+21,5}(k,L);
        clear   T_onset  T_endset i_onset i_endset baseline int_heat_rxn
    end
end

close



%% Combine all of your TGA data from individual tests in Nitrogen at 10K/min
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
m=10;
col_old=0;
i_legend=1;
for k=1:N_Labs
    if Test_count(m,k)~=0 && k~=14  %(14 is UMET, that data is /\/\/\)
        col_new=Test_count(m,k);
        legend_counter(i_legend:i_legend+Test_count(m,k)-1)=k;
        col_old=col_old+col_new;
        i_legend=i_legend+Test_count(m,k);
    end
end

for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    last = min(min(N_rows_all(k,:,m)-1,1021));
    if m==10 && k~=14  && L==Test_count(m,k)  % Just DSC Tests // UMET data is messed up /\/\/\ temperature program
        hold on
        for ix=1:L
            figure(1)
            if k==13
                shadedErrorBar(DSC_Temperature(1:last),DSC_heatflow(1:last,6,k,m),[2*DSC_heatflow(1:last,8,k,m) 2*DSC_heatflow(1:last,8,k,m)],'lineprops', {'M','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else
                plot(DSC_Temperature(1:last),DSC_heatflow(1:last,ix,k,m),'-','MarkerSize',5,'color',rgb(Colors{k}),'DisplayName',QMJHL{k});
            end
            figure(2)
            hold on
            plot(DSC_Temperature(1:last),DSC_int_heatflow(1:last,ix,k,m),'-','MarkerSize',5,'color',rgb(Colors{k}),'DisplayName',QMJHL{k});
        end
    end
end
m=10;
figure(1)
axis([300 800 -1 5]);
% title([Test_types{m} '_heatflow'], 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
xlabel('Temperature [K]');
ylabel('Heat Flow [W g^{-1}]');
legend(QMJHL{legend_counter},'Location','northwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_heatflow']));
            print(fig_filename,'-dpdf')

figure(2)
set(gcf, 'Position', [900 100 800 450])
axis([300 800 -200 2500]);
xlabel('Temperature [K]');
ylabel('Integral Heat Flow [J g^{-1}]');
legend(QMJHL{legend_counter},'Location','northwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_int_heatflow']));
            print(fig_filename,'-dpdf')
close all

%% Combine all of your TGA data from individual tests in N2/21%O2 at 10K/min
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
m=13;
col_old=0;
i_legend=1;
for k=1:N_Labs
    if Test_count(m,k)~=0 && k~=14 %(14 is UMET, that data is /\/\/\)
        col_new=Test_count(m,k);
        legend_counter(i_legend:i_legend+Test_count(m,k)-1)=k;
        col_old=col_old+col_new;
        i_legend=i_legend+Test_count(m,k);
    end
end

for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    last = min(min(N_rows_all(k,:,m)-1,1021));
    if m==13 && k~=14  && L==Test_count(m,k)     % Just DSC Tests // UMET data is messed up /\/\/\ temperature program
        hold on
        for ix=1:L
            figure(1)
            plot(DSC_Temperature(1:last),DSC_heatflow(1:last,ix,k,m),'-','MarkerSize',3,'color',rgb(Colors{k}));

            figure(2)
            hold on
            plot(DSC_Temperature(1:last),DSC_int_heatflow(1:last,ix,k,m),'-','MarkerSize',3,'color',rgb(Colors{k}));
        end
    end
end

m=13;
figure(1)
axis([300 800 -3 6.5]);
% title([Test_types{m} '_heatflow'], 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
xlabel('Temperature [K]');
ylabel('Heat Flow [W g^{-1}]');
legend(QMJHL{legend_counter},'Location','northwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_heatflow']));
            print(fig_filename,'-dpdf')

figure(2)
set(gcf, 'Position', [900 100 800 450])
axis([300 800 -500 2500]);
xlabel('Temperature [K]');
ylabel('Integral Heat Flow [J g^{-1}]');
legend(QMJHL{legend_counter},'Location','northwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_int_heatflow']));
            print(fig_filename,'-dpdf')
clear ix last
close all % Close figure

%% UMET data has a unique heating program, let's plot it separately
figure
set(gcf, 'Position', [900 100 700 400])
axis([190 435 -inf inf]);
xlabel('Temperature [K]');
ylabel('Heat Flow [W g^{-1}]');
ix=1;
col={'ko', 'r*', 'bd', 'g+', 'm.'};
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m>=6 && m<=16 && k==14       % Just DSC Tests
        hold on
        plot(EXP_DATA{k,L,m}(:,2),EXP_DATA{k,L,m}(:,3),col{ix});
        legend_UMET_DSC{ix,1}=Test_types{m};
        ix=ix+1;
    end
end
clear ix
axis([240 430 0 0.75]);
legend(legend_UMET_DSC,'Location','northwest', 'interpreter', 'none');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, 'UMET_DSC_heatflow']));
            print(fig_filename,'-dpdf')
close
