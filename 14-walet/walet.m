clear,clc
close all

%%%%%%　小波变换　%%%%%%%%%%%%%%%%
fs=256;
t=1/fs:1/fs:2;
f1=100;f2=20;f3=30;
s=10*cos(2*pi*f1*t.*(t>=0&t<0.4))+2*cos(2*pi*f2*t.*(t>=0&t<1))+3*sin(2*pi*f3*t.*(t>=0.8&t<=2));
%s=cos(2*pi*f1*t);
subplot(211)
plot(t,s,'b')
title('原始单频信号')


%%%%%%%%%%%%%%%%%%%%%%% 小波时频图绘制 %%%%%%%%%%%%%%%%%%%%%
wavename='cmor4-4'; %%选用带宽参数和中心频率均为4 的复morlet小波
totalscal=256;      %尺度序列的长度，即scal的长度
fc=centfrq(wavename)


%%%%%%%%% 绘制时间域小波波形 %%%%%
cparam = 2*fc*totalscal;
a = totalscal:-1:1;
scal = cparam./a;
coefs = cwt(s,scal,wavename,1/fs);

f = scal2frq(scal,wavename,1/fs);
subplot(212)
imagesc(t,f,abs(coefs));
colormap(jet)
colorbar
xlabel('时间 t/s')
ylabel('频率 f/Hz')
title('小波时频图')