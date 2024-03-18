from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from handbook import handbook
from services.file_handing import book

def create_keyboard_pagination(page_number, total_pages) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(
            text=handbook['backward'],
            callback_data='backward'
        ),
        InlineKeyboardButton(
            text=f'{page_number}/{total_pages}',
            callback_data='bookmark'
        ),
        InlineKeyboardButton(
            text=handbook['forward'],
            callback_data='forward'
        )]

    kb_builder.add(*buttons)

    return kb_builder.as_markup()

def create_keyboard_bookmarks(bookmarks) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in sorted(bookmarks):
        kb_builder.row(InlineKeyboardButton(
            text=f'{button} - {book[button][:100]}',
            callback_data=f'page {str(button)}'
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=handbook['edit_bookmarks_button'],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text=handbook['back_button'],
            callback_data='back_button'
        ),
        width=2
    )

    return kb_builder.as_markup()

def create_edit_keyboard(bookmarks: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in sorted(bookmarks):
        kb_builder.row(InlineKeyboardButton(
            text=f'{handbook["del"]} {button} - {book[button][:100]}',
            callback_data=f'{button} del'
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=handbook['cancel'],
            callback_data='cancel'
        )
    )

    return kb_builder.as_markup()