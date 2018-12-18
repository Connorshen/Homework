%GMM for glove
% clc;
% clear;
%--------------load data---------------------
load glove_grasp_6_13_20_100points.mat
Odata = glove_grasp_6_13_20;

[subjectnum, motionnum, repnum] = size(Odata);
totaltimeused = 0;
% allresult = zeros(subjectnum,motionnum);
% allrate = zeros(1,19);
%%--------------------------------------------
%%
 for modelnum = 1:1
    for subject = 1:6
        for motion = 1:motionnum
            
            tstart1 = tic;


            nbStates = 10;
            %%---------------modeling---------------------
            data4model = []; 
            for i = 1:modelnum                            %single��1
                tmp = [1:100;Odata{subject,motion,i}];    %single
                data4model = [data4model,tmp];            %single
            end                                           %single
            
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            nbVar = size(data4model,1);

            % Training of GMM by EM algorithm, initialized by k-means clustering.
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            tstart2 = tic;
            %prior��ʾK GMM������������  1*K
            %Mu��ʾK GMM���������
            %Sigma��ʾK GMM�����Э�������
            %nbStates��ʾGMM �������Ŀ����K
            %data4model��22*600���󣬱�ʾ22ά��600���ݵ�
            [Priors, Mu, Sigma] = EM_init_kmeans(data4model, nbStates);
            [Priors, Mu, Sigma] = EM(data4model, Priors, Mu, Sigma);
            tmodel = toc(tstart2);
            model = Mu(2:22,:);


            %--------------------------recognizing------------

            result = zeros( motionnum, repnum, motionnum);
            for j = 1:motionnum   %13
                for i = 1:repnum   %20
                    tstart = tic;   %��¼��ǰʱ�䣬��toc���ʹ������ʱ
                    testdata = Odata{subject,j,i}(:,fix(Mu(1,:)));  %21*10 double�� fix����������βȡ��, Mu(1,:)��ӡMu��һ�У�Mu��22*10����
                    result( j, i, motion) = sum(sum(abs(testdata - model)));
                    trecognize = toc(tstart);%�ķ�ʱ��
                end
            end
            result(:,:,motion) = result(:,:,motion) - (min(result(:,:,motion))'*ones(1,motionnum))';
            aa_tmp = (length(find (result(motion,modelnum+1:repnum,motion) == 0)))/(repnum-modelnum);

            allresult(subject,motion,modelnum) = aa_tmp;
            totaltimeused = totaltimeused + toc(tstart1);
            tremaining = toc(tstart1)*(subjectnum*motionnum - (subject-1)*motionnum - motion); 
            disp([num2str(modelnum),',iterations remaining:',num2str(subjectnum*motionnum - (subject-1)*motionnum - motion),'  time used:',num2str(totaltimeused),'s']);    
        end
    end
    modelnum;
    allrate(1,modelnum) = mean(mean(allresult(:,:,modelnum)));
    disp(['Finished! Overall recognition rate is: ', num2str(allrate)]);
end



