from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model.config import Config
import json
from flask import Flask, request
from flask_cors import CORS
import os
import logging
import datetime
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


# For dev logging - comment out for Gunicorn
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)

# ~ Databases ~ #
db = SQLAlchemy()  # <-Initialize database object
migrate = Migrate()  # <-Initialize migration object


def create_app():
    """Construct core application"""
    app = Flask(__name__)

    # For Gunicorn logging
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # app.logger.handlers = gunicorn_logger.handlers
    # app.logger.setLevel(gunicorn_logger.level)

    ###
    # NOTE: to print in Flask, do `app.logger.info(var_to_print)`
    ###

    # Pull from config file
    app.config.from_object(Config)
    db.init_app(app)  # <- This will get called in our models.py file
    migrate.init_app(app, db)  # <- Migration directory

    CORS(app, resources={r"/*": {"origins": "*"}})

    from model import models  # noqa
    from model.models import User, UserModelSession  # noqa

    # @app.route('/')
    # def home():
    #     return "ok"

    @app.route("/api/login", methods=["POST"])
    def login():
        user_info = json.loads(request.data)["user_info"]
        username = user_info["username"]
        password = user_info["password"]
        usernames = ["user" + str(i) for i in range(1, 31)]
        passwords = [
            "ph6n76gec9",
            "l98zjxj6vc",
            "mq577o05wz",
            "tcty170i9o",
            "1kgh4895fx",
            "ys175n9iv0",
            "0fvcfgxplj",
            "vu34rphc82",
            "hyhnyg9xob",
            "oqqct6wllc",
            "oswly1eaxq",
            "qe7inpmska",
            "7ilhsc46ox",
            "wo81yy0eci",
            "2kufnda8bs",
            "nzlljrerzt",
            "ft0jinctnm",
            "r3swsmr2rn",
            "4cbp35phhh",
            "falyezzw4r",
            "r5v0mrvpuv",
            "auee014rmj",
            "wpprodq8vb",
            "6nddssd3gg",
            "z2394iw3mq",
            "a3gkc6czb5",
            "ddxzlpkzhv",
            "2owdt20zas",
            "29uhzahhol",
            "mfhs4cyc4x",
        ]
        for i in range(len(usernames)):
            try:
                # Creates new accounts
                new_user = User(username=usernames[i], password=passwords[i])
                db.session.add(new_user)
                db.session.commit()

            except:  # noqa
                db.session.rollback()

        try:
            guest_user = User(username="guest", password="guest")
            db.session.add(guest_user)
            db.session.commit()
        except:  # noqa
            db.session.rollback()

        user = User.query.filter_by(username=username).first()
        if user is None:
            return {"validID": False, "userID": None}

        if password == user.password:
            opening_decision = decision_maker.QUESTIONS["ask_location"]
            model_prompt = opening_decision["model_prompt"]

            choices = opening_decision["choices"]

            # Creates current session; FE will need to pass in session id
            # with Session() as db_session:
            new_session = UserModelSession(user_id=user.id)
            db.session.add(new_session)
            db.session.commit()

            decision_maker.initialise_remaining_choices(user.id)
            decision_maker.initialise_prev_questions(user.id)
            decision_maker.clear_suggestions(user.id)
            decision_maker.clear_choices(user.id)
            decision_maker.clear_datasets(user.id)
            decision_maker.user_choices[user.id]["current_session_id"] = new_session.id

            return {
                "validID": True,
                "userID": user.id,
                "sessionID": new_session.id,
                "model_prompt": model_prompt,
                "choices": list(choices.keys()),
            }
        return {"validID": False, "userID": None}

    @app.route("/api/update_session", methods=["POST"])
    def update_session():
        user_info = json.loads(request.data)["choice_info"]
        user_id = user_info["user_id"]
        session_id = user_info["session_id"]
        input_type = user_info["input_type"]
        user_choice = user_info["user_choice"]

        if type(input_type) == list and len(input_type) == 0:
            input_type = "any"
        elif type(input_type) == list and len(input_type) == 1:
            input_type = input_type[0]

        user = User.query.filter_by(id=user_id).first()
        user_session = UserModelSession.query.filter_by(id=session_id).first()

        decision_maker.save_current_choice(
            user_id, input_type, user_choice, user_session, db.session, app
        )
        # return {"choice": choice.choice_desc}
        output = decision_maker.determine_next_choice(
            user_id, input_type, user_choice, db.session, user_session, app
        )
        # Update last accessed
        user.last_accessed = datetime.datetime.utcnow()
        db.session.commit()

        return {
            "chatbot_response": output["model_prompt"],
            "user_options": output["choices"],
        }

    return app


from model.rule_based_model import ModelDecisionMaker  # noqa

decision_maker = ModelDecisionMaker()

if __name__ == "__main__":
    app = create_app()
