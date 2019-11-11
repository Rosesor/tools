clear
clc
maindir='E:\yihang\database-sar\SAR11_rotate_at_1\train\';
subdir=dir(maindir);%先确定子文件夹
savedpath1='E:\yihang\database-sar\sar10_rotate\sar10_roata_train';%图像新保存到的路径
mkdir(savedpath1);
savedpath2='E:\yihang\database-sar\sar10_rotate\sar10_roata_valid';
mkdir(savedpath2);
savedpath3='E:\yihang\database-sar\sar10_rotate\sar10_roata_test';
mkdir(savedpath3);
%create label file
train=fopen('E:\yihang\database-sar\sar10_rotate\sar10_roata_train\train.txt','a');
test=fopen('E:\yihang\database-sar\sar10_rotate\sar10_roata_test\test.txt','a');
valid=fopen('E:\yihang\database-sar\sar10_rotate\sar10_roata_valid\valid.txt','a');

%在训练、验证、测试集中分别生成165个文件夹
for i=0:9  %总的类别数
    index=int2str(i);
    savedpath1=['E:\yihang\database-sar\sar10_rotate\sar10_roata_train','\',index];
    savedpath2=['E:\yihang\database-sar\sar10_rotate\sar10_roata_valid','\',index];
    savedpath3=['E:\yihang\database-sar\sar10_rotate\sar10_roata_test','\',index];
    mkdir(savedpath1);
    mkdir(savedpath2);
    mkdir(savedpath3);
end

for i=3:12
    subdirpath=fullfile(maindir,subdir(i).name,'*.jpg');
    images=dir(subdirpath);
    pic_num=length(images);
    Q=randperm(pic_num);
%     images(Q(1)).name
    label=i-3;
    for j=1:int32(pic_num*0.7)
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);%一个文件夹，12张图片中的一张被读入
        savedname=int2str(i-3);
        imwrite(ImageData,['E:\yihang\database-sar\sar10_rotate\sar10_roata_train','\',savedname,'\',images(Q(j)).name]);
        fprintf(train,'train/%d/%s %d\n',label,images(Q(j)).name,label);
    end
    for j=int32(pic_num*0.7)+1:int32(pic_num*0.9);
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);%一个文件夹，12张图片中的一张被读入
        savedname=int2str(i-3);
        imwrite(ImageData,['E:\yihang\database-sar\sar10_rotate\sar10_roata_valid','\',savedname,'\',images(Q(j)).name]);
        fprintf(valid,'valid/%d/%s %d\n',label,images(Q(j)).name,label);
    end
    for j=int32(pic_num*0.9)+1:pic_num
        Imagepath=fullfile(maindir,subdir(i).name,images(Q(j)).name);
        ImageData=imread(Imagepath);%一个文件夹，12张图片中的一张被读入
        savedname=int2str(i-3);
        imwrite(ImageData,['E:\yihang\database-sar\sar10_rotate\sar10_roata_test','\',savedname,'\',images(Q(j)).name]); 
        fprintf(test,'test/%d/%s %d\n',label,images(Q(j)).name,label);
    end

end
fclose(train);
fclose(test);
fclose(valid);
