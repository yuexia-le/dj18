# Vocab-Master K8s Edition

这是一个基于云原生架构的词汇学习系统交付方案。

## ✨ 核心特性
* **自动化交付**：集成 GitHub Actions，实现从源码到 K8s 运行环境的端到端自动化。
* **版本追踪**：镜像标签与 Git Commit SHA 绑定，支持 `kubectl rollout history` 追溯部署原因。
* **高可用架构**：2 副本 Deployment 部署，配合 K8s 调度机制确保服务高可用。
* **环境自愈**：利用 K8s 探针自动检测并重启异常容器，保障业务连续性。

## 🛠 部署架构图


## 📋 快速开始
1. 在 K8s 中创建秘钥：`kubectl create secret docker-registry aliyun-registry-secret ...`
2. 配置 GitHub Secrets：`KUBE_CONFIG`, `ALIYUN_REGISTRY_USER` 等。
3. 推送代码至 main 分支，观察 GitHub Actions 流水线自动完成部署。
