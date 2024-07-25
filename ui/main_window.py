import datetime
from PyQt6 import QtWidgets
from PyQt6.QtCore import QDate, QSettings, QTime, Qt, QByteArray, QDateTime
from PyQt6.QtGui import QCloseEvent

# one day, I will yaml or .ini this :D 
import tracker_config as tkc

# gui gui gui gooey gui
from ui.main_ui.gui import Ui_MainWindow

# my goofy logger setup
from logger_setup import logger

# navvy navvy navvy :D
from navigation.master_navigation import change_stack_page

# Window geometry and frame
from utility.app_operations.frameless_window import (
    FramelessWindow)
from utility.app_operations.window_controls import (
    WindowController)
from utility.app_operations.show_hide import toggle_views
# app ops
from utility.widgets_set_widgets.slider_spinbox_connections import (
    connect_slider_spinbox)

# Database connections
from database.database_manager import (
    DataManager)

# Delete Records
from database.database_utility.delete_records import (
    delete_selected_rows)

# setup Models
from database.database_utility.model_setup import (
    create_and_set_model)

# add data modules
from database.wefe_add_data import add_wefe_data
from database.mental_mental import add_mentalsolo_data
from database.cspr import add_cspr_data


class MainWindow(FramelessWindow, QtWidgets.QMainWindow, Ui_MainWindow):
    """
    The main window of the application.

    Inherits from FramelessWindow, QtWidgets.QMainWindow, and Ui_MainWindow.

    Attributes:
        mental_mental_model: The mental mental model.
        cspr_model: The CSPR model.
        wefe_model: The WEFE model.
        ui: The UI object.
        db_manager: The data manager object.
        settings: The QSettings object.
    """

    def __init__(self,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.mental_mental_model = None
        self.cspr_model = None
        self.wefe_model = None
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        # Database init
        self.db_manager = DataManager()
        self.setup_models()
        # QSettings settings_manager setup
        self.settings = QSettings(tkc.ORGANIZATION_NAME, tkc.APPLICATION_NAME)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.restore_state()
        self.app_operations()
        self.slider_set_spinbox()
        self.stack_navigation()
        self.commits()
        self.update_beck_summary()
        self.delete_group()
        self.auto_datettime()
        
        self.summing_box.setEnabled(False)
        for slider in [self.wellbeing_slider, self.excite_slider, self.focus_slider,
                       self.energy_slider]:
            slider.setRange(0, 10)
        
        self.wellbeing_slider.valueChanged.connect(self.update_beck_summary)
        self.excite_slider.valueChanged.connect(self.update_beck_summary)
        self.focus_slider.valueChanged.connect(self.update_beck_summary)
        self.energy_slider.valueChanged.connect(self.update_beck_summary)
    
    def auto_datettime(self) -> None:
        """
        Sets the current date and time for various widgets.

        This method sets the current date and time for the `mental_mental_time`,
        `mental_mental_date`, `wefe_time`, `wefe_date`, `cspr_time`, and `cspr_date`
        widgets to the current system date and time.

        Returns:
            None
        """
        self.mental_mental_time.setTime(QTime.currentTime())
        self.mental_mental_date.setDate(QDate.currentDate())
        self.wefe_time.setTime(QTime.currentTime())
        self.wefe_date.setDate(QDate.currentDate())
        self.cspr_time.setTime(QTime.currentTime())
        self.cspr_date.setDate(QDate.currentDate())
    
    def update_beck_summary(self):
            """
            Updates the averages of the sliders in the wellbeing and pain module such that
            the overall is the average of the whole.
            
            :return: None
            """
            try:
                values = [slider.value() for slider in
                          [self.wellbeing_slider, self.excite_slider, self.focus_slider,
                           self.energy_slider] if
                          slider.value() > 0]
                
                s = sum(values)
                
                self.summing_box.setValue(int(s))
            
            except Exception as e:
                logger.error(f"{e}", exc_info=True)
    
    def switch_to_page0(self):
        """
        Switches to page 0 in the stacked widget and adjusts the window size.

        This method sets the current widget of the stacked widget to the mm_page,
        which represents page 0. It also resizes the window to a width of 145 and
        a height of 265, and fixes the window size to prevent further resizing.

        Parameters:
            None

        Returns:
            None
        """
        self.stackedWidget.setCurrentWidget(self.mm_page)
        self.resize(145, 265)
        self.setFixedSize(145, 265)
    
    def switch_to_page1(self):
        """
        Switches the current widget to the 'wefe_page' and resizes the window.

        This method sets the current widget of the stackedWidget to the 'wefe_page',
        and then resizes the window to a fixed size of 145x265 pixels.

        Parameters:
        None

        Returns:
        None
        """
        self.stackedWidget.setCurrentWidget(self.wefe_page)
        self.resize(145, 265)
        self.setFixedSize(145, 265)
    
    def switch_to_page2(self):
        """
        Switches the current widget to the cspr_page and resizes the window.

        This method sets the current widget of the stackedWidget to the cspr_page,
        and resizes the window to a fixed size of 145x265 pixels.

        Parameters:
        None

        Returns:
        None
        """
        self.stackedWidget.setCurrentWidget(self.cspr_page)
        self.resize(145, 265)
        self.setFixedSize(145, 265)
    
    def switch_to_page4(self):
        """
        Switches the current widget to the data page and sets the window size to 850x450.

        This method is responsible for changing the current widget in the stacked widget to the data page.
        It also resizes the window to a fixed size of 850x450.

        Parameters:
            None

        Returns:
            None
        """
        self.stackedWidget.setCurrentWidget(self.data_page)
        self.resize(850, 450)
        self.setFixedSize(850, 450)

    def stack_navigation(self):
        """
        Connects the actions to their respective pages in the stacked widget.

        This method connects the actions (self.actionShowMM, self.actionShowWEFE, self.actionShowCSPR, self.actionShowData)
        to their respective pages (0, 1, 2, 3) in the stacked widget (self.stackedWidget). When an action is triggered,
        it calls the `change_stack_page` function with the stacked widget and the corresponding page as arguments.

        Raises:
            Exception: If an error occurs during the connection process.

        """
        try:
            change_stack_pages = {
                self.actionShowMM: 0,
                self.actionShowWEFE: 1,
                self.actionShowCSPR: 2,
                self.actionShowData: 3,
            }
            
            for action, page in change_stack_pages.items():
                action.triggered.connect(lambda _, p=page: change_stack_page(self.stackedWidget, p))
        
        except Exception as e:
            logger.error(f"An error has occurred: {e}", exc_info=True)
    
    def app_operations(self):
        """
        Performs the necessary setup operations for the application.

        This method connects the appropriate signals to their respective slots,
        sets the current index of the stacked widget based on the last saved index,
        and connects the actions to their corresponding page switches.

        Raises:
            Exception: If an error occurs during the setup process.

        """
        try:
            self.stackedWidget.currentChanged.connect(self.on_page_changed)
            last_index = self.settings.value("lastPageIndex", 0, type=int)
            self.stackedWidget.setCurrentIndex(last_index)
            
            self.actionShowMM.triggered.connect(self.switch_to_page0)
            self.actionShowWEFE.triggered.connect(self.switch_to_page1)
            self.actionShowCSPR.triggered.connect(self.switch_to_page2)
            self.actionShowData.triggered.connect(self.switch_to_page4)
        except Exception as e:
            logger.error(f"Error occurred while setting up app_operations : {e}", exc_info=True)
    
    def on_page_changed(self, index):
        """
        Callback method triggered when the page is changed in the UI.

        Args:
            index (int): The index of the new page.

        Raises:
            Exception: If an error occurs while setting the last page index.

        """
        try:
            self.settings.setValue("lastPageIndex", index)
        except Exception as e:
            logger.error(f"{e}", exc_info=True)
    
    def commits(self):
        """
        Executes the commit methods for mental_mental_table, cspr, and wefe.

        This method calls the following methods:
        - mental_mental_table_commit()
        - cspr_commit()
        - wefe_commit()
        """
        self.mental_mental_table_commit()
        self.cspr_commit()
        self.wefe_commit()
    
    def slider_set_spinbox(self):
        """
        Connects sliders to their corresponding spinboxes.

        This method connects each slider to its corresponding spinbox using a dictionary.
        The dictionary maps each slider object to its corresponding spinbox object.
        It then iterates over the dictionary and calls the `connect_slider_spinbox` function
        to establish the connection between each slider and spinbox.

        Returns:
            None
        """
        connect_slider_to_spinbox = {
            self.wellbeing_slider: self.wellbeing_spinbox,
            self.excite_slider: self.excite_spinbox,
            self.focus_slider: self.focus_spinbox,
            self.energy_slider: self.energy_spinbox,
            self.mood_slider: self.mood,
            self.mania_slider: self.mania,
            self.depression_slider: self.depression,
            self.mixed_risk_slider: self.mixed_risk,
            self.calm_slider: self.calm_spinbox,
            self.stress_slider: self.stress_spinbox,
            self.rage_slider: self.rage_spinbox,
            self.pain_slider: self.pain_spinbox,
        }
        
        for slider, spinbox in connect_slider_to_spinbox.items():
            connect_slider_spinbox(slider, spinbox)
    
    def mental_mental_table_commit(self) -> None:
        """
        Connects the 'commit' action to the 'add_mentalsolo_data' function and inserts data into the mental_mental_table.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            self.actionCommitMM.triggered.connect(
                lambda: add_mentalsolo_data(
                    self, {
                        "mental_mental_date": "mental_mental_date",
                        "mental_mental_time": "mental_mental_time",
                        "mood_slider": "mood_slider",
                        "mania_slider": "mania_slider",
                        "depression_slider": "depression_slider",
                        "mixed_risk_slider": "mixed_risk_slider",
                        "model": "mental_mental_model"
                    },
                    self.db_manager.insert_into_mental_mental_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def cspr_commit(self) -> None:
        """
        Connects the 'Commit CSPR' action to the 'add_cspr_data' function and inserts the CSPR exam data into the database.

        Raises:
            Exception: If an error occurs during the execution of the method.
        """
        try:
            self.actionCommitCSPR.triggered.connect(
                lambda: add_cspr_data(
                    self, {
                        "cspr_date": "cspr_date",
                        "cspr_time": "cspr_time",
                        "calm_slider": "calm_slider",
                        "stress_slider": "stress_slider",
                        "pain_slider": "pain_slider",
                        "rage_slider": "rage_slider",
                        "model": "cspr_model"
                    },
                    self.db_manager.insert_into_cspr_exam, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def wefe_commit(self) -> None:
        """
        Connects the actionCommitWEFE signal to the add_wefe_data function with the specified parameters.
        Inserts the WEFE data into the WEFE table using the db_manager.

        Raises:
            Exception: If an error occurs during the process.
        """
        try:
            self.actionCommitWEFE.triggered.connect(
                lambda: add_wefe_data(
                    self, {
                        "wefe_date": "wefe_date",
                        "wefe_time": "wefe_time",
                        "wellbeing_slider": "wellbeing_slider",
                        "excite_slider": "excite_slider",
                        "focus_slider": "focus_slider",
                        "energy_slider": "energy_slider",
                        "summing_box": "summing_box",
                        "model": "wefe_model"
                    },
                    self.db_manager.insert_into_wefe_table, ))
        except Exception as e:
            logger.error(f"An Error has occurred {e}", exc_info=True)
    
    def delete_group(self):
        """
        Connects the 'Delete' action to the corresponding delete_selected_rows function for multiple table views.

        This method connects the 'Delete' action to the delete_selected_rows function for multiple table views.
        It sets up the connections for deleting selected rows in the 'wefe_tableview', 'cspr_tableview', and 'mental_mental_table'.

        Parameters:
        - self: The instance of the main window.

        Returns:
        None
        """
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'wefe_tableview',
                'wefe_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'cspr_tableview',
                'cspr_model'
            )
        )
        self.actionDelete.triggered.connect(
            lambda: delete_selected_rows(
                self,
                'mental_mental_table',
                'mental_mental_model'
            )
        )
    
    def setup_models(self) -> None:
        """
        Sets up the models for the different table views in the main window.

        This method creates and sets the models for the 'wefe_tableview', 'cspr_tableview',
        and 'mental_mental_table' table views.

        Returns:
            None
        """
        self.wefe_model = create_and_set_model(
            "wefe_table",
            self.wefe_tableview
        )
        self.cspr_model = create_and_set_model(
            "cspr_table",
            self.cspr_tableview
        )
        self.mental_mental_model = create_and_set_model(
            "mental_mental_table",
            self.mental_mental_table
        )
    
    def save_state(self):
        """
        Saves the window geometry state and window state.

        This method saves the current geometry and state of the window
        using the QSettings object. It saves the window geometry state
        and the window state separately.

        Raises:
            Exception: If there is an error while saving the window geometry state or window state.
        """
        try:
            self.settings.setValue("geometry", self.saveGeometry())
        except Exception as e:
            logger.error(f"Error saving the minds_module geo{e}", exc_info=True)
        try:
            self.settings.setValue("windowState", self.saveState())
        except Exception as e:
            logger.error(f"Error saving the minds_module geo{e}", exc_info=True)
    
    def restore_state(self) -> None:
        """
        Restores the window geometry and state.

        This method restores the previous geometry and state of the window
        based on the values stored in the settings.

        Raises:
            Exception: If there is an error restoring the window geometry or state.
        """
        try:
            # restore window geometry state
            self.restoreGeometry(self.settings.value("geometry", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring the minds module : stress state {e}")
        
        try:
            self.restoreState(self.settings.value("windowState", QByteArray()))
        except Exception as e:
            logger.error(f"Error restoring WINDOW STATE {e}", exc_info=True)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Event handler for the close event of the window.

        Saves the state before closing the window.

        Args:
            event (QCloseEvent): The close event object.

        Returns:
            None
        """
        try:
            self.save_state()
        except Exception as e:
            logger.error(f"error saving state during closure: {e}", exc_info=True)
