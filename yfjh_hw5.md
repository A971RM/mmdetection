# 驭风计划作业5

## 安装环境
环境的安装有两个注意点：

1. torch, mmcv的版本
2. torch, mmcv的顺序

## 安装虚拟环境
建议不使用conda,而是直接使用python的模块venv，在当前目录下创建环境
1. python -m venv openmmlab3
2. cd openmmlab3
3. source bin/activate
4. 检查
   1. (openmmlab3) aistudio@jupyter-1060416-3829406:~/openmmlab3$ type python
   2. (openmmlab3) aistudio@jupyter-1060416-3829406:~/openmmlab3$ python -V


### 查看当前cuda版本
nvcc -V
我的版本是11.5

### 查找mmcv所支持的torch版本
https://github.com/open-mmlab/mmcv#installation

根据上面链接，可以查到CUDA11.5支持的torch版本是torch 1.11。所以只能安装torch 1.11

### 安装torch
torch 1.11 https://pytorch.org/get-started/locally/

如果旧版本查找 https://pytorch.org/get-started/previous-versions/

注意修改
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

为

pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu115

### 安装mmcv
https://github.com/open-mmlab/mmcv#installation

点开install可以看到

pip install mmcv-full=={mmcv_version} -f https://download.openmmlab.com/mmcv/dist/cu115/torch1.11.0/index.html

此时注意版本的选择，打开https://download.openmmlab.com/mmcv/dist/cu115/torch1.11.0/index.html

可以看到只支持版本1.4.7/1.4.8，所以选择1.4.8

pip install mmcv-full==1.4.8 -f https://download.openmmlab.com/mmcv/dist/cu115/torch1.11.0/index.html

### 安装mmdetection
https://github.com/open-mmlab/mmdetection/blob/master/docs/en/get_started.md

可以看到master	mmcv-full>=1.3.17, <1.5.0

下载代码。进行安装

git clone https://github.com/open-mmlab/mmdetection.git

cd mmdetection

pip install -r requirements/build.txt

pip install -v -e .  # or "python setup.py develop"

## 训练脚本
python tools/train.py configs/faster_rcnn/faster_rcnn_r50_fpn_1x_didi.py

## 生成test.json
cd ..\datasets\didi\dataset_release

python ..\..\..\mmdetection\tools\dataset_converters\images2testjson.py test val.json

## 预测结果
python tools/test.py  configs/faster_rcnn/faster_rcnn_r50_fpn_1x_didi.py ./work_dirs/faster_rcnn_r50_fpn_1x_didi/epoch_12.pth --format-only --options "jsonfile_prefix=./test_results"
