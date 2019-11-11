clear
clc
maindir='E:\yihang\database-sar\sar10_rotate\train\';
subdir=dir(maindir);%��ȷ�����ļ���
savedpath1='E:\yihang\database-sar\mini_sar234\train';%ͼ���±��浽��·��
mkdir(savedpath1);
savedpath2='E:\yihang\database-sar\mini_sar234\val';
mkdir(savedpath2);
savedpath3='E:\yihang\database-sar\mini_sar234\test';
mkdir(savedpath3);
%create label file
train=fopen('E:\yihang\database-sar\mini_sar234\train\train.txt','a');
test=fopen('E:\yihang\database-sar\mini_sar234\test\test.txt','a');
valid=fopen('E:\yihang\database-sar\mini_sar234\val\valid.txt','a');

%�����ļ���
for i=2:4  %�ܵ������
    index=int2str(i);
    savedpath1=['E:\yihang\database-sar\mini_sar234\train','\',index];
    savedpath2=['E:\yihang\database-sar\mini_sar234\val','\',index];
    savedpath3=['E:\yihang\database-sar\mini_sar234\test','\',index];
    mkdir(savedpath1);
    mkdir(savedpath2);
    mkdir(savedpath3);
end

for i=5:7
    subdirpath=fullfile(maindir,subdir(i).name,'*.jpg');
    images=dir(subdirpath);
    pic_num=length(images);
    Q=randperm(pic_num);
%     images(Q(1)).name
    label=i-3;
    for j=1:int32(2000*0.7)%һ���ļ��У��ٷ�֮70��ѵ����
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);
        savedname=int2str(i-3);
        imwrite(ImageData,['E:\yihang\database-sar\mini_sar234\train','\',savedname,'\',images(Q(j)).name]);
        fprintf(train,'train/%d/%s %d\n',label,images(Q(j)).name,label);
    end
    for j=int32(2000*0.7)+1:int32(2000*0.9);%һ���ļ��У��ٷ�֮20��val��
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);
        savedname=int2str(i-3);
        imwrite(ImageData,['E:\yihang\database-sar\mini_sar234\val','\',savedname,'\',images(Q(j)).name]);
        fprintf(valid,'valid/%d/%s %d\n',label,images(Q(j)).name,label);
    end
    for j=int32(2000*0.9)+1:int32(2000*1) %һ���ļ��У��ٷ�֮10��ѵ����
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);
        savedname=int2str(i-3);
        imwrite(ImageData,['E:\yihang\database-sar\mini_sar234\test','\',savedname,'\',images(Q(j)).name]); 
        fprintf(test,'test/%d/%s %d\n',label,images(Q(j)).name,label);
    end

end
fclose(train);
fclose(test);
fclose(valid);
