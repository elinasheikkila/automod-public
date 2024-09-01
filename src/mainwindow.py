import json

import numpy as np

from PySide6.QtCore import Qt, Slot, QSize
from PySide6.QtGui import QAction, QBrush, QIcon, QTransform, QPixmap
from PySide6.QtWidgets import (QMainWindow, QToolBar, QErrorMessage, QDockWidget, QStatusBar, QDoubleSpinBox,
                               QGraphicsView, QPushButton, QSpinBox, QFileDialog, QMenuBar, QMenu, QWidget, QGridLayout,
                               QLabel, QTabWidget)

from curvescene import CurveScene
from curveview import CurveView
from csview import CSView
from nodepoint import NodePoint
from helixpoint import HelixPoint, ReferencePoint

import icons_rc


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parameters = {"ihg": 0.5, "hd": 2.0, "ntl": 0.34, "ml": 0.34, "tl": 10.5, "gs": 20, "tt": np.pi / 8,
                           "zs": 1, "ts": 1, "rs": 1}

        self.scene = CurveScene(8 * self.parameters['gs'], self.parameters['gs'], parent=self)
        self.scene.setBackgroundBrush(QBrush(Qt.GlobalColor.white))

        self.ehandler = QErrorMessage.qtHandler()

        self.view = CurveView(self.scene, parent=self)
        self.setCentralWidget(self.view)
        self.view.show()

        ''' CURVE VIEW TOOLS '''

        curve_view_tools = QToolBar(parent=self)
        curve_view_tools.setFloatable(False)
        curve_view_tools.setMovable(False)
        curve_view_tools.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        curve_view_tools.setIconSize(QSize(32, 32))
        self.addToolBar(curve_view_tools)

        x_translate = QAction("XMove", self)
        x_translate.setStatusTip("XMove tool: Choose for moving main view items in the x-direction")
        x_translate.toggled.connect(self.x_translate_action)
        x_translate.setCheckable(True)
        arrow_red_map = QPixmap(":/icons/arrow_red.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        x_translate.setIcon(QIcon(arrow_red_map))
        x_translate.setIconText("XMove")
        curve_view_tools.addAction(x_translate)
        self.x_translate = x_translate

        y_translate = QAction("YMove", self)
        y_translate.setStatusTip("YMove tool: Choose for moving main view items in the y-direction")
        y_translate.toggled.connect(self.y_translate_action)
        y_translate.setCheckable(True)
        arrow_green_map = QPixmap(":/icons/arrow_green.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        y_translate.setIcon(QIcon(arrow_green_map))
        y_translate.setIconText("YMove")
        curve_view_tools.addAction(y_translate)
        self.y_translate = y_translate

        z_translate = QAction("ZMove", self)
        z_translate.setStatusTip("ZMove tool: Choose for moving main view items in the z-direction")
        z_translate.toggled.connect(self.z_translate_action)
        z_translate.setCheckable(True)
        arrow_blue_map = QPixmap(":/icons/arrow_blue.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        z_translate.setIcon(QIcon(arrow_blue_map))
        z_translate.setIconText("ZMove")
        curve_view_tools.addAction(z_translate)
        self.z_translate = z_translate

        x_rotate = QAction("XRotate", self)
        x_rotate.setStatusTip("XRotate tool: Choose for rotating main view items around the x-axis")
        x_rotate.toggled.connect(self.x_rotate_action)
        x_rotate.setCheckable(True)
        rotate_red_map = QPixmap(":/icons/rotate_red.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        x_rotate.setIcon(QIcon(rotate_red_map))
        x_rotate.setIconText("XRotate")
        curve_view_tools.addAction(x_rotate)
        self.x_rotate = x_rotate

        y_rotate = QAction("YRotate", self)
        y_rotate.setStatusTip("YRotate tool: Choose for rotating main view items around the y-axis")
        y_rotate.toggled.connect(self.y_rotate_action)
        y_rotate.setCheckable(True)
        rotate_green_map = QPixmap(":/icons/rotate_green.png").scaled(QSize(256, 256),
                                                                    Qt.AspectRatioMode.IgnoreAspectRatio)
        y_rotate.setIcon(QIcon(rotate_green_map))
        y_rotate.setIconText("YRotate")
        curve_view_tools.addAction(y_rotate)
        self.y_rotate = y_rotate

        z_rotate = QAction("ZRotate", self)
        z_rotate.setStatusTip("ZRotate tool: Choose for rotating main view items around the z-axis")
        z_rotate.toggled.connect(self.z_rotate_action)
        z_rotate.setCheckable(True)
        rotate_blue_map = QPixmap(":/icons/rotate_blue.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        z_rotate.setIcon(QIcon(rotate_blue_map))
        z_rotate.setIconText("ZRotate")
        curve_view_tools.addAction(z_rotate)
        self.z_rotate = z_rotate

        zoom = QAction("Zoom", self)
        zoom.setStatusTip("Zoom tool: Choose for scaling the main view")
        zoom.toggled.connect(self.zoom_action)
        zoom.setCheckable(True)
        zoom_map = QPixmap(":/icons/zoom.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        zoom.setIcon(QIcon(zoom_map))
        zoom.setIconText("Zoom")
        curve_view_tools.addAction(zoom)
        self.zoom = zoom

        restore = QAction("Restore", self)
        restore.setStatusTip("Restore: Click to restore the main view")
        restore.toggled.connect(self.restore_action)
        restore.setCheckable(True)
        restore_map = QPixmap(":/icons/restore.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        restore.setIcon(QIcon(restore_map))
        restore.setIconText("Restore")
        curve_view_tools.addAction(restore)
        self.restore = restore

        curve_view_tools.addSeparator()

        ''' DRAWING TOOLS '''

        drawing_tools = QToolBar(parent=self)
        drawing_tools.setFloatable(False)
        drawing_tools.setMovable(False)
        drawing_tools.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        drawing_tools.setIconSize(QSize(32, 32))
        self.addToolBar(drawing_tools)

        add_points = QAction("Insert", self)
        add_points.setStatusTip("Insert points tool: Click within the main view to create a new point")
        add_points.toggled.connect(self.add_points_action)
        add_points.setCheckable(True)
        add_points_map = QPixmap(":/icons/insert_plus2.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        add_points.setIcon(QIcon(add_points_map))
        drawing_tools.addAction(add_points)
        self.add_points = add_points

        connect_points = QAction("Connect", self)
        connect_points.setStatusTip("Connect points tool: Click on two points to connect them")
        connect_points.toggled.connect(self.connect_points_action)
        connect_points.setCheckable(True)
        connect_points_map = QPixmap(":/icons/connect4.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        connect_points.setIcon(QIcon(connect_points_map))
        drawing_tools.addAction(connect_points)
        self.connect_points = connect_points

        interpolate = QAction("Interpolate", self)
        interpolate.setStatusTip("Interpolate tool: Calculate and display curves")
        interpolate.toggled.connect(self.interpolate_action)
        interpolate.setCheckable(True)
        interpolate_map = QPixmap(":/icons/interpolate34.png").scaled(QSize(256, 256),
                                                                    Qt.AspectRatioMode.IgnoreAspectRatio)
        interpolate.setIcon(QIcon(interpolate_map))
        drawing_tools.addAction(interpolate)
        self.interpolate = interpolate

        drawing_tools.addSeparator()

        ''' OUTPUT TOOLS '''

        output_tools = QToolBar(parent=self)
        output_tools.setFloatable(False)
        output_tools.setMovable(False)
        output_tools.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        output_tools.setIconSize(QSize(32, 32))
        self.addToolBar(output_tools)

        write_tool = QAction("Write", self)
        write_tool.setStatusTip("Write: Click to write modifications into an existing file")
        write_tool.toggled.connect(self.write_tool_action)
        write_tool_map = QPixmap(":/icons/json.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        write_tool.setIcon(QIcon(write_tool_map))
        write_tool.setCheckable(True)
        output_tools.addAction(write_tool)
        self.write_tool = write_tool

        ''' POINT TOOLS '''

        self.point_tools = QToolBar(parent=self)
        self.point_tools.setFloatable(False)
        self.point_tools.setMovable(False)
        self.point_tools.setVisible(False)
        self.point_tools.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.point_tools.setIconSize(QSize(32, 32))
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.point_tools)

        point_z_translate = QAction("PointZMove", self)
        point_z_translate.setStatusTip("PointZMove tool: Choose for moving the selected point in the z-direction")
        point_z_translate.toggled.connect(self.point_z_translate_action)
        point_z_translate.setCheckable(True)
        point_z_translate.setIcon(QIcon(arrow_blue_map))
        point_z_translate.setIconText("PointZMove")
        self.point_tools.addAction(point_z_translate)
        self.point_z_translate = point_z_translate

        point_z_value = QDoubleSpinBox()
        point_z_value.setMaximum(1000000)
        point_z_value.setMinimum(-1000000)
        point_z_value.setSingleStep(0.1)
        point_z_value.valueChanged.connect(self.point_z_spin_translate_action)
        self.point_tools.addWidget(point_z_value)
        self.point_z_value = point_z_value

        point_y_translate = QAction("PointYMove", self)
        point_y_translate.setStatusTip("PointYMove tool: Choose for moving the selected point in the y-direction")
        point_y_translate.toggled.connect(self.point_y_translate_action)
        point_y_translate.setCheckable(True)
        point_y_translate.setIcon(QIcon(arrow_green_map))
        point_y_translate.setIconText("PointYMove")
        self.point_tools.addAction(point_y_translate)
        self.point_y_translate = point_y_translate

        point_y_value = QDoubleSpinBox()
        point_y_value.setMaximum(1000000)
        point_y_value.setMinimum(-1000000)
        point_y_value.setSingleStep(0.1)
        point_y_value.valueChanged.connect(self.point_y_spin_translate_action)
        self.point_tools.addWidget(point_y_value)
        self.point_y_value = point_y_value

        point_x_translate = QAction("PointXMove", self)
        point_x_translate.setStatusTip("PointXMove tool: Choose for moving the selected point in the x-direction")
        point_x_translate.toggled.connect(self.point_x_translate_action)
        point_x_translate.setCheckable(True)
        point_x_translate.setIcon(QIcon(arrow_red_map))
        point_x_translate.setIconText("PointXMove")
        self.point_tools.addAction(point_x_translate)
        self.point_x_translate = point_x_translate

        point_x_value = QDoubleSpinBox()
        point_x_value.setMaximum(1000000)
        point_x_value.setMinimum(-1000000)
        point_x_value.setSingleStep(0.1)
        point_x_value.valueChanged.connect(self.point_x_spin_translate_action)
        self.point_tools.addWidget(point_x_value)
        self.point_x_value = point_x_value

        delete_point = QAction("Delete", self)
        delete_point.setStatusTip("Delete tool: Click to delete the selected point")
        delete_point.setCheckable(True)
        delete_point_map = QPixmap(":/icons/trash.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        delete_point.setIcon(QIcon(delete_point_map))
        delete_point.toggled.connect(self.delete_point_action)
        self.point_tools.addAction(delete_point)
        self.delete_point = delete_point

        ''' CONNECTION TOOLS '''

        self.connection_tools = QToolBar(parent=self)
        self.connection_tools.setFloatable(False)
        self.connection_tools.setMovable(False)
        self.connection_tools.setVisible(False)
        self.connection_tools.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.connection_tools.setIconSize(QSize(64, 32))
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self.connection_tools)

        self.disconnect_prev = QAction("Disconnect previous", self)
        self.disconnect_prev.setStatusTip("Disconnect previous tool: Click to break the connection "
                                          "between the selected point and its predecessor")
        self.disconnect_prev.toggled.connect(self.disconnect_prev_action)
        self.disconnect_prev.setCheckable(True)
        disconnect_prev_map = QPixmap(":/icons/disconnect_prev.png").scaled(QSize(512, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        self.disconnect_prev.setIcon(QIcon(disconnect_prev_map))
        self.disconnect_prev.setIconText("Disconnect previous")
        self.connection_tools.addAction(self.disconnect_prev)

        self.disconnect_next = QAction("Disconnect next", self)
        self.disconnect_next.setStatusTip("Disconnect next tool: "
                                          "Click to break the connection between the selected point and its successor")
        self.disconnect_next.toggled.connect(self.disconnect_next_action)
        self.disconnect_next.setCheckable(True)
        disconnect_next_map = QPixmap(":/icons/delete_connect2.png").scaled(QSize(512, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        self.disconnect_next.setIcon(QIcon(disconnect_next_map))
        self.disconnect_next.setIconText("Disconnect next")
        self.connection_tools.addAction(self.disconnect_next)

        ''' CROSS SECTION TOOL '''

        cs_tool = QDockWidget("Cross section tool")
        cs_tool.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        cs_tool.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.cs_scene = None
        self.cs_node = None
        self.cs_view = CSView(parent=self)
        self.cs_view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        cs_tool.setWidget(self.cs_view)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, cs_tool)
        self.cs_tool = cs_tool
        cs_tool.setVisible(False)

        self.cs_toolbar = QToolBar(parent=self)
        self.cs_toolbar.setFloatable(False)
        self.cs_toolbar.setMovable(False)
        self.cs_toolbar.setVisible(False)
        self.cs_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.cs_toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, self.cs_toolbar)

        draw_hc = QAction("HC", self)
        draw_hc.setStatusTip("HC: Click to draw a honeycomb lattice on the cross section plane")
        draw_hc.toggled.connect(self.draw_hc_action)
        draw_hc.setCheckable(True)
        hc_map = QPixmap(":/icons/honeycomb.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        draw_hc.setIcon(QIcon(hc_map))
        draw_hc.setIconText("Honeycomb")
        self.cs_toolbar.addAction(draw_hc)
        self.draw_hc = draw_hc

        draw_sq = QAction("SQ", self)
        draw_sq.setStatusTip("SQ: Click to draw a square lattice on the cross section plane")
        draw_sq.toggled.connect(self.draw_sq_action)
        draw_sq.setCheckable(True)
        sq_map = QPixmap(":/icons/square.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        draw_sq.setIcon(QIcon(sq_map))
        draw_sq.setIconText("Square")
        self.cs_toolbar.addAction(draw_sq)
        self.draw_sq = draw_sq

        zoom_cs = QAction("Zoom", self)
        zoom_cs.setStatusTip("Zoom: Choose for scaling the cross section plane view")
        zoom_cs.toggled.connect(self.zoom_cs_action)
        zoom_cs.setCheckable(True)
        zoom_cs.setIcon(QIcon(zoom_map))
        zoom_cs.setIconText("Zoom")
        self.cs_toolbar.addAction(zoom_cs)
        self.zoom_cs = zoom_cs

        translate_ref = QAction("PointMove", self)
        translate_ref.setStatusTip("PointMove: Choose for moving the reference point of the cross section plane")
        translate_ref.toggled.connect(self.translate_ref_action)
        translate_ref.setCheckable(True)
        arrow_white_map = QPixmap(":/icons/arrows_white.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        translate_ref.setIcon(QIcon(arrow_white_map))
        translate_ref.setIconText("PointMove")
        self.cs_toolbar.addAction(translate_ref)
        self.translate_ref = translate_ref

        ref_point_x_value = QDoubleSpinBox()
        ref_point_x_value.setPrefix("X: ")
        ref_point_x_value.setMaximum(1000000)
        ref_point_x_value.setMinimum(-1000000)
        ref_point_x_value.valueChanged.connect(self.ref_point_x_spin_translate_action)
        self.cs_toolbar.addWidget(ref_point_x_value)
        self.ref_point_x_value = ref_point_x_value

        ref_point_y_value = QDoubleSpinBox()
        ref_point_y_value.setPrefix("Y: ")
        ref_point_y_value.setMaximum(1000000)
        ref_point_y_value.setMinimum(-1000000)
        ref_point_y_value.valueChanged.connect(self.ref_point_y_spin_translate_action)
        self.cs_toolbar.addWidget(ref_point_y_value)
        self.ref_point_y_value = ref_point_y_value

        rotate_lattice = QAction("Rotate", self)
        rotate_lattice.setStatusTip("Rotate: Choose for rotating the cross section plane view")
        rotate_lattice.toggled.connect(self.rotate_lattice_action)
        rotate_lattice.setCheckable(True)
        rotate_map = QPixmap(":/icons/rotate_test2.png").scaled(QSize(256, 256), Qt.AspectRatioMode.IgnoreAspectRatio)
        rotate_lattice.setIcon(QIcon(rotate_map))
        rotate_lattice.setIconText("Rotate")
        self.cs_toolbar.addAction(rotate_lattice)
        self.rotate_lattice = rotate_lattice

        cs_angle = QDoubleSpinBox()
        cs_angle.setSuffix("°")
        cs_angle.setMaximum(1000000)
        cs_angle.setMinimum(-1000000)
        cs_angle.valueChanged.connect(self.spin_rotate_lattice_action)
        self.cs_toolbar.addWidget(cs_angle)
        self.cs_angle = cs_angle

        add_remove_helices = QAction("Add/Remove", self)
        add_remove_helices.setStatusTip("Add/Remove: Choose for editing the cross section")
        add_remove_helices.toggled.connect(self.add_remove_helices_action)
        add_remove_helices.setIcon(QIcon(add_points_map))
        add_remove_helices.setCheckable(True)
        self.cs_toolbar.addAction(add_remove_helices)
        self.add_remove_helices = add_remove_helices

        renumber = QAction("Renumber", self)
        renumber.setStatusTip("Renumber: Choose for manually setting helix numbers")
        renumber.toggled.connect(self.renumber_helices)
        renumber_map = QPixmap(":/icons/renum.png").scaled(QSize(256, 128), Qt.AspectRatioMode.IgnoreAspectRatio)
        renumber.setIcon(QIcon(renumber_map))
        renumber.setCheckable(True)
        self.cs_toolbar.addAction(renumber)
        self.renumber = renumber

        self.connected_helix = None
        renumber_box = QSpinBox()
        renumber_box.setMinimum(0)
        renumber_box.setMaximum(400)
        renumber_box.valueChanged.connect(self.spin_renumber_action)
        renumber_action = self.cs_toolbar.addWidget(renumber_box)
        self.renumber_box = renumber_box
        self.renumber_action = renumber_action
        self.renumber_action.setVisible(False)

        self.stored_cs = None
        cs_copy = QPushButton("Copy")
        cs_copy.clicked.connect(self.copy_cs_action)
        self.cs_toolbar.addWidget(cs_copy)

        cs_paste = QPushButton("Paste")
        cs_paste.clicked.connect(self.paste_cs_action)
        self.cs_toolbar.addWidget(cs_paste)

        menu_bar = QMenuBar(None)
        main_menu = QMenu("AutoMod")
        user_settings = QAction("User Settings", self)
        user_settings.triggered.connect(self.set_settings_action)
        main_menu.addAction(user_settings)
        menu_bar.addMenu(main_menu)

        self.setMenuBar(menu_bar)
        self.settings_window = QWidget()
        self.init_settings_window()

        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)

        self.setWindowTitle("AutoMod")

    @Slot(float)
    def spin_interhelical_gap_action(self, value):
        self.parameters['ihg'] = value
        for _, node_lst in self.scene.get_storage().get_nodes().items():
            node_lst[0].redraw_lattice()
        self.scene.get_storage().interpolate()

    @Slot(float)
    def spin_helix_diameter_action(self, value):
        self.parameters['hd'] = value
        for _, node_lst in self.scene.get_storage().get_nodes().items():
            node_lst[0].redraw_lattice()
        self.scene.get_storage().interpolate()

    @Slot(float)
    def spin_nucleotide_length_action(self, value):
        self.parameters['ntl'] = value
        self.scene.get_storage().interpolate()

    @Slot(float)
    def spin_mod_length_action(self, value):
        self.parameters['ml'] = value
        self.scene.get_storage().interpolate()

    @Slot(float)
    def spin_turn_length_action(self, value):
        self.parameters['tl'] = value
        self.scene.get_storage().interpolate()

    @Slot(float)
    def spin_grid_scale_action(self, value):
        self.parameters['gs'] = value
        self.scene.update_grid_scale()
        self.scene.get_storage().redraw_grid()
        self.view.init_fit()
        self.view.update()

    @Slot(float)
    def spin_twist_tol_action(self, value):
        self.parameters['tt'] = value
        self.scene.get_storage().interpolate()

    @Slot(float)
    def spin_zoom_value(self, value):
        self.parameters["zs"] = (1 / value)

    @Slot(float)
    def spin_translate_value(self, value):
        self.parameters["ts"] = (1 / value)

    @Slot(float)
    def spin_rotate_value(self, value):
        self.parameters["rs"] = (1 / value)

    def init_settings_window(self):
        self.settings_window.setWindowTitle("User Settings")
        self.settings_window.setMinimumWidth(400)
        self.settings_window.setMinimumHeight(200)
        window_layout = QGridLayout()
        self.settings_window.setLayout(window_layout)

        tabs = QTabWidget()
        window_layout.addWidget(tabs)
        parameter_page = QWidget()
        parameter_layout = QGridLayout()
        parameter_page.setLayout(parameter_layout)
        tabs.addTab(parameter_page, "Parameters")
        view_control_page = QWidget()
        view_control_layout = QGridLayout()
        view_control_page.setLayout(view_control_layout)
        tabs.addTab(view_control_page, "View control")

        view_control_layout.addWidget(QLabel("Zoom Sensitivity:"), 0, 0)
        zoom_value = QDoubleSpinBox()
        zoom_value.setSingleStep(0.01)
        zoom_value.setMinimum(0.01)
        zoom_value.setValue(self.parameters["zs"])
        zoom_value.valueChanged.connect(self.spin_zoom_value)
        view_control_layout.addWidget(zoom_value, 1, 0)

        view_control_layout.addWidget(QLabel("Translate Sensitivity:"), 2, 0)
        translate_value = QDoubleSpinBox()
        translate_value.setSingleStep(0.01)
        translate_value.setMinimum(0.01)
        translate_value.setValue(self.parameters["ts"])
        translate_value.valueChanged.connect(self.spin_translate_value)
        view_control_layout.addWidget(translate_value, 3, 0)

        view_control_layout.addWidget(QLabel("Rotate Sensitivity:"), 4, 0)
        rotate_value = QDoubleSpinBox()
        rotate_value.setSingleStep(0.01)
        rotate_value.setMinimum(0.01)
        rotate_value.setValue(self.parameters["rs"])
        rotate_value.valueChanged.connect(self.spin_rotate_value)
        view_control_layout.addWidget(rotate_value, 5, 0)

        parameter_layout.addWidget(QLabel("Interhelical gap:"), 0, 0)
        interhelical_gap_value = QDoubleSpinBox()
        interhelical_gap_value.setSuffix(" nm")
        interhelical_gap_value.setSingleStep(0.01)
        interhelical_gap_value.setMinimum(0)
        interhelical_gap_value.setMaximum(10)
        interhelical_gap_value.setValue(self.parameters["ihg"])
        interhelical_gap_value.valueChanged.connect(self.spin_interhelical_gap_action)
        parameter_layout.addWidget(interhelical_gap_value, 1, 0)

        parameter_layout.addWidget(QLabel("Helix diameter:"), 2, 0)
        helix_diameter_value = QDoubleSpinBox()
        helix_diameter_value.setSuffix(" nm")
        helix_diameter_value.setSingleStep(0.01)
        helix_diameter_value.setMinimum(0.01)
        helix_diameter_value.setMaximum(10)
        helix_diameter_value.setValue(self.parameters["hd"])
        helix_diameter_value.valueChanged.connect(self.spin_helix_diameter_action)
        parameter_layout.addWidget(helix_diameter_value, 3, 0)

        parameter_layout.addWidget(QLabel("Nucleotide length:"), 4, 0)
        nucleotide_length_value = QDoubleSpinBox()
        nucleotide_length_value.setSuffix(" nm")
        nucleotide_length_value.setSingleStep(0.01)
        nucleotide_length_value.setValue(self.parameters["ntl"])
        nucleotide_length_value.valueChanged.connect(self.spin_nucleotide_length_action)
        parameter_layout.addWidget(nucleotide_length_value, 5, 0)

        parameter_layout.addWidget(QLabel("Modification length:"), 6, 0)
        mod_length_value = QDoubleSpinBox()
        mod_length_value.setSuffix(" nm")
        mod_length_value.setSingleStep(0.01)
        mod_length_value.setValue(self.parameters["ml"])
        mod_length_value.valueChanged.connect(self.spin_mod_length_action)
        parameter_layout.addWidget(mod_length_value, 7, 0)

        parameter_layout.addWidget(QLabel("Turn length:"), 8, 0)
        turn_length_value = QDoubleSpinBox()
        turn_length_value.setSuffix(" nucleotides")
        turn_length_value.setSingleStep(0.1)
        turn_length_value.setDecimals(1)
        turn_length_value.setValue(self.parameters["tl"])
        turn_length_value.valueChanged.connect(self.spin_turn_length_action)
        parameter_layout.addWidget(turn_length_value, 9, 0)

        parameter_layout.setColumnMinimumWidth(1, 10)

        parameter_layout.addWidget(QLabel("Grid scale:"), 0, 2)
        grid_scale_value = QSpinBox()
        grid_scale_value.setSuffix(" nm/interval")
        grid_scale_value.setSingleStep(1)
        grid_scale_value.setMinimum(1)
        grid_scale_value.setMaximum(99)
        grid_scale_value.setValue(self.parameters["gs"])
        grid_scale_value.valueChanged.connect(self.spin_grid_scale_action)
        parameter_layout.addWidget(grid_scale_value, 1, 2)

        parameter_layout.addWidget(QLabel("Twist tolerance:"), 2, 2)
        twist_tol_value = QDoubleSpinBox()
        twist_tol_value.setSuffix(" nm")
        twist_tol_value.setSingleStep(0.01)
        twist_tol_value.setValue(self.parameters["tt"])
        twist_tol_value.valueChanged.connect(self.spin_twist_tol_action)
        parameter_layout.addWidget(twist_tol_value, 3, 2)

    @Slot(bool)
    def set_settings_action(self):
        self.settings_window.show()

    @Slot(bool)
    def write_tool_action(self, checked):
        if checked and self.scene.get_storage().has_mod_map():
            maps = self.scene.get_storage().get_mod_maps()
            json_file_name = QFileDialog.getOpenFileName(self, "", "", "*.json")
            if json_file_name:
                if len(maps) > 1:
                    self.ehandler.showMessage("There are several curves defined at the moment. "
                                              "Remove redundant curves before writing to file.")
                else:
                    with open(json_file_name[0], "r", encoding="utf-8") as f:
                        dct = json.load(f)
                        for helix_number, mod_array in maps[0][0].items():
                            if not self.write_loops_skips(dct, helix_number, mod_array):
                                self.ehandler.showMessage("Modification writing was not fully successful. "
                                                          "Make sure that all helix numbers match.")
                            if not self.delete_twisted_cos(dct, helix_number, maps[0][1][helix_number]):
                                self.ehandler.showMessage("Crossover deletion was not fully successful. "
                                                          "Make sure that all helix numbers match.")
                            if not self.write_twistless_cos(dct, helix_number, maps[0][1][helix_number]):
                                self.ehandler.showMessage("Crossover writing was not successful. "
                                                          "Make sure that all helix numbers match.")
                    with open(json_file_name[0], "w", encoding="utf-8") as f:
                        json.dump(dct, f)
        self.write_tool.setChecked(False)

    @staticmethod
    def write_loops_skips(dct, helix_number, mod_array):
        if "vstrands" in dct:
            for strand in dct["vstrands"]:
                if strand["num"] == helix_number:
                    length = len(strand["loop"])
                    strand["loop"] = np.where(mod_array == 1, 1, 0).tolist()[0]
                    strand["skip"] = np.where(mod_array == -1, -1, 0).tolist()[0]
                    dif = len(strand["loop"]) - length
                    if dif > 0:
                        strand["loop"] = strand["loop"][0:length]
                        strand["skip"] = strand["skip"][0:length]
                    elif dif < 0:
                        strand["loop"] = strand["loop"] + [0 for _ in range(np.abs(dif))]
                        strand["skip"] = strand["skip"] + [0 for _ in range(np.abs(dif))]
                    return True
            else:
                return False
        else:
            return False

    @staticmethod
    def delete_twisted_cos(dct, helix_number, twist_lst):
        if "vstrands" in dct:
            for strand in dct["vstrands"]:
                if strand["num"] == helix_number:
                    for i, pos in enumerate(strand["scaf"]):
                        if i < len(twist_lst):
                            if pos[0] != helix_number and pos[0] != -1 and pos[0] not in twist_lst[i]:
                                pos[0] = -1
                                pos[1] = -1
                            elif pos[2] != helix_number and pos[2] != -1 and pos[2] not in twist_lst[i]:
                                pos[2] = -1
                                pos[3] = -1
                    for i, pos in enumerate(strand["stap"]):
                        if i < len(twist_lst):
                            if pos[0] != helix_number and pos[0] != -1 and pos[0] not in twist_lst[i]:
                                pos[0] = -1
                                pos[1] = -1
                            elif pos[2] != helix_number and pos[2] != -1 and pos[2] not in twist_lst[i]:
                                pos[2] = -1
                                pos[3] = -1
                    return True
            else:
                return False
        else:
            return False

    @staticmethod
    def write_twistless_cos(dct, helix_number, twist_lst):
        if "vstrands" in dct:
            for strand in dct["vstrands"]:
                if strand["num"] == helix_number:
                    skip = False
                    for i, pos in enumerate(strand["scaf"]):
                        if i < len(twist_lst) and len(twist_lst[i]) > 0 and 2 < i < len(strand["scaf"]) - 2 and not skip:
                            for helix, co_type in twist_lst[i].items():
                                if co_type[1] and pos[0] == helix_number and pos[2] == helix_number and helix_number % 2 == 0:
                                    pos[2] = helix
                                    pos[3] = pos[1] + 1
                                    skip = True
                                    strand["scaf"][i + 1][0] = -1
                                    strand["scaf"][i + 1][1] = -1
                                elif co_type[1] and pos[0] == helix_number and pos[2] == helix_number and helix_number % 2 == 1:
                                    pos[0] = helix
                                    pos[1] = pos[3] + 1
                                    skip = True
                                    strand["scaf"][i + 1][2] = -1
                                    strand["scaf"][i + 1][3] = -1
                                break
                        else:
                            skip = False
                    skip = False
                    for i, pos in enumerate(strand["stap"]):
                        if i < len(twist_lst) and len(twist_lst[i]) > 0 and 2 < i < len(strand["stap"]) - 2 and not skip:
                            for helix, co_type in twist_lst[i].items():
                                if co_type[0] and pos[0] == helix_number and pos[2] == helix_number and helix_number % 2 == 0:
                                    pos[0] = helix
                                    pos[1] = pos[3] + 1
                                    skip = True
                                    strand["stap"][i + 1][2] = -1
                                    strand["stap"][i + 1][3] = -1
                                elif co_type[0] and pos[0] == helix_number and pos[2] == helix_number and helix_number % 2 == 1:
                                    pos[2] = helix
                                    pos[3] = pos[1] + 1
                                    skip = True
                                    strand["stap"][i + 1][0] = -1
                                    strand["stap"][i + 1][1] = -1
                                break
                        else:
                            skip = False
                    return True
            else:
                return False
        else:
            return False

    def connect_to_renumber(self, helix):
        if self.connected_helix is not None:
            self.connected_helix.connected_to_renumber(False)
        self.connected_helix = helix
        self.connected_helix.connected_to_renumber(True)
        self.renumber_box.setValue(self.connected_helix.get_number())

    def disconnect_from_renumber(self):
        if self.connected_helix is not None:
            self.connected_helix.connected_to_renumber(False)
            self.connected_helix.update()
            self.connected_helix = None

    @Slot(int)
    def spin_renumber_action(self, value):
        if self.connected_helix is not None:
            self.connected_helix.renumber(value)

    @Slot()
    def copy_cs_action(self):
        self.translate_ref.setChecked(False)
        self.zoom_cs.setChecked(False)
        self.rotate_lattice.setChecked(False)
        self.add_remove_helices.setChecked(False)
        self.renumber.setChecked(False)
        if self.cs_node is not None:
            self.cs_node.save_cs_angle(self.cs_view.get_rotation_amount())
            self.cs_node.save_cs_transform(self.cs_view.transform())
            self.cs_node.set_ref_point(self.cs_view.get_ref_point())
            # self.cs_view.set_ref_point(None)
            self.stored_cs = [self.cs_node.get_cs_scene(), self.cs_view.get_ref_point(),
                              self.cs_view.get_rotation_amount(), self.cs_view.transform(),
                              self.cs_node.get_lattice_type()]

    @Slot()
    def paste_cs_action(self):
        if self.cs_node is not None and self.stored_cs is not None:
            self.cs_node.change_scene(self.stored_cs)
            self.activate_cs_tool()

    @Slot(float)
    def ref_point_x_spin_translate_action(self, dx):
        if self.cs_view.get_ref_point() is not None:
            delta = dx - self.cs_view.get_ref_point().x()
            if np.abs(delta) >= 0.01:
                self.cs_view.get_ref_point().setPos(self.cs_view.get_ref_point().x() + delta,
                                                    self.cs_view.get_ref_point().y())

    @Slot(float)
    def ref_point_y_spin_translate_action(self, dy):
        if self.cs_view.get_ref_point() is not None:
            delta = dy - self.cs_view.get_ref_point().y()
            if np.abs(delta) >= 0.01:
                self.cs_view.get_ref_point().setPos(self.cs_view.get_ref_point().x(),
                                                    self.cs_view.get_ref_point().y() + delta)

    @Slot(float)
    def spin_rotate_lattice_action(self, theta):
        delta = theta - self.cs_view.get_rotation_amount()
        if np.abs(delta) >= 0.01:
            self.cs_view.rotate(delta)
            self.cs_view.set_rotation_amount(self.cs_view.get_rotation_amount() + delta)

    @Slot(bool)
    def zoom_cs_action(self, checked):
        if checked:
            self.translate_ref.setChecked(False)
            self.rotate_lattice.setChecked(False)
            self.renumber.setChecked(False)
            self.add_remove_helices.setChecked(False)
            self.cs_view.activate_zoom()
        else:
            self.cs_view.deactivate_zoom()

    @Slot(bool)
    def renumber_helices(self, checked):
        if checked:
            self.renumber_action.setVisible(True)
            self.translate_ref.setChecked(False)
            self.rotate_lattice.setChecked(False)
            self.zoom_cs.setChecked(False)
            self.add_remove_helices.setChecked(False)
            self.cs_view.enable_helix_renumbering()
        else:
            self.disconnect_from_renumber()
            self.cs_view.disable_helix_renumbering()
            self.renumber_action.setVisible(False)

    @Slot(bool)
    def add_remove_helices_action(self, checked):
        if checked:
            self.translate_ref.setChecked(False)
            self.rotate_lattice.setChecked(False)
            self.zoom_cs.setChecked(False)
            self.renumber.setChecked(False)
            self.cs_view.enable_helix_editing()
        else:
            self.cs_view.disable_helix_editing()

    @Slot(bool)
    def translate_ref_action(self, checked):
        if checked:
            self.zoom_cs.setChecked(False)
            self.rotate_lattice.setChecked(False)
            self.add_remove_helices.setChecked(False)
            self.renumber.setChecked(False)
            self.cs_view.activate_translate_ref()
        else:
            self.cs_view.deactivate_translate_ref()

    @Slot(bool)
    def rotate_lattice_action(self, checked):
        if checked:
            self.zoom_cs.setChecked(False)
            self.translate_ref.setChecked(False)
            self.add_remove_helices.setChecked(False)
            self.cs_view.activate_rotate()
        else:
            self.cs_view.deactivate_rotate()

    @Slot(bool)
    def draw_hc_action(self, checked):
        if checked:
            self.cs_scene.clear()
            self.cs_angle.setValue(0)
            self.cs_view.setTransform(QTransform())
            rd = (self.parameters['hd'] * 10) / 2 + (self.parameters['ihg'] * 10) / 2
            n = 20
            dx = np.sqrt(3) * rd
            self.cs_scene.setSceneRect(0, 0, 2 * ((n - 1) * 2 * dx), 4 * ((n - 1) * rd + ((n - 1) // 2) * rd))
            ref_point = ReferencePoint(((n - 1) * 2 * dx) / 2, (n - 1) * rd + ((n - 1) // 2) * rd, 2)
            self.cs_scene.addItem(ref_point)
            self.cs_node.set_ref_point(ref_point)
            self.cs_node.set_lattice_type(1)
            ref_point.setZValue(10)
            self.cs_view.set_ref_point(ref_point)
            self.ref_point_x_value.setValue(ref_point.x())
            self.ref_point_y_value.setValue(ref_point.y())
            for i in range(2 * n):
                for j in range(n):
                    self.cs_scene.addItem(HelixPoint(self.cs_node.get_ref_point(), j, i, self, 1))
            self.cs_view.centerOn(2 * ref_point.x(), 2 * ref_point.y())
            self.draw_hc.setChecked(False)

    @Slot(bool)
    def draw_sq_action(self, checked):
        if checked:
            self.cs_scene.clear()
            self.cs_angle.setValue(0)
            self.cs_view.setTransform(QTransform())
            rd = (self.parameters['hd'] * 10) / 2 + (self.parameters["ihg"] * 10) / 2
            n = 20
            self.cs_scene.setSceneRect(0, 0, 2 * (rd + (n - 1) * 2 * rd), 2 * (rd + (n - 1) * 2 * rd) + 6 * rd)
            ref_point = ReferencePoint((rd + rd + (n - 1) * 2 * rd) / 2, (rd + rd + (n - 1) * 2 * rd) / 2, 2)
            self.cs_scene.addItem(ref_point)
            self.cs_node.set_ref_point(ref_point)
            self.cs_node.set_lattice_type(2)
            ref_point.setZValue(10)
            self.cs_view.set_ref_point(ref_point)
            self.ref_point_x_value.setValue(ref_point.x())
            self.ref_point_y_value.setValue(ref_point.y())
            for i in range(n):
                for j in range(n):
                    self.cs_scene.addItem(HelixPoint(self.cs_node.get_ref_point(), j, i, self, 2))
            self.cs_view.centerOn(2 * ref_point.x(), 2 * ref_point.y())
            self.draw_sq.setChecked(False)

    @Slot(bool)
    def add_points_action(self, checked):
        if checked:
            self.cutoff_view_tools()
            self.connect_points.setChecked(False)
            self.remove_point_selection()
            self.view.activate_add_points()
        else:
            self.view.deactivate_add_points()

    @Slot(bool)
    def delete_point_action(self, checked):
        if checked:
            self.scene.get_storage().delete_selected_point()
            self.delete_point.setChecked(False)

    @Slot(bool)
    def disconnect_prev_action(self, checked):
        if checked:
            self.scene.get_storage().delete_selected_prev()
            self.disconnect_prev.setChecked(False)

    @Slot(bool)
    def disconnect_next_action(self, checked):
        if checked:
            self.scene.get_storage().delete_selected_next()
            self.disconnect_next.setChecked(False)

    @Slot(bool)
    def interpolate_action(self, checked):
        if checked:
            if self.cs_node is not None:
                self.cs_node.save_cs_angle(self.cs_view.get_rotation_amount())
                self.cs_node.save_cs_transform(self.cs_view.transform())
            self.scene.get_storage().interpolate()
            self.interpolate.setChecked(False)

    @Slot(bool)
    def connect_points_action(self, checked):
        if checked:
            self.cutoff_view_tools()
            self.deactivate_point_tools()
            self.add_points.setChecked(False)
            self.remove_point_selection()
            self.deactivate_cs_tool()
            self.view.activate_connect_points()
        else:
            self.view.deactivate_connect_points()
            self.deactivate_connection_tools()
            self.remove_point_selection()

    @Slot(bool)
    def point_x_translate_action(self, checked):
        if checked:
            self.cutoff_view_tools()
            self.cutoff_drawing_tools()
            self.point_z_translate.setChecked(False)
            self.point_y_translate.setChecked(False)
            self.view.activate_point_x_translation()
        else:
            self.view.deactivate_point_x_translation()

    @Slot(bool)
    def point_y_translate_action(self, checked):
        if checked:
            self.cutoff_view_tools()
            self.cutoff_drawing_tools()
            self.point_x_translate.setChecked(False)
            self.point_z_translate.setChecked(False)
            self.view.activate_point_y_translation()
        else:
            self.view.deactivate_point_y_translation()

    @Slot(bool)
    def point_z_translate_action(self, checked):
        if checked:
            self.cutoff_view_tools()
            self.cutoff_drawing_tools()
            self.point_x_translate.setChecked(False)
            self.point_y_translate.setChecked(False)
            self.view.activate_point_z_translation()
        else:
            self.view.deactivate_point_z_translation()

    @Slot(bool)
    def x_translate_action(self, checked):
        if checked:
            self.y_translate.setChecked(False)
            self.z_translate.setChecked(False)
            self.x_rotate.setChecked(False)
            self.y_rotate.setChecked(False)
            self.z_rotate.setChecked(False)
            self.zoom.setChecked(False)
            self.cutoff_drawing_tools()
            self.view.activate_x_translation()
        else:
            self.view.deactivate_x_translation()

    @Slot(bool)
    def y_translate_action(self, checked):
        if checked:
            self.x_translate.setChecked(False)
            self.z_translate.setChecked(False)
            self.x_rotate.setChecked(False)
            self.y_rotate.setChecked(False)
            self.z_rotate.setChecked(False)
            self.zoom.setChecked(False)
            self.cutoff_drawing_tools()
            self.view.activate_y_translation()
        else:
            self.view.deactivate_y_translation()

    @Slot(bool)
    def z_translate_action(self, checked):
        if checked:
            self.x_translate.setChecked(False)
            self.y_translate.setChecked(False)
            self.x_rotate.setChecked(False)
            self.y_rotate.setChecked(False)
            self.z_rotate.setChecked(False)
            self.zoom.setChecked(False)
            self.cutoff_drawing_tools()
            self.view.activate_z_translation()
        else:
            self.view.deactivate_z_translation()

    @Slot(bool)
    def x_rotate_action(self, checked):
        if checked:
            self.x_translate.setChecked(False)
            self.y_translate.setChecked(False)
            self.z_translate.setChecked(False)
            self.z_rotate.setChecked(False)
            self.zoom.setChecked(False)
            self.y_rotate.setChecked(False)
            self.z_rotate.setChecked(False)
            self.cutoff_drawing_tools()
            self.view.activate_x_rotation()
        else:
            self.view.deactivate_x_rotation()

    @Slot(bool)
    def y_rotate_action(self, checked):
        if checked:
            self.x_translate.setChecked(False)
            self.y_translate.setChecked(False)
            self.z_translate.setChecked(False)
            self.zoom.setChecked(False)
            self.x_rotate.setChecked(False)
            self.z_rotate.setChecked(False)
            self.cutoff_drawing_tools()
            self.view.activate_y_rotation()
        else:
            self.view.deactivate_y_rotation()

    @Slot(bool)
    def z_rotate_action(self, checked):
        if checked:
            self.x_translate.setChecked(False)
            self.y_translate.setChecked(False)
            self.z_translate.setChecked(False)
            self.zoom.setChecked(False)
            self.x_rotate.setChecked(False)
            self.y_rotate.setChecked(False)
            self.cutoff_drawing_tools()
            self.view.activate_z_rotation()
        else:
            self.view.deactivate_z_rotation()

    @Slot(bool)
    def zoom_action(self, checked):
        if checked:
            self.x_translate.setChecked(False)
            self.y_translate.setChecked(False)
            self.z_translate.setChecked(False)
            self.x_rotate.setChecked(False)
            self.y_rotate.setChecked(False)
            self.z_rotate.setChecked(False)
            self.cutoff_drawing_tools()
            self.view.activate_zoom()
        else:
            self.view.deactivate_zoom()

    @Slot(bool)
    def restore_action(self, checked):
        if checked:
            self.x_translate.setChecked(False)
            self.y_translate.setChecked(False)
            self.z_translate.setChecked(False)
            self.x_rotate.setChecked(False)
            self.y_rotate.setChecked(False)
            self.z_rotate.setChecked(False)
            self.zoom.setChecked(False)
            self.cutoff_drawing_tools()
            self.deactivate_cs_tool()
            self.view.restore_view()
            self.restore.setChecked(False)

    @Slot(float)
    def point_x_spin_translate_action(self, d):
        delta = d - self.scene.get_storage().get_selected_node_pos()[0]
        if np.abs(delta) >= 0.01:
            self.scene.get_storage().translate_node(delta, 0, 0)

    @Slot(float)
    def point_y_spin_translate_action(self, d):
        delta = d - self.scene.get_storage().get_selected_node_pos()[1]
        if np.abs(delta) >= 0.01:
            self.scene.get_storage().translate_node(0, delta, 0)

    @Slot(float)
    def point_z_spin_translate_action(self, d):
        delta = d - self.scene.get_storage().get_selected_node_pos()[2]
        if np.abs(delta) >= 0.01:
            self.scene.get_storage().translate_node(0, 0, delta)

    def disable_view_tools(self):
        self.x_translate.setCheckable(False)
        self.y_translate.setCheckable(False)
        self.z_translate.setCheckable(False)
        self.x_rotate.setCheckable(False)
        self.y_rotate.setCheckable(False)
        self.z_rotate.setCheckable(False)
        self.zoom.setCheckable(False)

    def enable_view_tools(self):
        self.x_translate.setCheckable(True)
        self.y_translate.setCheckable(True)
        self.y_translate.setCheckable(True)
        self.x_rotate.setCheckable(True)
        self.y_rotate.setCheckable(True)
        self.z_rotate.setCheckable(True)
        self.zoom.setCheckable(True)

    def cutoff_view_tools(self):
        self.x_translate.setChecked(False)
        self.y_translate.setChecked(False)
        self.z_translate.setChecked(False)
        self.view.deactivate_x_translation()
        self.view.deactivate_y_translation()
        self.view.deactivate_z_translation()
        self.x_rotate.setChecked(False)
        self.y_rotate.setChecked(False)
        self.z_rotate.setChecked(False)
        self.view.deactivate_x_rotation()
        self.view.deactivate_y_rotation()
        self.view.deactivate_z_rotation()
        self.zoom.setChecked(False)
        self.view.deactivate_zoom()

    def cutoff_drawing_tools(self):
        self.add_points.setChecked(False)
        self.connect_points.setChecked(False)

    def cutoff_point_tools(self):
        self.point_x_translate.setChecked(False)
        self.point_y_translate.setChecked(False)
        self.point_z_translate.setChecked(False)
        self.view.deactivate_point_x_translation()
        self.view.deactivate_point_y_translation()
        self.view.deactivate_point_z_translation()

    def activate_point_tools(self):
        self.point_tools.setVisible(True)

    def activate_connection_tools(self):
        self.connection_tools.setVisible(True)

    def activate_cs_tool(self):
        for item in self.scene.items():
            if isinstance(item, NodePoint) and item.has_selection():
                self.cs_scene = item.get_cs_scene()
                self.cs_node = item
        self.cs_view.setScene(self.cs_scene)
        if self.cs_node.get_ref_point() is not None:
            self.ref_point_x_value.setValue(self.cs_node.get_ref_point().x())
            self.ref_point_y_value.setValue(self.cs_node.get_ref_point().y())
            self.cs_view.set_ref_point(self.cs_node.get_ref_point())
            self.cs_view.centerOn(2 * self.cs_node.get_ref_point().x(), 2 * self.cs_node.get_ref_point().y())
        else:
            self.ref_point_x_value.setValue(0)
            self.ref_point_y_value.setValue(0)
        self.cs_angle.setValue(self.cs_node.get_cs_angle())
        if self.cs_node.get_cs_transform() is not None:
            self.cs_view.setTransform(self.cs_node.get_cs_transform())
        else:
            self.cs_view.setTransform(QTransform())
        self.cs_tool.setVisible(True)
        self.cs_toolbar.setVisible(True)

    def deactivate_point_tools(self):
        self.point_tools.setVisible(False)
        self.cutoff_point_tools()

    def deactivate_connection_tools(self):
        self.connection_tools.setVisible(False)

    def deactivate_cs_tool(self):
        self.translate_ref.setChecked(False)
        self.zoom_cs.setChecked(False)
        self.rotate_lattice.setChecked(False)
        self.add_remove_helices.setChecked(False)
        self.renumber.setChecked(False)
        if self.cs_node is not None:
            self.cs_node.save_cs_angle(self.cs_view.get_rotation_amount())
            self.cs_node.save_cs_transform(self.cs_view.transform())
            self.cs_view.set_ref_point(None)
        self.cs_tool.setVisible(False)
        self.cs_toolbar.setVisible(False)

    def point_tools_active(self):
        return self.point_tools.isVisible()

    def connection_tools_active(self):
        return self.connection_tools.isVisible()

    def connect_points_active(self):
        return self.connect_points.isChecked()

    def cs_tool_active(self):
        return self.cs_tool.isVisible()

    def update_point_value(self, pos_3d):
        self.point_x_value.setValue(pos_3d[0])
        self.point_y_value.setValue(pos_3d[1])
        self.point_z_value.setValue(pos_3d[2])

    def update_ref_point_value(self, x, y):
        self.ref_point_x_value.setValue(x)
        self.ref_point_y_value.setValue(y)

    def update_cs_angle(self, theta):
        self.cs_angle.setValue(self.cs_angle.value() - theta)

    def get_view(self):
        return self.view

    def get_cs_view(self):
        return self.cs_view

    def remove_point_selection(self):
        for item in self.scene.items():
            if isinstance(item, NodePoint) and item.has_selection():
                item.set_selection(False)

    def get_tool_widths(self):
        return self.connection_tools.width(), self.point_tools.width(), self.cs_tool.width(), self.cs_toolbar.width()

    def closeEvent(self, event):
        self.settings_window.close()

    def get_parameters(self):
        return self.parameters
