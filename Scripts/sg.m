% sg.m - Savitzky-Golay length-N order-d smoother design.
%
% [B, S] = sg(d, N);
%
% N=2M+1 = filter length, d = polynomial order
% S = [s0, s1, ..., sd], F = S'S
% G = SF^(-1) = derivative filters
% B = S*F^(-1)*S' = smoothing filters
% indexing: B(M+1+m, M+1+k) = B_{mk}, m,k=-M:M
% m-th SG filter = B(:, M+1+m) = b_{m}, m=-M:M
% NRRs = diagonal entries of B.

function [B, S] = sg(d, N)

M = (N-1)/2;

for m=-M:M,
       for i=0:d,
              S(m+M+1, i+1) = m^i;
       end
end

F = S' * S;
B = S * F^(-1) * S';
