clear all
close all

load EXP_DATA.mat% This uses the related script 'Import_Data.m'

%% Information about the size of your datasets
N_files;    %total number of experiments
N_Labs;     %total number of labs
N_test_types;%number of different types of experiments
% N_rows_i=zeros(184,1);
N_rows_all=NaN*ones(N_Labs,max(max(Test_count(:,1:end-1))),N_test_types);    %Initialize a matrix to hold the number of rows (e.g., timesteps) in each dataset
EVAL_DATA=cell(N_Labs,max(max(Test_count(:,1:(end-1)))),N_test_types);      %Initialize your cell array to hold (N_labs, N_repeat_exps
TAB_DATA=cell(N_test_types,5);                                              %Tabulated data of discrete values (e.g., t_onset_MLR) # discrete values =5 (i.e., we can define up to 5 Tab values for each test type
% Recall, you have the following Types of Experimental data
% Test_types={'CAPA_25kW';'CAPA_60kW';...
%             'Cone_25kW';'Cone_50kW'; 'Cone_65kW';...
%             'DSC_N2_1K';'DSC_N2_2K';'DSC_N2_5K';'DSC_N2_10K';'DSC_N2_20K';...
%             'DSC_O2-10_10K';'DSC_O2-21_10K';'DSC_Ar_1K'; 'DSC_Ar_10K'; 'DSC_Ar_50K';...
%             'FPA_25kW';'FPA_50kW';'FPA_65kW';...
%             'Gasification_25kW';'Gasification_50kW';'Gasification_65kW';...
%             'MCC_N2_60K';...
%             'TGA_N2_1K';'TGA_N2_2K';'TGA_N2_2.5K';'TGA_N2_5K';'TGA_N2_10K';'TGA_N2_15K';'TGA_N2_20K';'TGA_N2_50K';'TGA_N2_100K';...
%             'TGA_O2-10_10K';'TGA_O2-21_10K'; 'TGA_Ar_1K'; 'TGA_Ar_10K'; 'TGA_Ar_50K'};

%%
%Read in all of your data  EXP_DATA is a 3D cell array of indexing {LabName,k | Test #, L | Test Type,m}
%Inside of each cell is a 2D array of indexing [timestep, data type]

% Create EVAL_DATA= [ t | mass | T1 | T2 | T3 | Tavg | dmdt*(1/(Asurf))| smooth dm/dt*(1/(m0*Asurf)] (all values interpolated to 1Hz)
figure
for i = 1:N_files   % Loop through all of your data sets
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m>=17 && m<=22       %All FPA and Gasification Tests
        t_start=round(min(EXP_DATA{k,L,m}(:,1)));   %find first timestep (rounded to nearest integer)
        t_end=round(max(EXP_DATA{k,L,m}(:,1)));     %find last timestep (rounded to nearest integer)
        m0=mean(EXP_DATA{k,L,m}(1:5,2));
        EVAL_DATA{k,L,m}(:,1)=[t_start:t_end-1]';                                                               % interpolate time step from 0 to t_end at 1 Hz
        EVAL_DATA{k,L,m}(:,2)=interp1(EXP_DATA{k,L,m}(:,1),EXP_DATA{k,L,m}(:,2), EVAL_DATA{k,L,m}(:,1));        % interpolate mass
%         if size(EXP_DATA{k,L,m},2)>2
%             EVAL_DATA{k,L,m}(:,3)=interp1(EXP_DATA{k,L,m}(:,1),EXP_DATA{k,L,m}(:,3), EVAL_DATA{k,L,m}(:,1));        % interpolate Temp
%         else
%             EVAL_DATA{k,L,m}(:,3)=NaN;
%         end
%         N_rows_i(i)=size(EXP_DATA{k,L,m}(:,:),1);
        N_rows_all(k,L,m)=size(EVAL_DATA{k,L,m}(:,:),1);
        Ncols=size(EXP_DATA{k,L,m}(:,:),2);         % Find out how many TCs / temp measurements were provided in this test
        % Interpolate and average Temperatures
        if Ncols>=3
            for j =3:Ncols
                 EVAL_DATA{k,L,m}(:,j)=interp1(EXP_DATA{k,L,m}(:,1),EXP_DATA{k,L,m}(:,j), EVAL_DATA{k,L,m}(:,1));       %interpolate Temps
            end
            for j = 1:N_rows_all(k,L,m)-2%(t_end-t_start)                                               %Find out duration of Temp measurement data (!!this only works for indexing b/c we're at 1Hz!!)
                EVAL_DATA{k,L,m}(j,6)=mean(nonzeros(EVAL_DATA{k,L,m}(j,3:Ncols)));  %Average all temp measurements at that timestep
            end
        end
        % Calculate dm/dt
        for j = 1:N_rows_all(k,L,m)-2%(t_end-t_start)                                               %Find out duration of Temp measurement data (!!this only works for indexing b/c we're at 1Hz!!)
            if j>2 && j<(N_rows_all(k,L,m)-2)
                EVAL_DATA{k,L,m}(j,7)=(1/(1000*Asurf(k)))*(EVAL_DATA{k,L,m}(j-2,2)-EVAL_DATA{k,L,m}(j+2,2))/(EVAL_DATA{k,L,m}(j+2,1)-EVAL_DATA{k,L,m}(j-2,1));   % Calculate (1/(Asurf)(d(m)/dt) [kg/s/m2] (to find ignition time, duration of steady burning)
            end
        end
%         EVAL_DATA{k,L,m}(:,8)=movmean(EVAL_DATA{k,L,m}(:,7),5);            %Calculate running average of d(m*)/dt
    frames=21;
    order=3;
    EVAL_DATA{k,L,m}(:,8)=sgfilt(order,frames,EVAL_DATA{k,L,m}(:,7));     %Savitzky Golay HRR, quadratic, 13s invtreval: smoothed d(m*)/dt

%     TAB_DATA{m,1}(k,L)=find((EVAL_DATA{k,L,m}(:,5))>1,1);            %Calculate t_ignition as the first time when dm*dt_smooth>1 g/(s-m2)

%--------------Intitial/test plots of your data---------------------------
        clf
        hold on
        plot(EVAL_DATA{k,L,m}(:,1),EVAL_DATA{k,L,m}(:,7),'.b');
        plot(EVAL_DATA{k,L,m}(:,1),EVAL_DATA{k,L,m}(:,8),'k');
        title(filenames{i}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 inf 0 inf]);
        xlabel('time [s]');
        ylabel('(dm"/dt) [kg s^{-1} m^{-2}]');
        yyaxis right
        plot(EVAL_DATA{k,L,m}(:,1),EVAL_DATA{k,L,m}(:,6),'.r');
        axis([0 inf 300 inf]);
        ylabel('Temperature [K]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, filenames{i}(1:end-4)]));
        print(fig_filename,'-dpdf')
    end
end
close

%% Analyze Time Resolved Gasification dm/dt Data with q"=25kWm-2
MLR25=NaN*ones(901,max(max(Test_count(3,1:15)))+3,N_Labs);
time25=[0:1200]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==17 | m==20        % Just 25 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,1200));
%         MLR25(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,7); % pull in (up to) the first 1200 rows/timesteps of MLR data
        MLR25(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,8); % pull in (up to) the first 1200 rows/timesteps of smoothed MLR data
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=MLR25(1:last,:,k);
            temp(temp==0)=NaN;
            MLR25(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
                if k~=5
                    MLR25(ix,L+1,k)=nnz(MLR25((ix-2:ix+2),(1:L),k));
                    MLR25(ix,L+2,k)=nanmean(MLR25((ix-2:ix+2),(1:L),k),'all');
                    MLR25(ix,L+3,k)=nanstd(MLR25((ix-2:ix+2),(1:L),k),0,'all');
                    MLR25(ix,L+4,k)=MLR25(ix,L+3,k)/sqrt(MLR25(ix,L+1,k));
                elseif k==5 % GIDAZE data is reported at ~(1/5 Hz) so we shouldn't average +/-2s
                    MLR25(ix,L+1,k)=nnz(MLR25((ix-0:ix+0),(1:L),k));
                    MLR25(ix,L+2,k)=nanmean(MLR25((ix-0:ix+0),(1:L),k),'all');
                    MLR25(ix,L+3,k)=nanstd(MLR25((ix-0:ix+0),(1:L),k),0,'all');
                    MLR25(ix,L+4,k)=MLR25(ix,L+3,k)/sqrt(MLR25(ix,L+1,k));
                end

            end
%             MLR25(1:last,L+2,k)=sgfilt(3,15,MLR25(1:last,L+2,k));,
            clear temp
            hold on
            for ix=1:L
                plot(time25(1:last),MLR25(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time25(1:last),MLR25(1:last,L+2,k),[2*MLR25(1:last,L+4,k) 2*MLR25(1:last,L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time25(1:last),MLR25(1:last,L+2,k),'k','LineWidth',2);
            end
%                 plot(time25(1:last),MLR25(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 1000 0 0.025]);
            xlabel('time [s]');
            ylabel('dm"/dt [kg s^{-1}m^{-2}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, LabNames{k},'_', Test_types{m} '_smoothed']));
        print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
end
clear last
close

% Plot average MLR curves together
figure('Renderer', 'painters', 'Position', [100 100 650 350])
hold on
title('Gasification Experiments, q^"_{ext}=25kW m^{-2}');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
axis([0 1000 0 0.0325]);
xlabel('time [s]');
ylabel('dm"/dt [kg s^{-1}m^{-2}]');
i_legend=0;
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==17 | m==20        % Just 25 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,1200));
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            shadedErrorBar(time25(1:last),MLR25(1:last,L+2,k),[2*MLR25(1:last,L+4,k) 2*MLR25(1:last,L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1}); %plot with shaded error bards = 2stdevmean
            i_legend=i_legend+1;
            legend_counter(i_legend)=k;
            legend_counter_test(i_legend)=m;
        end
    end
end

for i=1:length(legend_counter)
    str{i,1}={QMJHL{legend_counter(i)},Test_types{legend_counter_test(i)}};
    legend_final{i,1}=strjoin(str{i}, ', ');
end
%manually add legen entry for CAPA Data
shadedErrorBar(EXP_DATA{13,1,1}(:,1),EXP_DATA{13,1,1}(:,2),[EXP_DATA{13,1,1}(:,4) EXP_DATA{13,1,1}(:,4)],'lineprops', {'color', rgb(Colors{13}),'LineWidth',1}) % ADD in UMD CAPA DATA
str{end+1,1}={QMJHL{13},Test_types{1}};
legend_final{end+1}=strjoin(str{end}, ', ');
% legend(QMJHL{[legend_counter 13]},'Location','eastoutside');
legend(legend_final,'Location','northeast', 'Interpreter','none');
            h=3.75;                                  % height of plot in inches
            w=6.5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, 'Gasification_25kW_dmdt_smoothed']));
        print(fig_filename,'-dpdf')
clear i_legend legend_counter legend_final str
close% Close figure




%% Analyze Time Resolved Gasification dm/dt Data with q"=50kWm-2
MLR50=NaN*ones(401,max(max(Test_count(3,1:15)))+3,N_Labs);
time50=[0:400]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==18 | m==21        % Just 50 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,400));
        MLR50(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,8); % pull in (up to) the first 1200 rows/timesteps of MLR data
%         MLR50(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,8); % pull in (up to) the first 1200 rows/timesteps of smoothed MLR data
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=MLR50(1:last,:,k);
            temp(temp==0)=NaN;
            MLR50(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
                if k~=5
                    MLR50(ix,L+1,k)=nnz(MLR50((ix-2:ix+2),(1:L),k));
                    MLR50(ix,L+2,k)=nanmean(MLR50((ix-2:ix+2),(1:L),k),'all');
                    MLR50(ix,L+3,k)=nanstd(MLR50((ix-2:ix+2),(1:L),k),0,'all');
                    MLR50(ix,L+4,k)=MLR50(ix,L+3,k)/sqrt(MLR50(ix,L+1,k));
                elseif k==5 % GIDAZE data is reported at ~(1/5 Hz) so we shouldn't average +/-2s
                    MLR50(ix,L+1,k)=nnz(MLR50((ix-0:ix+0),(1:L),k));
                    MLR50(ix,L+2,k)=nanmean(MLR50((ix-0:ix+0),(1:L),k),'all');
                    MLR50(ix,L+3,k)=nanstd(MLR50((ix-0:ix+0),(1:L),k),0,'all');
                    MLR50(ix,L+4,k)=MLR50(ix,L+3,k)/sqrt(MLR50(ix,L+1,k));
                end

            end
%             MLR50(1:last,L+2,k)=sgfilt(3,15,MLR50(1:last,L+2,k));,
            clear temp
            hold on
            for ix=1:L
                plot(time50(1:last),MLR50(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time50(1:last),MLR50(1:last,L+2,k),[2*MLR50(1:last,L+4,k) 2*MLR50(1:last,L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time50(1:last),MLR50(1:last,L+2,k),'k','LineWidth',2);
            end
%                 plot(time50(1:last),MLR50(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 400 0 0.05]);
            xlabel('time [s]');
            ylabel('dm"/dt [kg s^{-1}m^{-2}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, LabNames{k},'_', Test_types{m} '_smoothed']));
        print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
end
clear last
close

% Plot average MLR curves together
figure('Renderer', 'painters', 'Position', [100 100 650 350])
hold on
title('Gasification Experiments, q^"_{ext}=50kW m^{-2}');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
axis([0 400 0 0.05]);
xlabel('time [s]');
ylabel('dm"/dt [kg s^{-1}m^{-2}]');
i_legend=0;
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==18 | m==21        % Just 50 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,400));
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
             if  isnan(MLR50(10,L+2,k)) == 0
                shadedErrorBar(time50(1:last),MLR50(1:last,L+2,k),[2*MLR50(1:last,L+4,k) 2*MLR50(1:last,L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1}); %plot with shaded error bards = 2stdevmean
                i_legend=i_legend+1;
                legend_counter(i_legend)=k;
                legend_counter_test(i_legend)=m;
             end
        end
    end
end

for i=1:length(legend_counter)
    str{i,1}={QMJHL{legend_counter(i)},Test_types{legend_counter_test(i)}};
    legend_final{i,1}=strjoin(str{i}, ', ');
end

legend(legend_final,'Location','northwest', 'Interpreter','none');
            h=3.75;                                  % height of plot in inches
            w=6.5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, 'Gasification_50kW_dmdt_smoothed']));
        print(fig_filename,'-dpdf')

clear i_legend legend_counter legend_final str
close% Close figure





%% Analyze Time Resolved Gasification dm/dt Data with q"=65kWm-2
MLR65=NaN*ones(301,max(max(Test_count(3,1:15)))+3,N_Labs);
time65=[0:300]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==19 | m==22        % Just 65 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,300));
%         MLR65(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,7); % pull in (up to) the first 1200 rows/timesteps of MLR data
        MLR65(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,8); % pull in (up to) the first 1200 rows/timesteps of smoothed MLR data
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=MLR65(1:last,:,k);
            temp(temp==0)=NaN;
            MLR65(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
                if k~=5
                    MLR65(ix,L+1,k)=nnz(MLR65((ix-2:ix+2),(1:L),k));
                    MLR65(ix,L+2,k)=nanmean(MLR65((ix-2:ix+2),(1:L),k),'all');
                    MLR65(ix,L+3,k)=nanstd(MLR65((ix-2:ix+2),(1:L),k),0,'all');
                    MLR65(ix,L+4,k)=MLR65(ix,L+3,k)/sqrt(MLR65(ix,L+1,k));
                elseif k==5 % GIDAZE data is reported at ~(1/5 Hz) so we shouldn't average +/-2s
                    MLR65(ix,L+1,k)=nnz(MLR65((ix-0:ix+0),(1:L),k));
                    MLR65(ix,L+2,k)=nanmean(MLR65((ix-0:ix+0),(1:L),k),'all');
                    MLR65(ix,L+3,k)=nanstd(MLR65((ix-0:ix+0),(1:L),k),0,'all');
                    MLR65(ix,L+4,k)=MLR65(ix,L+3,k)/sqrt(MLR65(ix,L+1,k));
                end

            end
%             MLR65(1:last,L+2,k)=sgfilt(3,15,MLR65(1:last,L+2,k));,
            clear temp
            hold on
            for ix=1:L
                plot(time65(1:last),MLR65(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time65(1:last),MLR65(1:last,L+2,k),[2*MLR65(1:last,L+4,k) 2*MLR65(1:last,L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time65(1:last),MLR65(1:last,L+2,k),'k','LineWidth',2);
            end
%                 plot(time65(1:last),MLR65(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 300 0 0.06]);
            xlabel('time [s]');
            ylabel('dm"/dt [kg s^{-1}m^{-2}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, LabNames{k},'_', Test_types{m} '_smoothed']));
        print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
end
clear last
close

% Plot average MLR curves together
figure('Renderer', 'painters', 'Position', [100 100 650 350])
hold on
title('Gasification Experiments, q^"_{ext}=65kW m^{-2}');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
axis([0 300 0 0.06]);
xlabel('time [s]');
ylabel('dm"/dt [kg s^{-1}m^{-2}]');
i_legend=0;
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==19 | m==22        % Just 65 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,300));
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            shadedErrorBar(time65(1:last),MLR65(1:last,L+2,k),[2*MLR65(1:last,L+4,k) 2*MLR65(1:last,L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1}); %plot with shaded error bards = 2stdevmean
            i_legend=i_legend+1;
            legend_counter(i_legend)=k;
            legend_counter_test(i_legend)=m;
        end
    end
end

shadedErrorBar(EXP_DATA{13,1,2}(:,1),EXP_DATA{13,1,2}(:,2),[EXP_DATA{13,1,2}(:,4) EXP_DATA{13,1,2}(:,4)],'lineprops', {'color', rgb(Colors{13}),'LineWidth',1}) % ADD in UMD CAPA DATA
for i=1:length(legend_counter)
    str{i,1}={QMJHL{legend_counter(i)},Test_types{legend_counter_test(i)}};
    legend_final{i,1}=strjoin(str{i}, ', ');
end
str{end+1,1}={QMJHL{13},Test_types{2}};
legend_final{end+1}=strjoin(str{end}, ', ');
% legend(QMJHL{[legend_counter 13]},'Location','eastoutside');
legend(legend_final,'Location','southeast', 'Interpreter','none');
            h=3.75;                                  % height of plot in inches
            w=6.5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, 'Gasification_65kW_dmdt_smoothed']));
        print(fig_filename,'-dpdf')
clear i_legend legend_counter legend_final str
close% Close figure


%% Analyze Time Resolved Gasification Temperature Data with q"=25kWm-2
TEMP25=NaN*ones(1201,3*max(max(Test_count(3,1:15)))+3,N_Labs);
time25=[0:1200]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==17 | m==20        % Just 25 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,1200));
        for i_temp=1:3
            TEMP25(1:last,3*(L-1)+i_temp,k)=EVAL_DATA{k,L,m}(1:last,3+i_temp); % pull in (up to) the first 600 rows/timesteps of  TEMP data
        end
        clear i_temp
        %         TEMP25(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,6); % pull in (up to) the first 1200 rows/timesteps of TEMP data

        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=TEMP25(1:last,:,k);
            temp(temp==0)=NaN;
            TEMP25(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
%                 TEMP25(ix,L+1,k)=nnz(TEMP25((ix-2:ix+2),(1:L),k));
%                 TEMP25(ix,L+2,k)=nanmean(TEMP25((ix-2:ix+2),(1:L),k),'all');
%                 TEMP25(ix,L+3,k)=nanstd(TEMP25((ix-2:ix+2),(1:L),k),0,'all');
%                 TEMP25(ix,L+4,k)=TEMP25(ix,L+3,k)/sqrt(TEMP25(ix,L+1,k));
                TEMP25(ix,3*L+1,k)=nnz(TEMP25((ix-2:ix+2),(1:3*L),k));
                TEMP25(ix,3*L+2,k)=nanmean(TEMP25((ix-2:ix+2),(1:3*L),k),'all');
                TEMP25(ix,3*L+3,k)=nanstd(TEMP25((ix-2:ix+2),(1:3*L),k),0,'all');
                TEMP25(ix,3*L+4,k)=TEMP25(ix,3*L+3,k)/sqrt(TEMP25(ix,3*L+1,k));
            end
%             TEMP25(1:last,L+2,k)=sgfilt(3,15,TEMP25(1:last,L+2,k));,
            clear temp
            hold on
            for ix=1:3*L
                plot(time25(1:last),TEMP25(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time25(1:last),TEMP25(1:last,3*L+2,k),[2*TEMP25(1:last,3*L+4,k) 2*TEMP25(1:last,3*L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time25(1:last),TEMP25(1:last,3*L+2,k),'k','LineWidth',2);
            end
%                 plot(time25(1:last),TEMP25(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 750 300 800]);
            xlabel('time [s]');
            ylabel('Back Surface Temperature [K]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, LabNames{k},'_', Test_types{m} '_Temp']));
        print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
end
clear last
close

% Plot average TEMP curves together
figure('Renderer', 'painters', 'Position', [100 100 650 350])
hold on
title('Gasification Experiments, q^"_{ext}=25kW m^{-2}');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
axis([0 650 300 700]);
xlabel('time [s]');
ylabel('Surface Temperature [K]');
i_legend=0;
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==17 | m==20        % Just 25 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,1200));
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            if  isnan(TEMP25(10,3*L+2,k)) == 0
                shadedErrorBar(time25(1:last),TEMP25(1:last,3*L+2,k),[2*TEMP25(1:last,3*L+4,k) 2*TEMP25(1:last,3*L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1 }); %plot with shaded error bards = 2stdevmean
                %             shadedErrorBar(time25(1:last),TEMP25(1:last,L+2,k),[2*TEMP25(1:last,L+4,k) 2*TEMP25(1:last,L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1}); %plot with shaded error bards = 2stdevmean
                i_legend=i_legend+1;
                legend_counter(i_legend)=k;
                legend_counter_test(i_legend)=m;
            end
        end
    end
end


for i=1:length(legend_counter)
    str{i,1}={QMJHL{legend_counter(i)},Test_types{legend_counter_test(i)}};
    legend_final{i,1}=strjoin(str{i}, ', ');
end
% Add in CAPA Data (custom error bars)
shadedErrorBar(EXP_DATA{13,2,1}(:,1),EXP_DATA{13,2,1}(:,3),[EXP_DATA{13,2,1}(:,5) EXP_DATA{13,2,1}(:,5)],'lineprops', {'color', rgb(Colors{13}),'LineWidth',1}) % ADD in UMD CAPA DATA
str{end+1,1}={QMJHL{13},Test_types{2}};
legend_final{end+1}=strjoin(str{end}, ', ');
% legend(QMJHL{[legend_counter 13]},'Location','eastoutside');
legend(legend_final,'Location','southeast', 'Interpreter','none');
            h=3.75;                                  % height of plot in inches
            w=6.5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, 'Gasification_25kW_Temperature']));
        print(fig_filename,'-dpdf')
clear i_legend legend_counter legend_final str
close% Close figure


%% Analyze Time Resolved Gasification Temperature Data with q"=50kWm-2
TEMP50=NaN*ones(401,3*max(max(Test_count(3,1:15)))+3,N_Labs);
time50=[0:400]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==18 | m==21        % Just 50 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,400));
        for i_temp=1:3
            TEMP50(1:last,3*(L-1)+i_temp,k)=EVAL_DATA{k,L,m}(1:last,3+i_temp); % pull in (up to) the first 600 rows/timesteps of  TEMP data
        end
        %         TEMP50(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,6); % pull in (up to) the first 1200 rows/timesteps of TEMP data
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=TEMP50(1:last,:,k);
            temp(temp==0)=NaN;
            TEMP50(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
%             TEMP50(ix,L+1,k)=nnz(TEMP50((ix-2:ix+2),(1:L),k));
%             TEMP50(ix,L+2,k)=nanmean(TEMP50((ix-2:ix+2),(1:L),k),'all');
%             TEMP50(ix,L+3,k)=nanstd(TEMP50((ix-2:ix+2),(1:L),k),0,'all');
%             TEMP50(ix,L+4,k)=TEMP50(ix,L+3,k)/sqrt(TEMP50(ix,L+1,k));
            TEMP50(ix,3*L+1,k)=nnz(TEMP50((ix-2:ix+2),(1:3*L),k));
            TEMP50(ix,3*L+2,k)=nanmean(TEMP50((ix-2:ix+2),(1:3*L),k),'all');
            TEMP50(ix,3*L+3,k)=nanstd(TEMP50((ix-2:ix+2),(1:3*L),k),0,'all');
            TEMP50(ix,3*L+4,k)=TEMP50(ix,3*L+3,k)/sqrt(TEMP50(ix,3*L+1,k));
            end
%             TEMP50(1:last,L+2,k)=sgfilt(3,15,TEMP50(1:last,L+2,k));,
            clear temp
            hold on
            for ix=1:3*L
                plot(time50(1:last),TEMP50(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time50(1:last),TEMP50(1:last,3*L+2,k),[2*TEMP50(1:last,3*L+4,k) 2*TEMP50(1:last,3*L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time50(1:last),TEMP50(1:last,3*L+2,k),'k','LineWidth',2);
            end
%                 plot(time50(1:last),TEMP50(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 300 0 900]);
            xlabel('time [s]');
            ylabel('Back Surface Temperature [K]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, LabNames{k},'_', Test_types{m} '_Temp']));
        print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
end
clear last
close

% Plot average TEMP curves together
figure('Renderer', 'painters', 'Position', [100 100 650 350])
hold on
title('Gasification Experiments, q^"_{ext}=50kW m^{-2}');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
axis([0 250 300 700]);
xlabel('time [s]');
ylabel('Front Surface Temperature [K]');
i_legend=0;
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==18 | m==21        % Just 50 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,400));
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            if isnan(TEMP50(10,3*L+2,k))==0
                shadedErrorBar(time50(1:last),TEMP50(1:last,3*L+2,k),[2*TEMP50(1:last,3*L+4,k) 2*TEMP50(1:last,3*L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1 }); %plot with shaded error bards = 2stdevmean
        %             shadedErrorBar(time50(1:last),TEMP50(1:last,L+2,k),[2*TEMP50(1:last,L+4,k) 2*TEMP50(1:last,L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1}); %plot with shaded error bards = 2stdevmean
                i_legend=i_legend+1;
                legend_counter(i_legend)=k;
                legend_counter_test(i_legend)=m;
            end
        end
    end
end


for i=1:length(legend_counter)
    str{i,1}={QMJHL{legend_counter(i)},Test_types{legend_counter_test(i)}};
    legend_final{i,1}=strjoin(str{i}, ', ');
end

legend(legend_final,'Location','southeast', 'Interpreter','none');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, 'Gasification_50kW_Temperature']));
        print(fig_filename,'-dpdf')
clear i_legend legend_counter legend_final str
close% Close figure

%% Analyze Time Resolved Gasification Temperature Data with q"=65kWm-2
TEMP65=NaN*ones(301,3*max(max(Test_count(3,1:15)))+3,N_Labs);
time65=[0:300]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==19 | m==22        % Just 65 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,300));
        for i_temp=1:3
            TEMP65(1:last,3*(L-1)+i_temp,k)=EVAL_DATA{k,L,m}(1:last,3+i_temp); % pull in (up to) the first 600 rows/timesteps of TEMP data
        end
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=TEMP65(1:last,:,k);
            temp(temp==0)=NaN;
            TEMP65(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
            TEMP65(ix,3*L+1,k)=nnz(TEMP65((ix-2:ix+2),(1:3*L),k));
            TEMP65(ix,3*L+2,k)=nanmean(TEMP65((ix-2:ix+2),(1:3*L),k),'all');
            TEMP65(ix,3*L+3,k)=nanstd(TEMP65((ix-2:ix+2),(1:3*L),k),0,'all');
            TEMP65(ix,3*L+4,k)=TEMP65(ix,3*L+3,k)/sqrt(TEMP65(ix,3*L+1,k));
%             TEMP65(ix,L+1,k)=nnz(TEMP65((ix-2:ix+2),(1:L),k));
%             TEMP65(ix,L+2,k)=nanmean(TEMP65((ix-2:ix+2),(1:L),k),'all');
%             TEMP65(ix,L+3,k)=nanstd(TEMP65((ix-2:ix+2),(1:L),k),0,'all');
%             TEMP65(ix,L+4,k)=TEMP65(ix,L+3,k)/sqrt(TEMP65(ix,L+1,k));
            end
%             TEMP65(1:last,L+2,k)=sgfilt(3,15,TEMP65(1:last,L+2,k));,
            clear temp
            hold on
            for ix=1:3*L
                plot(time65(1:last),TEMP65(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time65(1:last),TEMP65(1:last,3*L+2,k),[2*TEMP65(1:last,3*L+4,k) 2*TEMP65(1:last,3*L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time65(1:last),TEMP65(1:last,3*L+2,k),'k','LineWidth',2);
            end
%                 plot(time65(1:last),TEMP65(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 300 300 1000]);
            xlabel('time [s]');
            ylabel('Back Surface Temperature [K]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, LabNames{k},'_', Test_types{m} '_Temp']));
        print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
end
clear last
close

% Plot average TEMP curves together
figure('Renderer', 'painters', 'Position', [100 100 650 350])
hold on
title('Gasification Experiments, q^"_{ext}=65kW m^{-2}');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
axis([0 250 300 700]);
xlabel('time [s]');
ylabel('Surface Temperature [K]');
i_legend=0;
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==19 | m==22        % Just 65 kW FPA and Gasification Tests
        last = min(min(N_rows_all(k,:,m)-1,300));
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
           if isnan(TEMP65(10,3*L+2,k))==0
                shadedErrorBar(time65(1:last),TEMP65(1:last,3*L+2,k),[2*TEMP65(1:last,3*L+4,k) 2*TEMP65(1:last,3*L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1 }); %plot with shaded error bards = 2stdevmean
                %             shadedErrorBar(time65(1:last),TEMP65(1:last,L+2,k),[2*TEMP65(1:last,L+4,k) 2*TEMP65(1:last,L+4,k)],'lineprops', {'color', rgb(Colors{k}),'LineWidth',1}); %plot with shaded error bards = 2stdevmean
                i_legend=i_legend+1;
                legend_counter(i_legend)=k;
                legend_counter_test(i_legend)=m;
            end
        end
    end
end

for i=1:length(legend_counter)
    str{i,1}={QMJHL{legend_counter(i)},Test_types{legend_counter_test(i)}};
    legend_final{i,1}=strjoin(str{i}, ', ');
end
% Add in CAPA Data (custom error bars)
shadedErrorBar(EXP_DATA{13,2,2}(:,1),EXP_DATA{13,2,2}(:,3),[EXP_DATA{13,2,2}(:,5) EXP_DATA{13,2,2}(:,5)],'lineprops', {'color', rgb(Colors{13}),'LineWidth',1}) % ADD in UMD CAPA DATA
str{end+1,1}={QMJHL{13},Test_types{2}};
legend_final{end+1}=strjoin(str{end}, ', ');
% legend(QMJHL{[legend_counter 13]},'Location','eastoutside');
legend(legend_final,'Location','northeast', 'Interpreter','none');
            h=3.75;                                  % height of plot in inches
            w=6.5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, 'Gasification_65kW_Temperature']));
        print(fig_filename,'-dpdf')
clear i_legend legend_counter legend_final str
close% Close figure