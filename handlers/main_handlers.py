from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}')


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Готов помочь!')


@router.message()
async def echo_handler(message: Message):
    print(message.model_dump_json())
    await message.answer(f'Извини, команда {message.text} мне неизвестна')