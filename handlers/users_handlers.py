from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from handbook import handbook
from keyboards import (create_keyboard_pagination,
                       create_keyboard_bookmarks,
                       create_edit_keyboard)
from config import Config, add_config
from database import users_db, user_dict_template
from services import book


router = Router()
config = add_config()


@router.message(F.text == '/start')
async def process_command_start(message: Message):
    await message.answer(
        text=handbook['/start'],
        parse_mode='HTML'
    )
    id = message.from_user.id
    users_db.setdefault(id, user_dict_template)


@router.message(F.text == '/help')
async def process_command_help(message: Message):
    await message.answer(
        text=handbook['/help'],
        parse_mode='HTML'
    )


@router.message(F.text == '/beginning')
async def process_command_beginning(message: Message):
    users_db[message.from_user.id]['page'] = 1
    await message.answer(
        text=book[users_db[message.from_user.id]['page']],
        reply_markup=create_keyboard_pagination(
            users_db[message.from_user.id]['page'], len(book))
    )


@router.message(F.text == '/continue')
async def process_command_continue(message: Message):
    await message.answer(
        text=book[users_db[message.from_user.id]['page']],
        reply_markup=create_keyboard_pagination(
            users_db[message.from_user.id]['page'],
            len(book))
    )


@router.callback_query(F.data == 'bookmark')
async def process_press_bookmark(callback: CallbackQuery):
    number_page = users_db[callback.from_user.id]['page']
    text_bookmark = book[number_page][:100]
    if number_page in users_db[callback.from_user.id]['bookmarks']:
        await callback.answer(
            text=handbook['already_have_bookmark'],
            show_alert=True
        )
    else:
        users_db[callback.from_user.id]['bookmarks'].add(
            number_page)
        await callback.answer(
            text=handbook['add_bookmark'],
            show_alert=True
        )


@router.callback_query(F.data == 'backward')
async def process_press_backward(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] == 1:
        await callback.answer(
            text=handbook['already_open_first_page'],
            show_alert=True
        )
    else:
        users_db[callback.from_user.id]['page'] -= 1
        await callback.message.edit_text(
            text=book[users_db[callback.from_user.id]['page']],
            reply_markup=create_keyboard_pagination(
                page_number=users_db[callback.from_user.id]['page'],
                total_pages=len(book)
            )
        )


@router.callback_query(F.data == 'forward')
async def process_press_forward(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] == len(book):
        await callback.answer(
            text=handbook['already_open_last_page'],
            show_alert=True
        )
    else:
        users_db[callback.from_user.id]['page'] += 1
        await callback.message.edit_text(
            text=book[users_db[callback.from_user.id]['page']],
            reply_markup=create_keyboard_pagination(
                page_number=users_db[callback.from_user.id]['page'],
                total_pages=len(book)
            )
        )

@router.message(F.text == '/bookmarks')
async def process_command_bookmarks(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=handbook['/bookmarks'],
            parse_mode='HTML',
            reply_markup=create_keyboard_bookmarks(
                users_db[message.from_user.id]['bookmarks']
            )
        )
    else:
        await message.answer(text=handbook['no_bookmarks'])

@router.callback_query(F.data == 'back_button')
async def process_press_button_cancel(callback: CallbackQuery):
    await callback.message.delete()

@router.callback_query(F.data == 'cancel')
async def process_press_button_cancel(callback: CallbackQuery):
    await callback.message.edit_text(
        text=handbook['/bookmarks'],
        parse_mode='HTML',
        reply_markup=create_keyboard_bookmarks(
            bookmarks=users_db[callback.from_user.id]['bookmarks']
        )
    )

@router.callback_query(F.data == 'edit_bookmarks')
async def process_press_button_edit_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(
        text=handbook['edit_bookmarks'],
        parse_mode='HTML',
        reply_markup=create_edit_keyboard(
            bookmarks=users_db[callback.from_user.id]['bookmarks']
        )
    )

@router.callback_query(F.data[-3:] == 'del')
async def process_delete_bookmarks(callback: CallbackQuery):
    number_page_delete = int(callback.data.split()[0])
    users_db[callback.from_user.id]['bookmarks'].discard(
        number_page_delete)
    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(
            text=handbook['edit_bookmarks'],
            parse_mode='HTML',
            reply_markup=create_edit_keyboard(
                bookmarks=users_db[callback.from_user.id]['bookmarks']
            )
        )
    else:
        await callback.message.edit_text(
            text=handbook['list_of_bookmarks_is_none']
        )

@router.callback_query(F.data[:4] == 'page')
async def process_transition_on_page(callback: CallbackQuery):
    users_db[callback.from_user.id]['page'] = int(callback.data.split()[1])
    await callback.message.edit_text(
        text=book[users_db[callback.from_user.id]['page']],
        reply_markup=create_keyboard_pagination(
            page_number=users_db[callback.from_user.id]['page'],
            total_pages=len(book)
        )
    )

@router.message()
async def process_reception_other_messages(message: Message):
    await message.answer(
        text=handbook['other_messages']
    )