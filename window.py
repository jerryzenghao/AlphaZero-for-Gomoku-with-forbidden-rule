from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QPainter, QPen, QColor, QPalette, QBrush, QPixmap, QRadialGradient
from PyQt5.QtCore import Qt, QPoint, QTimer
import traceback
from gomoku import GomokuBoard
from corner_widget import CornerWidget


def run_with_exc(f):
    """游戏运行出现错误时，用messagebox把错误信息显示出来"""

    def call(window, *args, **kwargs):
        try:
            return f(window, *args, **kwargs)
        except Exception:
            exc_info = traceback.format_exc()
            QMessageBox.about(window, '错误信息', exc_info)
    return call


class GomokuWindow(QMainWindow):

    def __init__(self,size, player1='human_player', player2 = 'human_player', mode = 2, temp = 0.01):
        super().__init__()
        self.g = GomokuBoard((size[0],size[1]))  # 初始化游戏内容
        self.H = size[0]
        self.W = size[1]
        self.init_ui()  # 初始化游戏界面
        self.last_pos = (-1, -1)
        self.res = 0  # 记录那边获得了胜利
        self.operate_status = 0  # 游戏操作状态。0为游戏中（可操作），1为游戏结束闪烁过程中（不可操作
        self.player1 = player1
        self.player2 = player2
        self.temp = temp
        self.mode = mode

    def init_ui(self):
#         """初始化游戏界面"""
#         # 1. 确定游戏界面的标题，大小和背景颜色
        self.setObjectName('MainWindow')
        self.setWindowTitle('五子棋')
        self.setFixedSize(50+self.H*40, 50+self.W*40)
#        self.setStyleSheet('#MainWindow{background-color: green}')
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap('imgs/muzm.jpg')))
        self.setPalette(palette)
        # 2. 开启鼠标位置的追踪。并在鼠标位置移动时，使用特殊符号标记当前的位置
        self.setMouseTracking(True)
        # 3. 鼠标位置移动时，对鼠标位置的特殊标记
        self.corner_widget = CornerWidget(self)
        self.corner_widget.repaint()
        self.corner_widget.hide()
        self.show()

    @run_with_exc
    def paintEvent(self, e):
#         """绘制游戏内容"""

        def draw_map():
#             """绘制棋盘"""
            qp.setPen(QPen(QColor(0, 0, 0), 2, Qt.SolidLine))  # 棋盘的颜色为黑色
#             # 绘制横线
            for x in range(self.H):
                qp.drawLine(40 * (x + 1), 40, 40 * (x + 1), self.H*40)
#             # 绘制竖线
            for y in range(self.W):
                qp.drawLine(40, 40 * (y + 1), self.W*40, 40 * (y + 1))
#             # 绘制棋盘中的黑点
#             qp.setBrush(QColor(0, 0, 0))
#             key_points = [(4, 4), (12, 4), (4, 12), (12, 12), (8, 8)]
#             for t in key_points:
#                 qp.drawEllipse(QPoint(40 * t[0], 40 * t[1]), 5, 5)

        def draw_pieces():
#             """绘制棋子"""
#             # 绘制黑棋子
            qp.setPen(QPen(QColor(0, 0, 0), 1, Qt.SolidLine))
            #qp.setBrush(QColor(0, 0, 0))
            for x in range(self.H):
                for y in range(self.W):
                    if self.g.chessboard[x,y] == 1:
#                        if self.flash_cnt % 2 == 1 and (x, y) in self.flash_pieces:
#                             continue
                        radial = QRadialGradient(40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35)  # 棋子的渐变效果
                        radial.setColorAt(0, QColor(96, 96, 96))
                        radial.setColorAt(1, QColor(0, 0, 0))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(40 * (x + 1), 40 * (y + 1)), 15, 15)
#             # 绘制白棋子
            qp.setPen(QPen(QColor(160, 160, 160), 1, Qt.SolidLine))
            #qp.setBrush(QColor(255, 255, 255))
            for x in range(self.H):
                for y in range(self.W):
                    if self.g.chessboard[x,y] == 2:
#                         if self.flash_cnt % 2 == 1 and (x, y) in self.flash_pieces:
#                             continue
                        radial = QRadialGradient(40 * (x + 1), 40 * (y + 1), 15, 40 * x + 35, 40 * y + 35)  # 棋子的渐变效果
                        radial.setColorAt(0, QColor(255, 255, 255))
                        radial.setColorAt(1, QColor(160, 160, 160))
                        qp.setBrush(QBrush(radial))
                        qp.drawEllipse(QPoint(40 * (x + 1), 40 * (y + 1)), 15, 15)

        if hasattr(self, 'g'):  # 游戏还没开始的话，就不用画了
            qp = QPainter()
            qp.begin(self)
            draw_map()  # 绘制棋盘
            draw_pieces()  # 绘制棋子
            qp.end()
            
    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Space and self.mode == 2:
            turn = self.player1
            while self.mode == 2:
                move = turn.get_action(self.g,self.temp)
                self.g.do_move(move)
                result= self.g.get_result()

                if result == 0:
                    turn = self.player2 if turn == self.player1 else self.player1
                    self.repaint(0, 0, self.H*40+50, self.W*40+50)
                else:
                    self.repaint(0, 0, self.H*40+50, self.W*40+50)
                    self.game_restart(result)
                    break
    @run_with_exc
    def mouseMoveEvent(self, e):
        if self.mode == 2:
            return
        # 1. 首先判断鼠标位置对应棋盘中的哪一个格子
        mouse_x = e.windowPos().x()
        mouse_y = e.windowPos().y()
        if 25 <= mouse_x <= 615 and 25 <= mouse_y <= 615 and (mouse_x % 40 <= 15 or mouse_x % 40 >= 25) and (mouse_y % 40 <= 15 or mouse_y % 40 >= 25):
            game_x = int((mouse_x + 15) // 40) - 1
            game_y = int((mouse_y + 15) // 40) - 1
        else:  # 鼠标当前的位置不对应任何一个游戏格子，将其标记为(01, 01
            game_x = -1
            game_y = -1

        # 2. 然后判断鼠标位置较前一时刻是否发生了变化
        pos_change = False  # 标记鼠标位置是否发生了变化
        if game_x != self.last_pos[0] or game_y != self.last_pos[1]:
            pos_change = True
        self.last_pos = (game_x, game_y)
        # 3. 最后根据鼠标位置的变化，绘制特殊标记
        if pos_change and game_x != -1:
            self.setCursor(Qt.PointingHandCursor)
        if pos_change and game_x == -1:
            self.setCursor(Qt.ArrowCursor)
        if pos_change and game_x != -1:
            self.corner_widget.move(25 + game_x * 40, 25 + game_y * 40)
            self.corner_widget.show()
        if pos_change and game_x == -1:
            self.corner_widget.hide()

    @run_with_exc
    def mousePressEvent(self, e):
        if self.mode == 2:
            return
        if not (hasattr(self, 'operate_status') and self.operate_status == 0):
            return
        if e.button() == Qt.LeftButton:
        # 1. 首先判断按下了哪个格子
            mouse_x = e.windowPos().x()
            mouse_y = e.windowPos().y()
            if (mouse_x % 40 <= 10 or mouse_x % 40 >= 30) and (mouse_y % 40 <= 10 or mouse_y % 40 >= 30):
                game_x = int((mouse_x + self.H) // 40) - 1
                game_y = int((mouse_y + self.W) // 40) - 1
            else:  # 鼠标点击的位置不正确
                return
            self.g.do_move((game_x, game_y))
            #self.show()
            # 2. 根据操作结果进行一轮游戏循环
            res = self.g.get_result()  # 判断游戏结果
            if res != 0:  # 如果游戏结果为“已经结束”，则显示游戏内容，并退出主循环
                self.repaint(0, 0, self.H*40+50, self.W*40+50)
                self.game_restart(res)
                return
            self.repaint(0, 0, self.H*40+50, self.W*40+50)  # 在游戏还没有结束的情况下，显示游戏内容，并继续下一轮循环

            if self.mode == 1:
                move = self.player2.get_action(self.g, self.temp)
                self.g.do_move(move)
                res = self.g.get_result()  # 判断游戏结果
                if res != 0:  # 如果游戏结果为“已经结束”，则显示游戏内容，并退出主循环
                    self.repaint(0, 0, self.H*40+50, self.W*40+50)
                    self.game_restart(res)
                    return
                self.repaint(0,0, self.H*40+50, self.W*40+50)

    def game_restart(self, res):
        """游戏出现开始"""
        self.res = res  # 标记谁获胜了
        # 1. 显示游戏结束的信息
        if self.res == 1:
            #QMessageBox.about(self, '游戏结束', 'Player1获胜!')
            inform = QMessageBox.information(self,'游戏结束','黑棋获胜',QMessageBox.Yes, QMessageBox.Yes)
        elif self.res == 2:
            #QMessageBox.about(self, '游戏结束', 'Player2获胜!')
            inform = QMessageBox.information(self,'游戏结束','白棋获胜',QMessageBox.Yes, QMessageBox.Yes)
        elif self.res == 3:
            #QMessageBox.about(self, '游戏结束', '平局!')
            inform = QMessageBox.information(self,'游戏结束','平局!',QMessageBox.Yes, QMessageBox.Yes)
        else:
            raise ValueError('当前游戏结束的标志位为' + self.res + '. 而游戏结束的标志位必须为1, 2 或 3')
            # 2. 游戏重新开始的操作
        self.res = 0
        self.operate_status = 0
        self.g = GomokuBoard((self.H, self.W))  # 重新初始化游戏内容
        self.repaint(0, 0, self.H*40+50, self.W*40+50)  # 重新绘制游戏界面
