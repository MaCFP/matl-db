% McDermott
% 9-16-2020
% test_mean_nonan.m

close all
clear all

X = magic(3);
X([1 6:9]) = NaN;

Y = mean_nonan(X)
S = std_nonan(X)