import subprocess
import sys
import os
import threading

from ui import *
from functions import *
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

headers = {
    'Referer': 'https://www.bilibili.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}


def run(coroutine):
    try:
        coroutine.send(None)
    except StopIteration as e:
        return e.value


def qualityid(t):
    if t == '1080P':
        return 80
    elif t == '720P':
        return 64
    elif t == '480P':
        return 32
    elif t == '360P':
        return 16


class EmationThread(QThread):  # 继承QThread
    resSignal = pyqtSignal(str)  # 注册一个信号
    formattingSignal = pyqtSignal(str)
    ffmpegNotFoundSignal = pyqtSignal(str)
    def __init__(self, vname, bv, flv_url, headers, page_num):  # 从前端界面中传递参数到这个任务后台
        super().__init__()
        self.vname = vname
        self.bv = bv
        self.flv_url = flv_url
        self.headers = headers
        self.page_num = page_num

    def run(self):  # 重写run  比较耗时的后台任务可以在这里运行
        self.Resematin = get_flv(
            self.vname, self.bv, self.flv_url, self.headers, self.page_num)
        if os.path.isfile(self.Resematin):
            self.formattingSignal.emit(self.Resematin)  # 下载 FLV 完成, 发送开始转码信号
        else:
            self.resSignal.emit(self.Resematin) # FLV 下载失败, 终止下载线程
            return
        if not os.path.isfile('ffmpeg.exe'): # 如果 ffmpeg.exe 不存在, 发送"FFMPEG未找到"信号, 终止线程
            self.ffmpegNotFoundSignal.emit(self.Resematin)
            return
        outputfile = self.Resematin.replace('flv', 'mp4') # 准备转码
        class t(threading.Thread):
            def __init__(self, inputfile, outputfile):
                threading.Thread.__init__(self)
                self.inputfile = inputfile
                self.outputfile = outputfile
            def run(self):
                sp = subprocess.Popen('ffmpeg.exe -i "{inputfile}" "{outputfile}"'.format(inputfile=self.inputfile, outputfile=self.outputfile), shell=True)
                sp.wait() # 等待转MP4完成
        th = t(self.Resematin, self.Resematin.replace('flv', 'mp4'))
        th.start()
        th.join()
        os.remove(self.Resematin)
        self.resSignal.emit(outputfile) # 转码完成, 发送转码


class DLUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.savedir = os.getcwd() # 保存位置初始化
        self.w = QMainWindow() # 创建主窗口
        self.setupUi(self.w) # 初始化窗口组件
        self.w.setWindowFlags(Qt.WindowMinimizeButtonHint |
                              Qt.MSWindowsFixedSizeDialogHint | Qt.WindowCloseButtonHint) # 设置窗口属性
        # 信号绑定
        self.lineEdit.editingFinished.connect(self.changename)
        self.download.clicked.connect(self.dl)
        self.saveat.clicked.connect(self.asksaveat)

    @pyqtSlot(int)
    def changename(self):
        try:
            self.videoname.setText(
                '视频名称: ' + name(bvre(self.lineEdit.text()), headers))
        except Exception as e:
            self.videoname.setText('视频名称: 无')

    @pyqtSlot(int)
    def dl(self):
        try:
            bv = bvre(self.lineEdit.text()) # 获取 BV 号
        except:
            QMessageBox.critical(self, '下载失败!', '无效的 BV 号! 请检查您的输入...')
            return
        self.videoname.setText('正在下载...') # 设置 下载文本 , 正式开始下载
        # 获取一些数据
        try:
            cid_get = page(bv)
        except Exception as e:
            print(e)
            self.videoname.setText('视频名称: 无')
            QMessageBox.critical(self, '下载失败!', '获取视频 CID 失败, 请检查您的网络是否正常!')
            return
        cid = cid_get[0]
        page_num = cid_get[1]
        vname = name(bv, headers)
        # 获取 清晰度
        quality = str(qualityid(self.quality.currentText()))
        text = flv(cid, bv, headers, quality)
        qn = text['data']['support_formats']
        foundquality = False
        highquality = None
        # 检查 目标视频 是否支持选定的清晰度
        for qu in qn:
            if highquality == None:
                highquality = str(qu['quality'])
            if str(qu['quality']) == quality:
                foundquality = True
                break
        if foundquality == False: # 如果没有找到
            QMessageBox.critical(
                self, '下载失败!', '下载失败! 您要下载的视频不支持选择的清晰度!\n此视频支持的最佳画质: ' + str(highquality))
            return
        # 获取 下载 URL
        flv_url = text['data']['durl'][0]['url']
        # QThread下载, 等待信号
        ThreadEmation = EmationThread(
            vname, bv, flv_url, headers, page_num)
        ThreadEmation.formattingSignal.connect(
            lambda: self.videoname.setText('FLV 获取成功, 正在转 MP4, 耗时较长, 请耐心等待 ...'))
        ThreadEmation.ffmpegNotFoundSignal.connect(self.ffmpegNotFound)
        ThreadEmation.resSignal.connect(
            self.DownloadOK)  # 把任务完成的信号与任务完成后处理的槽函数绑定
        ThreadEmation.start() # 开始下载

    def DownloadOK(self, return_value):
        if os.path.isfile(return_value):
            QMessageBox.information(self, '下载完成!', '下载成功! 保存到: ' + return_value)
        else:
            QMessageBox.critical(self, '下载失败!', '下载失败! 错误原因: ' + return_value)
        self.videoname.setText('视频名称: 无')
        self.lineEdit.clear()

    def ffmpegNotFound(self, filename):
        QMessageBox.critical(None, '转 MP4 失败!', 'ffmpeg.exe 没有找到! 无法转 MP4 ...\n已下载的原始 FLV 文件: ' + filename)
        self.videoname.setText('视频名称: 无')
        self.lineEdit.clear()

    @pyqtSlot(int)
    def asksaveat(self):
        self.savedir = QFileDialog.getExistingDirectory(
            self, "请选择文件夹路径", os.getcwd())

    def show(self):
        self.w.show()


if __name__ == "__main__":
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "wbilidownloader")
    app = QApplication(sys.argv)
    ui = DLUI()
    ui.show()
    sys.exit(app.exec_())
