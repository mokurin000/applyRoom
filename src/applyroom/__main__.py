import re
import os
import asyncio
from asyncio import sleep
from datetime import datetime, timedelta, time

import pytz
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()

PERSISTENT = os.environ["APPLY_ROOM_PERSISTENT"]

# days from current day
DIFF_DAY: int = 2
assert DIFF_DAY in [1, 2], "DIFF_DAY must be 1 or 2!"

BASE_URL = "https://aaof.berklee.edu/rooms/wtdpractice.php"
COOKIES = [
    {
        "name": "persistent",
        "value": PERSISTENT,
        "httpOnly": True,
        "secure": True,
        "sameSite": "None",
        "domain": "berklee.onelogin.com",
        "path": "/",
    },
]


def get_time():
    ny_tz = pytz.timezone("America/New_York")
    ny_time = datetime.now(ny_tz)

    start_time = datetime.combine(
        date=ny_time.date(), time=time.fromisoformat("19:00:00"), tzinfo=ny_tz
    )
    diff = (start_time - ny_time).total_seconds()

    target_day = (ny_time + timedelta(days=DIFF_DAY)).strftime("%Y-%m-%d")

    return diff, target_day


async def wait_for_target_time():
    diff, target_day = get_time()
    target_url = f"{BASE_URL}?day={target_day}&p=MPE"
    print("Target URL:", target_url)

    if DIFF_DAY == 2:
        if diff > 0:
            print(f"Will wait {diff} seconds...")
            await sleep(diff)
        else:
            print("You're too late! hurry up!")

    return target_url


def prompt_user_input():
    room = input("> target room: ").strip()
    r = re.compile(r"\d{1,2}[ap]m")
    time_range = input('> time range ("2am 6am" e.g.): ').strip()
    time_range = r.findall(time_range)
    start, end = time_range

    print()
    print(f"Room: {room}")
    print(f"Time Range: {start}~{end}")
    print()

    print("Please ensure Room and Time Range are correct!")
    confirm = input("> (y/n) ")
    if not confirm.lower().startswith("y"):
        print("Cancelled.")
        exit(1)

    return room, start, end


async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=False,
        )
        ctx = await browser.new_context(no_viewport=True)
        await ctx.add_cookies(COOKIES)
        page = await ctx.new_page()
        await page.goto(BASE_URL)

        room, start, end = prompt_user_input()
        target_slot = f"{room}, {start} - {end}"

        target_url = await wait_for_target_time()

        await ctx.tracing.start(screenshots=True, snapshots=True)
        await page.goto(target_url)

        slot_selector = f"td.bookslot[data-roomtime='{target_slot}']"

        frame = page.frame_locator("#scheduleframe")
        slot_loc = frame.locator(slot_selector)
        submit_loc = page.locator("input#submitbtn")

        try:
            await slot_loc.wait_for(state="attached")
            await slot_loc.click()
            await submit_loc.wait_for(state="visible")
            await submit_loc.click()
        finally:
            await ctx.tracing.stop(path="trace.zip")
            await ctx.close()
            await browser.close()

            sleep_time = 1000
            print(f"Operation finished! will exit after {sleep_time}s...")
            await sleep(1000)


if __name__ == "__main__":
    asyncio.run(main())
