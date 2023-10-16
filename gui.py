from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSlider, QLabel, QVBoxLayout
from config import AVOID_FACTOR, CENTERING_FACTOR, MATCHING_FACTOR, SCREEN_HEIGHT,SCREEN_WIDTH, MAX_SPEED,MIN_SPEED
from boidswidget import BoidsWidget


class BoidsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Boids Simulation")
        self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout()

        # Create sliders and labels
        slider_layout = QHBoxLayout()

        self.avoid_slider, avoid_label = self.create_sliderSeparation("Avoid Factor", AVOID_FACTOR)
        self.centering_slider, centering_label = self.create_sliderCentering("Centering Factor", CENTERING_FACTOR)
        self.matching_slider, matching_label = self.create_sliderMatching("Matching Factor", MATCHING_FACTOR)
        self.max_speed_slider, max_speed_label = self.create_sliderMaxSpeed("Max Speed", MAX_SPEED)
        self.min_speed_slider,min_speed_slider = self.create_sliderMaxSpeed("Min Speed", MIN_SPEED)
        slider_layout.addWidget(self.max_speed_slider)
        slider_layout.addWidget(max_speed_label)
        slider_layout.addWidget(self.min_speed_slider)
        slider_layout.addWidget(min_speed_slider)
        slider_layout.addWidget(avoid_label)
        slider_layout.addWidget(self.avoid_slider)
        slider_layout.addWidget(centering_label)
        slider_layout.addWidget(self.centering_slider)
        slider_layout.addWidget(matching_label)
        slider_layout.addWidget(self.matching_slider)

        layout.addLayout(slider_layout)

        # Create a container widget for the BoidsWidget
        boids_container = QWidget()
        boids_layout = QVBoxLayout()
        self.boids_widget = BoidsWidget()
        boids_layout.addWidget(self.boids_widget)
        boids_container.setLayout(boids_layout)

        # Add the layouts to the central widget
        layout.addWidget(boids_container)
        central_widget.setLayout(layout)

    def create_sliderMaxSpeed(self,label_text,initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(5,20)
        slider.setValue(int(initial_value))
        slider.valueChanged.connect(self.slider_value_changed)
        
        label = QLabel(label_text)
        
        return slider,label


    def create_sliderMinSpeed(self,label_text,initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0,4)
        slider.setValue(int(initial_value))
        slider.valueChanged.connect(self.slider_value_changed)
        
        label = QLabel(label_text)
        
        return slider,label

    def create_sliderSeparation(self, label_text, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 100)
        slider.setValue(int(initial_value * 100))
        slider.valueChanged.connect(self.slider_value_changed)

        label = QLabel(label_text)

        return slider, label
    def create_sliderCentering(self, label_text, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 100)
        slider.setValue(int(initial_value * 10000))
        slider.valueChanged.connect(self.slider_value_changed)

        label = QLabel(label_text)

        return slider, label
    def create_sliderMatching(self, label_text, initial_value):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(1, 100)
        slider.setValue(int(initial_value * 100))
        slider.valueChanged.connect(self.slider_value_changed)

        label = QLabel(label_text)

        return slider, label
    def slider_value_changed(self):
        # Update the variables based on the slider values
        global AVOID_FACTOR
        global CENTERING_FACTOR
        global MATCHING_FACTOR
        AVOID_FACTOR = self.avoid_slider.value() / 100.0
        CENTERING_FACTOR = self.centering_slider.value() / 10000.0
        MATCHING_FACTOR = self.matching_slider.value() / 100.0
    
    def speed_slider_value_changed(self):
        global MAX_SPEED
        global MIN_SPEED
        MAX_SPEED = self.max_speed_slider.value()
        MIN_SPEED = self.min_speed_slider.value()