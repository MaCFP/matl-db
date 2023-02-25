clear all
close all

load EXP_DATA.mat % This uses the related script 'Import_Data.m'

%% Information about the size of your datasets
N_files;    %total number of experiments
N_Labs;     %total number of labs
N_test_types; %number of different types of experiments
N_rows_i=zeros(N_files,1);
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

% Create EVAL_DATA= [ t | T | m/m0_smoothed | dm*/dt | dT/dt] (all values interpolated to 0.5 K intervals)
figure
for i =1:N_files   % Loop through all of your data sets
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if contains(filenames{i},"TGA")==1        % TGA Tests
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

%         Intitial/test plots of your data
        clf
        hold on
        yyaxis left
        ylabel('(m/m_0) [g/g]');
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,3),'+','MarkerSize',3);
        axis([300 900 -inf inf]);

        yyaxis right
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,4),'r');
        axis([300 900 0 6e-3]);
        title(filenames{i}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        xlabel('Temperature [K]');
        ylabel('(1/m_0)dm/dt [s^{-1}]');
% smooth dm*/dt with a svgolayfilter
        frames=31;
        order=3;
        EVAL_DATA{k,L,m}(:,3)=sgfilt(order,frames,EVAL_DATA{k,L,m}(:,3));
%         EVAL_DATA{k,L,m}(:,3)=sgolayfilt(EVAL_DATA{k,L,m}(:,3),order,frames);  %svgolay using MATLAB's filter 
        yyaxis left
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,3),'-','MarkerSize',1, 'Color', 'green');

        for p=1:size(EVAL_DATA{k,L,m},1)-1
            if p==1
            EVAL_DATA{k,L,m}(p,4)=0;
            else
            EVAL_DATA{k,L,m}(p,4)=(EVAL_DATA{k,L,m}(p-1,3)-EVAL_DATA{k,L,m}(p+1,3))/(EVAL_DATA{k,L,m}(p+1,1)-EVAL_DATA{k,L,m}(p-1,1));
            end
        end
               yyaxis right
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,4),'k');
        axis([300 900 0 6e-3]);
%         if i~= 113
%         title(filenames{i}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
%         else
%             title('Halifax_TGA_N2_10K_1');     %Example NIST/Halifax data anonymously for Prelim. Exp. Report
%         end
        xlabel('Temperature [K]');
        ylabel('(1/m_0)dm/dt [s^{-1}]');
        legend({'m/m_0','m/m_0, filtered','d(m/m_0)/dt','d(m/m_0)/dt, filtered'},'Location','west')

        h=4;                                  % height of plot in inches
        w=5;                                  % width of plot in inches
        set(gcf, 'PaperSize', [w h]);           % set size of PDF page
        set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, filenames{i}(1:end-4)]));
        print(fig_filename,'-dpdf')

        TAB_DATA{m,1}(k,L)=max(EVAL_DATA{k,L,m}(:,4));%            %Calculate dm/dt max maximum dm/dt [g/g-s]
        T_max=find((EVAL_DATA{k,L,m}(:,4))==max(EVAL_DATA{k,L,m}(:,4)));
        T_onset=find((EVAL_DATA{k,L,m}(:,4))>0.1*max(EVAL_DATA{k,L,m}(:,4)),1);
        T_endset=find((EVAL_DATA{k,L,m}(:,4))>0.1*max(EVAL_DATA{k,L,m}(:,4)),1,'last');
%         T_onset=min(find((EVAL_DATA{k,L,m}(:,4))>0.1*max(EVAL_DATA{k,L,m}(:,4))));
%         T_endset=max(find((EVAL_DATA{k,L,m}(:,4))>0.1*max(EVAL_DATA{k,L,m}(:,4))));
        TAB_DATA{m,2}(k,L)=EVAL_DATA{k,L,m}(T_max,2);   %         %Calculate T_Max as the first Temperature when dm/dt = dm/dt max
        TAB_DATA{m,3}(k,L)=EVAL_DATA{k,L,m}(T_onset,2); %         %Calculate T_onset as the first Temperature when dm/dt > 0.1*dm/dt max
        TAB_DATA{m,4}(k,L)=EVAL_DATA{k,L,m}(T_endset,2);%         %Calculate T_endset as the first Temperature when dm/dt > 0.1*dm/dt max
        TAB_DATA{m,5}(k,L)=(EVAL_DATA{k,L,m}(T_onset,3)-EVAL_DATA{k,L,m}(T_endset,3));%         %Calculate dm_rxn as the % mass loss during between T_onset and T_endset
        clear T_max T_onset T_endset m0 fig_filename

% % Plot heating rate for each dataset
        clf
        hold on
        ylabel('(dT/dt) [K/min]');
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,5),'-','MarkerSize',2);
        axis([300 900 0 inf]);
        title(filenames{i}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        xlabel('Temperature [K]');
        h = 4;                                  % height of plot in inches
        w = 5;                                  % width of plot in inches
        set(gcf, 'PaperSize', [w h]);           % set size of PDF page
        set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, char(filenames{i}(1:end-4)),'_dTdt']));
        print(fig_filename,'-dpdf')
    end

end
close all


%% Analyze Tabulated Values
%p=1 --> max(dm*/dt)
%p=2 --> T_max(dm*/dt)
%p=3 --> T_onset (10% of max dm*/dt)
for m=1:N_test_types    
    if contains(Test_types{m},"TGA")==1
        for p=1:3
            N_Labs_TGA=size(TAB_DATA{m,p},1);
            temp=TAB_DATA{m,p}(:,:);
            temp(temp==0)=NaN;
            TAB_DATA{m,p}(:,:)=temp;
            for k=1:N_Labs_TGA
                TAB_DATA{m,p}(k,max(max(Test_count(m,p:N_Labs_TGA)))+1)=mean(TAB_DATA{m,p}(k,1:max(max(Test_count(m,p:N_Labs_TGA)))),'omitnan');       %Calculate mean of t_ignition for this lab
                TAB_DATA{m,p}(k,max(max(Test_count(m,p:N_Labs_TGA)))+2)=std(TAB_DATA{m,p}(k,1:max(max(Test_count(m,p:N_Labs_TGA)))),'omitnan');       %Calculate stdev of t_ignition for this lab
            end
        end
    end
end
clear temp N_Labs_cone

%p=3 --> T_onset (10% of max dm*/dt)
figure
    histogram(TAB_DATA{28,3}([1:11,13,15:end],1:3),10) % Remove TIFP, UDRI
        title("Onset Temperature of Decomposition (TGA in N_2)");     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
%         axis([60 160 0 10]);
        xlabel('Temperature [K]');
        ylabel('Frequency');
        h = 4;                                  % height of plot in inches
        w = 5;                                  % width of plot in inches
        set(gcf, 'PaperSize', [w h]);           % set size of PDF page
        set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner        
        fig_filename=fullfile(char([Script_Figs_dir, 'TGA_N2_histogram_Tonset']));
        print(fig_filename,'-dpdf')

%p=2 --> T_max(dm*/dt)
        figure
    histogram(TAB_DATA{28,2}([1:11,13,15:end],1:3),12)             % Remove TIFP, UDRI
        title("Temperature of peak MLR (TGA in N_2)");     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
%         axis([60 160 0 10]);
        xlabel('Temperature [K]');
        ylabel('Frequency');
        h = 4;                                  % height of plot in inches
        w = 5;                                  % width of plot in inches
        set(gcf, 'PaperSize', [w h]);           % set size of PDF page
        set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, 'TGA_N2_histogram_Tmax']));
        print(fig_filename,'-dpdf')
        
% Scatter Plot showing MLR peak vs. T peak for each TGA test at 10K/min in N2
figure
hold on
i_legend=0;
all_marks = {'o','+','*','h','x','s','d','^','v','>','<','p','.','o','+','*','h','x','s','d','^','v','>','<','p','.'};
for k=1:N_Labs
        if Test_count(28,k)~=0    %If this dataset is the last one for this lab, do some statistics
            i_legend=i_legend+1;
            legend_counter(i_legend)=k;
            plot(TAB_DATA{28,2}(k,1:8),TAB_DATA{28,1}(k,1:8),'LineStyle','none','Marker',all_marks{i_legend},'LineWidth', 2,'color',rgb(Colors{k}));
        end
end


%         title("Onset Temperature of Decomposition (TGA in N_2)");     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([620 655 0 3.5e-3]);
        box on
        xlabel('T_{max} [K]');
        ylabel('Peak Mass Loss Rate (s^{-1})');
        legend(LabNames{legend_counter},'Location','eastoutside'); %; Real Names
        h = 4;                                  % height of plot in inches
        w = 6;                                  % width of plot in inches
        set(gcf, 'PaperSize', [w h]);           % set size of PDF page
        set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner        
        fig_filename=fullfile(char([Script_Figs_dir, 'TGA_N2_PeakMLR_vs_Tpeak']));
        print(fig_filename,'-dpdf')
        clear legend_counter i_legend
close all


%% Quick code to determine minimum temperature reported in your TGA data
min_T=300;  %initialize minimum temperature reported in TGA datataunt
% for i=1:N_files
%     k=files{i,3};   % Find Lab Name
%     L=files{i,4};   % Find Test Count
%     m=files{i,2};   % Find Test Type
% if contains(filenames{i},"TGA")==1        % TGA Tests
%     temp=min(EVAL_DATA{k,L,m}(:,2));
%     if temp>min_T
%         min_T=temp;
%     end
%     end
% end
% clear temp

%% Analyze Temperature-Resolved TGA dTdt Data
TGA_dTdt=NaN*ones(1021,max(max(Test_count(24:37,1:15)))+4,N_Labs,37);
TGA_Temperature=[295:0.5:805]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
        if contains(filenames{i},"TGA")==1        % TGA Tests
        last = min(min(N_rows_all(k,:,m)-1,1021));

        max_T =max(EVAL_DATA{k,L,m}(:,2));
        max_T_idx=min((max_T-295)*2+1,1021);    %we pull in all data up to 1021 rows of data (~up to 800K)

        min_T=min(EVAL_DATA{k,L,m}(:,2));
        min_T_idx=(min_T-295)*2+1;

%         TGA_Mass//TGA_MLR(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 1021 rows/timesteps of Mass and MLR data

            TGA_dTdt(min_T_idx:max_T_idx,L,k,m)=EVAL_DATA{k,L,m}(1:(max_T_idx+1-min_T_idx),5);

            if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp_dTdt=TGA_dTdt(:,:,k,m);
            temp_dTdt(temp_dTdt==0)=NaN;
            TGA_dTdt(1:last,:,k,m)=temp_dTdt;

            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
                TGA_dTdt(ix,L+1,k,m)=nnz(TGA_dTdt((ix-2:ix+2),(1:L),k,m));
                TGA_dTdt(ix,L+2,k,m)=mean_nonan(TGA_dTdt((ix-2:ix+2),(1:L),k,m));
                TGA_dTdt(ix,L+3,k,m)=std_nonan(TGA_dTdt((ix-2:ix+2),(1:L),k,m));
                TGA_dTdt(ix,L+4,k,m)=TGA_dTdt(ix,L+3,k,m)/sqrt(TGA_dTdt(ix,L+1,k,m));
            end
            clear temp_dTdt temp_Mass

            hold on
%         yyaxis left
            for ix=1:L
                plot(TGA_Temperature(1:last),TGA_dTdt(1:last,ix,k,m),'.','MarkerSize',3);
            end
            shadedErrorBar(TGA_Temperature(1:last),TGA_dTdt(1:last,L+2,k,m),[2*TGA_dTdt(1:last,L+4,k,m) 2*TGA_dTdt(1:last,L+4,k,m)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean

            if contains(filenames{i},["50K","100K"])==1        % TGA Testsm==31 || m==32 || m==37  %higher heating rates, zoom out on the axes
                axis([300 800 0 100]);
            else
                axis([300 800 0 25]);
            end
%             title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed; QMJHL Names
            title({LabNames{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed; Real Names
            xlabel('Temperature [K]');
            ylabel('dT/dt [K/min]]');
            h = 4;                                  % height of plot in inches
            w = 5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k} Test_types{m}, '_dTdt_avg']));
            print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
    clear min_T last
end
clear last
close% Close figure

%% All dT/dt curves at 10 K/min
figure('Renderer', 'painters', 'Position', [100 100 650 350])
box on 
hold on
i_legend=1;
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if contains(filenames{i},"TGA")==1 && contains(filenames{i},"10K")==1  % Just 10K/min TGA Tests
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            last = min(min(N_rows_all(k,:,m)-1,1021));
            legend_counter(i_legend)=k;
            i_legend=i_legend+1;
%             for ix=1:L
%                 plot(TGA_Temperature(1:last),TGA_dTdt(1:last,ix,k,m),'.','MarkerSize',2,'color',rgb(Colors{legend_counter(k)}));
%             end
                plot(TGA_Temperature(1:last),TGA_dTdt(1:last,L+2,k,m),'.','MarkerSize',6,'color',rgb(Colors{k}));
        end
    end
end
            axis([300 750 0 22]);
            title('dT/dt in TGA tests at 10 K/min', 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            xlabel('Temperature [K]');
            ylabel('Heating Rate, dT/dt  [K min^{-1}]');
%             legend(QMJHL{legend_counter},'Location','northeastoutside'); %; QMJHL Names
            legend(LabNames{legend_counter},'Location','eastoutside' ,'FontSize', 7); %; Real Names

            h=3.25;                                  % height of plot in inches
            w=6;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, 'TGA_10K_dTdt']));
            print(fig_filename,'-dpdf')
            clear last i_legend legend_counter
close
        %% All dT/dt curves at 20 K/min
figure('Renderer', 'painters', 'Position', [100 100 650 350])
box on 
hold on
i_legend=1;
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if contains(filenames{i},"TGA")==1 && contains(filenames{i},"20K")==1  % Just 20K/min TGA Tests
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            last = min(min(N_rows_all(k,:,m)-1,1021));
            legend_counter(i_legend)=k;
            i_legend=i_legend+1;
%             for ix=1:L
%                 plot(TGA_Temperature(1:last),TGA_dTdt(1:last,ix,k,m),'.','MarkerSize',2,'color',rgb(Colors{legend_counter(k)}));
%             end
                plot(TGA_Temperature(1:last),TGA_dTdt(1:last,L+2,k,m),'.','MarkerSize',6,'color',rgb(Colors{k}));
        end
    end
end
            axis([300 750 10 30]);
            title('dT/dt in TGA tests at 20 K/min', 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            xlabel('Temperature [K]');
            ylabel('Heating Rate, dT/dt  [K min^{-1}]');
%             legend(QMJHL{legend_counter},'Location','northeastoutside');    % QMJHL Names
            legend(LabNames{legend_counter},'Location','southeast');    % Real Names
            h=3.25;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, 'TGA_20K_dTdt']));
            print(fig_filename,'-dpdf')
            clear last i_legend legend_counter
close
%% Analyze Temperature-Resolved TGA MLR Data
TGA_MLR=NaN*ones(1021,max(max(Test_count(24:37,1:15)))+4,N_Labs,37);
TGA_Mass=NaN*ones(1021,max(max(Test_count(24:37,1:15)))+4,N_Labs,37);
TGA_Temperature=[295:0.5:805]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if contains(filenames{i},"TGA")==1  % Just TGA Tests
        last = min(min(N_rows_all(k,:,m)-1,1021));

        max_T =max(EVAL_DATA{k,L,m}(:,2));
        max_T_idx=min((max_T-295)*2+1,1021);    %we pull in all data up to 1021 rows of data (~up to 800K)

        min_T=min(EVAL_DATA{k,L,m}(:,2));
        min_T_idx=(min_T-295)*2+1;

%         TGA_Mass//TGA_MLR(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 1021 rows/timesteps of Mass and MLR data
            TGA_Mass(min_T_idx:max_T_idx,L,k,m)=EVAL_DATA{k,L,m}(1:(max_T_idx+1-min_T_idx),3);
            TGA_MLR(min_T_idx:max_T_idx,L,k,m)=EVAL_DATA{k,L,m}(1:(max_T_idx+1-min_T_idx),4);

            if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp_MLR=TGA_MLR(:,:,k,m);
            temp_MLR(temp_MLR==0)=NaN;
            TGA_MLR(1:last,:,k,m)=temp_MLR;

            temp_Mass=TGA_Mass(:,:,k,m);
            temp_Mass(temp_Mass==0)=NaN;
            TGA_Mass(1:last,:,k,m)=temp_Mass;

            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
            if contains(filenames{i},"TIFP")==1    % TIFP TGA DATA: Tests 1 and 2 did not have a full N2 purge prior too measurement--> these should be plotted but not averaged (oxidation)
                TGA_MLR(ix,L+1,k,m)=nnz(TGA_MLR((ix-2:ix+2),(3:L),k,m));
                TGA_MLR(ix,L+2,k,m)=mean_nonan(TGA_MLR((ix-2:ix+2),(3:L),k,m));
                TGA_MLR(ix,L+3,k,m)=std_nonan(TGA_MLR((ix-2:ix+2),(3:L),k,m));
                TGA_MLR(ix,L+4,k,m)=TGA_MLR(ix,L+3,k,m)/sqrt(TGA_MLR(ix,L+1,k,m));

                TGA_Mass(ix,L+1,k,m)=nnz(TGA_Mass((ix-2:ix+2),(3:L),k,m));
                TGA_Mass(ix,L+2,k,m)=mean_nonan(TGA_Mass((ix-2:ix+2),(3:L),k,m));
                TGA_Mass(ix,L+3,k,m)=std_nonan(TGA_Mass((ix-2:ix+2),(3:L),k,m));
                TGA_Mass(ix,L+4,k,m)=TGA_Mass(ix,L+3,k,m)/sqrt(TGA_Mass(ix,L+1,k,m));
                
            else
                TGA_MLR(ix,L+1,k,m)=nnz(TGA_MLR((ix-2:ix+2),(1:L),k,m));
                TGA_MLR(ix,L+2,k,m)=mean_nonan(TGA_MLR((ix-2:ix+2),(1:L),k,m));
                TGA_MLR(ix,L+3,k,m)=std_nonan(TGA_MLR((ix-2:ix+2),(1:L),k,m));
                TGA_MLR(ix,L+4,k,m)=TGA_MLR(ix,L+3,k,m)/sqrt(TGA_MLR(ix,L+1,k,m));

                TGA_Mass(ix,L+1,k,m)=nnz(TGA_Mass((ix-2:ix+2),(1:L),k,m));
                TGA_Mass(ix,L+2,k,m)=mean_nonan(TGA_Mass((ix-2:ix+2),(1:L),k,m));
                TGA_Mass(ix,L+3,k,m)=std_nonan(TGA_Mass((ix-2:ix+2),(1:L),k,m));
                TGA_Mass(ix,L+4,k,m)=TGA_Mass(ix,L+3,k,m)/sqrt(TGA_Mass(ix,L+1,k,m));
            end
            end
            clear temp_MLR temp_Mass

            hold on
        yyaxis left
            for ix=1:L
                plot(TGA_Temperature(1:last),TGA_Mass(1:last,ix,k,m),'.','MarkerSize',3);
            end
            shadedErrorBar(TGA_Temperature(1:last),TGA_Mass(1:last,L+2,k,m),[2*TGA_Mass(1:last,L+4,k,m) 2*TGA_Mass(1:last,L+4,k,m)],'lineprops', {'-k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean

            axis([300 800 0 1.05]);
            ylabel('(m/m_0) [g/g]');
            clear ix


        yyaxis right
            for ix=1:L
                plot(TGA_Temperature(1:last),TGA_MLR(1:last,ix,k,m),'.','MarkerSize',3);
            end
            shadedErrorBar(TGA_Temperature(1:last),TGA_MLR(1:last,L+2,k,m),[2*TGA_MLR(1:last,L+4,k,m) 2*TGA_MLR(1:last,L+4,k,m)],'lineprops', {'-k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean

            if contains(filenames{i},["20K","50K","100K"])==1  %higher heating rates, zoom out on the axes
                axis([300 800 0 inf]);
            else
                axis([300 800 0 0.003]);
            end
%             title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed; QMJHL Names
            title({LabNames{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed; Real Names
            xlabel('Temperature [K]');
            ylabel('dm*/dt [s^{-1}]');
            h=3;                                  % height of plot in inches
            w=4;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{m} '_avg']));
            print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
    clear min_T last fig_filename
end
clear last
close% Close figure

%% Combine all of your TGA data from individual tests in N2 at 5K/min
col_old=0;
i_legend=1;
m=find(Test_types=="TGA_N2_5K");
        TGA_N2_5K_all=zeros(1021, Test_count(m,end)+4,2);
for k=1:N_Labs
    if Test_count(m,k)~=0
        col_new=Test_count(m,k);
        legend_counter(i_legend:i_legend+Test_count(m,k)-1)=k;
        TGA_N2_5K_all(:,col_old+1:(col_old+col_new),1)=TGA_Mass(:,1:col_new,k,m);
        TGA_N2_5K_all(:,col_old+1:(col_old+col_new),2)=TGA_MLR(:,1:col_new,k,m);
        col_old=col_old+col_new;
        i_legend=i_legend+Test_count(m,k);
    end
end

clear col_new col_old clear i_legend fig_filename


TGA_N2_5K_all(TGA_N2_5K_all==0)=NaN;
% Do some Statistics now that you have all of your data together
%Calculate mean and stdeviation +/- 0 timesteps
for ix=1:1021
    TGA_N2_5K_all(ix,(Test_count(m,end)+1),1)=nnz(TGA_N2_5K_all((ix-0:ix+0),1:Test_count(m,end),1));          % Count, N
    TGA_N2_5K_all(ix,(Test_count(m,end)+2),1)=mean_nonan(TGA_N2_5K_all((ix-0:ix+0),[1:Test_count(m,end)],1));        % mean
    TGA_N2_5K_all(ix,(Test_count(m,end)+3),1)=std_nonan(TGA_N2_5K_all((ix-0:ix+0),[1:Test_count(m,end)],1));         % stdmean (all data +/- 1 s
    TGA_N2_5K_all(ix,(Test_count(m,end)+4),1)=TGA_N2_5K_all(ix,(Test_count(m,end)+3),1)/sqrt(TGA_N2_5K_all(ix,Test_count(m,end)+1,1));  % stdev mean

    TGA_N2_5K_all(ix,(Test_count(m,end)+1),2)=nnz(TGA_N2_5K_all((ix-0:ix+0),1:Test_count(m,end),2));          % Count, N
    TGA_N2_5K_all(ix,(Test_count(m,end)+2),2)=mean_nonan(TGA_N2_5K_all((ix-0:ix+0),[1:Test_count(m,end)],2));        % mean
    TGA_N2_5K_all(ix,(Test_count(m,end)+3),2)=std_nonan(TGA_N2_5K_all((ix-0:ix+0),[1:Test_count(m,end)],2));         % stdmean (all data +/- 1 s
    TGA_N2_5K_all(ix,(Test_count(m,end)+4),2)=TGA_N2_5K_all(ix,(Test_count(m,end)+3),2)/sqrt(TGA_N2_5K_all(ix,Test_count(m,end)+1,2));  % stdev mean
end


%plot Average m/m0 with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 650 350])
hold on
box on
for k=1:Test_count(m,end)
    plot(TGA_Temperature(:),TGA_N2_5K_all(:,k,1),'-','MarkerSize',2,'color',rgb(Colors{legend_counter(k)})) ;
end

        title(char(Test_types{m}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([300 800 0 1]);
        xlabel('Temperature [K]');
        ylabel('m/m_0 [g/g]');
%         legend({QMJHL{legend_counter}},'Location','southwest'); % QMJHL Names
        legend({LabNames{legend_counter}},'Location','southwest'); % Real Names
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_Mass']));
            print(fig_filename,'-dpdf')
        shadedErrorBar(TGA_Temperature(:),(TGA_N2_5K_all(:,Test_count(m,end)+2,1)),[2*(TGA_N2_5K_all(:,Test_count(m,end)+4,1)) 2*(TGA_N2_5K_all(:,Test_count(m,end)+4,1))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         legend({QMJHL{legend_counter}},'Location','southwest'); % QMJHL Names
        legend({LabNames{legend_counter}},'Location','southwest'); % Real Names
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_Mass_w_avg']));
            print(fig_filename,'-dpdf')



%plot Average d(m/m0)/dt with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 650 350])
hold on
box on
for k=1:Test_count(m,end)
    plot(TGA_Temperature(:),TGA_N2_5K_all(:,k,2),'-','MarkerSize',2,'color',rgb(Colors{legend_counter(k)})) ;
end

        title(char(Test_types{m}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([300 800 0 0.002]);
        xlabel('Temperature [K]');
        ylabel('d(m/m_0)/dt [s^{-1}]');
%         legend({QMJHL{legend_counter}},'Location','southwest'); % QMJHL Names
        legend({LabNames{legend_counter}},'Location','southwest'); % Real Names
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_dmdt']));
            print(fig_filename,'-dpdf')
        shadedErrorBar(TGA_Temperature(:),(TGA_N2_5K_all(:,Test_count(m,end)+2,2)),[2*(TGA_N2_5K_all(:,Test_count(m,end)+4,2)) 2*(TGA_N2_5K_all(:,Test_count(m,end)+4,2))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         legend({QMJHL{legend_counter},'Average'},'Location','northwest');   % QMJHL Names
        legend({LabNames{legend_counter},'Average'},'Location','northwest');   % Real Names
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_dmdt_w_avg']));
            print(fig_filename,'-dpdf')

clear m legend_counter fig_filename
close all

%% Combine all of your TGA data from individual tests in N2 at 10K/min (ALSO 10K/min in Argon)
Test_count_10K=Test_count(find(Test_types=="TGA_N2_10K"),end)+Test_count(find(Test_types=="TGA_Ar_10K"),end);       %N2 + Argon()
m=find(Test_types=="TGA_N2_10K");
TGA_N2_10K_all=zeros(1021, Test_count_10K+4,2);
col_old=0;
i_legend=1;
for k=1:N_Labs
    if Test_count(m,k)~=0
        col_new=Test_count(m,k);
        legend_counter(i_legend:i_legend+Test_count(m,k)-1)=k;
        TGA_N2_10K_all(:,col_old+1:(col_old+col_new),1)=TGA_Mass(:,1:col_new,k,m);
        TGA_N2_10K_all(:,col_old+1:(col_old+col_new),2)=TGA_MLR(:,1:col_new,k,m);
        col_old=col_old+col_new;
        i_legend=i_legend+Test_count(m,k);
    end
end

m = find(Test_types=="TGA_Ar_10K");
for k=1:N_Labs
    if Test_count(m,k)~=0
        col_new=Test_count(m,k);
        legend_counter(i_legend:i_legend+Test_count(m,k)-1)=k;
        TGA_N2_10K_all(:,col_old+1:(col_old+col_new),1)=TGA_Mass(:,1:col_new,k,m);
        TGA_N2_10K_all(:,col_old+1:(col_old+col_new),2)=TGA_MLR(:,1:col_new,k,m);
        col_old=col_old+col_new;
        i_legend=i_legend+Test_count(m,k);
    end
end
clear col_new col_old clear i_legend


TGA_N2_10K_all(TGA_N2_10K_all==0)=NaN;
% Do some Statistics now that you have all of your data together
%Calculate mean and stdeviation +/- 0 timesteps

%NOTE: Some datasets have been neglected when calculating these statistics...
% because they have been identified as outliers [LCPP(dT/dt is too high), UDRI (20K temp shift), TIFP (two peaks), Ulster (50K-60K temp shift)] 
% Hence the special indexing: [1:4 8:12  15:21 23:Test_count]. 
%Feb. 24, 2023 - identify this indexing issue, create short loop and [TGA_N2_10K_indexing] to address it but solution remains incomplete, keep previous indexing for now  
m=find(Test_types=="TGA_N2_10K");
temp_counter=0;
for k=1:N_Labs
    if contains(LabNames(k),["LCPP" "TIFP" "UDRI" "ULSTER"])==0
%         temp_counter=temp_counter+1;
        TGA_N2_10K_indexing(1,k)=Test_count(m,k);
    elseif contains(LabNames(k),["LCPP" "TIFP" "UDRI" "ULSTER"])==1
        TGA_N2_10K_indexing(2,k)=Test_count(m,k);
    end
end
clear temp_counter m

for ix=1:1021
    TGA_N2_10K_all(ix,(Test_count_10K+1),1)=nnz(TGA_N2_10K_all((ix-0:ix+0),[1:4 8:12  15:21 23:Test_count_10K],1));          % Count, N
    TGA_N2_10K_all(ix,(Test_count_10K+2),1)=mean_nonan(TGA_N2_10K_all((ix-0:ix+0),[1:4 8:12  15:21 23:Test_count_10K],1));        % mean
    TGA_N2_10K_all(ix,(Test_count_10K+3),1)=std_nonan(TGA_N2_10K_all((ix-0:ix+0),[1:4 8:12  15:21 23:Test_count_10K],1));         % stdmean (all data +/- 1 s
    TGA_N2_10K_all(ix,(Test_count_10K+4),1)=TGA_N2_10K_all(ix,(Test_count_10K+3),1)/sqrt(TGA_N2_10K_all(ix,Test_count_10K+1,1));  % stdev mean

    TGA_N2_10K_all(ix,(Test_count_10K+1),2)=nnz(TGA_N2_10K_all((ix-0:ix+0),[1:4 8:12  15:21 23:Test_count_10K],2));          % Count, N
    TGA_N2_10K_all(ix,(Test_count_10K+2),2)=mean_nonan(TGA_N2_10K_all((ix-0:ix+0),[1:4 8:12  15:21 23:Test_count_10K],2));        % mean
    TGA_N2_10K_all(ix,(Test_count_10K+3),2)=std_nonan(TGA_N2_10K_all((ix-0:ix+0),[1:4 8:12  15:21 23:Test_count_10K],2));         % stdmean (all data +/- 1 s
    TGA_N2_10K_all(ix,(Test_count_10K+4),2)=TGA_N2_10K_all(ix,(Test_count_10K+3),2)/sqrt(TGA_N2_10K_all(ix,Test_count_10K+1,2));  % stdev mean
end

m=find(Test_types=="TGA_N2_10K");
%plot Average m/m0 with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
for k=1:Test_count_10K
    plot(TGA_Temperature(:),TGA_N2_10K_all(:,k,1),'-','MarkerSize',5,'color',rgb(Colors{legend_counter(k)})) ;
end
        title(char(Test_types{m}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([300 800 0 1]);
        xlabel('Temperature [K]');
        ylabel('m/m_0 [g/g]');
%         legend(QMJHL{legend_counter},'Location','southwest');   % QMJHL Names
        legend(LabNames{legend_counter},'Location','eastoutside','FontSize',7);   % Real Names
            h=5;                                  % height of plot in inches
            w=7;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_Mass']));
            print(fig_filename,'-dpdf')
        shadedErrorBar(TGA_Temperature(:),(TGA_N2_10K_all(:,Test_count_10K+2,1)),[2*(TGA_N2_10K_all(:,Test_count_10K+4,1)) 2*(TGA_N2_10K_all(:,Test_count_10K+4,1))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         legend({QMJHL{legend_counter}, 'Average'},'Location','southwest');  % QMJHL Names
        legend({LabNames{legend_counter}, 'Average'},'Location','eastoutside','FontSize',7);  % Real Names
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_Mass_w_avg']));
            print(fig_filename,'-dpdf')


%plot Average d(m/m0)/dt with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
for k=1:Test_count_10K
    plot(TGA_Temperature(:),TGA_N2_10K_all(:,k,2),'-','MarkerSize',5,'color',rgb(Colors{legend_counter(k)})) ;
end
        box on
        title(char(Test_types{m}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([300 800 0 0.004]);
        xlabel('Temperature [K]');
        ylabel('d(m/m_0)/dt [s^{-1}]');
%         legend(QMJHL{legend_counter},'Location','northwest');   % QMJHL Names
        legend(LabNames{legend_counter},'Location','eastoutside','FontSize',7);   % Real Names
            h=5;                                  % height of plot in inches
            w=7;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_dmdt']));
            print(fig_filename,'-dpdf')
        shadedErrorBar(TGA_Temperature(:),(TGA_N2_10K_all(:,Test_count_10K+2,2)),[2*(TGA_N2_10K_all(:,Test_count_10K+4,2)) 2*(TGA_N2_10K_all(:,Test_count_10K+4,2))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         legend({QMJHL{legend_counter}, 'Average'},'Location','northwest');  % QMJHL Names
        legend({LabNames{legend_counter}, 'Average'},'Location','eastoutside','FontSize',7);  % Real Names
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_dmdt_w_avg']));
            print(fig_filename,'-dpdf')

clear m legend_counter
close all

%% Combine all of your TGA data from individual tests in N2 at 20K/min
m=find(Test_types=="TGA_N2_20K");
TGA_N2_20K_all=zeros(1021, Test_count(m,end)+4,2);
col_old=0;
i_legend=1;
for k=1:N_Labs
    if Test_count(m,k)~=0
        col_new=Test_count(m,k);
        legend_counter(i_legend:i_legend+Test_count(m,k)-1)=k;
        TGA_N2_20K_all(:,col_old+1:(col_old+col_new),1)=TGA_Mass(:,1:col_new,k,m);
        TGA_N2_20K_all(:,col_old+1:(col_old+col_new),2)=TGA_MLR(:,1:col_new,k,m);
        col_old=col_old+col_new;
        i_legend=i_legend+Test_count(m,k);
    end
end

clear col_new col_old clear i_legend


TGA_N2_20K_all(TGA_N2_20K_all==0)=NaN;
% Do some Statistics now that you have all of your data together
%Calculate mean and stdeviation +/- 0 timesteps
for ix=1:1021
    TGA_N2_20K_all(ix,(Test_count(m,end)+1),1)=nnz(TGA_N2_20K_all((ix-0:ix+0),[1:Test_count(m,end)],1));          % Count, N
    TGA_N2_20K_all(ix,(Test_count(m,end)+2),1)=mean_nonan(TGA_N2_20K_all((ix-0:ix+0),[1:Test_count(m,end)],1));        % mean
    TGA_N2_20K_all(ix,(Test_count(m,end)+3),1)=std_nonan(TGA_N2_20K_all((ix-0:ix+0),[1:Test_count(m,end)],1));         % stdmean (all data +/- 1 s
    TGA_N2_20K_all(ix,(Test_count(m,end)+4),1)=TGA_N2_20K_all(ix,(Test_count(m,end)+3),1)/sqrt(TGA_N2_20K_all(ix,Test_count(m,end)+1,1));  % stdev mean

    TGA_N2_20K_all(ix,(Test_count(m,end)+1),2)=nnz(TGA_N2_20K_all((ix-0:ix+0),[1:Test_count(m,end)],2));          % Count, N
    TGA_N2_20K_all(ix,(Test_count(m,end)+2),2)=mean_nonan(TGA_N2_20K_all((ix-0:ix+0),[1:Test_count(m,end)],2));        % mean
    TGA_N2_20K_all(ix,(Test_count(m,end)+3),2)=std_nonan(TGA_N2_20K_all((ix-0:ix+0),[1:Test_count(m,end)],2));         % stdmean (all data +/- 1 s
    TGA_N2_20K_all(ix,(Test_count(m,end)+4),2)=TGA_N2_20K_all(ix,(Test_count(m,end)+3),2)/sqrt(TGA_N2_20K_all(ix,Test_count(m,end)+1,2));  % stdev mean
end


%plot Average m/m0 with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
for k=1:Test_count(m,end)
    plot(TGA_Temperature(:),TGA_N2_20K_all(:,k,1),'-','MarkerSize',2,'color',rgb(Colors{legend_counter(k)})) ;
end

        title(char(Test_types{m}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([300 800 0 1]);
        xlabel('Temperature [K]');
        ylabel('m/m_0 [g/g]');
%         legend(QMJHL{legend_counter},'Location','southwest');   % QMJHL Names
        legend(LabNames{legend_counter},'Location','southwest');   % QMJHL Names
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_Mass']));
            print(fig_filename,'-dpdf')

        shadedErrorBar(TGA_Temperature(:),(TGA_N2_20K_all(:,Test_count(m,end)+2,1)),[2*(TGA_N2_20K_all(:,Test_count(m,end)+4,1)) 2*(TGA_N2_20K_all(:,Test_count(m,end)+4,1))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         legend({QMJHL{legend_counter}, 'Average'},'Location','southwest');  % QMJHL Names
        legend({LabNames{legend_counter}, 'Average'},'Location','southwest');  % QMJHL Names
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_Mass_w_avg']));
            print(fig_filename,'-dpdf')

%plot Average d(m/m0)/dt with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
for k=1:Test_count(m,end)
    plot(TGA_Temperature(:),TGA_N2_20K_all(:,k,2),'-','MarkerSize',2,'color',rgb(Colors{legend_counter(k)})) ;
end

        title(char(Test_types{m}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([300 800 0 0.0065]);
        xlabel('Temperature [K]');
        ylabel('d(m/m_0)/dt [s^{-1}]');
%         legend(QMJHL{legend_counter},'Location','northwest');   % QMJHL Names
        legend(LabNames{legend_counter},'Location','northwest');   % Real Names
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_dmdt']));
            print(fig_filename,'-dpdf')

        shadedErrorBar(TGA_Temperature(:),(TGA_N2_20K_all(:,Test_count(m,end)+2,2)),[2*(TGA_N2_20K_all(:,Test_count(m,end)+4,2)) 2*(TGA_N2_20K_all(:,Test_count(m,end)+4,2))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         legend({QMJHL{legend_counter}, 'Average'},'Location','northwest');  % QMJHL Names
        legend({LabNames{legend_counter}, 'Average'},'Location','northwest');  % Real Names
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_dmdt_w_avg']));
            print(fig_filename,'-dpdf')

clear m legend_counter fig_filename
close all
%% Combine all of your TGA data from individual tests in N2/21%O2 at 10K/min
m=find(Test_types=="TGA_O2-21_10K");
TGA_N2_O2_21_10K_all=zeros(1021, Test_count(m,end)+4,2);
col_old=0;
i_legend=1;
for k=1:N_Labs
    if Test_count(m,k)~=0
        col_new=Test_count(m,k);
        legend_counter(i_legend:i_legend+Test_count(m,k)-1)=k;
        TGA_N2_O2_21_10K_all(:,col_old+1:(col_old+col_new),1)=TGA_Mass(:,1:col_new,k,m);
        TGA_N2_O2_21_10K_all(:,col_old+1:(col_old+col_new),2)=TGA_MLR(:,1:col_new,k,m);
        col_old=col_old+col_new;
        i_legend=i_legend+Test_count(m,k);
    end
end

clear col_new col_old clear i_legend


TGA_N2_O2_21_10K_all(TGA_N2_O2_21_10K_all==0)=NaN;
% Do some Statistics now that you have all of your data together
%Calculate mean and stdeviation +/- 0 timesteps

for ix=1:1021
    TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+1),1)=nnz(TGA_N2_O2_21_10K_all((ix-0:ix+0),[1:Test_count(m,end)],1));          % Count, N
    TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+2),1)=mean_nonan(TGA_N2_O2_21_10K_all((ix-0:ix+0),[1:Test_count(m,end)],1));        % mean
    TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+3),1)=std_nonan(TGA_N2_O2_21_10K_all((ix-0:ix+0),[1:Test_count(m,end)],1));         % stdmean (all data +/- 1 s
    TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+4),1)=TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+3),1)/sqrt(TGA_N2_O2_21_10K_all(ix,Test_count(m,end)+1,1));  % stdev mean

    TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+1),2)=nnz(TGA_N2_O2_21_10K_all((ix-0:ix+0),[1:Test_count(m,end)],2));          % Count, N
    TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+2),2)=mean_nonan(TGA_N2_O2_21_10K_all((ix-0:ix+0),[1:Test_count(m,end)],2));        % mean
    TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+3),2)=std_nonan(TGA_N2_O2_21_10K_all((ix-0:ix+0),[1:Test_count(m,end)],2));         % stdmean (all data +/- 1 s
    TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+4),2)=TGA_N2_O2_21_10K_all(ix,(Test_count(m,end)+3),2)/sqrt(TGA_N2_O2_21_10K_all(ix,Test_count(m,end)+1,2));  % stdev mean
end


%plot Average m/m0 with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
for k=1:Test_count(m,end)
    plot(TGA_Temperature(:),TGA_N2_O2_21_10K_all(:,k,1),'-','MarkerSize',2,'color',rgb(Colors{legend_counter(k)})) ;
end
        title(char(Test_types{m}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([300 800 0 1]);
        xlabel('Temperature [K]');
        ylabel('m/m_0 [g/g]');
%         legend(QMJHL{legend_counter},'Location','southwest');   %QMJHL Names
        legend(LabNames{legend_counter},'Location','southwest');   %Real Names
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_Mass']));
            print(fig_filename,'-dpdf')

        shadedErrorBar(TGA_Temperature(:),(TGA_N2_O2_21_10K_all(:,Test_count(m,end)+2,1)),[2*(TGA_N2_O2_21_10K_all(:,Test_count(m,end)+4,1)) 2*(TGA_N2_O2_21_10K_all(:,Test_count(m,end)+4,1))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         legend({QMJHL{legend_counter}, 'Average'},'Location','southwest');  %QMJHL Names
        legend({LabNames{legend_counter}, 'Average'},'Location','southwest');  %Real Names
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_Mass_w_avg']));
            print(fig_filename,'-dpdf')
%plot Average d(m/m0)/dt with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
for k=1:Test_count(m,end)
    plot(TGA_Temperature(:),TGA_N2_O2_21_10K_all(:,k,2),'-','MarkerSize',2,'color',rgb(Colors{legend_counter(k)})) ;
end
        title(char(Test_types{m}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([300 800 0 0.004]);
        xlabel('Temperature [K]');
        ylabel('d(m/m_0)/dt [s^{-1}]');
%         legend(QMJHL{legend_counter},'Location','northwest');   %QMJHL Names
        legend(LabNames{legend_counter},'Location','northwest');   %Real Names
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_dmdt']));
            print(fig_filename,'-dpdf')

        shadedErrorBar(TGA_Temperature(:),(TGA_N2_O2_21_10K_all(:,Test_count(m,end)+2,2)),[2*(TGA_N2_O2_21_10K_all(:,Test_count(m,end)+4,2)) 2*(TGA_N2_O2_21_10K_all(:,Test_count(m,end)+4,2))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         legend({QMJHL{legend_counter}, 'Average'},'Location','northwest');  %QMJHL Names
        legend({LabNames{legend_counter}, 'Average'},'Location','northwest');  %Real Names
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_dmdt_w_avg']));
            print(fig_filename,'-dpdf')
clear m legend_counter
close all

%% Plot Average TGA data in N2 at 5, 10, 20 K/min
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on

shadedErrorBar(TGA_Temperature(:),(TGA_N2_20K_all(:,end-2,1)),[2*(TGA_N2_20K_all(:,end,1)) 2*(TGA_N2_20K_all(:,end,1))],'lineprops', {'r','LineWidth',2}); %plot with shaded error bards = 2stdevmean
shadedErrorBar(TGA_Temperature(:),(TGA_N2_10K_all(:,end-2,1)),[2*(TGA_N2_10K_all(:,end,1)) 2*(TGA_N2_10K_all(:,end,1))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
shadedErrorBar(TGA_Temperature(:),(TGA_N2_5K_all(:,end-2,1)),[2*(TGA_N2_5K_all(:,end,1)) 2*(TGA_N2_5K_all(:,end,1))],'lineprops', {'b','LineWidth',2}); %plot with shaded error bards = 2stdevmean
box on
title(char('TGA in Nitrogen'));
axis([300 800 0 1]);
xlabel('Temperature [K]');
ylabel('m/m_0 [g/g]');
legend('20 K/min','10 K/min','5 K/min','Location','southwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, 'TGA-N2_5_10_20K_Mass']));
            print(fig_filename,'-dpdf')



clf
shadedErrorBar(TGA_Temperature(:),(TGA_N2_20K_all(:,end-2,2)),[2*(TGA_N2_20K_all(:,end,2)) 2*(TGA_N2_20K_all(:,end,2))],'lineprops', {'r','LineWidth',2}); %plot with shaded error bards = 2stdevmean
shadedErrorBar(TGA_Temperature(:),(TGA_N2_10K_all(:,end-2,2)),[2*(TGA_N2_10K_all(:,end,2)) 2*(TGA_N2_10K_all(:,end,2))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
shadedErrorBar(TGA_Temperature(:),(TGA_N2_5K_all(:,end-2,2)),[2*(TGA_N2_5K_all(:,end,2)) 2*(TGA_N2_5K_all(:,end,2))],'lineprops', {'b','LineWidth',2}); %plot with shaded error bards = 2stdevmean
% shadedErrorBar(TGA_Temperature(:),(TGA_N2_20K_all(:,Test_count(30,end)+2,2)),[2*(TGA_N2_20K_all(:,Test_count(30,end)+4,2)) 2*(TGA_N2_20K_all(:,Test_count(30,end)+4,2))],'lineprops', {'r','LineWidth',2}); %plot with shaded error bards = 2stdevmean
% shadedErrorBar(TGA_Temperature(:),(TGA_N2_10K_all(:,Test_count(28,end)+2,2)),[2*(TGA_N2_10K_all(:,Test_count(28,end)+4,2)) 2*(TGA_N2_10K_all(:,Test_count(28,end)+4,2))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
% shadedErrorBar(TGA_Temperature(:),(TGA_N2_5K_all(:,Test_count(27,end)+2,2)),[2*(TGA_N2_5K_all(:,Test_count(27,end)+4,2)) 2*(TGA_N2_5K_all(:,Test_count(27,end)+4,2))],'lineprops', {'b','LineWidth',2}); %plot with shaded error bards = 2stdevmean
box on
title(char('TGA in Nitrogen'));
axis([300 800 0 0.006]);
xlabel('Temperature [K]');
ylabel('d(m/m_0)/dt [s^{-1}]');
legend('20 K/min','10 K/min','5 K/min','Location','northwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, 'TGA-N2_5_10_20K_dmdt']));
            print(fig_filename,'-dpdf')
close all