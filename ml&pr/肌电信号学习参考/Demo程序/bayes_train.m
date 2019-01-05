function [cpu_time,Accuracy] = bayes_train()
clearvars
tic

filename = 'chf.txt';  %�����ļ�����
data_all = importdata(filename);

data1 = data_all(6001:9000,1:16);  %��һ������
data2 = data_all(16001:19000,1:16); %�ڶ�������
data3 = data_all(26001:29000,1:16); %����������
data4 = data_all(36001:39000,1:16); %���ĸ�����
data5 = data_all(46001:49000,1:16); %���������

%�Ը������ƶ������ֵ��źŽ���RMS�ź���ȡ
data_1_1 = GetRMS(data1, 300, 50);
data_2_1 = GetRMS(data2, 300, 50);
data_3_1 = GetRMS(data3, 300, 50);
data_4_1 = GetRMS(data4, 300, 50);
data_5_1 = GetRMS(data5, 300, 50);

%�Ը������ƶ������ֵ��źű궨����ǩ
a1 = ones(55,1) * 1;
a2 = ones(55,1) * 2;
a3 = ones(55,1) * 3;
a4 = ones(55,1) * 4;
a5 = ones(55,1) * 5;

%�γ�ѵ������+�������ݺϼ�
data_1 = [data_1_1 a1];
data_2 = [data_2_1 a2];
data_3 = [data_3_1 a3];
data_4 = [data_4_1 a4];
data_5 = [data_5_1 a5];

%�ֱ��ձ����γ�ѵ�����Ͳ��Լ�
[row, col] = size(data_1);
data_traing = [data_1;data_2;data_3;data_4];
[m, n] = size(data_traing);
num_train = fix(m * 0.7);
num_test = fix(m * 0.3);
accuracy = zeros(30,1);

for i = 1:30
    num=0;
    choose = randperm(length(data_traing));
    %�γ������ѵ������ѵ������ǩ�����Լ��Լ����Լ���ǩ
    TrainData = data_traing(choose(1:num_train),:);
    TrainLabel = TrainData(:,end);
    TrainData = TrainData(1:num_train,1:col-1);
    TestData = data_traing(choose(num_train+1:end),:);
    TestLabel = TestData(:,end);
    TestData = TestData(1:num_test,1:col-1);
    
    % %  4.Bayes����
    classifer = fitcnb(TrainData, TrainLabel);
    predict_label = predict(classifer,TestData);
    accuracy(i) = length(find(predict_label == TestLabel))/length(TestLabel);
end

cpu_time = toc;
Accuracy = mean(accuracy);
end