name='20条河流的水质情况数据.xlsx';
poi='B2:E21';
datas=xlsread(name,poi);                %获得Excel文件的数据
num=[];% input('请输入要处理的列数,如[1 2 3]');
w=ones(1,size(num,1));
Type=[];% input('请输入对应的类型，1是极小型，2是中间型，3是区间型，如[2 3 1]：');
Judge=0;% input('请问是否需要输入权重？需要则输入1，不需要则输入0：');
if Judge==1
    w=[];% input('请输入每一列的相应权重,如[0.6 0.9 0.8]：');
end
for i=1:size(num,2)
    if Type(i)==1
        datas(:,num(i))=TOPSIS_MIN(datas(:,num(i)));           %极小型
    elseif Type(i)==2
        datas(:,num(i))=TOPSIS_MID(datas(:,num(i)),num(i));     %中间型
    elseif Type(i)==3
        datas(:,num(i))=TOPSISInterval(datas(:,num(i)),num(i));        %区间型
    end
end
%无量钢化，标准化
for i=1:size(num,2)
    datas2(:,i)=datas(:,i)./sum(datas(:,i));   %标准化
end

%归一化sum(datas2,1)
DPositive=((datas2-repmat(max(datas2),size(datas2,1),1)).^2).^0.5;
DPositive=repmat(w,size(datas2,1),1).*DPositive;
DNegative=((datas2-repmat(min(datas2),size(datas2,1),1)).^2).^0.5;
DNegative=repmat(w,size(datas2,1),1).*DNegative;
datas3=DNegative./(DPositive+DNegative);
for i=1:size(num,2)
    datas4(:,i)=datas(:,i)./sum(datas(:,i));   %标准化
end

