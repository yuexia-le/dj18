# Vocab-Master 生产级部署方案

本项目不仅是一个 Flask 词汇管理应用，更是一套完整的容器化自动运维实验场。

## 🏗 架构说明
- **前端/后端**: Flask + Python 3.12
- **数据库**: MySQL 8.0 (持久化挂载至宿主机)
- **部署引擎**: Docker + Docker Compose
- **自动化**: GitHub Actions (CI/CD)

## 🚀 部署特性
1. **全自动 CI**: 代码 Push 后自动触发镜像构建并同步至阿里云镜像站。
2. **私有化 CD**: 利用 Self-hosted Runner 在内网 Ubuntu 24.04 环境实现安全重启。
3. **高安全性**: 敏感 API Key 通过 GitHub Secrets 动态注入，不泄露在代码库中。

## 🛠 本地快速启动
```bash
docker login ...
docker pull ...
docker run -d --name vocab_container ...
