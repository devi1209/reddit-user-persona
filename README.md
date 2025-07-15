   git clone https://github.com/your_username/reddit-user-persona.git
   cd reddit-user-persona
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python reddit_user_persona.py
