from src.db.models import Accounts


async def get_accounts() -> str:
    accounts = await Accounts.all()
    if not accounts:
        return "No accounts"
    column_width = 20  # You can adjust this to suit your needs

    output = "\n".join(
        [
            "Statistic:\n",
            f"{'phone':_<{column_width}}{'is_working':_^{column_width}}{'reacted':_^{column_width}}\n\n",
        ]
        + [
            f"{account.phone:_<{column_width}}{account.is_working:_^{column_width}}{account.reacted:_^{column_width}}"
            for account in accounts
        ]
    )

    return output


async def add_account(phone: str, pwd: str, session_string: str) -> None:
    await Accounts.create(phone=phone, pwd=pwd, session_string=session_string)
