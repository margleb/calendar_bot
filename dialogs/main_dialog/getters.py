from aiogram_dialog import DialogManager


async def dialog_data_getter(dialog_manager: DialogManager, **kwargs):
    dialog_data = dialog_manager.dialog_data
    return {
        'selected_date': dialog_data.get('selected_date'),
        'total_events': dialog_data.get('total_events')
    }