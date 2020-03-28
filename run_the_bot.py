import os
from test_medic_bot import MedicBot
from new_bot import NewMedicBot
from bot_no_three import ThirdMedicBot
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    # medic_bot = MedicBot(access_token=os.getenv("BOT_TOKEN"))
    # medic_bot = NewMedicBot(access_token=os.getenv("BOT_TOKEN"))
    medic_bot = ThirdMedicBot(access_token=os.getenv("BOT_TOKEN"))
    medic_bot.run_bot()
