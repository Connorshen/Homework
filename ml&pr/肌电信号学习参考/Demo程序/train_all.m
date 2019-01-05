clearvars

[cpu_time_lda,accuracy_lda] = lda_train();
[cpu_time_svm,accuracy_svm] = svm_train();
[cpu_time_knn,accuracy_knn] = knn_train();
[cpu_time_bayes,accuracy_bayes] = bayes_train();

figure;
hold all;
subplot(2,1,1);
x = [1,2,3,4];
y = [cpu_time_lda,cpu_time_svm,cpu_time_knn,cpu_time_bayes];
y = roundn(y,-2);
bar(x,y)
for i = 1:length(x)
    text(x(i),y(i),num2str(y(i),'%g'),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom')
end
title('分类算法耗时比较')
set(gca,'xticklabel',{"lda","svm","knn","bayes"});
xlabel('分类算法')
ylabel('时间(s)')

subplot(2,1,2);
x = [1,2,3,4];
y = [accuracy_lda,accuracy_svm,accuracy_knn,accuracy_bayes];
y = y*100;
y = roundn(y,-2);
bar(x,y)
for i = 1:length(x)
    text(x(i),y(i),num2str(y(i),'%g%%'),...
    'HorizontalAlignment','center',...
    'VerticalAlignment','bottom')
end
title('分类算法精确度比较')
set(gca,'xticklabel',{"lda","svm","knn","bayes"});
xlabel('分类算法')
ylabel('精确度(%)')
hold off;
