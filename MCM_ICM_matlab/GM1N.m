%灰色预测模型GM（1，n）模型的matlab源代码，包括预测模型的建立，以及模型的精度检验指标c,p的计算
%假设预测3步，N=3
%如在命令窗口键入：
%gm=ycgm1n([1.6,1.7,2,1.8,1.9],[2,2.4,3,3.2,3.1],[3,3.1,3.2,3.5,2.8],3)
% function GM=ycgm1n(data1,data2,data3,N) %data1:纵摇，data2:升沉，data3:波浪
data1=[1.6,1.7,2,1.8,1.9];
data2=[2,2.4,3,3.2,3.1];
data3=[3,3.1,3.2,3.5,2.8];
N=3;
T=length(data1);  

PYX1=data1;
PYX2=data2;
PYX3=data3;
%进行数据预处理，这里用初值化
X0_1=PYX1./PYX1(1);
X0_2=PYX2./PYX2(1);
X0_3=PYX3./PYX3(1);
%用AGO生成一阶累加生成模块
X1_1(1)=X0_1(1);
X1_2(1)=X0_2(1);
X1_3(1)=X0_3(1);
for i=2:T  
X1_1(i)=X1_1(i-1)+X0_1(i); 
X1_2(i)=X1_2(i-1)+X0_2(i);
X1_3(i)=X1_3(i-1)+X0_3(i);
end 
%构造累加矩阵B
for i=1:T-1 
M1(i)=(0.5*(X1_1(i)+X1_1(i+1)));
M2(i)=(0.5*(X1_2(i)+X1_2(i+1)));
M3(i)=(0.5*(X1_3(i)+X1_3(i+1)));
end 

B1=zeros(T-1,3); 
for i=1:(T-1) 
B1(i,1)=-M1(i);   %-(X1_1(i)+X1_1(i+1)))/2; 
B1(i,2)=X1_2(i+1); 
B1(i,3)=X1_3(i+1);
end
B2=zeros(T-1,2); 
for i=1:(T-1) 
B2(i,1)=-M2(i);   %-(X1_2(i)+X1_2(i+1)))/2; 
B2(i,2)=X1_3(i+1); 
end
B3=zeros(T-1,2); 
for i=1:(T-1) 
B3(i,1)=-M3(i);   %-(X1_3(i)+X1_3(i+1)))/2; 
B3(i,2)=1; 
end
save B1 B1;
save B2 B2;
save B3 B3;
%构造常数项向量Y
for i=2:T                          
Y1(i-1)=X0_1(i); 
Y2(i-1)=X0_2(i);
Y3(i-1)=X0_3(i);
end 
HCS1=inv(B1'*B1)*B1'*Y1';               %用最小二乘法求灰参数HCS1 
H1=HCS1';                            %H1=[a,b2,b3]
HCS2=inv(B2'*B2)*B2'*Y2';               %用最小二乘法求灰参数HCS2 
H2=HCS2';                            %H2=[a,b3]
HCS3=inv(B3'*B3)*B3'*Y3';               %用最小二乘法求灰参数HCS3 
H3=HCS3';                            %H3=[b,a]

%计算出X3的累加序列
for i=1:T+N                         
YCX13(i)=(X0_3(1)-H3(2)/H3(1))*exp(-1*H3(1)*(i-1))+H3(2)/H3(1); 
end 
for i=2:T+N                     
% K(i)=XR1(i)-XR1(i-1); 
YCX0_3(i)=YCX13(i)-YCX13(i-1);
end
YCX0_3(1)=X0_3(1);

%对参数作alpha，beta变换
H2=H2./(1+0.5*H2(1));
%还原计算出X2的预测值
YCX0_2(1)=X0_2(1);
for i=2:T                     
YCX0_2(i)=H2(2).*X1_3(i)-H2(1).*X1_2(i-1);
end
YCX12(T)=X1_2(T);
for i=T+1:T+N
YCX0_2(i)=H2(2).*YCX13(i)-H2(1).*YCX12(i-1);
YCX12(i)=YCX0_2(i)+YCX12(i-1);
end


%对参数作alpha，beta变换
H1=H1./(1+0.5*H1(1));
%还原计算出X1的预测值
YCX0_1(1)=X0_1(1);
for i=2:T                     
YCX0_1(i)=H1(2).*X1_2(i)+H1(3).*X1_3(i)-H1(1).*X1_1(i-1);
end
YCX11(T)=X1_1(T);
for i=T+1:T+N
YCX0_1(i)=H1(2).*YCX12(i)+H1(3).*YCX13(i)-H1(1).*YCX11(i-1);
YCX11(i)=YCX0_1(i)+YCX11(i-1);
end

%数据还原
GM=YCX0_1;  %.*PYX1(1);  
save GM GM; 
e0(1,T-1)=zeros;   
for i=1:T-1                      %求X1到X5的残差值e0                     
e0(i)=(X0_1(i+1)-YCX0_1(i+1))/X0_1(i+1); %1-YCX0_1(i+1)/X0_1(i+1);
end 
save e0 e0; 
e0_average=sum(abs(e0))/length(e0)
p=1-e0_average;


X_average=mean(X0_1)              %求原始数据x0均值 
s1=std(PYX1)                     %求原始数据的标准差 
s2=std(e0) 
c=s2/s1                          %计算方差比c,c&lt;0.35为好 

