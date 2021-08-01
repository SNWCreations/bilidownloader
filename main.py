import os
import subprocess
import sys

from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PySide2.QtGui import QCloseEvent

from functions import *
from ui import *

headers = {
    'Referer': 'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}


class DownloadThread(QThread):  # 继承QThread
    # 注册信号
    downloadOKSignal = pyqtSignal(str)
    formattingSignal = pyqtSignal(str)
    ffmpegNotFoundSignal = pyqtSignal(str)
    fileAlreadyExistsSignal = pyqtSignal(str)

    def __init__(self, vname, bv, flv_url, headers, page_num, is_will_convert, save_dir, no_delete_original_video, quality, videoNameLabel, is_will_delete_exists_file, videoFormatType):  # 从前端界面中传递参数到这个任务后台
        super().__init__()
        self.vname = vname
        self.bv = bv
        self.flv_url = flv_url
        self.headers = headers
        self.page_num = page_num
        self.is_will_convert = is_will_convert
        self.savedir = save_dir
        self.no_delete_original_video = no_delete_original_video
        self.quality = quality
        self.videoNameLabel = videoNameLabel
        self.is_will_delete_exists_file = is_will_delete_exists_file
        self.videoFormatType = videoFormatType

    def run(self):  # 重写run  比较耗时的后台任务可以在这里运行
        # 尝试下载, 如果失败发送下载完成信号(但参数为 None, 会使函数产生下载失败提示框) 并终止线程
        try:
            gettedFile = os.path.abspath(get_flv(
                self.vname, self.bv, self.flv_url, self.headers, self.page_num))  # 下载 FLV 文件
        except:
            self.downloadOKSignal.emit(None)
            return

        if (self.videoFormatType == 'flv') or (not self.is_will_delete_exists_file):  # 如果目标格式是 FLV
            self.downloadOKSignal.emit(gettedFile)  # 发送完成信号
            return

        outputfile = gettedFile.replace(
            '.flv', '.' + self.videoFormatType)  # 准备 转换 的 目标文件名

        # region 如果用户下载的是 360P 流畅 的视频文件 (格式已经为 MP4, 无需转换) 或者 用户请求不转 MP4, 发送下载完成信号, 终止线程
        if not self.is_will_convert:
            if self.quality == 16:  # 如果下载的是 360P 的视频文件
                # 获取的视频文件默认为 MP4 格式, 但保存的文件格式为 FLV, 要进行重命名
                os.rename(gettedFile, outputfile)
                self.downloadOKSignal.emit(gettedFile)  # 发送完成信号
                return
        # endregion

        # region 如果 ffmpeg.exe 不存在, 发送"FFMPEG未找到"信号, 终止线程
        if not os.path.isfile('ffmpeg.exe'):
            self.ffmpegNotFoundSignal.emit(gettedFile)
            return
        # endregion

        # region 检查是否要求删除已存在文件
        if self.is_will_delete_exists_file and os.path.exists(outputfile):
            os.remove(outputfile)
        # endregion

        self.formattingSignal.emit(gettedFile)  # 下载 FLV 完成, 发送转换信号

        # region 开始转 MP4
        def get_seconds(time):
            h = int(time[0:2])
            m = int(time[3:5])
            s = int(time[6:8])
            ms = int(time[9:12])
            ts = (h * 60 * 60) + (m * 60) + s + (ms / 1000)
            return ts

        process = subprocess.Popen('ffmpeg.exe -i "{inputfile}" "{outputfile}"'.format(
            inputfile=gettedFile, outputfile=outputfile), stderr=subprocess.PIPE, bufsize=0, universal_newlines=True, shell=True, encoding="utf-8")

        duration = None
        while process.poll() is None:
            line = process.stderr.readline().strip()
            if line:
                duration_res = re.search(r'Duration: (?P<duration>\S+)', line)
                if duration_res is not None:
                    duration = duration_res.groupdict()['duration']
                    duration = re.sub(r',', '', duration)

                result = re.search(r'time=(?P<time>\S+)', line)
                if result is not None and duration is not None:
                    elapsed_time = result.groupdict()['time']

                    currentTime = get_seconds(elapsed_time)
                    allTime = get_seconds(duration)

                    progress = currentTime * 100/allTime
                    self.videoNameLabel.setText(
                        'FLV 获取成功, 正在转 ' + self.videoFormatType.upper() + ' , 请耐心等待 ... ' + str(int(progress)) + '%')
        # endregion

        if not self.no_delete_original_video:  # 如果用户没有选择保留原始视频文件
            os.remove(gettedFile)  # 删除不再需要的 FLV 文件

        self.downloadOKSignal.emit(outputfile)  # 转 MP4 完成, 发送信号



class DownloaderUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        # region 保存位置初始化
        self.savedir = os.path.abspath('./Downloads')
        if not os.path.exists(self.savedir):
            os.mkdir(self.savedir)
        # endregion

        # region 其他初始化
        self.currentBV = None  # 初始化 "当前 BV" 属性
        self.w = QMainWindow()  # 创建主窗口
        self.setupUi(self.w)  # 初始化窗口组件
        self.w.setWindowFlags(Qt.WindowMinimizeButtonHint |
                              Qt.MSWindowsFixedSizeDialogHint | Qt.WindowCloseButtonHint)  # 设置窗口属性
        # endregion

        # region 信号绑定
        self.lineEdit.editingFinished.connect(self.__changename)
        self.download.clicked.connect(self.__download)
        self.saveAtButton.clicked.connect(self.__asksaveat)
        # endregion

    @pyqtSlot(int)
    def __changename(self):
        if self.lineEdit.text() == "":
            return
        try:
            self.currentBV = bvre(self.lineEdit.text())
        except:
            QMessageBox.critical(self, '错误', '无效的 BV 号, 请检查您的输入!')
            return
        else:
            try:
                self.videoName.setText(
                    '视频名称: ' + name(self.currentBV, headers))
            except:
                QMessageBox.critical(self, '错误', '无法获取视频名称, 请检查您的网络环境!')
                return

    @pyqtSlot(int)
    def __download(self):
        # 禁用一些控件
        self.__controlWidgets(False)

        videoFormat = self.videoFormatType.currentText().lower() # 视频格式

        # region 是否在 360P 下使用 FLV 格式
        if self.quality.currentText() == '360P' and videoFormat == 'flv':
            QMessageBox.critical(self, '错误!', '360P 清晰度的视频不支持 FLV 格式!')
            self.__controlWidgets(True)
            return
        # endregion

        # region 获取一些数据 (CID)
        page_num = int(self.videoPage.text())  # 页码
        try:
            cid = get_cid(self.currentBV, page_num)
        except CIDNotFoundException:  # CID 不存在
            QMessageBox.critical(
                self, '错误!', '您要下载的视频并没有第 ' + self.videoPage.text() + ' 页。')
            self.__controlWidgets(True)
        except:  # 其他网络错误
            QMessageBox.critical(self, '错误!', '获取视频 CID 失败, 请检查您的网络是否正常!')
            self.__controlWidgets(True)
            return
        # endregion

        vname = name(self.currentBV, headers)

        # region 获取 清晰度
        int_quality = qualityid(self.quality.currentText())
        text = play_url(cid, self.currentBV, headers, str(int_quality))
        accept_quality = text['data']['accept_quality']
        # endregion

        # region 检查 目标视频 是否支持选定的清晰度
        if not int_quality in accept_quality:  # 如果没有找到
            for x in text['data']['support_formats']:
                if max(accept_quality) == x['quality']:
                    max_quality = x['new_description']
            QMessageBox.critical(
                self, '下载失败!', '您要下载的视频不支持选择的清晰度!\n此视频支持的最佳画质: ' + max_quality)
            self.__controlWidgets(True)
            return
        # endregion

        # region 检查用户下载的视频的清晰度是否为 360P, 或者用户选择的视频格式不是 MP4, 如果是, 则在开始下载时为下载线程传入不转换 的参数。
        is_will_convert = True
        if int_quality == 16 or videoFormat == 'flv':
            is_will_convert = False
        # endregion

        # region 如果用户希望转视频格式为 其他 则检查文件是否已存在
        is_will_delete_exists_file = False
        testname = os.path.join(
            self.savedir, vname + ' - PAGE ' + self.videoPage.text() + '.' + videoFormat)
        if os.path.exists(testname):
            if QMessageBox.question(self, '提示!', testname + ' 已经存在! 是否覆盖?\n若不覆盖, 则只会下载原始视频文件。') == QMessageBox.Yes:
                is_will_delete_exists_file = True
        # endregion

        self.videoName.setText('正在下载...')  # 设置 下载提示文本

        # 准备 QThread
        self.DownloadQThread = DownloadThread(vname, self.currentBV, text['data']['durl'][0]['url'], headers,
                                              page_num, is_will_convert, self.savedir, self.saveOriginalVideo.isChecked(), int_quality, self.videoName, is_will_delete_exists_file, self.videoFormatType.currentText().lower())
        # region 下载线程的信号连接
        self.DownloadQThread.formattingSignal.connect(
            lambda: self.videoName.setText('FLV 获取成功, 正在转 ' + videoFormat.upper() + ' , 请耐心等待 ...'))
        self.DownloadQThread.ffmpegNotFoundSignal.connect(
            self.__ffmpegNotFound)
        self.DownloadQThread.downloadOKSignal.connect(
            self.__DownloadOK)  # 把任务完成的信号与任务完成后处理的槽函数绑定
        # endregion

        self.DownloadQThread.start()  # 开始下载

    def __controlWidgets(self, arg_bool: bool):
        self.lineEdit.setEnabled(arg_bool)
        self.download.setEnabled(arg_bool)
        self.saveAtButton.setEnabled(arg_bool)
        self.videoPage.setEnabled(arg_bool)
        self.quality.setEnabled(arg_bool)
        self.videoFormatType.setEnabled(arg_bool)
        self.saveOriginalVideo.setEnabled(arg_bool)

    def __ResetInputData(self):
        self.videoName.setText('输入完 BV 号后, 在输入框里按下回车即可在这里看到视频名称!')
        self.lineEdit.clear()
        self.__controlWidgets(True)

    def __DownloadOK(self, return_value):
        if os.path.isfile(return_value):
            QMessageBox.information(
                self, '下载完成!', '保存到: ' + return_value)
        else:
            QMessageBox.critical(self, '下载失败!', '下载失败! 请再试一次!')
        self.__ResetInputData()

    def __ffmpegNotFound(self, filename):
        QMessageBox.critical(
            self, '转 MP4 失败!', 'ffmpeg.exe 没有找到! 无法转 MP4 ...\n已下载的原始 FLV 文件: ' + filename)
        self.__ResetInputData()

    def __asksaveat(self):
        self.savedir = QFileDialog.getExistingDirectory(
            self, "请选择文件夹路径", os.getcwd())

    def show(self):
        self.w.show()


if __name__ == "__main__":
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "bilidownloader")
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    ui = DownloaderUI()
    ui.show()
    return_code = app.exec_()
    # os.system('taskkill /f /im ffmpeg.exe')
    sys.exit(return_code)
