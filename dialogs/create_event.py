from typing import Any

from aiogram.enums import ContentType
from aiogram.filters import Filter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Next, Back
from aiogram_dialog.widgets.text import Const


class CreateEventDialog(StatesGroup):
    title = State() # что
    description = State() # описание
    photo = State() # фото
    address = State() # где
    datetime = State() # дата/время

def validate_text(title: str, min_letters: int, max_letters: int):
    # Проверка, что title не состоит только из цифр
    if title.replace(" ", "").isdigit():
        raise ValueError("Текст не может состоять только из цифр")
    # Проверка длины
    if len(title) < min_letters or len(title) > max_letters:
        raise ValueError(f"Текст должен быть {min_letters} - {max_letters} символов")

async def error_text(
        message: Message,
        dialog_: Any,
        manager: DialogManager,
        error_: ValueError
):
    await message.answer(str(error_))

async def handle_photo(message: Message, message_input: MessageInput, manager: DialogManager):
    # Проверяем, что сообщение содержит фото
    if message.photo:
        photo = message.photo[-1]  # Берем самое большое изображение
        file_id = photo.file_id
        # Сохраняем file_id в DialogManager (например, в dialog_data)
        manager.dialog_data["photo_id"] = file_id
        await manager.done()  # Переходим к следующему шагу
    else:
        await message.answer("Пожалуйста, отправьте фотографию!")

dialog_create_event = Dialog(
    Window(
        Const('Название мероприятия:'),
        TextInput(
            id='title',
            type_factory=lambda x: validate_text(x, 5, 20),
            on_success=Next(),
            on_error=error_text,
        ),
        state=CreateEventDialog.title,
    ),
    Window(
        Const('Описание мероприятия:'),
        TextInput(
            id='description',
            type_factory=lambda x: validate_text(x, 20, 100),
            on_success=Next(),
            on_error=error_text,
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.description,
    ),
    Window(
        Const('Фотография мероприятия:'),
        MessageInput(
            handle_photo,  # Обработчик загрузки фото
            # content_types=[ContentType.PHOTO],  # Принимаем только фото
            # filter=photo_filter
        ),
        Back(Const('Назад')),
        state=CreateEventDialog.photo,
    ),
)