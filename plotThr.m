load('APVtolCmds.mat');

## hold on
## plot(t_s, vtol_throttle_0)
## plot(t_s, vtol_throttle_1)
## plot(t_s, vtol_throttle_2)
## plot(t_s, vtol_throttle_3)
## hold off

len = length(vtol_throttle_0);

names = {'throttle_0 [%]','throttle_1 [%]','throttle_2 [%]','throttle_3 [%]'};

fid = fopen('throttle_export.txt','w');

fprintf(fid,'%s\t%s\t%s\t%s\n',names{1},names{2},names{3},names{4});

for i=1:1:len
   fprintf(fid,'%.2f\t%.2f\t%.2f\t%.2f\n',vtol_throttle_0(i),vtol_throttle_1(i),vtol_throttle_2(i),vtol_throttle_3(i));
end

fclose(fid);
