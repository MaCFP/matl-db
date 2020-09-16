% McDermott
% 9-16-2020
% mean_nonan.m

function Y = mean_nonan(X)

n = size(X);
length(n);

for dim=1:length(n)
    X = mean(X,'omitnan');
end
Y = X;

return