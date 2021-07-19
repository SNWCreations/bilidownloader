import sys

from ui import *
from functions import *
from PyQt5.QtCore import pyqtSlot

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

class DLUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.savedir = '.'
        self.w = QMainWindow()
        self.setupUi(self.w)
        self.w.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowCloseButtonHint)
        self.lineEdit.editingFinished.connect(self.changename)
        self.download.clicked.connect(self.dl)
        self.saveat.clicked.connect(self.asksaveat)
    @pyqtSlot(int)
    def changename(self):
        try:
            self.videoname.setText('视频名称: ' + name(bvre(self.lineEdit.text()), headers))
        except Exception as e:
            self.videoname.setText('视频名称: 无')
    @pyqtSlot(int)
    def dl(self):
        # 获取 CID
        default = self.videoname.text()
        try:
            bv = bvre(self.lineEdit.text())
        except:
            QMessageBox.critical(self, '下载失败!', '无效的 BV 号! 请检查您的输入...')
            self.videoname.setText(default)
            return
        self.videoname.setText('正在下载...')
        cid_get = page(bv)
        cid = cid_get[0]
        page_num = cid_get[1]
        vname = name(bv, headers)
        # 获取 清晰度
        quality = str(qualityid(self.quality.currentText()))
        text = flv(cid, bv, headers, quality)
        qn = text['data']['support_formats']
        foundquality = False
        highquality = None
        for qu in qn:
            if highquality == None:
                highquality = str(qu['quality'])
            if str(qu['quality']) == quality:
                foundquality = True
                break
        if foundquality == False:
            QMessageBox.critical(self, '下载失败!', '下载失败!您要下载的视频不支持选择的清晰度!\n此视频支持的最佳画质: ' + str(highquality))
            return
        # 获取 下载 URL
        flv_url = text['data']['durl'][0]['url']
        # 开线程下载, 等待
        gflv = get_flv(vname, bv, flv_url, headers, page_num)
        try:
            gflv.send(None)
        except StopIteration as e:
            ret = os.path.abspath(e.value)
        if os.path.isfile(ret):
            QMessageBox.information(self, '下载完成!', '下载成功! 保存到: ' + ret)
        else:
            QMessageBox.critical(self, '下载失败!', '下载失败!\n错误原因: ' + ret)
        self.videoname.setText('视频名称: 无')
        self.lineEdit.clear()
    @pyqtSlot(int)
    def asksaveat(self):
        self.savedir = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", os.getcwd())
    def show(self):
        self.w.show()

if __name__ == "__main__":
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("wbilidownloader")
    app = QApplication(sys.argv)
    ui = DLUI()
    ui.show()
    sys.exit(app.exec_())