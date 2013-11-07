function [ modeStack ] = systemModesInPupilGrid(IM,IFM)
%SYSTEMMODESINPUPILGRID Summary of this function goes here
%   Detailed explanation goes here

[U,S,V]=svd(IM);

mode = zeros(size(IM,2),1);
modeStack = zeros(size(IFM,1),size(IFM,2),size(IM,2));
for i=1:60
    mode(:,1) = V(:,i);
    for j=1:size(IM,2)
        modeStack(:,:,i) = modeStack(:,:,i) + mode(j).*IFM(:,:,j);
    end
end

end

