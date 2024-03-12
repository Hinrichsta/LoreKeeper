from Website.builder import create_site
from Discord.builder import create_bot

from dotenv import load_dotenv
import os

site = create_site()

if __name__ == '__main__':
    site.run(debug=True,ssl_context='adhoc')