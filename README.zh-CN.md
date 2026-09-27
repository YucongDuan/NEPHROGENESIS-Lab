# NEPHROGENESIS-Lab

[English](README.md) · [项目展示页](https://yucongduan.github.io/NEPHROGENESIS-Lab/) · [下载与版本](https://github.com/YucongDuan/NEPHROGENESIS-Lab/releases) · [快速开始](GETTING_STARTED.md)

本项目是段玉聪、吴中道《肾脏简史》的英文开源计算配套系统，将书中的研究问题转化为可执行实验、明确假设、模型比较和可追溯记录。

提供 24 个实验入口、18 章实验导读、22 项书中方程检查，以及带单位的计算、守恒动力学、研究数据拟合与 DIKWP 实验记录。

## 本地运行

下载并解压源码后，在项目目录中运行（Python 3.10+，无需额外运行依赖）：

```sh
python -m nephrogenesis verify
python -m nephrogenesis run transport --out runs/first-experiment
python -m nephrogenesis replay runs/first-experiment
python -m nephrogenesis serve --port 8765
```

打开 `http://127.0.0.1:8765` 使用可编辑参数的计算界面。网页展示页提供预先计算的示例报告；重新计算请运行本地 Python 程序。

2026-09-27 发布准备中已通过 **198 项本地测试**。具体环境、原始附件校验与运行日志见 [发布记录](PUBLICATION.md)，云端测试状态见 [GitHub Actions](https://github.com/YucongDuan/NEPHROGENESIS-Lab/actions)。

代码与原创配套文档采用 Apache-2.0。书稿未包含在仓库中，也不因软件发布而改变版权。计算结果的适用范围以各实验声明的条件为准。

[另一个图书配套项目](https://github.com/YucongDuan/DIKWP-HepatoGenesis-Lab) · [段玉聪 GitHub 主页](https://github.com/YucongDuan) · [全部项目目录](https://github.com/YucongDuan/YucongDuan/blob/main/REPOSITORY_DIRECTORY.zh-CN.md)
