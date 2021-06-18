% input data:
% please replace ',' to '\t' before copy to matlab
% data: out1.txt

nt = size(data,1); % number of time steps
np = size(data,2)/3; % number of probe points (reslooution)

mat_coor = reshape(data(1,:),[3,np]);
mat_coor = mat_coor';

spa_coor = NaN(np,3,nt);
for t = 1:nt
    spa_coor(:,:,t) = transpose(reshape(data(t,:),[3,np]));
end
%     mat_coor(8,:) = [];
%     spa_coor(8,:,:) = [];

% clear invalid points (because of interpolation)
% invalid_idx=[];
% for i = 2:np-1
%     for t = 1:nt
%         if spa_coor(i,2,nt) == 0 || isnan(spa_coor(i,2,nt))
%             invalid_idx(end+1)=i;
%         end
%     end
% end
% % invalid_idx=[5,8];
% spa_coor(invalid_idx,:,:)=[];
% mat_coor(invalid_idx,:,:)=[];


figure(1);clf;
for t = 1:nt
    plot(mat_coor(:,3), spa_coor(:,2,t),'-o');
    hold on;
end
title({'y coordinates of material points @ axis',
    ['multiple time steps']});
xlabel('z [m]');
ylabel('y [m]');

% x_mat = NaN(t,np,3);    % material coordinates. dim: time x pnt x 3
% x_spa = NaN(t,np,3);    % spatial coordinates. dim: time x pnt x 3
% 
% for i = 1:nt
%     for j = 1:np
%         for k = 1:3 % x,y,z
%             x_mat(i,j,k) = data1(i,3*(j-1)+k);
%         end
%     end
%     for j = 1:np
%         for k = 1:3 
%             x_spa(i,j,k) = data1(i,3*(j+np-1)+k);
% %             if i==1 fprintf('%d\t',3*(j+np-1)+k), end
%         end
% %         if i==1 fprintf('\n'), end
%     end
% end
% 
% p1stress = NaN(nt,3,3);
% p2stress = NaN(nt,3,3);
% 
% for i = 1:nt
%     for j = 1:3
%         for k = 1:3
%             p1stress(i,j,k) = data2(i,3*(j-1)+k);
%             if i==1 fprintf('%d\t',3*(j-1)+k), end
%         end
%     end
%     if i==1 fprintf('\n'), end
%     for j = 1:3
%         for k = 1:3
%             p2stress(i,j,k) = data2(i,9+3*(j-1)+k);
%             if i==1 fprintf('%d\t',9+3*(j-1)+k), end
%         end
%     end
%     if i==1 fprintf('\n'), end
% end


% % plot y displacement along z axis
% figure(1);
% clf;
% for t = 1:10:190
%     plot(x_mat(t,:,3), x_spa(t,:,2), '-');
%     hold on;
% end
% title('y displacement along z axis');
% xlabel('z[m]');
% ylabel('\Deltay[m]');
% text(0.05,0.25e-3,'from up to down, time marches from 0 to 0.193s');
% 
% % plot stress magnitude versus time
% figure(2);clf;
% p1zz = NaN(size(p1stress,1),1);
% p2zz = NaN(size(p1stress,1),1);
% for i = 1:size(p1stress,1)
%     p1zz(i) = p1stress(i,3,3);
%     p2zz(i) = p2stress(i,3,3);
% end
% time = (1:size(p1stress,1))*1e-4;
% plot(time, p1zz, '-')
% hold on
% plot(time, p2zz, '-');
% title('Stress @ 2 points');
% xlabel('t[s]');
% ylabel('\sigma_{zz} [Pa]');
% legend('point (0,0.05,0.314) (compressed)',...
%     'point (0,-0.05,0.314) (strenched)');