function result=TOPSISInterval(datas,poi)           %区间型
minData=input(['这是第' num2str(poi) '列数据，输入最佳区间的下界:']);                 
maxData=input('输入最佳区间的上界:');
result=zeros(size(datas,1),1);%预分配
M=max(minData-min(datas),max(datas)-maxData);
for i=1:size(datas)
    if datas(i)<=maxData&&datas(i)>=minData
        result(i)=1;
    elseif datas(i)>maxData
        result(i)=1-(datas(i)-maxData)/M;
    else
        result(i)=1-(minData-min(datas))/M;       
    end
end