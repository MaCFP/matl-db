% McDermott
% 9-16-2020
% std_nonan.m

function Y = std_nonan(X)

n = size(X);
length(n);

for dim=1:length(n)
    X = std(X,'omitnan');
end
Y = X;

return