%建立符号变量a(发展系数)和b(灰作用量)
syms a b;
c = [a b]';

%原始数列 A
A = [174, 179, 183, 189, 207, 234, 220.5, 256, 270, 285];
n = length(A);

%对原始数列 A 做累加得到数列 B
B = cumsum(A);

%对数列 B 做紧邻均值生成
for i = 2:n
    C(i) = (B(i) + B(i - 1))/2; 
end
C(1) = [];

%构造数据矩阵 
B = [-C;ones(1,n-1)];
Y = A; Y(1) = []; Y = Y';

%使用最小二乘法计算参数 a(发展系数)和b(灰作用量)
c = inv(B*B')*B*Y;
c = c';
a = c(1); b = c(2);

%预测后续数据,F用于保存后续的数据,F为累加数据
F = []; F(1) = A(1);
year=10;
for i = 2:(n+year)
    F(i) = (A(1)-b/a)/exp(a*(i-1))+ b/a;
end

%对数列 F 累减还原,得到预测出的数据,G为分解累加数据之后真实的结果
G = []; G(1) = A(1);
for i = 2:(n+year)
    G(i) = F(i) - F(i-1); %得到预测出来的数据
end

disp('预测数据为：');
G

% %模型检验
% 
% H = G(1:10);
% %计算残差序列
% epsilon = A - H;
% 
% %法一：相对残差Q检验
% %计算相对误差序列
% delta = abs(epsilon./A);
% %计算相对误差Q
% disp('相对残差Q检验：')
% Q = mean(delta)
% 
% %法二：方差比C检验
% disp('方差比C检验：')
% C = std(epsilon, 1)/std(A, 1)
% 
% %法三：小误差概率P检验
% S1 = std(A, 1);
% tmp = find(abs(epsilon - mean(epsilon))< 0.6745 * S1);
% disp('小误差概率P检验：')
% P = length(tmp)/n
% 
% %绘制曲线图
% t1 = 1995:2004;
% t2 = 1995:2014;
% 
% plot(t1, A,'ro'); hold on;
% plot(t2, G, 'g-');
% xlabel('年份'); ylabel('污水量/亿吨');
% legend('实际污水排放量','预测污水排放量');
% title('长江污水排放量增长曲线');
% grid on;