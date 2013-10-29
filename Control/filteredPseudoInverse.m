
function [ Minv ] = filteredPseudoInverse(M, numFilteredModes)      
    % filteredPseudoinverse  Calculates the pseudoinverse matrix of the input with filtering of lowest singular value modes
    %                        Input arguments:
    %                        - M: matrix to be inverted
    %                        - numFilteredModes: number of lowest singular value modes to be filtered
    %                        Output arguments:
    %                        - Minv: filtered pseudoinverse of M
    [U,S,V] = svd(M);
    D = 1./diag(S(:,1:end-numFilteredModes));
    S(:,end-numFilteredModes+1:end) = 0;
    I = 1:size(S,1)+1:size(S,1)*numel(D);
    S(I) = D;
    Minv = V*S'*U';
end        
    
