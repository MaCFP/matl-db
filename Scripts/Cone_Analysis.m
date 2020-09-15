clear all
close all
clc
load Exp_Data.mat% This uses the related script 'Import_Data.m'

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

%% 
%Read in all of your data  EXP_DATA is a 3D cell array of indexing {LabName,k | Test #, L | Test Type,m}   
%Inside of each cell is a 2D array of indexing [timestep, data type]

% Create EVAL_DATA= [ t | m/m0 | HRR | T1 | T2 | T3 | Tavg | HRR_smooth| smooth d(HRR_smooth)/dt | THR] (all values interpolated to 1Hz)
figure
for i = 1:N_files   % Loop through all of your data sets
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m>=3 && m<=5
        t_start=round(min(EXP_DATA{k,L,m}(:,1)));   %find first timestep (rounded to nearest integer)
        t_end=round(max(EXP_DATA{k,L,m}(:,1)));     %find last timestep (rounded to nearest integer)
        m0=mean(EXP_DATA{k,L,m}(1:5,2));
        EVAL_DATA{k,L,m}(:,1)=[t_start:t_end-1]';                                                               % interpolate time step from 0 to t_end at 1 Hz
        EVAL_DATA{k,L,m}(:,2)=interp1(EXP_DATA{k,L,m}(:,1),EXP_DATA{k,L,m}(:,2), EVAL_DATA{k,L,m}(:,1))/m0;     % interpolate mass, normalize by m0
        EVAL_DATA{k,L,m}(:,3)=interp1(EXP_DATA{k,L,m}(:,1),EXP_DATA{k,L,m}(:,3), EVAL_DATA{k,L,m}(:,1));        % interpolate HRR
        if k~=7
            EVAL_DATA{k,L,m}(:,8)=sgolayfilt(EVAL_DATA{k,L,m}(:,3),2,5);                                        % Calculate smoothed HRR
        elseif k==7
            EVAL_DATA{k,L,m}(:,8)=(EVAL_DATA{k,L,m}(:,3));                                                      % Keep raw data for LCPP b/c of 0.2 Hz output
        end
        TAB_DATA{m,1}(k,L)=min(find((EVAL_DATA{k,L,m}(:,3))>24));              %Calculate t_ignition as the first time when HRR_smooth>24 kW/m2
        TAB_DATA{m,2}(k,L)=min(find((EVAL_DATA{k,L,m}(:,3))>240));             %Calculate t_100_0 as the first time when HRR_smooth>100 kW/m2
        TAB_DATA{m,3}(k,L)=max(find((EVAL_DATA{k,L,m}(:,3))>240));             %Calculate t_100_0 as the last time when HRR_smooth>100 kW/m2
        TAB_DATA{m,4}(k,L)=m0;
        Ncols=size(EXP_DATA{k,L,m}(:,:),2);         % Find out how many TCs / temp measurements were provided in this test
        N_rows_i(i)=size(EXP_DATA{k,L,m}(:,:),1);
        N_rows_all(k,L,m)=size(EXP_DATA{k,L,m}(:,:),1);
%         temp1=EVAL_DATA{k,L,m}(:,:);
%         temp2=EXP_DATA{k,L,m}(:,:);
        % Interpolate and average Temperatures
        if Ncols>=4
            for j =4:Ncols
                 EVAL_DATA{k,L,m}(:,j)=interp1(EXP_DATA{k,L,m}(:,1),EXP_DATA{k,L,m}(:,j), EVAL_DATA{k,L,m}(:,1));       %interpolate Temps
            end
            for j = 1:N_rows_all(k,L,m)-2%(t_end-t_start)                           %Find out duration of Temp measurement data (!!this only works for indexing b/c we're at 1Hz!!)
                EVAL_DATA{k,L,m}(j,7)=mean(nonzeros(EVAL_DATA{k,L,m}(j,4:Ncols)));  %Average all temp measurements at that timestep
            end
        end
         
        for j = 1:N_rows_all(k,L,m)-2%(t_end-t_start)                                               %Find out duration of Temp measurement data (!!this only works for indexing b/c we're at 1Hz!!)
            if j~=1 && j~=(N_rows_all(k,L,m)-2)
                EVAL_DATA{k,L,m}(j,9)=(EVAL_DATA{k,L,m}(j+1,8)-EVAL_DATA{k,L,m}(j-1,8))/(EVAL_DATA{k,L,m}(j+1,1)-EVAL_DATA{k,L,m}(j-1,1));   % Calculate d(HRR_smooth)/dt (to find ignition time, duration of steady burning) 
            end
        end
        EVAL_DATA{k,L,m}(:,9)=movmean(EVAL_DATA{k,L,m}(:,9),5);   % Calculate running average of d(HRR_smooth)/dt [5s interval, +/- 2 s]
    %     EVAL_DATA{k,L,m}(:,9)=sgolayfilt(EVAL_DATA{k,L,m}(:,9),2,13);     %Savitzky Golay HRR, quadratic, 13s invtreval: smoothed d(HRR_smooth)/dt
        
            p_end=size(EVAL_DATA{k,L,m},1); 
        for p=1:p_end                 %Calculate [4] total heat flow and [5] dT/dt (+/- one time step, delta_T=1k]
            if p==1
            EVAL_DATA{k,L,m}(p,10)=0;
            elseif p<p_end
            EVAL_DATA{k,L,m}(p,10)=EVAL_DATA{k,L,m}(p-1,10)+0.5*(EVAL_DATA{k,L,m}(p-1,8)+EVAL_DATA{k,L,m}(p,8))*(EVAL_DATA{k,L,m}(p,1)-EVAL_DATA{k,L,m}(p-1,1));  %Integral heat flow
            else
            EVAL_DATA{k,L,m}(p,10)=EVAL_DATA{k,L,m}(p-1,10)+0.5*(EVAL_DATA{k,L,m}(p-1,8)+EVAL_DATA{k,L,m}(p,8))*(EVAL_DATA{k,L,m}(p,1)-EVAL_DATA{k,L,m}(p-1,1));  %Integral heat flow    
            end
        end
        clear p_end 
        
%          Intitial/test plots of your data
        clf
        hold on
        plot(EVAL_DATA{k,L,m}(:,1),EVAL_DATA{k,L,m}(:,3),'.');
        plot(EVAL_DATA{k,L,m}(:,1),EVAL_DATA{k,L,m}(:,8));
        title(filenames{i}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 600 0 1500]);
        xlabel('time [s]');
        ylabel('HRR [kW m^{-2}]');
        fig_filename=fullfile(char([Script_Figs_dir, filenames{i}(1:end-4)]));
        print(fig_filename,'-dpdf')
    end
end
close

%% Analyze Tabulated Values
%Ignition Time
for m=3:5
    N_Labs_cone=size(TAB_DATA{m,1},1);
    temp=TAB_DATA{m,1}(:,:);
    temp(temp==0)=NaN;
    TAB_DATA{m,1}(:,:)=temp;
    for k=1:N_Labs_cone
        TAB_DATA{m,1}(k,max(max(Test_count(m,1:N_Labs_cone)))+1)=mean(TAB_DATA{m,1}(k,1:max(max(Test_count(m,1:N_Labs_cone)))),'omitnan');       %Calculate mean of t_ignition for this lab
        TAB_DATA{m,1}(k,max(max(Test_count(m,1:N_Labs_cone)))+2)=std(TAB_DATA{m,1}(k,1:max(max(Test_count(m,1:N_Labs_cone)))),'omitnan');       %Calculate stdev of t_ignition for this lab
    end
end
clear temp N_Labs_cone
figure
histogram(TAB_DATA{3,1}(:,1:4),10)
        title("Ignition Time", 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([60 160 0 10]);
        xlabel('time [s]');
        ylabel('Frequency');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner    
        fig_filename=fullfile(char([Script_Figs_dir, 'Cone_IgnTime_histogram']));
        print(fig_filename,'-dpdf')
close

% Heat of Combustion, Hc [kJ/g]
for m=3:5
    N_Labs_cone=size(TAB_DATA{m,1},1);
    for k=1:N_Labs_cone
        N_tests_cone=Test_count(m,k);
        for L=1:N_tests_cone
            if TAB_DATA{m,2}(k,L)~=0 && TAB_DATA{m,3}(k,L)~=0
                Total_MassLoss=TAB_DATA{m,4}(k,L)*(EVAL_DATA{k,L,m}(TAB_DATA{m,2}(k,L),2)-EVAL_DATA{k,L,m}(TAB_DATA{m,3}(k,L),2));      % m0*((mass at tHRR_init>100)-(mass at tHRR_final>100))
                Total_HeatRelease= Asurf(k)*(EVAL_DATA{k,L,m}(TAB_DATA{m,3}(k,L),10)-EVAL_DATA{k,L,m}(TAB_DATA{m,2}(k,L),10));                      % (THR at tHRR_final>100)-(THR at tHRR_int>100))
                TAB_DATA{m,5}(k,L)=Total_HeatRelease/Total_MassLoss;
                clear Total_MassLoss Total_HeatRelease
            end
        end
    end
end
clear N_Labs_cone N_tests_cone

for m=3:5
    N_Labs_cone=size(TAB_DATA{m,5},1);
    temp=TAB_DATA{m,5}(:,:);
    temp(temp==0)=NaN;
    TAB_DATA{m,5}(:,:)=temp;
    for k=1:N_Labs_cone
        TAB_DATA{m,5}(k,max(max(Test_count(m,1:N_Labs_cone)))+1)=mean(TAB_DATA{m,5}(k,1:max(max(Test_count(m,1:N_Labs_cone)))),'omitnan');       %Calculate mean of t_ignition for this lab
        TAB_DATA{m,5}(k,max(max(Test_count(m,1:N_Labs_cone)))+2)=std(TAB_DATA{m,5}(k,1:max(max(Test_count(m,1:N_Labs_cone)))),'omitnan');       %Calculate stdev of t_ignition for this lab
    end
end
clear N_Labs_cone 
close all

%% Analyze Time Resolved Cone HRR Data with q"=25kWm-2
HRR25=NaN*ones(901,max(max(Test_count(3,1:15)))+3,N_Labs);
time25=[0:900]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==3        % Just 25 kW Cone Tests
        last = min(min(N_rows_all(k,:,m)-1,900));    
        HRR25(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 600 rows/timesteps of HRR data
%         HRR25(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,8); % pull in (up to) the first 600 rows/timesteps of smoothed HRR data
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=HRR25(1:last,:,k);
            temp(temp==0)=NaN;
            HRR25(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%                 HRR25(ix,L+1,k)=nnz(~isnan(HRR25(ix,(1:L),k)));         % N, # of values at this timestep; L+1
%                 HRR25(ix,L+2,k)=mean(HRR25(ix,(1:L),k),'omitnan');      % mean of N values at this timestep; L+2
%                 HRR25(ix,L+3,k)=std(HRR25(ix,(1:L),k),'omitnan');       % stdev of N values at this timestep; L+3
%                 HRR25(ix,L+4,k)=HRR25(ix,L+3,k)/sqrt(HRR25(ix,L+1,k));  % stdev,mean of N values at this timestep; L+4
            
%             Calculate mean and stdeviation +/- 2 timesteps
            HRR25(ix,L+1,k)=nnz(HRR25((ix-2:ix+2),(1:L),k));
            HRR25(ix,L+2,k)=nanmean(HRR25((ix-2:ix+2),(1:L),k),'all');
            HRR25(ix,L+3,k)=nanstd(HRR25((ix-2:ix+2),(1:L),k),0,'all');
            HRR25(ix,L+4,k)=HRR25(ix,L+3,k)/sqrt(HRR25(ix,L+1,k));
            
            end
%             HRR25(1:last,L+2,k)=sgolayfilt(HRR25(1:last,L+2,k),3,15);,
            clear temp
            hold on
            for ix=1:L
                plot(time25(1:last),HRR25(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time25(1:last),HRR25(1:last,L+2,k),[2*HRR25(1:last,L+4,k) 2*HRR25(1:last,L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time25(1:last),HRR25(1:last,L+2,k),'k','LineWidth',2);
            end
%                 plot(time25(1:last),HRR25(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{3}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 600 0 800]);
            xlabel('time [s]');
            ylabel('HRR [kW m^{-2}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner    
        fig_filename=fullfile(char([Script_Figs_dir, LabNames{k} ,'_', Test_types{3}, '_HRR']));
        print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
end
clear last 
close% Close figure
%% Combine all of your HRR data from individual cone test at q"=25kW
HRR25_all=zeros(901, Test_count(3,end)+4);
col_old=0;
for k=1:N_Labs
    if Test_count(3,k)~=0
        col_new=Test_count(3,k);
        HRR25_all(:,col_old+1:(col_old+col_new))=HRR25(:,1:col_new,k);
        col_old=col_old+col_new;
    end
end
clear col_new col_old
% col_new=1;
for k=1:N_Labs
%     if Test_count(3,k)~=0
%         col_new=col_new+1;
        HRR25_all_avg(:,k)=HRR25(:,Test_count(3,k)+2,k);
%     end
end
% clear col_new 

HRR25_all(HRR25_all==0)=NaN;
% Do some Statistics now that you have all of your data together
%Avoid [12,13 (HK Poly data is wrong] and [14-17 (LCPP is underresolved)]
% for ix=1:550
%     HRR25_all(ix,(Test_count(3,end)+1))=nnz(~isnan(HRR25_all((ix),[1:11 18:Test_count(3,end)])));          % Count, N
%     HRR25_all(ix,(Test_count(3,end)+2))=mean(HRR25_all((ix),[1:11 18:Test_count(3,end)]),'omitnan');        % mean
%     HRR25_all(ix,(Test_count(3,end)+3))=std(HRR25_all((ix),[1:11 18:Test_count(3,end)]),'omitnan');         % stdmean (all data +/- 1 s
%     HRR25_all(ix,(Test_count(3,end)+4))=HRR25_all(ix,(Test_count(3,end)+3))/sqrt(HRR25_all(ix,Test_count(3,end)+1));  % stdev mean
% end


%Calculate mean and stdeviation +/- 0 timesteps
for ix=1:900
    HRR25_all(ix,(Test_count(3,end)+1))=nnz(HRR25_all((ix-0:ix+0),[1:11 14:Test_count(3,end)]));          % Count, N
    HRR25_all(ix,(Test_count(3,end)+2))=nanmean(HRR25_all((ix-0:ix+0),[1:11 14:Test_count(3,end)]),'all');        % mean
    HRR25_all(ix,(Test_count(3,end)+3))=nanstd(HRR25_all((ix-0:ix+0),[1:11 14:Test_count(3,end)]),0,'all');         % stdmean (all data +/- 1 s
    HRR25_all(ix,(Test_count(3,end)+4))=HRR25_all(ix,(Test_count(3,end)+3))/sqrt(HRR25_all(ix,Test_count(3,end)+1));  % stdev mean
end

    

% %plot Average with shaded errorbars WITH avg HRR curves from all Labs
% figure('Renderer', 'painters', 'Position', [100 100 650 350])
% hold on
% i_legend=0;
% for k=1:N_Labs %size(HRR25_all_avg,2)
% %     if k~=6
%         if  isnan(HRR25_all_avg(20,k)) == 0
%             i_legend=i_legend+1;
%             legend_counter(i_legend,1)=k;
%             h(i_legend)=plot(time25(:),HRR25_all_avg(:,k),'.','Color',rgb(Colors{k}),'DisplayName',QMJHL{k});
%         end    
% %     end
% end
%         shadedErrorBar(time25,(HRR25_all(:,Test_count(3,end)+2)),[2*(HRR25_all(:,Test_count(3,end)+4)) 2*(HRR25_all(:,Test_count(3,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         title(char(Test_types{3}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
%         axis([0 600 0 800]);
%         xlabel('time [s]');
%         ylabel('HRR [kW m^{-2}]');
% %         legend(QMJHL{legend_counter},'Location','eastoutside');
%         legend(h,'Location','eastoutside');
%             h=4.5;                                  % height of plot in inches
%             w=6;                                  % width of plot in inches
%             set(gcf, 'PaperSize', [w h]);           % set size of PDF page
%             set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner    
%         fig_filename=fullfile(char([Script_Figs_dir, Test_types{3}, '_avgHRR']));
%         print(fig_filename,'-dpdf')
%         clear i_legend legend_counter h

%plot Average with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 800 550])
hold on
i_legend=0;
for k=1:N_Labs
    for L=1:Test_count(3,k)
        if  isnan(HRR25(20,L,k))==0 && (HRR25_all_avg(20,k))~=0
        i_legend=i_legend+1;
        legend_counter(i_legend,1)=k;
        h(i_legend)=plot(time25(:),HRR25(1:size(time25(:),1),L,k),'.','MarkerSize',7.5,'Color',rgb(Colors{k}),'DisplayName',QMJHL{k});
        end
    end
end

% for k=1:Test_count(3,end) 
%     if k<= 11 | k>=18
%         plot(time25(:),HRR25_all(:,k),'.');
%     end
% end
        
        title(char(Test_types{3}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 600 0 800]);
        xlabel('time [s]');
        ylabel('HRR [kW m^{-2}]');
        legend(h,'Location','eastoutside');
            h=6;                                  % height of plot in inches
            w=8;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner            
        fig_filename=fullfile(char([Script_Figs_dir, Test_types{3} '_indivHRR_noavg']));
        print(fig_filename,'-dpdf')
%         shadedErrorBar(time25,(HRR25_all(:,Test_count(3,end)+2)),[2*(HRR25_all(:,Test_count(3,end)+4)) 2*(HRR25_all(:,Test_count(3,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         fig_filename=fullfile(char([Script_Figs_dir, Test_types{3} '_indivHRR']));
%         print(fig_filename,'-dpdf')
        clear i_legend legend_counter h 
close all

%% Analyze Time Resolved Cone HRR Data with q"=50kWm-2
HRR50=NaN*ones(401,max(max(Test_count(3,1:15)))+3,N_Labs);
time50=[0:400]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==4        % Just 50 kW Cone Tests
        last = min(min(N_rows_all(k,:,m)-1,400));    
        HRR50(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 600 rows/timesteps of HRR data
%         HRR50(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,8); % pull in (up to) the first 600 rows/timesteps of smoothed HRR data
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=HRR50(1:last,:,k);
            temp(temp==0)=NaN;
            HRR50(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%                 HRR50(ix,L+1,k)=nnz(~isnan(HRR50(ix,(1:L),k)));         % N, # of values at this timestep; L+1
%                 HRR50(ix,L+2,k)=mean(HRR50(ix,(1:L),k),'omitnan');      % mean of N values at this timestep; L+2
%                 HRR50(ix,L+3,k)=std(HRR50(ix,(1:L),k),'omitnan');       % stdev of N values at this timestep; L+3
%                 HRR50(ix,L+4,k)=HRR50(ix,L+3,k)/sqrt(HRR50(ix,L+1,k));  % stdev,mean of N values at this timestep; L+4
            
%             Calculate mean and stdeviation +/- 2 timesteps
            HRR50(ix,L+1,k)=nnz(HRR50((ix-2:ix+2),(1:L),k));
            HRR50(ix,L+2,k)=nanmean(HRR50((ix-2:ix+2),(1:L),k),'all');
            HRR50(ix,L+3,k)=nanstd(HRR50((ix-2:ix+2),(1:L),k),0,'all');
            HRR50(ix,L+4,k)=HRR50(ix,L+3,k)/sqrt(HRR50(ix,L+1,k));
            
            end
%             HRR50(1:last,L+2,k)=sgolayfilt(HRR50(1:last,L+2,k),3,15);,
            clear temp
            hold on
            for ix=1:L
                plot(time50(1:last),HRR50(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time50(1:last),HRR50(1:last,L+2,k),[2*HRR50(1:last,L+4,k) 2*HRR50(1:last,L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time50(1:last),HRR50(1:last,L+2,k),'k','LineWidth',2);
            end
%                 plot(time50(1:last),HRR50(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{4}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 300 0 1300]);
            xlabel('time [s]');
            ylabel('HRR [kW m^{-2}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
        fig_filename=fullfile(char([Script_Figs_dir, LabNames{k} ,'_',Test_types{4}, '_HRR']));
        print(fig_filename,'-dpdf')
            clear ix
            clf
        end
    end
end
clear last 
close all

%% Combine all of your HRR data from individual cone test at q"=50kW
HRR50_all=zeros(401, Test_count(4,end)+4);
col_old=0;
for k=1:N_Labs
    if Test_count(4,k)~=0
        col_new=Test_count(4,k);
        HRR50_all(:,col_old+1:(col_old+col_new))=HRR50(:,1:col_new,k);
        col_old=col_old+col_new;
    end
end
clear col_new col_old
% col_new=1;
for k=1:N_Labs
%     if Test_count(4,k)~=0
%         col_new=col_new+1;
        HRR50_all_avg(:,k)=HRR50(:,Test_count(4,k)+2,k);
%     end
end
% clear col_new 

HRR50_all(HRR50_all==0)=NaN;
% Do some Statistics now that you have all of your data together
%Avoid [12,13 (HK Poly data is wrong] and [14-17 (LCPP is underresolved)]
% for ix=1:550
%     HRR50_all(ix,(Test_count(4,end)+1))=nnz(~isnan(HRR50_all((ix),[1:11 18:Test_count(4,end)])));          % Count, N
%     HRR50_all(ix,(Test_count(4,end)+2))=mean(HRR50_all((ix),[1:11 18:Test_count(4,end)]),'omitnan');        % mean
%     HRR50_all(ix,(Test_count(4,end)+3))=std(HRR50_all((ix),[1:11 18:Test_count(4,end)]),'omitnan');         % stdmean (all data +/- 1 s
%     HRR50_all(ix,(Test_count(4,end)+4))=HRR50_all(ix,(Test_count(4,end)+3))/sqrt(HRR50_all(ix,Test_count(4,end)+1));  % stdev mean
% end


%Calculate mean and stdeviation +/- 0 timesteps [HERE, you actually do +/- 2 timesteps because we have data from only one lab; for most across-lab-averages, use +/-0]
for ix=3:398
    HRR50_all(ix,(Test_count(4,end)+1))=nnz(HRR50_all((ix-2:ix+2),[1:Test_count(4,end)]));          % Count, N
    HRR50_all(ix,(Test_count(4,end)+2))=nanmean(HRR50_all((ix-2:ix+2),[1:Test_count(4,end)]),'all');        % mean
    HRR50_all(ix,(Test_count(4,end)+3))=nanstd(HRR50_all((ix-2:ix+2),[1:Test_count(4,end)]),0,'all');         % stdmean (all data +/- 1 s
    HRR50_all(ix,(Test_count(4,end)+4))=HRR50_all(ix,(Test_count(4,end)+3))/sqrt(HRR50_all(ix,Test_count(4,end)+1));  % stdev mean
end

    
figure('Renderer', 'painters', 'Position', [100 100 500 350])
hold on
i_legend=0;
%plot Average with shaded errorbars WITH avg HRR curves from all Labs
% for k=1:N_Labs %size(HRR50_all_avg,2)
%     if k~=6
%         plot(time50(:),HRR50_all_avg(:,k),'.','MarkerEdgeColor',rgb(Colors{k}));
%        if  isnan(HRR50_all_avg(10,k)) == 0
%             i_legend=i_legend+1;
%             legend_counter(i_legend)=k;
%         end            
%     end
% end
%         shadedErrorBar(time50,(HRR50_all(:,Test_count(4,end)+2)),[2*(HRR50_all(:,Test_count(4,end)+4)) 2*(HRR50_all(:,Test_count(4,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         title(char(Test_types{4}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
%         axis([0 300 0 1300]);
%         xlabel('time [s]');
%         ylabel('HRR [kW m^{-2}]');
%         legend(QMJHL{legend_counter},'Location','Northwest');
%             h=3;                                  % height of plot in inches
%             w=5;                                  % width of plot in inches
%             set(gcf, 'PaperSize', [w h]);           % set size of PDF page
%             set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   

%         fig_filename=fullfile(char([Script_Figs_dir, Test_types{4}, '_avgHRR']));
%         print(fig_filename,'-dpdf')
%         clear i_legend legend_counter
        

%plot Average with shaded errorbars WITH individual data points from all tests
for k=1:Test_count(4,end) 
    if k<= 11 | k>=18
        plot(time50(:),HRR50_all(:,k),'.');
    end
end

        title(char(Test_types{4}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 300 0 1300]);
        xlabel('time [s]');
        ylabel('HRR [kW m^{-2}]');
        legend({'Test 1', 'Test 2', 'Test 3'}, 'Location','Northwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
        fig_filename=fullfile(char([Script_Figs_dir, Test_types{4}, '_indivHRR_noavg']));
        print(fig_filename,'-dpdf')

%         shadedErrorBar(time50,(HRR50_all(:,Test_count(4,end)+2)),[2*(HRR50_all(:,Test_count(4,end)+4)) 2*(HRR50_all(:,Test_count(4,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         fig_filename=fullfile(char([Script_Figs_dir, Test_types{4}, '_indivHRR']));
%         print(fig_filename,'-dpdf')

close all        

%% %% Analyze Time Resolved Cone HRR Data with q"=65kWm-2
HRR65=NaN*ones(601,max(max(Test_count(5,1:15)))+3,N_Labs);
time65=[0:600]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==5        % Just 65 kW Cone Tests
        last = min(min(N_rows_all(k,:,m)-1,600));    
        HRR65(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 600 rows/timesteps of HRR data
%         HRR65(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,8); % pull in (up to) the first 600 rows/timesteps of smoothed HRR data
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=HRR65(1:last,:,k);
            temp(temp==0)=NaN;
            HRR65(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%                 HRR65(ix,L+1,k)=nnz(~isnan(HRR65(ix,(1:L),k)));         % N, # of values at this timestep; L+1
%                 HRR65(ix,L+2,k)=mean(HRR65(ix,(1:L),k),'omitnan');      % mean of N values at this timestep; L+2
%                 HRR65(ix,L+3,k)=std(HRR65(ix,(1:L),k),'omitnan');       % stdev of N values at this timestep; L+3
%                 HRR65(ix,L+4,k)=HRR65(ix,L+3,k)/sqrt(HRR65(ix,L+1,k));  % stdev,mean of N values at this timestep; L+4
            
%             Calculate mean and stdeviation +/- 2 timesteps
            HRR65(ix,L+1,k)=nnz(HRR65((ix-2:ix+2),(1:L),k));
            HRR65(ix,L+2,k)=nanmean(HRR65((ix-2:ix+2),(1:L),k),'all');
            HRR65(ix,L+3,k)=nanstd(HRR65((ix-2:ix+2),(1:L),k),0,'all');
            HRR65(ix,L+4,k)=HRR65(ix,L+3,k)/sqrt(HRR65(ix,L+1,k));

            
            end
%             HRR65(1:last,L+2,k)=sgolayfilt(HRR65(1:last,L+2,k),3,15);,
            clear temp
            hold on
            for ix=1:L
                plot(time65(1:last),HRR65(1:last,ix,k),'.');
            end
            if L>=1     %So long as you can calculate stdev, plot with errorbars
                shadedErrorBar(time65(1:last),HRR65(1:last,L+2,k),[2*HRR65(1:last,L+4,k) 2*HRR65(1:last,L+4,k)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            else        %If you have 2 or fewer test repeats, don't show errorbars, just plot avg curve
                plot(time65(1:last),HRR65(1:last,L+2,k),'k','LineWidth',2);
            end
%                 plot(time65(1:last),HRR65(1:last,L+2,k),'k','LineWidth',2);
%             title({LabNames{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            title({QMJHL{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 300 0 1500]);
            xlabel('time [s]');
            ylabel('HRR [kW m^{-2}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{5},'_HRR']));
            print(fig_filename,'-dpdf')

            clear ix
            clf
        end
    end
end
clear last 
close all 

%% Combine all of your time resolved HRR data from individual cone test at q"=65kW
HRR65_all=zeros(601, Test_count(5,end)+4);
col_old=0;
for k=1:N_Labs
    if Test_count(5,k)~=0
        col_new=Test_count(5,k);
        HRR65_all(:,col_old+1:(col_old+col_new))=HRR65(:,1:col_new,k);
        col_old=col_old+col_new;
    end
end
clear col_new col_old
% col_new=1;
for k=1:N_Labs
%     if Test_count(5,k)~=0
%         col_new=col_new+1;
        HRR65_all_avg(:,k)=HRR65(:,Test_count(5,k)+2,k);
%     end
end
% clear col_new 

HRR65_all(HRR65_all==0)=NaN;
% Do some Statistics now that you have all of your data together
%Avoid [12,13 (HK Poly data is wrong] and [14-17 (LCPP has two bad data sets ANDis underresolved)]
% for ix=1:300
%     HRR65_all(ix,(Test_count(5,end)+1))=nnz(~isnan(HRR65_all((ix),[1:11 18:Test_count(5,end)])));          % Count, N
%     HRR65_all(ix,(Test_count(5,end)+2))=mean(HRR65_all((ix),[1:11 18:Test_count(5,end)]),'omitnan');        % mean
%     HRR65_all(ix,(Test_count(5,end)+3))=std(HRR65_all((ix),[1:11 18:Test_count(5,end)]),'omitnan');         % stdmean (all data +/- 1 s
%     HRR65_all(ix,(Test_count(5,end)+4))=HRR65_all(ix,(Test_count(5,end)+3))/sqrt(HRR65_all(ix,Test_count(5,end)+1));  % stdev mean
% end


%Calculate mean and stdeviation +/- 2 timesteps
for ix=1:600
    HRR65_all(ix,(Test_count(5,end)+1))=nnz(HRR65_all((ix-0:ix+0),[1:11 18:Test_count(5,end)]));          % Count, N
    HRR65_all(ix,(Test_count(5,end)+2))=nanmean(HRR65_all((ix-0:ix+0),[1:11 18:Test_count(5,end)]),'all');        % mean
    HRR65_all(ix,(Test_count(5,end)+3))=nanstd(HRR65_all((ix-0:ix+0),[1:11 18:Test_count(5,end)]),0,'all');         % stdmean (all data +/- 1 s
    HRR65_all(ix,(Test_count(5,end)+4))=HRR65_all(ix,(Test_count(5,end)+3))/sqrt(HRR65_all(ix,Test_count(5,end)+1));  % stdev mean
end

    

% %plot Average with shaded errorbars WITH avg HRR curves from all Labs
% figure('Renderer', 'painters', 'Position', [100 100 750 500])
% hold on
% i_legend=0;
% for k=1:N_Labs %size(HRR65_all_avg,2)
% %     if k~=6
%         if  isnan(HRR65_all_avg(20,k)) == 0
%             i_legend=i_legend+1;
%             legend_counter(i_legend,1)=k;
%             h(i_legend)=plot(time65(:),HRR65_all_avg(:,k),'.','Color',rgb(Colors{k}),'DisplayName',QMJHL{k});
%         end    
% %     end
% end
% 
%         shadedErrorBar(time65,(HRR65_all(:,Test_count(5,end)+2)),[2*(HRR65_all(:,Test_count(5,end)+4)) 2*(HRR65_all(:,Test_count(5,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         title(char(Test_types{5}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
%         axis([0 300 0 1500]);
%         xlabel('time [s]');
%         ylabel('HRR [kW m^{-2}]');
%         legend(QMJHL{legend_counter},'Location','eastoutside');
%             h=4.5;                                  % height of plot in inches
%             w=6;                                  % width of plot in inches
%             set(gcf, 'PaperSize', [w h]);           % set size of PDF page
%             set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
%             fig_filename=fullfile(char([Script_Figs_dir, Test_types{5} '_avgHRR']));
%             print(fig_filename,'-dpdf')

%         clear i_legend legend_counter h

%plot Average with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 800 550])
hold on
i_legend=0;

for k=1:N_Labs
    for L=1:Test_count(5,k)
        if  isnan(HRR65(20,L,k))==0 && (HRR65_all_avg(20,k))~=0
        i_legend=i_legend+1;
        legend_counter(i_legend,1)=k;
        h(i_legend)=plot(time65(:),HRR65(1:size(time65(:),1),L,k),'.','MarkerSize',7.5,'Color',rgb(Colors{k}),'DisplayName',QMJHL{k});
        end
    end
end



        
        title(char(Test_types{5}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 300 0 1500]);
        xlabel('time [s]');
        ylabel('HRR [kW m^{-2}]');
        legend(h,'Location','eastoutside');
            h=6;                                  % height of plot in inches
            w=8;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{5} '_indivHRR_noavg']));
            print(fig_filename,'-dpdf')        
%         shadedErrorBar(time65,(HRR65_all(:,Test_count(5,end)+2)),[2*(HRR65_all(:,Test_count(5,end)+4)) 2*(HRR65_all(:,Test_count(5,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%             fig_filename=fullfile(char([Script_Figs_dir, Test_types{5} '_indivHRR']));
%             print(fig_filename,'-dpdf')        

clear i_legend legend_counter h 
close all

%% Plot HRR from all three test conditions: 25. 50, 65 kW/m2
figure('Renderer', 'painters', 'Position', [100 100 500 350])
hold on
shadedErrorBar(time65,(HRR65_all(:,Test_count(5,end)+2)),[2*(HRR65_all(:,Test_count(5,end)+4)) 2*(HRR65_all(:,Test_count(5,end)+4))],'lineprops', {'r','LineWidth',2}); %plot with shaded error bards = 2stdevmean
shadedErrorBar(time50,(HRR50_all(:,Test_count(4,end)+2)),[2*(HRR50_all(:,Test_count(4,end)+4)) 2*(HRR50_all(:,Test_count(4,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
shadedErrorBar(time25,(HRR25_all(:,Test_count(3,end)+2)),[2*(HRR25_all(:,Test_count(3,end)+4)) 2*(HRR25_all(:,Test_count(3,end)+4))],'lineprops', {'b','LineWidth',2}); %plot with shaded error bards = 2stdevmean

title(char('Cone Calorimeter'));     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
axis([0 500 0 1300]);
legend('65 kW m^{-2}','50 kW m^{-2}','25 kW m^{-2}');
xlabel('time [s]');
ylabel('HRR [kW m^{-2}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
            fig_filename=fullfile(char([Script_Figs_dir, 'Cone-Calorimeter-all-fluxes']));
            print(fig_filename,'-dpdf')        

close all

%% Analyze Time Resolved Cone Temperature Data with q"=25kWm-2
TEMP25=NaN*ones(901,3*max(max(Test_count(3,1:15)))+3,N_Labs);   %sure, you likely don't have 3 TCs for all Test 
% time25=[0:900]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==3        % Just 25 kW Cone Tests
        last = min(min(N_rows_all(k,:,m)-1,900));    
%         TEMP25(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 600 rows/timesteps of TEMP data
        for i_temp=1:3
            TEMP25(1:last,3*(L-1)+i_temp,k)=EVAL_DATA{k,L,m}(1:last,3+i_temp); % pull in (up to) the first 600 rows/timesteps of smoothed TEMP data
        end
        clear i_temp
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=TEMP25(1:last,:,k);
            temp(temp==0)=NaN;
            TEMP25(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%                 TEMP25(ix,L+1,k)=nnz(~isnan(TEMP25(ix,(1:L),k)));         % N, # of values at this timestep; L+1
%                 TEMP25(ix,L+2,k)=mean(TEMP25(ix,(1:L),k),'omitnan');      % mean of N values at this timestep; L+2
%                 TEMP25(ix,L+3,k)=std(TEMP25(ix,(1:L),k),'omitnan');       % stdev of N values at this timestep; L+3
%                 TEMP25(ix,L+4,k)=TEMP25(ix,L+3,k)/sqrt(TEMP25(ix,L+1,k));  % stdev,mean of N values at this timestep; L+4
            
%             Calculate mean and stdeviation +/- 2 timesteps
            TEMP25(ix,3*L+1,k)=nnz(TEMP25((ix-2:ix+2),(1:L),k));
            TEMP25(ix,3*L+2,k)=nanmean(TEMP25((ix-2:ix+2),(1:3*L),k),'all');
            TEMP25(ix,3*L+3,k)=nanstd(TEMP25((ix-2:ix+2),(1:3*L),k),0,'all');
            TEMP25(ix,3*L+4,k)=TEMP25(ix,3*L+3,k)/sqrt(TEMP25(ix,3*L+1,k));
            
            end
%             TEMP25(1:last,L+2,k)=sgolayfilt(TEMP25(1:last,L+2,k),3,15);,
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
            title({QMJHL{k} Test_types{3}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 500 250 900]);
            xlabel('time [s]');
            ylabel('Back Surface Temperature [K]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{3} '_Temp']));
            print(fig_filename,'-dpdf')        
            clear ix
            clf
        end
    end
end
clear last 
close

%% Combine all of your Temperature data from individual cone test at q"=25kW
TEMP25_all=zeros(901, Test_count(3,end)+4);
col_old=0;
for k=1:N_Labs
    if Test_count(3,k)~=0
        col_new=Test_count(3,k);
        TEMP25_all(:,col_old+1:(col_old+3*col_new))=TEMP25(:,1:3*col_new,k);
        col_old=col_old+3*col_new;
    end
end
clear col_new col_old
% col_new=1;
for k=1:N_Labs
%     if Test_count(3,k)~=0
%         col_new=col_new+1;
        TEMP25_all_avg(:,k)=TEMP25(:,3*Test_count(3,k)+2,k);
%     end
end
% clear col_new 

TEMP25_all(TEMP25_all==0)=NaN;
% Do some Statistics now that you have all of your data together
%Avoid [12,13 (HK Poly data is wrong] and [14-17 (LCPP is underresolved)]
% for ix=1:550
%     TEMP25_all(ix,(Test_count(3,end)+1))=nnz(~isnan(TEMP25_all((ix),[1:11 18:Test_count(3,end)])));          % Count, N
%     TEMP25_all(ix,(Test_count(3,end)+2))=mean(TEMP25_all((ix),[1:11 18:Test_count(3,end)]),'omitnan');        % mean
%     TEMP25_all(ix,(Test_count(3,end)+3))=std(TEMP25_all((ix),[1:11 18:Test_count(3,end)]),'omitnan');         % stdmean (all data +/- 1 s
%     TEMP25_all(ix,(Test_count(3,end)+4))=TEMP25_all(ix,(Test_count(3,end)+3))/sqrt(TEMP25_all(ix,Test_count(3,end)+1));  % stdev mean
% end


%Calculate mean and stdeviation +/- 0 timesteps
for ix=1:900
    TEMP25_all(ix,(3*Test_count(3,end)+1))=nnz(TEMP25_all((ix-0:ix+0),[1:18 29 32 34:3*Test_count(3,end)]));          % Count, N | THIS WEIRD INDEXING: |1:18 29 32 34:3*Test_count(3,end)] skips Edinburgh (too low) and GIDAZE (not taken at the back surface)Temperature data 
    TEMP25_all(ix,(3*Test_count(3,end)+2))=nanmean(TEMP25_all((ix-0:ix+0),[1:18 29 32 34:3*Test_count(3,end)]),'all');        % mean
    TEMP25_all(ix,(3*Test_count(3,end)+3))=nanstd(TEMP25_all((ix-0:ix+0),[1:18 29 32 34:3*Test_count(3,end)]),0,'all');         % stdmean (all data +/- 1 s
    TEMP25_all(ix,(3*Test_count(3,end)+4))=TEMP25_all(ix,(3*Test_count(3,end)+3))/sqrt(TEMP25_all(ix,3*Test_count(3,end)+1));  % stdev mean
end

    

%plot Average with shaded errorbars WITH avg TEMP curves from all Labs
figure('Renderer', 'painters', 'Position', [100 100 700 350])
hold on
i_legend=0;
for k=1:N_Labs %size(TEMP25_all_avg,2)
    if k~=100
        
       if  isnan(TEMP25_all_avg(10,k)) == 0
            i_legend=i_legend+1;
            legend_counter(i_legend)=k;
            h(i_legend)=plot(time25(:),TEMP25_all_avg(:,k),'.','MarkerEdgeColor',rgb(Colors{k}),'DisplayName',QMJHL{k});
        end              
    end
end
        shadedErrorBar(time25,(TEMP25_all(:,3*Test_count(3,end)+2)),[2*(TEMP25_all(:,3*Test_count(3,end)+4)) 2*(TEMP25_all(:,3*Test_count(3,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
        title(char(Test_types{3}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 500 250 900]);
        xlabel('time [s]');
        ylabel('Back Surface Temperature [K]');
%         legend(QMJHL{legend_counter},'Location','eastoutside');
        legend(h,'Location','eastoutside');
            h=4.5;                                  % height of plot in inches
            w=6;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{3} '_avgTEMP']));
            print(fig_filename,'-dpdf')        
        clear i_legend legend_counter h


% %plot Average with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 700 550])
hold on
i_legend=0;
i_legend_old=0;
ix=0;
for k=1:N_Labs
    if Test_count(3,k)~=0
        i_legend=i_legend_old+3*Test_count(3,k);
        for i= i_legend_old+1:i_legend
            if  isnan(TEMP25_all(10,i))==0
                ix=ix+1;
                legend_counter(ix)=k;
                h(ix)=plot(time25(:),TEMP25_all(:,i),'.','MarkerSize',7.5,'MarkerEdgeColor',rgb(Colors{k}),'DisplayName',QMJHL{k});
            end
        end
        
        i_legend_old=i_legend;
    end
end
% for k=1:3*Test_count(3,end) 
% %     if k~= 19 && k~= 22 && k~= 25 && k~= 28 && k~= 30 && k~= 31 && k~=33 %THIS skips Edinburgh (too low) and GIDAZE (not taken at the back surface)Temperature data 
%         plot(time25(:),TEMP25_all(:,k),'.');
% %     end
% end
        
        title(char(Test_types{3}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 500 250 900]);
        xlabel('time [s]');
        ylabel('Back Surface Temperature [K]');
        legend(h,'Location','eastoutside');
            h=6;                                  % height of plot in inches
            w=8;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{3} '_indivTEMP_noavg']));
            print(fig_filename,'-dpdf')        
%         shadedErrorBar(time25,(TEMP25_all(:,3*Test_count(3,end)+2)),[2*(TEMP25_all(:,3*Test_count(3,end)+4)) 2*(TEMP25_all(:,3*Test_count(3,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         fig_filename=fullfile(char([Script_Figs_dir, Test_types{3} '_indivTEMP']));
%         print(fig_filename,'-dpdf')        
        clear i_legend i_legend_old h legend_counter ix
close all


%% Analyze Time Resolved Temperature Data with q"=50kWm-2
% You only have one set of temperature data this heat flux, DBI_Lund_Test1.
% Let's just plot that.
figure('Renderer', 'painters', 'Position', [100 100 500 350])
TEMP50=EVAL_DATA{2,1,4}(:,4); % pull in TEMP data from DBI_Lund_Cone_50kW_1 
time50x=[0:size(TEMP50,1)-1]';
plot(time50x,TEMP50,'.');
clear time50x
   
        title({QMJHL{2} char(Test_types{4})}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 300 250 1100]);
        xlabel('time [s]');
        ylabel('Back Surface Temperature [K]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner           
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{4} '_Temp']));
            print(fig_filename,'-dpdf')        
        
% close        
        
%% Analyze Time Resolved Cone Temperature Data with q"=65kWm-2
TEMP65=NaN*ones(901,3*max(max(Test_count(3,1:15)))+3,N_Labs);   %sure, you likely don't have 3 TCs for all Test 
time65=[0:900]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==5        % Just 65 kW Cone Tests
        last = min(min(N_rows_all(k,:,m)-1,900));    
%         TEMP65(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 600 rows/timesteps of TEMP data
        for i_temp=1:3
            TEMP65(1:last,3*(L-1)+i_temp,k)=EVAL_DATA{k,L,m}(1:last,3+i_temp); % pull in (up to) the first 600 rows/timesteps of smoothed TEMP data
        end
        clear i_temp
        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp=TEMP65(1:last,:,k);
            temp(temp==0)=NaN;
            TEMP65(1:last,:,k)=temp;
            for ix = 3:last-2 %1:last
%                 TEMP65(ix,L+1,k)=nnz(~isnan(TEMP65(ix,(1:L),k)));         % N, # of values at this timestep; L+1
%                 TEMP65(ix,L+2,k)=mean(TEMP65(ix,(1:L),k),'omitnan');      % mean of N values at this timestep; L+2
%                 TEMP65(ix,L+3,k)=std(TEMP65(ix,(1:L),k),'omitnan');       % stdev of N values at this timestep; L+3
%                 TEMP65(ix,L+4,k)=TEMP65(ix,L+3,k)/sqrt(TEMP65(ix,L+1,k));  % stdev,mean of N values at this timestep; L+4
            
%             Calculate mean and stdeviation +/- 2 timesteps
            TEMP65(ix,3*L+1,k)=nnz(TEMP65((ix-2:ix+2),(1:L),k));
            TEMP65(ix,3*L+2,k)=nanmean(TEMP65((ix-2:ix+2),(1:3*L),k),'all');
            TEMP65(ix,3*L+3,k)=nanstd(TEMP65((ix-2:ix+2),(1:3*L),k),0,'all');
            TEMP65(ix,3*L+4,k)=TEMP65(ix,3*L+3,k)/sqrt(TEMP65(ix,3*L+1,k));
            
            end
%             TEMP65(1:last,L+2,k)=sgolayfilt(TEMP65(1:last,L+2,k),3,15);,
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
            title({QMJHL{k} Test_types{5}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            axis([0 400 250 1200]);
            xlabel('time [s]');
            ylabel('Back Surface Temperature [K]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{5} '_Temp']));
            i
            print(fig_filename,'-dpdf')        
            clear ix
            clf
        end
    end
end
clear last 
close% Close figure
%% Combine all of your Temperature data from individual cone test at q"=65kW
TEMP65_all=zeros(901, Test_count(5,end)+4);
col_old=0;
for k=1:N_Labs
    if Test_count(5,k)~=0
        col_new=Test_count(5,k);
        TEMP65_all(:,col_old+1:(col_old+3*col_new))=TEMP65(:,1:3*col_new,k);
        col_old=col_old+3*col_new;
    end
end
clear col_new col_old
% col_new=1;
for k=1:N_Labs
%     if Test_count(5,k)~=0
%         col_new=col_new+1;
        TEMP65_all_avg(:,k)=TEMP65(:,3*Test_count(5,k)+2,k);
%     end
end
% clear col_new 

TEMP65_all(TEMP65_all==0)=NaN;

%Calculate mean and stdeviation +/- 0 timesteps
%Avoid [12,13 (HK Poly data is wrong] and [14-17 (LCPP is underresolved)]
for ix=1:900
    TEMP65_all(ix,(3*Test_count(5,end)+1))=nnz(TEMP65_all((ix-0:ix+0),[1:18 34:42 47:3*Test_count(5,end)]));          % Count, N | THIS WEIRD INDEXING: |1:18 29 32 34:3*Test_count(3,end)] skips Edinburgh (too low) and GIDAZE (not taken at the back surface)Temperature data 
    TEMP65_all(ix,(3*Test_count(5,end)+2))=nanmean(TEMP65_all((ix-0:ix+0),[1:18 29 32 34:42 47:3*Test_count(5,end)]),'all');        % mean
    TEMP65_all(ix,(3*Test_count(5,end)+3))=nanstd(TEMP65_all((ix-0:ix+0),[1:18 29 32 34:42 47:3*Test_count(5,end)]),0,'all');         % stdmean (all data +/- 1 s
    TEMP65_all(ix,(3*Test_count(5,end)+4))=TEMP65_all(ix,(3*Test_count(5,end)+3))/sqrt(TEMP65_all(ix,3*Test_count(5,end)+1));  % stdev mean
end

    
%--------------new format, proper legend BELOW
%plot Average with shaded errorbars WITH avg TEMP curves from all Labs
figure('Renderer', 'painters', 'Position', [100 100 700 350])
hold on
i_legend=0;
for k=1:N_Labs %size(TEMP25_all_avg,2)
   if  isnan(TEMP65_all_avg(10,k))==0
        i_legend=i_legend+1;
        legend_counter(i_legend)=k;
        h(i_legend)=plot(time65(:),TEMP65_all_avg(1:size(time65(:),1),k),'.','MarkerEdgeColor',rgb(Colors{k}),'DisplayName',QMJHL{k});
    end              
end
%         shadedErrorBar(time65,(TEMP65_all(:,3*Test_count(5,end)+2)),[2*(TEMP65_all(:,3*Test_count(5,end)+4)) 2*(TEMP65_all(:,3*Test_count(5,end)+4))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
        shadedErrorBar(time65,(TEMP65_all(1:size(time65(:),1),end-2)),[2*(TEMP65_all(1:size(time65(:),1),end)) 2*(TEMP65_all(1:size(time65(:),1),end))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
        title(char(Test_types{5}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 350 250 1120]);
        xlabel('time [s]');
        ylabel('Back Surface Temperature [K]');
%         legend(QMJHL{legend_counter},'Location','eastoutside');
        legend(h,'Location','eastoutside');
            h=6;                                  % height of plot in inches
            w=8;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
        fig_filename=fullfile(char([Script_Figs_dir, Test_types{5} '_avgTEMP']));
        print(fig_filename,'-dpdf')        
        clear i_legend legend_counter h


% %plot Average with shaded errorbars WITH individual data points from all tests
figure('Renderer', 'painters', 'Position', [100 100 700 600])
hold on
i_legend=0;
i_legend_old=0;
ix=0;
for k=1:N_Labs
    if Test_count(5,k)~=0
        i_legend=i_legend_old+3*Test_count(5,k);
        for i= i_legend_old+1:i_legend
            if  isnan(TEMP65_all(10,i))==0
                ix=ix+1;
                legend_counter(ix)=k;
                h(ix)=plot(time65(:),TEMP65_all(1:size(time65(:),1),i),'.','MarkerSize',7.5,'MarkerEdgeColor',rgb(Colors{k}),'DisplayName',QMJHL{k});
            end
        end
        
        i_legend_old=i_legend;
    end
end

% for k=1:3*Test_count(5,end) 
% %     if k~= 19 && k~= 22 && k~= 25 && k~= 28 && k~= 30 && k~= 31 && k~=33 %THIS skips Edinburgh (too low) and GIDAZE (not taken at the back surface)Temperature data 
%         plot(time25(:),TEMP25_all(:,k),'.');
% %     end
% end

        title(char(Test_types{5}), 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        axis([0 350 250 1100]);
        xlabel('time [s]');
        ylabel('Back Surface Temperature [K]');
        legend(h,'Location','eastoutside');
            h=6.5;                                  % height of plot in inches
            w=8.5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner           
        fig_filename=fullfile(char([Script_Figs_dir, Test_types{5} '_indivTEMP_noavg']));
        print(fig_filename,'-dpdf')        
        
%         shadedErrorBar(time65,(TEMP65_all(1:size(time65(:),1),end-2)),[2*(TEMP65_all(1:size(time65(:),1),end)) 2*(TEMP65_all(1:size(time65(:),1),end))],'lineprops', {'k','LineWidth',2}); %plot with shaded error bards = 2stdevmean
%         fig_filename=fullfile(char([Script_Figs_dir, Test_types{5} '_indivTEMP']));
%         print(fig_filename,'-dpdf')        
        clear i_legend i_legend_old h legend_counter ix
 close all
 
%% Plot Temperatures from all three test conditions: 25. 50, 65 kW/m2
figure('Renderer', 'painters', 'Position', [100 100 500 350])
hold on
shadedErrorBar(time65(1:195),(TEMP65_all(1:195,3*Test_count(5,end)+2)),[2*(TEMP65_all(1:195,3*Test_count(5,end)+4)) 2*(TEMP65_all(1:195,3*Test_count(5,end)+4))],'lineprops', {'r','LineWidth',2}); %plot with shaded error bards = 2stdevmean
time50x=[0:size(TEMP50,1)-1]';
plot(time50x(1:241),TEMP50(1:241),'k.');
clear time50x
shadedErrorBar(time25(1:401),(TEMP25_all(1:401,3*Test_count(3,end)+2)),[2*(TEMP25_all(1:401,3*Test_count(3,end)+4)) 2*(TEMP25_all(1:401,3*Test_count(3,end)+4))],'lineprops', {'b','LineWidth',2}); %plot with shaded error bards = 2stdevmean

title(char('Cone Calorimeter'));     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
axis([0 400 250 650]);
legend('65 kW m^{-2}','50 kW m^{-2}','25 kW m^{-2}','Location','southeast');
xlabel('time [s]');
ylabel('Back Surface Temperature [K]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner   
        fig_filename=fullfile(char([Script_Figs_dir, 'Cone-Calorimeter-all-fluxes_TEMP']));
        print(fig_filename,'-dpdf')        
close