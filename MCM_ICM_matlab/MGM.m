clear all
clc
%输入待预测时刻 k 及原始序列 X0
% k=9;%k等于9，表示第9个的预测值
X0=[481.8, 509.3, 532.9, 544.5, 554.2, 576.7, 617.3, 618.2, 623.5, 614.7, 621.0;
    166.2, 175.9, 200.1, 258.1, 293.5, 334.8, 376.4, 405.9, 421.3, 390.1, 389.7];
X0=X0';
%对原始序列 X0 累加生成序列 X1
[n,m]=size(X0);%m为指标，n为样本个数
for j=1:m 
    c=0;
    for i=1:n
 	  c=X0(i,j)+c;
      X1(i,j)=c;
    end
end
%计算数据矩阵 L
for j=1:m
    for i=1:n- 1
        l(i,j)=(X1(i,j)+X1(i+1,j))/2;
    end
end
L=[l ones(n- 1,1)];
%计算 Y 及参数估计值
for j=1:m
    Y(1:n-1,j)=X0(2:n,j);
    D(:,j)=inv(L'*L)*L'*Y(1:n- 1,j) ;
end
D=D';
A=D(1:end,1:end- 1);
B=D(1:end,end);
% %计算模型的拟合值或预测值
% S=X1(1,1:end);
% if k==1
%     Z=S'
% elseif k>1
% %     Z=expm2(A*(k- 1))*S' +inv(A)*(expm2(A*(k- 1))- eye(size(expm2(A*(k- 1)))))*B- (expm2(A*(k- 2))*S'+inv(A)*(expm2(A*(k- 2))- eye(size(expm2(A*(k- 2)))))*B)
%     Z=myFunction(A*(k- 1))*S' +inv(A)*(myFunction(A*(k- 1))- eye(size(myFunction(A*(k- 1)))))*B- (myFunction(A*(k- 2))*S'+inv(A)*(myFunction(A*(k- 2))- eye(size(myFunction(A*(k- 2)))))*B)
% else
%     disp(' 输入错误! k 不得小于 1')
% end
S=X1(1,1:end);
year=13;
Z=zeros(year,m);
Z(1,1:m)=S';
for i=2:year
    Z(i,1:m)=myFunction(A*(i- 1))*S' +inv(A)*(myFunction(A*(i- 1))- eye(size(myFunction(A*(i- 1)))))*B- (myFunction(A*(i- 2))*S'+inv(A)*(myFunction(A*(i- 2))- eye(size(myFunction(A*(i-2)))))*B)
end
