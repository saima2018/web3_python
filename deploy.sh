#!/bin/bash

time=$(date +'%Y-%m-%d-%H-%M')

dst_path=/root/planckx2-jar-yaml/planckx2-web3

cd  $dst_path

echo "构建镜像.推送到仓库"

docker  build -t planckx-web3  . &&docker tag planckx-web3  10.10.10.88:8890/pre-planckx2/planckx-web3-$time &&docker push  10.10.10.88:8890/pre-planckx2/planckx-web3-$time


[ $? -ne 0 ] && echo "构建镜像失败 请检查" && exit 1

echo "开始更新k8s镜像"
kubectl set image  deployment/deployment-pre-planckx2-web3 app-pre-planckx2-web3=10.10.10.88:8890/pre-planckx2/planckx-web3-$time  -n pre-planckx
[ $? -ne 0 ] && echo "k8s更新镜像失败 请检查" && exit 1


sleep 3

echo "开始删除仓库镜像"
docker rmi -f 10.10.10.88:8890/pre-planckx2/planckx-web3-$time

[ $? -ne 0 ] && echo "删除镜像失败 请检查" && exit 1

echo " finish "
