from aiogram import Router, types, F
from aiogram.filters import Command
from app.keyboards import options_inline_kb
from app.db import (
    get_quiz_index, get_correct_count, set_quiz_state, reset_quiz_state,
    save_result
)
from app.services.quiz_loader import load_questions

quiz_router = Router()
QUESTIONS = load_questions()  # грузим один раз
TOTAL = len(QUESTIONS)

# --- запуск квиза ---
@quiz_router.message(F.text == "Начать игру")
@quiz_router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    user_id = message.from_user.id
    await reset_quiz_state(user_id)
    await message.answer("Давайте начнём квиз!")
    await send_question(message.chat.id, user_id, message.bot)

async def send_question(chat_id: int, user_id: int, bot):
    idx = await get_quiz_index(user_id)
    if idx >= TOTAL:
        await finish_quiz(chat_id, user_id, bot)
        return
    q = QUESTIONS[idx]
    kb = options_inline_kb(q["options"])
    await bot.send_message(chat_id, f"Вопрос {idx+1}/{TOTAL}:\n{q['question']}", reply_markup=kb)

# --- обработка ответа ---
@quiz_router.callback_query(F.data.startswith("answer:"))
async def on_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    msg = callback.message

    # Снимаем кнопки
    try:
        await callback.bot.edit_message_reply_markup(chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=None)
    except Exception:
        pass

    # Достаём индекс вопроса и выбранный вариант
    idx = await get_quiz_index(user_id)
    if idx >= TOTAL:
        await callback.answer()  # на всякий
        return
    q = QUESTIONS[idx]

    chosen_idx = int(callback.data.split(":")[1])
    chosen_text = q["options"][chosen_idx]
    correct_idx = q["correct_option"]
    correct_text = q["options"][correct_idx]

    # Показываем текст ответа пользователя (кнопки уже сняты)
    await callback.message.answer(f"Ваш ответ: {chosen_text}")

    # Обновляем счёт и продвигаем индекс
    correct_count = await get_correct_count(user_id)
    if chosen_idx == correct_idx:
        correct_count += 1
        await callback.message.answer("Верно!")
    else:
        await callback.message.answer(f"Неверно. Правильный ответ: {correct_text}")

    idx += 1
    await set_quiz_state(user_id, idx, correct_count)

    # Следующий вопрос или финиш
    if idx < TOTAL:
        await send_question(msg.chat.id, user_id, callback.bot)
    else:
        await finish_quiz(msg.chat.id, user_id, callback.bot)

    await callback.answer()

async def finish_quiz(chat_id: int, user_id: int, bot):
    # забираем финальный счёт
    idx = await get_quiz_index(user_id)
    correct = await get_correct_count(user_id)
    await save_result(user_id, correct, TOTAL)
    await bot.send_message(chat_id, f"🏁 Квиз завершён! Результат: {correct}/{TOTAL}\nПосмотреть статистику: /stats")
