% 层次分析法

CR=0.1;
while CR>=0.1
    A = input( '输入矩阵' );            %矩阵A
    [Vector,Values] = eig( A );         %Vector特征向量，Values特征值
    % disp( Vector );
    % disp( Values );
    maxValue=max( max( Values ) );      %maxValue最大特征值
    [n n]=size(A);                      %求列数目
    CI=( maxValue-n )/( n-1 );          %一致性指标consistency index
    RI=[0 0 0.52 0.89 1.12 1.26 1.36 1.41 1.46 1.49 1.52 1.54 1.56 1.58 1.599];
    % size(RI,2);
    CR=CI/RI(n);                        %求一致性比例CR,n>10可考虑二级指标
    if CR>=0.1
        disp( '一致性比例大于0.1，请重新输入' );
    end
end
disp( '一致性比例为' );
CR;
%%
% % 算数平均法求权重
columnSum=sum( A );                     %求每一列
columnSumMatrix=repmat(columnSum,n,1);  %拓展矩阵
standardMatrix=A./columnSumMatrix;      %相除
disp( '算数平均法权重为' );
result1=sum( standardMatrix,2 )/n       %结果
%%
% % 几何平均法求权重
rowProd=prod( A ,2);                    %行相乘结果
rowProd2=rowProd.^(1/n);                %结果开n次方
sumRow=sum(rowProd2);                   %结果总数
disp( '几何平均法求权重' );
result2=rowProd2./sumRow               %权重
%%
% % 特征值求权重
[Vector,Values] = eig( A );         %Vector特征向量，Values特征值
maxValue=max( max( Values ) );           %最大的特征值
[row,column]=find(Values==maxValue ,1);%最大特征值的位置
disp( '特征值求权重结果为' );
result3=Vector(:,column)/sum(Vector(:,column))