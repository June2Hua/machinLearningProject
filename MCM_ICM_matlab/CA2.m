%有交叉口的车辆模拟情况
%直行进入研究区域
%function []=in_yuanbao(p,long)
%p 车辆驶入的概率
%long 道路长度 m
%width 小区宽度 m
%n执行的步长 为1000次
%主道路均为4条
%小区道路为两条
p=20;
long=500;
width=500;
n=1000;
L_car=ones(width/5,long/5).*1.2;
V_car=ones(width/5,long/5).*1.2;
L_car(width/10,:)=0;
L_car(:,long/10)=0;
flag=0;%flag 用于判断是否有车在等待区即将离开该区域
a=0;
 figure();
 H=imshow(L_car,[]);
 set(gcf,'position',[241 132 560 420]) ;%241 132 560 420(设定plot输出图片的尺寸)
 set(gcf,'doublebuffer','on'); %设定为双缓冲模式
 title('元胞自动机交通模拟','color','b');
Tred=10;
Tgreen=10;%红绿灯时间
 L=L_car(width/10,1:long/10-1);
 V=V_car(width/10,1:long/10-1);
 L_1=L_car(width/10,long/10+1:end);%直行路段统计
 V_1=V_car(width/10,long/10+1:end);
 bL_2=L_car(width/10+1:end,long/10);%右转路段统计
 bV_2=V_car(width/10+1:end,long/10);
 bL_3=L_car(width/10-1:-1:1,long/10);%左转路段统计
 bV_3=V_car(width/10-1:-1:1,long/10);
 L_2=bL_2';
 L_3=bL_3';
 V_2=bV_2';
 V_3=bV_3';
 gs1=zeros(1,n);
for i=1:n
    a=a+1;%用于计时，当作红绿灯计算
        V(:,:)=0;
        V_1(:,:)=0;
        V_2(:,:)=0;
        V_3(:,:)=0;
    if   p>=rand(1)*100
         L(1,1)=1;
    end  
    %速度设定
    V(L(:,1:end-2)==1&L(:,2:end-1)==0&L(:,3:end)==0)=2;
    V(L(:,1:end-2)==1&L(:,2:end-1)==0&L(:,3:end)==1)=1;
    V(L(:,1:end-2)==1&L(:,2:end-1)==1)=0;
    %    a=a+1;      
       % V(:,long/5-1)=0
    %end
    if L(1,end)==0&&L(1,end-1)==1
        L(1,end)=1;
        L(1,end-1)=0;
    end
    L([zeros(1,1) V(:,1:end-1)]==1)=1;
    L([zeros(1,2) V(:,1:end-2)]==2)=1;
    L(V(:,1:end)==2|V(:,1:end)==1)=0;

%以上为之前的直行路段。
    if a>Tred
        if a<Tred+Tgreen               
            if L(1,end)==1 %如果有车等待
                L_car(width/10,1:long/10)=1;
                L_car(width/10,1:long/10)=0;
                L(1,end)=0;
                turn=randperm(3,1); 
                if turn==1
              %判断为直线
                L_1(1,1)=1;   
                end
              if turn==2
              %判断为右转
                L_2(1,1)=1;   
              end
                if turn==3
              %判断为左转
                L_3(1,1)=1;   
                end
            end
        else
            a=0;
        end                             
    end
    %--------------------------------------------------------
    V_1(L_1(:,1:end-2)==1&L_1(:,2:end-1)==0&L_1(:,3:end)==0)=2;
    V_1(L_1(:,1:end-2)==1&L_1(:,2:end-1)==0&L_1(:,3:end)==1)=1;
    V_1(L_1(:,1:end-2)==1&L_1(:,2:end-1)==1)=0;

    L_1([zeros(1,1) V_1(:,1:end-1)]==1)=1;
    L_1([zeros(1,2) V_1(:,1:end-2)]==2)=1;
    L_1(V_1(:,1:end)==2|V_1(:,1:end)==1)=0;
    L_1(1,end)=0;
    L_1(1,end-1)=0;
    
    %--------------------------------------------------------
    V_2(L_2(:,1:end-2)==1&L_2(:,2:end-1)==0&L_2(:,3:end)==0)=2;
    V_2(L_2(:,1:end-2)==1&L_2(:,2:end-1)==0&L_2(:,3:end)==1)=1;
    V_2(L_2(:,1:end-2)==1&L_2(:,2:end-1)==1)=0;
    L_2([zeros(1,1) V_2(:,1:end-1)]==1)=1;
    L_2([zeros(1,2) V_2(:,1:end-2)]==2)=1;
    L_2(V_2(:,1:end)==2|V_2(:,1:end)==1)=0;
    L_2(1,end)=0;
    L_2(1,end-1)=0;
    %--------------------------------------------------------
    V_3(L_3(:,1:end-2)==1&L_3(:,2:end-1)==0&L_3(:,3:end)==0)=2;
    V_3(L_3(:,1:end-2)==1&L_3(:,2:end-1)==0&L_3(:,3:end)==1)=1;
    V_3(L_3(:,1:end-2)==1&L_3(:,2:end-1)==1)=0;
    L_3([zeros(1,1) V_3(:,1:end-1)]==1)=1;
    L_3([zeros(1,2) V_3(:,1:end-2)]==2)=1;
    L_3(V_3(:,1:end)==2|V_3(:,1:end)==1)=0;
    L_3(1,end)=0;
    L_3(1,end-1)=0;
    
    
    L_car(width/10,1:long/10-1)=L;
    L_car(width/10,long/10+1:end)=L_1;
    L_car(width/10+1:end,long/10)=L_2';%右转路段统计
    L_car(width/10-1:-1:1,long/10)=L_3';
    set(H,'CData',L_car);
    n1=find(L>=1);
    gs1(1,i)=length(n1);
    pause(0.1);
end
%end
