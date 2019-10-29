function [trans,matrix] = LDA_two(data,label)    

    % x 一列是一个样本,label 一列是一个样本的标签
    [n,m] = size(label);


    % 获取每个类别的中心点和样本集合
    feature = {};
    center = {};
    figure(1)
    c=['r','g'];
    for i = 1:2
        % 特征 i
        label_fit = zeros(n,m);
        label_fit(i,:) = 1;
        feature{i} = data(:,sum(label_fit == label,1) == 2);
        center{i} = sum(feature{i},2)/size(feature{i},2);
        plot(feature{i}(1,:),feature{i}(2,:),[c(i) '*'],'markersize',10,'linewidth',2);
        hold on
    end

    plot(center{1}(1),center{1}(2),'ro','markersize',20,'linewidth',2)
    plot(center{2}(1),center{2}(2),'go','markersize',20,'linewidth',2)
    

    % 类间距
    center{1}-center{2}
    Sb = (center{1}-center{2})*(center{1}-center{2})'
    
    % 类内间距
    Sw = 0;
    for i = 1:size(label,1)
        distance = 0;
    %     center{i}-global_center
        for j = 1:size(feature{i},2)
            distance = distance + (feature{i}(:,j)-center{i}) * ...
                (feature{i}(:,j)-center{i})';                           %4x1 1x4
        end
        Sw = Sw+distance;
    end
%     Sw


    [V,D] = eig(Sw^-1*Sb,'vector'); % D-特征值向量  V-特征向量矩阵

    dimension=1;
    % get trans Matrix
    transform = [];
    for j = 1:dimension
        Max = -10000;index = 0;
        for i = 1:length(D)
            if(Max<D(i))
                Max = D(i);index=i;
            end
        end
        D(index)=-10000;
        transform = [transform V(:,index)];
    end

    % plot 
    k = transform(2)/transform(1);
    for i = 1:size(label,1)
        for j = 1:size(feature{i},2)
            sample = feature{i}(:,j);
            x_trans = transform'*sample;
            xl = x_trans*1/sqrt(1+k^2);
            yl = sign(k)*x_trans*1/sqrt(1+1/k^2);
            plot(xl,yl,'bx','markersize',10,'linewidth',2)
            plot([xl sample(1)],[yl sample(2)],[c(i) '--'],'markersize',10,'linewidth',2)
            hold on;
            fprintf('投影线与变换矩阵的夹角:%f\n',k*(sample(2)-yl)/(sample(1)-xl))
        end
    end
    x_trans*1/sqrt(1+k^2);
    x_trans*1/sqrt(1+1/k^2);
    
    x=[-10 0 30]*transform(1);
    y=[-10 0 30]*transform(2);
    plot(x,y,'yx-','linewidth',2);

    
    matrix = transform';
    trans = matrix*data;
    
end