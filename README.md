# Bilibili Downloader

无聊写的一个程序，基于 PyQt5 。

此程序只可以下载 B站 上由 UP主 上传的视频 (即链接为 www.bilibili.com/video/BVxxxxxxxxxx 格式的)。

**警告:** 此程序不支持在 Windows 以外的平台运行。

本人一般不会对其进行维护，除非出现重大错误 ~~(或者作者闲的无聊)~~。

## 使用

您可以在 Releases 获得每次更新的 Windows 可执行文件。

也可以直接运行 main.py (**对于 macOS / Linux 用户, 这是最好的**) 。

如果您要直接运行 main.py 来使用此程序，请先在命令行里输入以下命令:

    对于 macOS / Linux 用户:
    python3 -m pip install -r requirements.txt
    对于 Windows 用户:
    pip3 install -r reqirements.txt

每次下载视频后都会把下载的视频名和视频地址写入程序所在目录下的 "DownloadHistory.txt" 文件。(不会记录下载时间)

## 关于 FFMPEG

此程序已内置 [FFMPEG](https://ffmpeg.org) (版本 N-102989-g7f6d20931b-20210717, 来自 [BtbN 的 Github 构建仓库](https://github.com/BtbN/FFmpeg-Builds))。

此程序除 FFMPEG 程序遵守 LGPL 许可证外, 其余代码以 MIT 协议和 "特此声明" 部分的条款 授权。

FFMPEG (C) 2000-2021 the FFmpeg developers.

## 特此声明

若您使用本程序，则代表您同意以下条款 和 MIT 协议，否则您无权使用此软件:

***此软件禁止用于商业用途，使用此软件引发的任何后果与作者无关，作者不承担责任。***
