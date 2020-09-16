% McDermott
% 9-16-2020
% std_nonan.m

function Y = std_nonan(X)

X_1D=X(:);

Y = std(X_1D,'omitnan');

return