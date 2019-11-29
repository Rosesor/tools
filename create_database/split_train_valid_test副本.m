clear
clc
maindir='F:\FKP\left_index\left_index\';
subdir=dir(maindir);%先确定子文件夹
savedpath1='F:\FKP\left_index\left_index_train';%图像新保存到的路径
mkdir(savedpath1);
savedpath2='F:\FKP\left_index\left_index_valid';
mkdir(savedpath2);
savedpath3='F:\FKP\left_index\left_index_test';
mkdir(savedpath3);

%在训练、验证、测试集中分别生成165个文件夹
for i=1:165  %总的类别数
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
        ImageData=imread(Imagepath);%一个文件夹，12张图片中的一张被读入
        savedname=int2str(i-2);
        imwrite(ImageData,['F:\FKP\left_index\left_index_train','\',savedname,'\',images(Q(j)).name]);        
    end
    j=7;
    Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
    ImageData=imread(Imagepath);%一个文件夹，12张图片中的一张被读入
    savedname=int2str(i-2);
    imwrite(ImageData,['F:\FKP\left_index\left_index_valid','\',savedname,'\',images(Q(j)).name]);      
    for j=8:12
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);%一个文件夹，12张图片中的一张被读入
        savedname=int2str(i-2);
        imwrite(ImageData,['F:\FKP\left_index\left_index_test','\',savedname,'\',images(Q(j)).name]); 
    end

end
