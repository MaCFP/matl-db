% McDermott
% 9-16-2020
% mean_nonan.m

function Y = mean_nonan(X)

X_1D=X(:);

Y=mean(X_1D,'omitnan');

return