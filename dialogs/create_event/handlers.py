from datetime import datetime, date
from typing import Any

from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from models import Event


async def handle_photo(message: Message, message_input: MessageInput, manager: DialogManager):
    if message.photo:
        manager.dialog_data['photo'] = message.photo[-1].file_id
        await manager.next()
    else:
        await message.reply('🔴 Пожалуйста, загрузите свою фотографию')


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


async def on_public_event(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):

    session = dialog_manager.middleware_data.get("session")
    event_data = dialog_manager.dialog_data  # Здесь должны быть все данные события

    try:
        # Создаем запрос на вставку нового события
        stmt = insert(Event).values(
            tg_user_id=callback.from_user.id,
            image_id=event_data.get("photo"),
            title=dialog_manager.find('title').get_value(),
            description=dialog_manager.find('description').get_value(),
            city=dialog_manager.start_data["selected_city"],
            date=dialog_manager.start_data["selected_date"],
            username=callback.from_user.username,
            moderation=False,
        )

        # Выполняем запрос
        await session.execute(stmt)
        await session.commit()

        await callback.answer("✅ Событие успешно опубликовано и отправлено на модерацию!")
        await dialog_manager.done()  # Закрываем диалог

    except SQLAlchemyError as e:
        await session.rollback()
        await callback.answer(f"❌ Ошибка при сохранении: {str(e)}", show_alert=True)