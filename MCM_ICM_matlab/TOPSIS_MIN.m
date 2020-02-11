function result=TOPSISM_MIN(datas)                      %极小型转化为极大型
maxData=max(datas);                                     %最大值
result=maxData-datas;                                   %结果