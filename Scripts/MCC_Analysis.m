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
%             'MCC_N2_1K';'MCC_N2_2K';'MCC_N2_5K';'MCC_N2_10K';'MCC_N2_20K';...
%             'MCC_O2-10_10K';'MCC_O2-21_10K';'MCC_Ar_1K'; 'MCC_Ar_10K'; 'MCC_Ar_50K';...
%             'FPA_25kW';'FPA_50kW';'FPA_65kW';...
%             'Gasification_25kW';'Gasification_50kW';'Gasification_65kW';...
%             'MCC_N2_60K';...
%             'TGA_N2_1K';'TGA_N2_2K';'TGA_N2_2.5K';'TGA_N2_5K';'TGA_N2_10K';'TGA_N2_15K';'TGA_N2_20K';'TGA_N2_50K';'TGA_N2_100K';...
%             'TGA_O2-10_10K';'TGA_O2-21_10K'; 'TGA_Ar_1K'; 'TGA_Ar_10K'; 'TGA_Ar_50K'};

%% CREATE EVAL_DATA, HRR, total heat released
%Read in all of your data  EXP_DATA is a 3D cell array of indexing {LabName,k | Test #, L | Test Type,m}
%Inside of each cell is a 2D array of indexing [timestep, data type]

% Create EVAL_DATA= [ t | T | HRR | Total Heat Released ] (all values interpolated to 0.5 K intervals)
figure
for i =1:N_files   % Loop through all of your data sets
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
    if m==23        % Just MCC Tests

        T_start=ceil(min(EXP_DATA{k,L,m}(:,2)));            %find first timestep (rounded to nearest integer)
        T_end=floor(max(EXP_DATA{k,L,m}(:,2)));             %find last timestep (rounded to nearest integer)
        delta_T=0.5;
        EVAL_DATA{k,L,m}(:,2)=[T_start:delta_T:T_end-1]';   % generate uniform T from Tmin to Tmin at 0.5K intervals
%Thursday AM
        [T,sortidx_T]=unique(EXP_DATA{k,L,m}(:,2));         % Find all of your unique Temps
        T_idx=[T sortidx_T];
        T_idx=sortrows(T_idx,'ascend');
        HRR=EXP_DATA{k,L,m}(:,3);
        HRR=HRR(sortidx_T);                       % Find all of the HRR values asssociated with these unique temperatures
        time=EXP_DATA{k,L,m}(:,1);
        time=time(sortidx_T);
        EVAL_DATA{k,L,m}(:,1)=interp1(T,time,EVAL_DATA{k,L,m}(:,2));         % interpolate time (to T)
        EVAL_DATA{k,L,m}(:,3)=interp1(T,HRR,EVAL_DATA{k,L,m}(:,2));     % interpolate masses (to T)
%         x_eval=EVAL_DATA{k,L,m};
%         x_exp=EXP_DATA{k,L,m};
        p_end=size(EVAL_DATA{k,L,m},1);
        for p=1:p_end                 %Calculate [4] total heat flow and [5] dT/dt (+/- one time step, delta_T=1k]
            if p==1
            EVAL_DATA{k,L,m}(p,5)=0;
            EVAL_DATA{k,L,m}(p,4)=0;
            elseif p<p_end
            EVAL_DATA{k,L,m}(p,5)=(EVAL_DATA{k,L,m}(p-1,2)-EVAL_DATA{k,L,m}(p+1,2))/(EVAL_DATA{k,L,m}(p+1,1)-EVAL_DATA{k,L,m}(p-1,1));  %dT/dt
            EVAL_DATA{k,L,m}(p,4)=EVAL_DATA{k,L,m}(p-1,4)+0.5*(EVAL_DATA{k,L,m}(p-1,3)+EVAL_DATA{k,L,m}(p,3))*(EVAL_DATA{k,L,m}(p,1)-EVAL_DATA{k,L,m}(p-1,1));  %Integral HRR
            else
            EVAL_DATA{k,L,m}(p,4)=EVAL_DATA{k,L,m}(p-1,4)+0.5*(EVAL_DATA{k,L,m}(p-1,3)+EVAL_DATA{k,L,m}(p,3))*(EVAL_DATA{k,L,m}(p,1)-EVAL_DATA{k,L,m}(p-1,1));  %Integral HRR
            end
        end
        clear p_end

        clear time HRR sortidx_T T_idx T_start T_end

        clf
        hold on
        yyaxis left
        ylabel('Normalized HRR [W g^{-1}]');
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,3),'-','MarkerSize',2);   %HRR
        axis([300 900 -inf inf]);

        yyaxis right
        plot(EVAL_DATA{k,L,m}(:,2),EVAL_DATA{k,L,m}(:,4),'r');      %Integral HRR
        axis([300 900 -inf inf]);
        title(filenames{i}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
        xlabel('Integral HRR [J g^{-1}]');
        ylabel('(1/m_0)dm/dt [s^{-1}]');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
        fig_filename=fullfile(char([Script_Figs_dir, filenames{i}(1:end-4)]));
        print(fig_filename,'-dpdf')
    end
end
% close

%% Quick code to determine minimum temperature reported in ALL MCC datasets
% min_T=300;  %initialize minimum temperature reported in TGA data
% for i=1:N_files
%     k=files{i,3};   % Find Lab Name
%     L=files{i,4};   % Find Test Count
%     m=files{i,2};   % Find Test Type
%     if m>=6 && m<=15        % Just MCC Tests
%     temp=min(EVAL_DATA{k,L,m}(:,2));
%     if temp>min_T
%         min_T=temp;
%     end
%     if temp==0
%         i
%     end
%     end
% end
% clear temp

%% Analyze Temperature-Resolved MCC heat flow Data
MCC_HRR=NaN*ones(901,max(max(Test_count(6:15,1:15)))+4,N_Labs,37);
MCC_int_HRR=NaN*ones(901,max(max(Test_count(6:15,1:15)))+4,N_Labs,37);
MCC_Temperature=[350:0.5:800]';
figure('Renderer', 'painters', 'Position', [100 100 400 300])
for i=1:N_files
    k=files{i,3};   % Find Lab Name
    L=files{i,4};   % Find Test Count
    m=files{i,2};   % Find Test Type
%         clear xxx xxx_exp
        xxx=EVAL_DATA{k,L,m};
    if m==23       % Just MCC Tests // UMET data is messed up /\/\/\ temperature program

        last = min(min(N_rows_all(k,:,m)-1,901));

        max_T =max(EVAL_DATA{k,L,m}(:,2));
        max_T_idx=min((max_T-350)*2+1,901);    %we pull in all data up to 901 rows of data (~up to 800K)

        min_T=min(EVAL_DATA{k,L,m}(:,2));
        min_T_idx=(min_T-350)*2+1;

%         MCC_Mass//MCC_MLR(1:last,L,k)=EVAL_DATA{k,L,m}(1:last,3); % pull in (up to) the first 901 rows/timesteps of Mass and MLR data
            MCC_int_HRR(min_T_idx:max_T_idx,L,k,m)=EVAL_DATA{k,L,m}(1:(max_T_idx+1-min_T_idx),4);
            MCC_HRR(min_T_idx:max_T_idx,L,k,m)=EVAL_DATA{k,L,m}(1:(max_T_idx+1-min_T_idx),3);

        if L==Test_count(m,k)    %If this dataset is the last one for this lab, do some statistics
            %Turn all 0 values into NaN so that you can ignore them in std , mean calculations
            temp_MLR=MCC_HRR(:,:,k,m);
            temp_MLR(temp_MLR==0)=NaN;
            MCC_HRR(1:last,:,k,m)=temp_MLR;

            temp_Mass=MCC_int_HRR(:,:,k,m);
            temp_Mass(temp_Mass==0)=NaN;
            MCC_int_HRR(1:last,:,k,m)=temp_Mass;

            for ix = 3:last-2 %1:last
%             Calculate mean and stdeviation +/- 2 timesteps
                MCC_HRR(ix,5,k,m)=nnz(MCC_HRR((ix-2:ix+2),(1:L),k,m));
                MCC_HRR(ix,6,k,m)=mean_nonan(MCC_HRR((ix-2:ix+2),(1:L),k,m));
                MCC_HRR(ix,7,k,m)=std_nonan(MCC_HRR((ix-2:ix+2),(1:L),k,m));
                MCC_HRR(ix,8,k,m)=MCC_HRR(ix,7,k,m)/sqrt(MCC_HRR(ix,5,k,m));

                MCC_int_HRR(ix,5,k,m)=nnz(MCC_int_HRR((ix-2:ix+2),(1:L),k,m));
                MCC_int_HRR(ix,6,k,m)=mean_nonan(MCC_int_HRR((ix-2:ix+2),(1:L),k,m));
                MCC_int_HRR(ix,7,k,m)=std_nonan(MCC_int_HRR((ix-2:ix+2),(1:L),k,m));
                MCC_int_HRR(ix,8,k,m)=MCC_int_HRR(ix,7,k,m)/sqrt(MCC_int_HRR(ix,5,k,m));
            end
%             HRR25(1:last,L+2,k)=sgolayfilt(HRR25(1:last,L+2,k),3,15);,
            clear temp_MLR temp_Mass

%             if k==13    % plot UMD with their own error bars
%                 shadedErrorBar(EXP_DATA{k,L,m}(:,2),EXP_DATA{k,L,m}(:,3),[EXP_DATA{k,L,m}(:,4) EXP_DATA{k,L,m}(:,4)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
%                 axis([300 800 -inf inf]);
%                 title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
%                 xlabel('Temperature [K]');
%                 ylabel('Heat Flow [W g^{-1}]');
%                 clear ix
%                 print([LabNames{k} Test_types{m} '_HRR'],'-dpdf')
%                 clf
%             else    %plot everyone else's data with my errorbars
%                 hold on
                for ix=1:L
                    plot(MCC_Temperature(1:last),MCC_HRR(1:last,ix,k,m),'.','MarkerSize',3);
                end
                shadedErrorBar(MCC_Temperature(1:last),MCC_HRR(1:last,6,k,m),[2*MCC_HRR(1:last,8,k,m) 2*MCC_HRR(1:last,8,k,m)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
                axis([350 800 -inf inf]);
                title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
                xlabel('Temperature [K]');
                ylabel('HRR [W g^{-1}]');
                clear ix
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{m} '_HRR_avg']));
            print(fig_filename,'-dpdf')
                clf
%             end

            hold on
            for ix=1:L
                plot(MCC_Temperature(1:last),MCC_int_HRR(1:last,ix,k,m),'.','MarkerSize',3);
            end
            shadedErrorBar(MCC_Temperature(1:last),MCC_int_HRR(1:last,6,k,m),[2*MCC_int_HRR(1:last,8,k,m) 2*MCC_int_HRR(1:last,8,k,m)],'lineprops', {'k','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
            axis([350 800 -inf inf]);
            title({QMJHL{k} Test_types{m}}, 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
            ylabel('Integral HRR [J g^{-1}]');
            clear ix
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, LabNames{k}, '_', Test_types{m} '_int_HRR_avg']));
            print(fig_filename,'-dpdf')
            clf
        end
    end
    clear min_T max_T last fig_filename
end
clear last
close all % Close figure

%% Combine all of your TGA data from individual tests in N2/21%O2 at 10K/min
figure('Renderer', 'painters', 'Position', [100 100 800 450])
hold on
m=23;
col_old=0;
i_legend=1;
clear legend_counter
for k=1:N_Labs
    if Test_count(m,k)~=0
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
    last = min(min(N_rows_all(k,:,m)-1,901));
    if m==23 && L==Test_count(m,k)     % Just MCC Tests
        hold on
        for ix=1:L
            figure(1)
            hold on
            plot(MCC_Temperature(1:last),MCC_HRR(1:last,ix,k,m),'-','MarkerSize',5,'color',rgb(Colors{k}));

            figure(2)
            hold on
            plot(MCC_Temperature(1:last),MCC_int_HRR(1:last,ix,k,m),'-','MarkerSize',5,'color',rgb(Colors{k}));
        end
        if k==13            % add UMD with their error bars
            hold on
            figure(1)
            shadedErrorBar(EXP_DATA{k,L,m}(:,2),EXP_DATA{k,L,m}(:,3),[EXP_DATA{k,L,m}(:,4) EXP_DATA{k,L,m}(:,4)],'lineprops', {'M','LineWidth',1 }); %plot with shaded error bards = 2stdevmean
        end

    end
end

m=23;
figure(1)
set(gcf, 'Position', [100 100 600 350])
axis([350 800 0 350]);
% title([Test_types{m} '_HRR'], 'interpreter', 'none');     %title the figure based on the name of dataset i; turn off interpreter so _ is explicitly displayed
xlabel('Temperature [K]');
ylabel('HRR [W g^{-1}]');
legend(QMJHL{legend_counter},'Location','northwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_HRR']));
            print(fig_filename,'-dpdf')

figure(2)
set(gcf, 'Position', [100 100 600 350])
axis([350 800 0 inf]);
xlabel('Temperature [K]');
ylabel('Integral HRR [J g^{-1}]');
legend(QMJHL{legend_counter},'Location','northwest');
            h=3;                                  % height of plot in inches
            w=5;                                  % width of plot in inches
            set(gcf, 'PaperSize', [w h]);           % set size of PDF page
            set(gcf, 'PaperPosition', [0 0 w h]);   % put plot in lower-left corner
            fig_filename=fullfile(char([Script_Figs_dir, Test_types{m} '_int_HRR']));
            print(fig_filename,'-dpdf')
clear ix last
close all % Close figure
