from PyQt6.QtCore import QDate, QTime
import tracker_config as tkc
from logger_setup import logger
from typing import Dict, Any, Callable, Tuple, Optional, List

def add_wefe_data(main_window_instance: Any, widget_names: Dict[str, str], db_insert_method: Callable[..., None]) -> None:
    """
    Add WEFE data to the database.

    Args:
        main_window_instance: An instance of the main window.
        widget_names: A dictionary containing the names of the widgets.
        db_insert_method: The method used to insert data into the database.

    Returns:
        None
    """
    widget_methods: Dict[str, Tuple[Optional[str], str, Optional[str]]] = {
        widget_names['wefe_date']: (None, 'date', "yyyy-MM-dd"),
        widget_names['wefe_time']: (None, 'time', "hh:mm:ss"),
        widget_names['wellbeing_slider']: (None, 'value', None),
        widget_names['excite_slider']: (None, 'value', None),
        widget_names['focus_slider']: (None, 'value', None),
        widget_names['energy_slider']: (None, 'value', None),
        widget_names['summing_box']: (None, 'value', None),
    }

    data_to_insert: List[Any] = []
    for widget_name, (widget_attr, method, format_type) in widget_methods.items():
        widget = getattr(main_window_instance, widget_name)
        try:
            value = getattr(widget, method)()
            if format_type:
                value = value.toString(format_type)
            data_to_insert.append(value)
        except Exception as e:
            logger.error(f"Error getting value from widget {widget_name}: {e}")

    try:
        db_insert_method(*data_to_insert)
        reset_wefe_data(main_window_instance, widget_names)
    except Exception as e:
        logger.error(f"Error inserting data into the database: {e}")


def reset_wefe_data(main_window_instance: Any, widget_names: Dict[str, str]) -> None:
    """
    Reset the WEFE data in the main window.

    Args:
        main_window_instance: An instance of the main window.
        widget_names: A dictionary containing the names of the widgets.

    Returns:
        None

    Raises:
        Exception: If there is an error resetting the pain levels form.
    """
    try:
        getattr(main_window_instance, widget_names['wefe_date']).setDate(QDate.currentDate())
        getattr(main_window_instance, widget_names['wefe_time']).setTime(QTime.currentTime())
        getattr(main_window_instance, widget_names['wellbeing_slider']).setValue(0)
        getattr(main_window_instance, widget_names['excite_slider']).setValue(0)
        getattr(main_window_instance, widget_names['focus_slider']).setValue(0)
        getattr(main_window_instance, widget_names['energy_slider']).setValue(0)
        getattr(main_window_instance, widget_names['summing_box']).setValue(0)
        getattr(main_window_instance, widget_names['model']).select()
    except Exception as e:
        logger.error(f"Error resetting pain levels form: {e}")
