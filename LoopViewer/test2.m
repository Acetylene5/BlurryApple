data=fitsread('test_data.fits', 'bintable')
CM=fitsread('HODM_CM0.fits');
CM=CM(1:60,:);
ref=fitsread('HOCtr.ACT_POS_REF_MAP.fits');
cmdData=data{1,6};
slpData=data{1,5};

cmd489=cmdData(489,:);
slp489=slpData(489,:);
expected=ref'-0.1*CM*slp489';
max(expected-cmd489')

figure
plot(cmd489)
hold all
%plot(ref)
%hold all
plot(expected )
hold all
leg = legend('Frame 491', 'ACT_POS_REF_MAP', 'Expected');


%slp490=slpData(490,:);
%cmd490=cmdData(490,:);
%expected=cmd489'-0.1*CM*slp490';
%max(expected-cmd490')

%slp491=slpData(491,:);
%cmd491=cmdData(491,:);
%expected=cmd490'-0.1*CM*slp491';
%max(abs(expected-cmd491'))


%figure
%plot(cmd491)
%hold all
%plot(ref)
%hold all
%plot(expected )
%hold all
%leg = legend('Frame 491', 'ACT_POS_REF_MAP', 'Expected');
%