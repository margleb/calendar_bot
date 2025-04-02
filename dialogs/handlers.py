from datetime import datetime, date
from typing import Any

from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput


async def handle_photo(message: Message, message_input: MessageInput, manager: DialogManager):
    if message.photo:
        manager.dialog_data['photo'] = message.photo[-1].file_id
        await manager.next()
    else:
        await message.reply('🔴 Пожалуйста, загрузите свою фотографию')


async def on_date_selected(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    if selected_date < datetime.now().date():
        # Если дата в прошлом - показываем предупреждение
        await callback.answer("Нельзя запланировать событие на прошедшую дату.", show_alert=True)
    else:
        # Если дата валидна - сохраняем и уведомляем
        manager.dialog_data["selected_date"] = selected_date
    await manager.next()  # Переходим к следующему шагу


async def selected_city(callback: CallbackQuery, widget: Any, manager: DialogManager, city: str):
    manager.dialog_data['city'] = city
    await manager.next()


def validate_text(title: str, min_letters: int, max_letters: int) -> str:
    # Проверка, что текст не состоит только из цифр
    if title.replace(" ", "").isdigit():
        raise ValueError("🔴 Текст не может состоять только из цифр")
    # Проверка длины
    if len(title) < min_letters or len(title) > max_letters:
        raise ValueError(f"🔴 Текст должен быть <b>{min_letters} - {max_letters}</b> символов")
    return title


async def error_text(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.reply(str(error_), parse_mode=ParseMode.HTML)