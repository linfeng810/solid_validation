% input data:
% please replace ',' to '\t' before copy to matlab
% data1: out1.txt
% data2: out2.txt

nt = size(data1,1); % number of time steps 
np = (size(data1,2)-1)/6; % number of probe points

x_mat = NaN(t,np,3);    % material coordinates. dim: time x pnt x 3
x_spa = NaN(t,np,3);    % spatial coordinates. dim: time x pnt x 3

for i = 1:nt
    for j = 1:np
        for k = 1:3 % x,y,z
            x_mat(i,j,k) = data1(i,3*(j-1)+k);
        end
    end
    for j = 1:np
        for k = 1:3 
            x_spa(i,j,k) = data1(i,3*(j+np-1)+k);
%             if i==1 fprintf('%d\t',3*(j+np-1)+k), end
        end
%         if i==1 fprintf('\n'), end
    end
end

p1stress = NaN(nt,3,3);
p2stress = NaN(nt,3,3);

for i = 1:nt
    for j = 1:3
        for k = 1:3
            p1stress(i,j,k) = data2(i,3*(j-1)+k);
            if i==1 fprintf('%d\t',3*(j-1)+k), end
        end
    end
    if i==1 fprintf('\n'), end
    for j = 1:3
        for k = 1:3
            p2stress(i,j,k) = data2(i,9+3*(j-1)+k);
            if i==1 fprintf('%d\t',9+3*(j-1)+k), end
        end
    end
    if i==1 fprintf('\n'), end
end


% plot y displacement along z axis
figure(1);
clf;
for t = 1:10:190
    plot(x_mat(t,:,3), x_spa(t,:,2), '-');
    hold on;
end
title('y displacement along z axis');
xlabel('z[m]');
ylabel('\Deltay[m]');
text(0.05,0.25e-3,'from up to down, time marches from 0 to 0.193s');

% plot stress magnitude versus time
figure(2);clf;
p1zz = NaN(size(p1stress,1),1);
p2zz = NaN(size(p1stress,1),1);
for i = 1:size(p1stress,1)
    p1zz(i) = p1stress(i,3,3);
    p2zz(i) = p2stress(i,3,3);
end
time = (1:size(p1stress,1))*1e-4;
plot(time, p1zz, '-')
hold on
plot(time, p2zz, '-');
title('Stress @ 2 points');
xlabel('t[s]');
ylabel('\sigma_{zz} [Pa]');
legend('point (0,0.05,0.314) (compressed)',...
    'point (0,-0.05,0.314) (strenched)');