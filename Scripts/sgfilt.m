% sgfilt.m - filtering with length-N order-d SG smoother.
%
% y = sgfilt(d, N, x);
%
% x and y are L-dimensional column vectors; and N = 2M+1. Must have L > N+1.
% B(:, i)     = b_{i-M-1} = input-on transient filters, i=1:M+1
% B(:, M+1)   = b_0       = steady-state filter
% B(:, M+1+i) = b_{i}     = input-off transient filters, i=0:M

function  y = sgfilt(d, N, x)

M = (N-1)/2;
[L, L1] = size(x);

B = sg(d, N);                                    % design filter

for i = 1:M+1,                                   % input-on transients
       y(i,1) = B(:,i)' * x(1:N);
end

for n = M+2:L-M-1,                               % steady-state
       y(n,1) = B(:,M+1)' * x(n-M:n+M);
end

for i = 0:M,                                     % input-off transients
       y(L-M+i,1) = B(:,M+1+i)' * x(L-N+1:L);
end
