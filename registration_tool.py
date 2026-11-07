import sys
import open3d as o3d
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QLabel
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.gt = None
        self.pred = None

        self.setWindowTitle(
            "Point Cloud Registration Tool"
        )

        self.resize(
            1000,
            700
        )

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        layout = QVBoxLayout()

        central_widget.setLayout(
            layout
        )

        self.load_gt_button = QPushButton(
            "Load GT"
        )

        self.load_gt_button.clicked.connect(
            self.load_gt
        )

        self.load_pred_button = QPushButton(
            "Load Pred"
        )
        self.view_gt_button = QPushButton(
            "View GT"
        )

        self.view_pred_button = QPushButton(
            "View Pred"
        )

        self.load_pred_button.clicked.connect(
            self.load_pred
        )

        self.view_gt_button.clicked.connect(
            self.view_gt
        )

        self.view_pred_button.clicked.connect(
            self.view_pred
        )

        layout.addWidget(
            self.load_gt_button
        )

        layout.addWidget(
            self.load_pred_button
        )

        layout.addWidget(
            self.view_gt_button
        )

        layout.addWidget(
            self.view_pred_button
        )
        
        self.gt_label = QLabel(
            "GT : Not Loaded"
        )

        self.pred_label = QLabel(
            "Pred : Not Loaded"
        )

        layout.addWidget(
            self.gt_label
        )

        layout.addWidget(
            self.pred_label
        )

    def load_gt(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select GT Point Cloud",
            "",
            "Point Clouds (*.ply)"
        )

        if file_path:

            self.gt = o3d.io.read_point_cloud(
                file_path
            )

            print()
            print("GT loaded!")

            print(
                f"Points: {len(self.gt.points):,}"
            )
            self.gt_label.setText(
                f"GT : {Path(file_path).name}"
            )

    def load_pred(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Pred Point Cloud",
            "",
            "Point Clouds (*.ply)"
        )

        if file_path:

            self.pred = o3d.io.read_point_cloud(
                file_path
            )

            print()
            print("Pred loaded!")

            print(
                f"Points: {len(self.pred.points):,}"
            )

            self.pred_label.setText(
                f"Pred : {Path(file_path).name}"
            )

    def view_gt(self):

        if self.gt is None:

            print("GT not loaded!")

            return

        o3d.visualization.draw_geometries(
            [self.gt]
        )


    def view_pred(self):

        if self.pred is None:

            print("Pred not loaded!")

            return

        o3d.visualization.draw_geometries(
            [self.pred]
        )

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    app.exec()