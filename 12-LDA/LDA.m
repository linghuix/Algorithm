clc
clear all

% 多维降维
[x,label] = iris_dataset;       % x 一列是一个样本,label 一列是一个样本的标签
% x(5,:) = 5;
[trans,Matrix] = LDA_multi(x,label,2,1);


%% 二维降维
clc
clear all
x = [1 2 3 9 12 10];
y = [5 -6 5 0 10 5];
label_x = [1 1 1 0 0 0];
label_y = [0 0 0 1 1 1];


[trans,Matrix]=LDA_two([x;y],[label_x;label_y])

%%
% [n,m] = size(label)
% 
% 
% feature = {};
% center = {};
% 
% global_center = sum(x,2)/m;
% for i = 1:size(label,1)
%     % 特征 i
%     label_fit = zeros(n,m);
%     label_fit(i,:) = 1;
%     feature{i} = x(:,sum(label_fit == label,1) == 3);
%     center{i} = sum(feature{i},2)/size(feature{i},2);
% end
% 
% % 类间距
% Sb = 0;
% for i = 1:size(label,1)
% %     center{i}-global_center
%     distance = (center{i}-global_center)*(center{i}-global_center)'; %4x1 1x4 
%     Sb = Sb + size(feature{i},2) * distance;
% end
% Sb
% 
% % 类内间距
% Sw = 0;
% for i = 1:size(label,1)
%     distance = 0;
% %     center{i}-global_center
%     for j = 1:size(feature{i},2)
%         distance = distance + (feature{i}(:,j)-center{i}) * ...
%             (feature{i}(:,j)-center{i})';                           %4x1 1x4
%     end
%     Sw = Sw+distance;
% end
% Sw
% 
% dimension =2;
% [V,D] = eig(Sw^-1*Sb,'vector')
% 
% 
% % get trans Matrix
% transform = [];
% for j = 1:dimension
%     Max = -10000;index = 0;
%     for i = 1:length(D)
%         if(Max<D(i))
%             Max = D(i);index=i;
%         end
%     end
%     D(index)=-10000;
% %     Max
% %     index
%     transform = [transform V(:,index)];
% end
% 
% % plot 
% c = ['r','g','b'];
% for i = 1:size(label,1)
%     x_trans = feature{i}'*transform;
%     plot(x_trans(:,1),x_trans(:,2),[c(i) '*'])
%     hold on;
% end
