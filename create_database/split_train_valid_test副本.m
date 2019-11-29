clear
clc
maindir='F:\FKP\left_index\left_index\';
subdir=dir(maindir);%��ȷ�����ļ���
savedpath1='F:\FKP\left_index\left_index_train';%ͼ���±��浽��·��
mkdir(savedpath1);
savedpath2='F:\FKP\left_index\left_index_valid';
mkdir(savedpath2);
savedpath3='F:\FKP\left_index\left_index_test';
mkdir(savedpath3);

%��ѵ������֤�����Լ��зֱ�����165���ļ���
for i=1:165  %�ܵ������
    index=int2str(i);    
    savedpath1=['F:\FKP\left_index\left_index_train','\',index];
    savedpath2=['F:\FKP\left_index\left_index_valid','\',index];
    savedpath3=['F:\FKP\left_index\left_index_test','\',index];
    mkdir(savedpath1);
    mkdir(savedpath2);
    mkdir(savedpath3);
end

for i=3:167
    subdirpath=fullfile(maindir,subdir(i).name,'*.jpg');
    images=dir(subdirpath);
    Q=randperm(12);
    for j=1:6
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);%һ���ļ��У�12��ͼƬ�е�һ�ű�����
        savedname=int2str(i-2);
        imwrite(ImageData,['F:\FKP\left_index\left_index_train','\',savedname,'\',images(Q(j)).name]);        
    end
    j=7;
    Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
    ImageData=imread(Imagepath);%һ���ļ��У�12��ͼƬ�е�һ�ű�����
    savedname=int2str(i-2);
    imwrite(ImageData,['F:\FKP\left_index\left_index_valid','\',savedname,'\',images(Q(j)).name]);      
    for j=8:12
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);%һ���ļ��У�12��ͼƬ�е�һ�ű�����
        savedname=int2str(i-2);
        imwrite(ImageData,['F:\FKP\left_index\left_index_test','\',savedname,'\',images(Q(j)).name]); 
    end

end
