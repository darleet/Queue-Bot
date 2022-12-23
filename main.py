import logging
import queue_func
import admin_func

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def enque_position(update: Update, context: CallbackContext) -> None:
    """Adds the user on some position in the queue."""
    user_id = update.effective_user.id
    message_id = update.message.message_id

    if not admin_func.is_admin(user_id):
        add_username = "ERROR"
        update.effective_chat.send_message(
            text="Ты не админ)) Используй /eq если хочешь"
                 "добавиться в очередь",
            reply_to_message_id=message_id,
        )

    elif len(context.args) >= 3:
        add_username = str(context.args[0]).replace("@", "")
        add_name = [str(s) for s in context.args[2:]]
        add_name = " ".join(add_name)

        try:
            position = int(context.args[1])
            user_added = queue_func.queue_enqueue(add_username, add_username, add_name, position)
            if user_added:
                update.effective_chat.send_message(
                    text=f"@{add_username} добавлен в очередь!",
                    reply_to_message_id=message_id,
                )
            else:
                update.effective_chat.send_message(
                    text=f"@{add_username} уже в очереди...",
                    reply_to_message_id=message_id,
                )
        except ValueError:
            update.effective_chat.send_message(
                text="Некорректный номер позиции!",
                reply_to_message_id=message_id,
            )

    else:
        add_username = "ERROR"
        update.effective_chat.send_message(
            text="Некорректные аргументы... Использование:\n\n"
                 "/eq {@username} {position} *{name}",
            reply_to_message_id=message_id,
        )

    logger.info("User %s was enqueued.", add_username)


def enque(update: Update, context: CallbackContext) -> None:
    """Adds the user in the queue."""

    name = update.effective_user.full_name
    user_id = update.effective_user.id
    username = update.effective_user.username
    message_id = update.message.message_id

    if not context.args and admin_func.check_status():
        if username is None:
            add_username = user_id
        else:
            add_username = username
        add_name = name
        user_added = queue_func.queue_enqueue(user_id, add_username, add_name)

        if user_added:
            update.effective_chat.send_message(
                text="Ты был добавлен в очередь!",
                reply_to_message_id=message_id,
            )
        else:
            update.effective_chat.send_message(
                text="Ты уже в очереди...",
                reply_to_message_id=message_id,
            )

    elif context.args and (not ("@" in context.args[0])) and admin_func.check_status():
        if username is None:
            add_username = user_id
        else:
            add_username = username
        add_name = [str(s) for s in context.args[0:]]
        add_name = " ".join(add_name)
        user_added = queue_func.queue_enqueue(user_id, add_username, add_name)

        if user_added:
            update.effective_chat.send_message(
                text="Ты был добавлен в очередь!",
                reply_to_message_id=message_id,
            )
        else:
            update.effective_chat.send_message(
                text="Ты уже в очереди...",
                reply_to_message_id=message_id,
            )

    elif admin_func.is_admin(user_id) and len(context.args) >= 2:
        add_username = context.args[0].replace("@", "")
        add_name = [str(s) for s in context.args[1:]]
        add_name = " ".join(add_name)
        user_added = queue_func.queue_enqueue(add_username, add_username, add_name)

        if user_added:
            update.effective_chat.send_message(
                text=f"@{add_username} добавлен в очередь!",
                reply_to_message_id=message_id,
            )
        else:
            update.effective_chat.send_message(
                text=f"@{username} уже добавлен в очередь...",
                reply_to_message_id=message_id,
            )

    elif admin_func.is_admin(user_id):
        add_username = "ERROR"
        update.effective_chat.send_message(
            text=f"Неправильное использование команды!",
            reply_to_message_id=message_id,
        )

    elif not admin_func.check_status():
        add_username = "ERROR"
        update.effective_chat.send_message(
            text=f"Очередь закрыта для добавления!",
            reply_to_message_id=message_id,
        )

    else:
        add_username = "ERROR"
        update.effective_chat.send_message(
            text=f"Ты не админ, чтобы записывать других в очередь))",
            reply_to_message_id=message_id,
        )

    logger.info("User %s was enqueued.", add_username)


def show_queue(update: Update, context: CallbackContext) -> None:
    """Displays the queue."""
    username = update.effective_user.username
    update.effective_chat.send_message(
        text=queue_func.queue_show()
    )

    logger.info("The queue was shown by %s request.", username)


def form_queue(update: Update, context: CallbackContext) -> None:
    """Forms the static queue."""
    message_id = update.message.message_id
    user_id = update.effective_user.id

    if admin_func.is_admin(user_id):
        queue_func.queue_form()
        update.effective_chat.send_message(
            text="Временная очередь перемешана. Очереди объединены.",
            reply_to_message_id=message_id,
        )
    else:
        update.effective_chat.send_message(
            text="Хорошая попытка, но ты не админ :)",
            reply_to_message_id=message_id,
        )

    logger.info("The queue was formed.")


def dequeue(update: Update, context: CallbackContext) -> None:
    """Deletes the user from the queue."""
    message_id = update.message.message_id
    user_id = update.effective_user.id
    username = update.effective_user.username

    if context.args and admin_func.is_admin(user_id):
        delete_username = str(context.args[0]).replace("@", "")
        user_deleted = queue_func.queue_dequeue(delete_username)
        if user_deleted:
            update.effective_chat.send_message(
                text=f"{delete_username} был удален из очереди.",
                reply_to_message_id=message_id,
            )
        else:
            update.effective_chat.send_message(
                text=f"{delete_username} и так не было в очереди..."
            )

    elif context.args:
        delete_username = "ERROR"
        update.effective_chat.send_message(
            text="Ты не админ))\n\nИспользуй /deq без дополнительного"
                 " аргумента, если хочешь удалить самого себя из очереди",
            reply_to_message_id=message_id,
        )

    else:
        if username is None:
            delete_username = user_id
        else:
            delete_username = username
        user_deleted = queue_func.queue_dequeue(delete_username)
        if user_deleted:
            update.effective_chat.send_message(
                text="Ты был удален из очереди!",
                reply_to_message_id=message_id,
            )
        else:
            update.effective_chat.send_message(
                text="Ты и так не в очереди...",
                reply_to_message_id=message_id,
            )

    logger.info("User %s was dequeued by %s.", delete_username, user_id)


def next_student(update: Update, context: CallbackContext) -> None:
    """Moves to the next student in the queue."""
    username = update.effective_user.username
    user_id = update.effective_user.id

    if admin_func.is_admin(user_id) or queue_func.is_next(username, user_id):
        student = queue_func.next_student()

        if student:
            update.effective_chat.send_message(
                text=f"Очередь сдвинулась. Следующий: @{student}"
            )
            update.effective_chat.send_message(
                text=queue_func.queue_show()
            )
        else:
            update.effective_chat.send_message(
                text="Очередь пуста!"
            )
    else:
        update.effective_chat.send_message(
            text="Ты не админ! Очередь двигать могут только админы и модераторы."
        )

    logger.info("The queue was moved to the next student by %s.", user_id)


def commands(update: Update, context: CallbackContext) -> None:
    update.effective_chat.send_message(
        text="Бот поддерживает следующие команды:\n\n"
             "/help - справка\n"
             "/queue - показ очереди\n"
             "/add [name] - добавление себя в очередь\n"
             "/delete - удаление себя из очереди\n"
             "/next - перемещение к следующему в очереди\n"
             "/commands - список команд\n\n\n"
             "Команды для админов:\n\n"
             "/add @{username} {name} - добавление в очередь\n"
             "/delete @{username} - удаление из очереди\n"
             "/addpos @{username} {position} {name} - добавление в очередь на позицию\n"
             "/form - формирование статичной очереди\n"
             "/open - открытие очереди на добавление\n"
             "/close - закрытие очереди на добавление"
    )


def bot_help(update: Update, context: CallbackContext):
    update.effective_chat.send_message(
        text="Этот бот умеет создавать очереди и позволяет назначенным админам"
             " ими управлять. По любым вопросам обращайтесь к @darl33t.\n\n"
             "Список команд: /commands\n\n"
             "Версия: Edgerunner 1.1.2"
    )


def openq(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    message_id = update.effective_message.message_id
    if admin_func.is_admin(user_id):
        admin_func.openq()
        update.effective_chat.send_message(
            text=f"Очередь открыта.",
            reply_to_message_id=message_id,
        )


def closeq(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    message_id = update.effective_message.message_id
    if admin_func.is_admin(user_id):
        admin_func.closeq()
        update.effective_chat.send_message(
            text=f"Очередь закрыта.",
            reply_to_message_id=message_id,
        )


def main() -> None:
    """Start the bot."""
    f = open("bot_token.txt", "r")
    token = f.readline().strip()
    f.close()

    # Create the updater
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("help", bot_help))
    dispatcher.add_handler(CommandHandler("commands", commands))
    dispatcher.add_handler(CommandHandler("add", enque))
    dispatcher.add_handler(CommandHandler("addpos", enque_position))
    dispatcher.add_handler(CommandHandler("queue", show_queue))
    dispatcher.add_handler(CommandHandler("open", openq))
    dispatcher.add_handler(CommandHandler("close", closeq))
    dispatcher.add_handler(CommandHandler("next", next_student))
    dispatcher.add_handler(CommandHandler("form", form_queue))
    dispatcher.add_handler(CommandHandler("delete", dequeue))

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()


if __name__ == "__main__":
    main()
