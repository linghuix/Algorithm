% 信号观测

data= SignalBuilder('G',5000,5,20);
plot(data,'*')
hold on
plot( 1:length(data),5*ones(1,length(data)),'black' )

%
% 卡尔曼滤波
% 已知
% 系统输入为常数，系统内部噪声方差为0

% 输入为0
u = 0*ones(1,length(data));
% 系统输入噪声方差为0
N = 0;
% 传感器测量噪声方差
W = 20;
% 系统状态 x 初始值
x0 = 1;
% 系统内部误差协方差初值 200  初值最好取得大一点，因为一开始你必须要相信观测到的值
P0 = 20;

% 传感器观测到的数据data
[data_filiter,P] = kalmanFilter( u, data, N, W, x0, P0 );
% 传感器测量噪声方差越大，则卡尔曼滤波更加相信预测的结果，所以观测到的y对预测的校正力度比较小，
% 所以如果建立模型的时候观测的误差过大，虽然校正后的曲线变得更加光滑，不符合观测的结果，所以校正后的值与实际的值会有一定的偏差
% 所以如果建立模型的时候观测的误差过小，校正后的曲线变得更加陡峭，引入了大量的观测噪声，校正后的值与实际的值会有一定的偏差，

plot(data_filiter,'gp--');
plot(P,'r-');
legend('sensor output','ground value','filiter','P');


%% 输入噪声不为零，P无法趋于0

figure(5)
data= SignalBuilder('G',1500,0.3,0.1);
plot(data,'*')
hold on
plot( 1:length(data),0.3*ones(1,length(data)),'black' )

[data_filiter,P] = kalmanFilter( zeros(1,length(data)), data, 0, 0.1, 0.3, 1 );

plot(data_filiter,'gp--');
plot(P,'r-');
legend('sensor output','ground value','filiter','P');

% 为什么Pk只会减小，不会变大？而老师演示的视频里面不确定区域会变大

