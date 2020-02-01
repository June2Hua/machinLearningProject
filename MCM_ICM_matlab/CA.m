%直行进入研究区域
%function []=in_yuanbao(p,long)

p=20;       %p 车辆驶入的概率
long=500;   %long 道路长度 m
n=1000;     %n执行的步长 为1000次
L=zeros(1,long/5+1);    %是否有车辆标记
V=zeros(1,long/5+1);    %速度
flag=0;%flag 用于判断是否有车在等待区即将离开该区域
a=0;

%画图
figure();
H=imshow(L,[]);     %显示
set(gcf,'position',[241 132 560 420]);      %241 132 560 420(设定plot输出图片的尺寸)
set(gcf,'doublebuffer','on');               %设定为双缓冲模式
title('元胞自动机交通模拟','color','b');
for i=1:n
    flag=L(1,long/5+1);
    if   p>=rand(1)*100     %有车进入
         L(1,1)=1;
    end
    %速度设定,调整车速
    V(1,L(1,1:end-2)==1&L(1,2:end-1)==0&L(1,3:end)==0)=2;
    V(1,L(1,1:end-2)==1&L(1,2:end-1)==0&L(1,3:end)==1)=1;
    V(1,L(1,1:end-2)==1&L(1,2:end-1)==1)=0;
    
    
    if flag==1
        a=a+1;
        flag=0;
        L(1,long/5+1)=0;
        V(1,long/5)=0;
    elseif  L(1,long/5)==1
        V(1,long/5)=1;
    end
    L([zeros(1,1) V(1,1:end-1)]==1)=1;
    L([zeros(1,2) V(1,1:end-2)]==2)=1;
    L(V(1,1:end)==2|V(1,1:end)==1)=0;
    %L(1,(V(1,1:end)==2)+2)=1;
    %L(1,(V(1,1:end)==2)+1)=0;
    %L(1,V(1,1:end)==1+1)=1;
    V=zeros(1,long/5+1);
    

    set(H,'CData',L);
    pause(0.1)
end
%end
