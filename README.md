# kaggle_starter

## Anaconda Install 

[参考URL](https://www.virment.com/setup-anaconda-python-jupyter-ubuntu/)

```
$ wget https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
$ bash Anaconda3-2019.03-Linux-x86_64.sh
$ source ~/.bashrc
$ conda -V
```

## Prepare Jupyter notebook

[参考URL](https://qiita.com/tk_01/items/307716a680460f8dbe17)
```
$ conda install notebook
$ cd ~
$ jupyter notebook --generate-config
$ cd .jupyter
$ openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mykey.key -out mycert.pem

#色々情報求められるがEnterで無視

$ python #Launch python

>>> from notebook.auth import passwd; passwd()
Enter password:[Enter password]


>>> quit()
$ cd .jupyter
$ vi jupyter_notebook_config.py
# 下記修正箇所はデフォルトでコメントアウトされているので、コメントアウトしない
# OpenSSLで作ったファイルへのパス
c.NotebookApp.certfile = u'/home/username/.jupyter/mycert.pem'
c.NotebookApp.keyfile  = u'/home/username/.jupyter/mykey.key'

# どのIPアドレスからのアクセスも受け入れる
c.NotebookApp.ip = '0.0.0.0'

# passwd()コマンドで作ったパスワードのハッシュを貼る
c.NotebookApp.password = u'sha1:...'

# 勝手にブラウザを起動しない
c.NotebookApp.open_browser = False

# 外部からアクセスするためのポート番号を指定する
c.NotebookApp.port = 8888

[Esc] + : + wq + [Enter]

# notebook extensionsを使用する
pip install jupyter-contrib-nbextensions
pip install jupyter-nbextensions-configurator
jupyter contrib nbextension install --user
jupyter nbextensions_configurator enable --user

```


## Install CUDA Toolkit

[NVIDIA](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1604&target_type=deblocal)  
[GCP GPUの追加](https://cloud.google.com/compute/docs/gpus/add-gpus?hl=ja)

```
$ wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-ubuntu1604.pin
$ sudo mv cuda-ubuntu1604.pin /etc/apt/preferences.d/cuda-repository-pin-600
$ wget http://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda-repo-ubuntu1604-10-1-local-10.1.243-418.87.00_1.0-1_amd64.deb
$ sudo dpkg -i cuda-repo-ubuntu1604-10-1-local-10.1.243-418.87.00_1.0-1_amd64.deb
$ sudo apt-key add /var/cuda-repo-10-1-local-10.1.243-418.87.00/7fa2af80.pub
$ sudo apt-get update
$ sudo apt-get -y install cuda
$ sudo nvidia-smi -pm 1
$ nvidia-smi #GPU 認識
$ cat /proc/driver/nvidia/version #NVIDIA バージョン確認
```

## cuDNN 7.6.3 for cuda 10.1 DL (GCE 前提)
[参考URL](https://tech.zeals.co.jp/entry/2019/01/08/094054#cuDNN70%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)  
①NVIDIA のページでアカウント登録  
②ローカルPCにDL  
③GStorageにUL  
④GCEにて下記コマンド  
```
$ #gsutil cp gs://[INSTANCE NAME]/libcudnn7-dev_7.6.3.30-1+cuda10.1_amd64.deb .
$ #gsutil cp gs://[INSTANCE NAME]/libcudnn7-doc_7.6.3.30-1+cuda10.1_amd64.deb .
$ #gsutil cp gs://[INSTANCE NAME]/libcudnn7_7.6.3.30-1+cuda10.1_amd64.deb .
$ #sudo dpkg -i libcudnn7_7.6.3.30-1+cuda10.1_amd64.deb
$ #sudo dpkg -i libcudnn7-dev_7.6.3.30-1+cuda10.1_amd64.deb
$ #sudo dpkg -i libcudnn7-doc_7.6.3.30-1+cuda10.1_amd64.deb
$ gsutil cp gs://[INSTANCE NAME]/libcudnn7-dev_7.6.3.30-1+cuda10.0_amd64.deb .
$ gsutil cp gs://[INSTANCE NAME]/libcudnn7-doc_7.6.3.30-1+cuda10.0_amd64.deb .
$ gsutil cp gs://[INSTANCE NAME]/libcudnn7_7.6.3.30-1+cuda10.0_amd64.deb .
$ sudo dpkg -i libcudnn7_7.6.3.30-1+cuda10.0_amd64.deb
$ sudo dpkg -i libcudnn7-dev_7.6.3.30-1+cuda10.0_amd64.deb
$ sudo dpkg -i libcudnn7-doc_7.6.3.30-1+cuda10.0_amd64.deb

```

## Build Tesorflow Enviroment
```
$ conda create --name tensorflow python=3.6
$ conda activate tensorflow
$ pip install tensorflow-gpu
$ #pip install tensorflow #CPUを使うとき、cuda 10.0を使う2019-9-8時点で10.1はサポートされていないよう
$ pip install keras
$ pip install jupyter notebook
```

## Useful Github commands
### Install Github
```
$ sudo apt-get install git

```

### [GitHub](https://github.com/shinsei66) Connection
[参考URL](https://qiita.com/shizuma/items/2b2f873a0034839e47ce)
```
$ cd ~/.ssh
$ ssh-keygen -t rsa
>> id_git_rsa
$ vi id_rsa.pub
##SSH keyをコピーする
##[github/settings/sshkey](https://github.com/settings/keys)でコピーしたSSH鍵を追加する
$ echo Host github github.com > config
$ echo HostName github.com >> config
$ echo IdentityFile ~/.ssh/id_git_rsa >> config
$ echo User git >> config
$ ssh -T git@github.com
> Warning: Permanently added the RSA host key for IP address 'XXX.XX.XXX.X' to the list of known hosts.
> Hi shinsei66! You've successfully authenticated, but GitHub does not provide shell access.
$ ssh-keygen -R 1X0.XX.XXX.X ##IPは警告メッセージに対応させる
$ ssh -T git@github.com
```


### Copying remote repository to existing directory and push as a new repository to the remote
[参考URL](https://qiita.com/takamicii/items/b0d1cc92fd172468fbf3)
```

# Create a new empty repository named [NEW EMPTY REPOSITORY] for your new project in advance.
git clone git@github.com:shinsei66/[NEW EMPTY REPOSITORY].git # A new directory is made in your local.
cd [NEW EMPTY REPOSITORY]
git remote add [EXISTING REPOSITORY] git@github.com:shinsei66/[EXISTING REPOSITORY].git
git pull [EXISTING REPOSITORY] master # The contents of the existing directory you want is copied to the directory.
git add -A
git commit -m "first commit"
git remote rm [EXISTING REPOSITORY]
git push -u origin master


# 上記の流れをシェルスクリプトにまとめたので、以下をコマンド上で実施すればOK
sh git_newrepo_clone.sh GITHUB_USERNAME NEW_REPOSITORY_NAME
# GITHUB_USERNAMEはgithubのユーザー名、NEW_REPOSITORY_NAMEは新規で作りたいkaggle用のレポジトリ名で、この二つを引数として渡す

```

### Other Github Commands

```
$ git rm -r [すでにaddしているもので管理対象から外したいフォルダ]
$ git revert HEAD #直前のコミットを取り消し
```


## Pytorch Installation
[参考URL](https://pytorch.org/get-started/locally/)
```
$ conda create --name pytorch python=3.7
$ conda activate pytorch
$ conda install pytorch torchvision cudatoolkit=10.0 -c pytorch
$ pip install catalyst
$ pip install pretrainedmodels
$ pip install pytorch_toolbelt
$ pip install albumentations
$ pip install pyarrow
$# pip install git+https://github.com/qubvel/segmentation_models.pytorch
```

## Kaggle API
```
$ pip install kaggle
$ mkdir .kaggle
$ cd .kaggle
$ gsutil cp gs://xuqliu_kaggle_6/kaggle.json ./.kaggle
$ ##kaggle data download API###
$ kaggle datasets download XXX/XXX
```

## Useful commands

### tmux conmands
```
# Install tmux
$ sudo apt install git emacs build-essential tmux
$ sudo apt update
# ネットワーク経由でサーバーを使用するときに、ネットワークが切れることによるセッション終了を防ぐためにtmuxを用いる
# これによりネットワークが切れてもtmuxの踏み台サーバーがあることで、セッションは継続される
$ tmux new-session -s <session-name>
$ tmux ls
$ tmux a -t <session-name>
```

### Connect GCP from local

``` 
$ ssh-keygen -t rsa -b 4096 -C "XXXX@XXXX.com"
$ cat ~/.ssh/id_rsa.pub
```

### Check memory status

```
$ free -g                          #GB単位で空きメモリ容量を確認
$ df                               #各アカウントのディスク占有を確認
$ du -sh ./* | sort -rn | head -5  #現在のディレクトリ内の各フォルダのディスク占有Top5を確認
```

### File transfer

```
$ scp -r [アカウント]@[IP]:[ダウンロード元ディレクトリ] [ダウンロード先ディレクトリ]
```
### Change Time zone
```
$ sudo timedatectl set-timezone Asia/Tokyo
```
## Unzip files and change authority

```
$ sudo apt install unzip
$ unzip
$ unzip '*.zip'
#change authority
$ chmod -R 777 train.csv
$ chmod -R 777 *.csv
$ chmod -R 777 *
$ tar -xvf '*.tar'
```
