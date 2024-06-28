import datetime
import uuid

from loguru import logger
import aiogram
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
import aiogram.filters
import aiogram.filters.callback_data
from aiogram.filters.command import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from telegram.keyboards import (
    main_menu_keyboard,
    reminder_prop_choice_keyboard,
    get_reminders_to_update_keyboard,
)
from telegram.callback_data import (
    UserCmdCallback,
    UserCmds,
    UpdateReminderCallback,
    ReminderToUpdateChoice,
    ReminderEditMenu,
    ReminderEditMenuOpts,
)
from telegram.utils import (
    parse_remind_cmd_args,
)
from controllers import (
    RequestExecStatus,
    create_reminder,
    get_user_reminders,
    update_reminder,
)
from app_models import ReminderCreateRequest, User


router = aiogram.Router(name="rem")


@router.message(Command("start"))  # type: ignore
async def cmd_start(
    message: aiogram.types.Message,
) -> None:
    """
    Handles `/start` command.

    ...
    """

    if message.from_user is not None:
        logger.debug(f"Recieved /start command from {message.from_user.username}")

    await message.answer(
        "Choose operation",
        reply_markup=main_menu_keyboard,
    )


@router.message(Command("remind"))  # type: ignore
async def cmd_create_reminder(
    message: aiogram.types.Message,
    command: CommandObject,
) -> None:
    """
    Handles `/remind` command.

    ...
    """

    fromuser = message.from_user
    if fromuser is None:
        logger.debug(f"Unable to get user of the message")
        return

    logger.debug(f"Recieved /remind command from {message.from_user.username}")

    args = parse_remind_cmd_args(command.args)
    if args is None:
        logger.debug(f"Invalid remind command args: {command.args}")
        await message.answer(f"Invalid command format")
        return

    res = await create_reminder(
        user_tg_id=fromuser.id, reminder_time=args.rem_time, reminder_text=args.text
    )

    if res == RequestExecStatus.OK:
        date = args.rem_time.date()
        answer = (
            f"Reminder has been successfully set.\n"
            f"Time: {date.day}.{date.month} {args.rem_time.hour}:{args.rem_time.minute}\n"
            f"Text: {args.text}"
        )
        await message.answer(answer)
    else:
        await message.answer(f"Something went wrong ({res.name})")


@router.callback_query(UserCmdCallback.filter(F.cmd == UserCmds.CREATE_REMINDER))  # type: ignore
async def clb_create_reminder(query: aiogram.types.CallbackQuery) -> None:

    if query.data is None:
        return

    query.message.answer(
        "Select date and time for a reminder",
        reply_markup=...,
    )

    await query.answer("Not implemented")


@router.callback_query(UserCmdCallback.filter(F.cmd == UserCmds.LIST_REMINDERS))  # type: ignore
async def clb_list_reminders(query: aiogram.types.CallbackQuery) -> None:
    """Triggered when user sends a query to list his reminders"""

    if query.data is None:
        return

    reminders = await get_user_reminders(query.from_user.id)

    if reminders is None:
        await query.message.answer("Unknown user")
        return

    if len(reminders) == 0:
        await query.message.answer("No reminders were set yet")
        return

    await query.message.answer(
        "\n".join(map(str, reminders)), reply_markup=main_menu_keyboard
    )

    # delete previous message
    await query.message.delete()


# UPDATE


class UpdateReminderForm(StatesGroup):  # type: ignore

    reminder_choice = State()
    reminder_edit_menu = State()
    prop_edit = State()
    time_edit = State()
    text_edit = State()


@router.callback_query(UserCmdCallback.filter(F.cmd == UserCmds.UPDATE_REMINDER))  # type: ignore
async def clb_list_reminders_for_update(
    query: aiogram.types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Triggered when user sends a query to list reminders available for update"""

    logger.debug("Querying reminders available for update...")
    reminders = await get_user_reminders(query.from_user.id)

    if reminders is None:
        await query.message.answer("Unknown user")
        return

    logger.debug(f"Got {len(reminders)} available reminders for update")

    if len(reminders) == 0:
        await query.message.answer("No reminders were set yet")

    await state.set_state(UpdateReminderForm.reminder_choice)

    await query.message.answer(
        "Choose reminder to update",
        reply_markup=get_reminders_to_update_keyboard(reminders),
    )

    await query.message.delete()


@router.callback_query(
    UpdateReminderForm.reminder_choice,
    ReminderToUpdateChoice.filter(),
)  # type: ignore
async def clb_on_update_reminder_choice(
    query: aiogram.types.CallbackQuery,
    callback_data: ReminderToUpdateChoice,
    state: FSMContext,
) -> None:
    """Triggered when user chooses reminder to update

    Replies with inline keyboard to select reminder properties for update
    """

    logger.debug(f"User has chosen to update reminder '{callback_data.id_}'")

    await state.update_data(
        reminder_id=callback_data.id_,
        reminder_time=callback_data.time,
    )
    await state.set_state(UpdateReminderForm.reminder_edit_menu)

    await query.message.answer(
        "Choose what to update",
        reply_markup=reminder_prop_choice_keyboard,
    )

    # TODO handle errors
    await query.message.delete()


@router.callback_query(
    UpdateReminderForm.reminder_edit_menu,
    ReminderEditMenu.filter(F.opt == ReminderEditMenuOpts.CANCEL),
)  # type: ignore
async def on_reminder_edit_cancel(
    query: aiogram.types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Triggered when user cancels reminder update process

    Ends update FSM state
    """

    logger.debug("User cancelled reminder update")

    await state.clear()

    await query.answer("Update operation cancelled")
    await query.message.answer(
        text="Choose option",
        reply_markup=main_menu_keyboard,
    )
    await query.message.delete()


@router.callback_query(
    UpdateReminderForm.reminder_edit_menu,
    ReminderEditMenu.filter(F.opt == ReminderEditMenuOpts.CONFIRM),
)  # type: ignore
async def on_reminder_edit_confirm(
    query: aiogram.types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Triggered when user confirms reminder update process

    Ends update FSM state
    """

    logger.debug("User confirmed reminder update")

    data = await state.get_data()
    updated_time = data.get("updated_time", None)
    updated_text = data.get("updated_text", None)

    if (updated_time, updated_text) == (None, None):
        logger.debug("User updated nothing")
        await query.answer("Nothing selected for update, returning...")
    else:
        await update_reminder(id_=data["id"], time=updated_time, text=updated_text)
        await query.answer("Reminder has been successfully updated")

    await state.clear()
    await query.message.answer(
        text="Choose option",
        reply_markup=main_menu_keyboard,
    )
    await query.message.delete()


@router.callback_query(
    UpdateReminderForm.reminder_edit_menu,
    ReminderEditMenu.filter(F.opt == ReminderEditMenuOpts.UPD_TIME),
)  # type: ignore
async def on_reminder_time_update_choice(
    query: aiogram.types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Triggered when user chooses to update reminder time"""

    logger.debug("Updating reminder time")

    await state.set_state(UpdateReminderForm.time_edit)
    await query.message.answer(f"Enter new reminder time below:")


@router.callback_query(
    UpdateReminderForm.reminder_edit_menu,
    ReminderEditMenu.filter(F.opt == ReminderEditMenuOpts.UPD_TXT),
)  # type: ignore
async def on_reminder_text_update_choice(
    query: aiogram.types.CallbackQuery,
    state: FSMContext,
) -> None:
    """Triggeered when user chooses to update reminder text"""

    logger.debug("Updating reminder text")

    await state.set_state(UpdateReminderForm.text_edit)
    await query.message.answer(f"Enter new reminder text below:")


@router.message(UpdateReminderForm.time_edit)  # type: ignore
async def on_reminder_time_edit(message: Message, state: FSMContext) -> None:
    """Triggered when user enters new time for reminder

    Sets state back to reminder update menu
    """

    logger.debug(f"User entered new reminder time: {message.text}")

    # TODO parse time properly
    new_time = datetime.datetime.strptime(message.text, "%d %B, %Y")
    await state.update_data(updated_time=new_time)

    data = await state.get_data()
    await message.answer(
        f"Updated time of reminder {data['reminder_id']} with {new_time}"
    )

    await state.set_state(UpdateReminderForm.reminder_edit_menu)
    await message.delete()


@router.message(UpdateReminderForm.text_edit)  # type: ignore
async def on_reminder_text_edit(message: Message, state: FSMContext) -> None:
    """Triggered when user enters new text for reminder

    Sets state back to reminder update menu
    """

    logger.debug(f"user entered new reminder text: {message.text}")

    # TODO parse and validate new text
    new_text = message.text
    await state.update_data(updated_text=new_text)

    data = await state.get_data()
    await message.answer(f"Updated text of reminder {data['reminder_id']}")

    await state.set_state(UpdateReminderForm.reminder_edit_menu)
    await message.delete()


# DELETE


@router.callback_query(UserCmdCallback.filter(F.cmd == UserCmds.DELETE_REMINDER))  # type: ignore
async def clb_delete_reminder(query: aiogram.types.CallbackQuery) -> None:

    if query.data is None:
        return

    await query.answer("Not implemented")
