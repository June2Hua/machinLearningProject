function result=TOPSIS_MID(datas,poi)                   %中间型转化为极大型
mid=input(['这是第' num2str(poi) '列数据，请输入最佳的数值:']);                       %最佳值
M=max(abs(datas-mid));                                  %区间!!!!!!!
result=1-abs(datas-mid)./M;