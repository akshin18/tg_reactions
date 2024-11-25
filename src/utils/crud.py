from typing import Optional

from src.db.models import Accounts, Channels


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


async def get_channels() -> str:
    channels = await Channels.all()
    if not channels:
        return "No channels"
    column_width = 20  # You can adjust this to suit your needs

    output = "\n".join(
        [
            f"{channel.channel_id:_<{column_width}}{channel.channel_link}"
            for channel in channels
        ]
    )

    return output


async def add_account(phone: str, pwd: Optional[str], session_string: str) -> None:
    await Accounts.create(phone=phone, pwd=pwd, session_string=session_string)


async def delete_account(phone: str) -> bool:
    return bool(await Accounts.filter(phone=phone).delete())


async def add_channel(channel_id: str, channel_link: str) -> None:
    await Channels.create(channel_id=channel_id, channel_link=channel_link)


async def delete_channel(channel_id: str) -> bool:
    return bool(await Channels.filter(channel_id=channel_id).delete())
