%清空
clc;
clear;
set(gcf,'DoubleBuffer','on');   %gcf是当前图像的句柄
N=256;   %格子的数目
grid=zeros(N);  %网格 N*N
grid(6,8)=1;       %随机初始化为1
Ii=imshow(1-grid,[]);  %1为白色，0为黑色
axis square;
grid_calc=zeros(N+2);   %为了计算边界
while(1)
    grid_calc(2:end-1,2:end-1)=grid;
    tmp=grid_calc(1:end-2,2:end-1)+grid_calc(3:end,2:end-1)+grid_calc(2:end-1,1:end-2)+grid_calc(2:end-1,3:end);
    grid=mod(tmp,2);
    set(Ii,'CData',1-grid);
    pause(0.1);
end
figure;