function [trans,matrix] = LDA_multi(data,label,dimension,figure_i)    

    % x 一列是一个样本,label 一列是一个样本的标签
    [n,m] = size(label);
    
    if(dimension > min(n-1,size(data,2)))
        error('警告：LDA dimension 参数与事实不符！')
    end

    % 获取每个类别的中心点和样本集合
    feature = {};
    center = {};

    global_center = sum(data,2)/m;
    for i = 1:size(label,1)
        % 特征 i
        label_fit = zeros(n,m);
        label_fit(i,:) = 1;
        feature{i} = data(:,sum(label_fit == label,1) == 3);
        center{i} = sum(feature{i},2)/size(feature{i},2);
    end

    % 类间距
    Sb = 0;
    for i = 1:size(label,1)
    %     center{i}-global_center
        distance = (center{i}-global_center)*(center{i}-global_center)'; %4x1 1x4 
        Sb = Sb + size(feature{i},2) * distance;
    end
    % 由于Sb的rank只能小于class数量-1
    fprintf('Sb rank is %d\n', rank(Sb));
    

    % 全局散度矩阵
    St = 0;
    for j = 1:size(data,2)
        St = St + (data(:,j)-global_center) * ...
            (data(:,j)-global_center)';                           %4x1 1x4
    end

    
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

%     St
%     Sb+Sw
    fprintf('可以通过先求St，Sb，然后获得Sw来简化代码\n')                % Sb+Sw == St

    [V,D] = eig(Sw^-1*Sb,'vector') % D-特征值向量  V-特征向量矩阵
    fprintf('Sw^-1*Sb  rank is %d\n', rank(Sw^-1*Sb));
    fprintf('特征值数量 %d，非零特征值数量必为 %d \n', length(D),n-1);

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
    %     Max
    %     index
        transform = [transform V(:,index)];
    end

    % plot 
    figure(figure_i)
    c = ['y','r','g','b'];
    for i = 1:size(label,1)
        x_trans = transform'*feature{i};
        plot(x_trans(1,:),x_trans(2,:),[c(mod(i,4)+1) '*'])
        hold on;
    end
    
    figure(figure_i+1)
    for i = 1:size(label,1)
        plot(feature{i}(1,:),feature{i}(2,:),[c(mod(i,4)+1) '*'])
        hold on;
    end
    
    matrix = transform';
    trans = matrix*data;

end