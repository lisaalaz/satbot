from collections import deque

from model.models import UserModelRun, UserModelSession, Choice, Protocol
from model.classifiers import get_classification, get_sentence_score
from model.countries import CountryFinder

import datetime
import numpy as np
import pandas as pd
import random
import re
import time


class ModelDecisionMaker:
    def __init__(self):

        self.data = pd.read_csv('/Users/lisaxy/satbot2.0/model/empatheticPersonas12_responses_only_with_scores.csv', encoding='ISO-8859-1') #change path

        # Titles from workshops (Title 7 adapted to give more information)
        self.EXERCISE_TITLES = [
            "0: None",
            "1: Recalling childhood memories",
            "2: Embracing and comforting the Child",
            "3: Singing a song of affection",
            "4: Expressing love and care for the Child",
            "5: Pledging to support and care for the Child",
            "6: Restoring our emotional world",
            "7: Maintaining a loving relationship with the Child and creating zest for life", 
            "8: Enjoying nature", #it says "on one day this week. should it change? Also says "achieving this will help you want to spend more time in nature after this course ends"
            "9: Overcoming current negative emotions", 
            "10: Overcoming past pain", 
            "11: Muscle relaxation and playful face for intentional laughing", #this says early in the morning. should it change?
            "12: Victory laughter on our own", #"immediately after"...can this be changed
            "13: Laughing with our childhood self",  
            "14: Intentional laughter", 
            "15: Learning to change your perspective", 
            "16: Learning to be playful about your past pains", 
            "17: Identifying patterns of acting out personal resentments", 
            "18: Planning more constructive actions", 
            "19: Updating our rigid beliefs to enhance creativity", #this says new topic every dat. should it change?
            "20: Practicing Affirmations", #are the inspirational affirmations already chosen during the course or can they be chosen/rechosen?
            "21: Recognizing and containing the internal persecutor", 
            "22: Solving personal crises",
            "23: Discovering your true, free, and sovereign self in this age of emergency", 
        ]
        #checked 7, 8, 9, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 

        self.TITLE_TO_EXERCISE = {
            self.EXERCISE_TITLES[i]: i for i in range(len(self.EXERCISE_TITLES))
        }

        self.EXERCISE_TEXTS = [
            ["None"],
            ["In a quiet place, look at your happy and unhappy photos. Recall positive and negative childhood memories and early relationships in the family."],
            [
                "2a:",
                  "(i) With your eyes closed, first imagine your happy photo/avatar, imagining that the child is near you.",
                  "(ii) now imagine you are embracing the child.",
                  "(iii) now imagine you are playing with the child, e.g. a game that you played as a child.",
                  "(iv) now imagine you are dancing with the child.",
                  "Reflect on how you feel in each phase from (i) to (iv).",
                "2b:",
                  "(i) With your eyes closed, imagine your unhappy photo/avatar, imagining the child is near you.",
                  "(ii) now imagine you are embracing and consoling the child.",
                  "(iii) Open your eyes, put on the Google Cardboard or and:",
                    "(a) Set a negative emotion (sad, angry, fearful or disgusted) on your avatar.",
                    "(b) Then click on Auto Emotion ” and by staring at your child avatar imagine you are reassuring and comforting your child which makes the child happy and eventually dance.",
                  "Reflect on how you feel in each phase from (i) to (iii).",
            ],
            ["Print copies of happy photo to display at home, work, and in your wallet. Consider setting its digital image as the background on your phone and laptop, etc. Select a jolly lyrical song you cherish that invokes feelings of warmth, affection, love. Learn the song by heart and sing it as often as you can in your daily routine. While looking at the happy photo/avatar, sing the song, as a way to establish a deep emotional bond with the child in your mind. Start quietly; then, over time, allow your voice to become louder while using more of your body (e.g. shaking your shoulders, hands, and lifting your eyebrows up and down). Imagine that in this way, like a parent, you are have a loving, passionate dialogue and are joyfully dancing and playing with the child."],
            ["While genuinely smiling at the happy photo/avatar, loudly say to your child: 'I passionately love you and deeply care for you'."],
            ["In this exercise, we start to care for the child as our own child. We attribute and project our own emotions to the child. We, as our adult self, begin with a pledge we make at an especial time and place. After reading the pledge silently, we confidently pledge out loud the following: 'From now on, I will seek to act as a devoted and loving parent to this child, consistently and wholeheartedly care for them in every way possible. I will do everything I can to support the health and emotional growth of this child'."],
            ["Through imagination or by drawing, consider your emotional world as a home with some derelict parts that you will fully renovate. The new home is intended to provide a safe haven at times of distress for the child and a safe base for the child to tackle life's challenges. The new home and its garden is bright and sunny; we imagine carrying out these self attachment exercises in this environment. The unrestored basement of the new house is the remnant of the derelict house and contains our negative emotions. When suffering negative emotions, imagine that the child is trapped in the basement but can gradually learn to open the door of the basement, walk out and enter the bright rooms, reuniting with the adult."],
            [
                "7a: Choose some short phrase, e.g., 'You are my beautiful child' or 'My love'. Say it slowly, out loud at least five times as you look at the happy photo/avatar. Then sing your favourite chosen love song at least five times. As previously, increase your volume and begin to use your whole body.",
                "7b: While looking in a mirror, imagine your image to be that of the Child (i.e., your emotional self), then begin to loudly sing your previously chosen song. As previously, increase your volume and begin to use your whole body. (If you find it difficult to imagine the Child in the mirror, put the 'Happy' photo of your Child in front of the mirror and do the exercise while looking at your Happy childhood photo in the mirror). Do this twice now and then as many times as possible in different circumstances during the day, such as while on the way to work or while cooking dinner, to integrate them into your new life. When singing your favourite song becomes a habit of yours, it becomes an effective tool for enhancing positive affects and managing emotions.",
            ],
            ["Creating an attachment to nature for your Child is an effective way to increase joy and reduce negative emotions. On one day this week, go to a local park, wood or forest. Spend at least 5 minutes admiring a tree, attempting to appreciate its real beauty as you have never previously experienced. Repeat this process, including with other aspects of nature (e.g. sky, stars, plants, birds, rivers, sea, your favourite animal), until you feel you have developed an attachment to nature that helps regulate your emotions. Achieving this will help you want to spend more time in nature after this course ends."],
            [
                "With closed eyes, imagine the unhappy photo/avatar and project your negative emotions to the unhappy photo/avatar representing the Child.",
                "While doing this:",
                "(i) loudly reassure the Child.",
                "(ii) give your face/neck/head a self massage.",
                "Repeat these steps until you are calmed and comforted.",
            ],
            [
                "With closed eyes, recall a painful childhood episode, such as emotional or physical abuse or loss of a significant figure, with all the details your still remember. Associate the face of the Child you were in the past with the selected unhappy photo/avatar. As you remember the associated emotions, e.g., helplessness, humiliation and rage, with closed eyes, imagine your Adult intervening in the scene like a good parent. ",
                "Imagine your Adult:",
                   "(i) approaching your Child quickly like any good parent with their child in distress.",
                   "(ii) loudly reassuring the Child that you have now come to save them, by standing up with a loud voice to any perpetrator, for example: 'Why are you hitting my Child?', and by supporting the Child with a loud voice, for example: 'My darling, I will not let them hurt you anymore'.",
                   "(iii) imaginatively cuddling your Child, by giving yourself a face/neck/head self-massage.",
                "Repeat (i), (ii), (iii) until comforted and soothed, acquiring mastery over the trauma.",
            ],
            ["Early in the morning, act like a child: loosen up facial and body muscles, open up your mouth and sing your favourite song while laughing (or at least smiling) on your own."],
            ["Immediately after accomplishing something, e.g. doing household chores, having a conversation with a neighbour, or reading an article, smile at the thought of this as an achievement, then once you are comfortable, begin to laugh for at least ten seconds."],
            ["Looking at your happy photo/avatar, smile and then begin to laugh for at least ten seconds. Repeat this process at least three times."],
            ["At a time when you are alone, open your mouth slightly, loosen your face muscles, raise your eyebrows, then slowly and continuously repeat one of the following tones, each of which uses a minimum amount of energy: 'eh, eh, eh, eh'; or 'ah, ah, ah, ah'; or 'oh, oh, oh, oh'; or 'uh, uh, uh, uh'; or 'ye, ye, ye, ye'. If you need a subject to laugh at, you can laugh at the silliness of the exercise! Once this continuous intentional laughter becomes a habit, you would be able to shape it according to your personality and style to create your own brand of laughter."],
            ["Stare at the black vase. Laugh or at least smile for one minute the moment your perception changes and you see two white faces, conceived as Adult and Child, looking at each other (IT, ST, PT). Stare at the two white faces and laugh or at least smile for one minute the moment your perception changes and you see the black vase (IT, ST)."],
            ["Visualize a painful event that took place in the past (it can be a recent event that you have struggled with, or a painful event that took place in your childhood and you have endured for a long time), and despite its painfulness, try to see a positive impact it has had for you. Use any of the theories for humour to try to laugh or at least smile at the event."],
            ["Try to identify any pattern of narcissistic and anti social feelings that your Child has acted out in your current or past relationships or any long term resentment borne against someone. Try to recognize how much of your time and energy is consumed in such acting out and bearing resentment."],
            [
                "Work out a new way to handle, in the future, what you have identified as acting out antisocial feelings or bearing personal resentment in your life.",
                "1. Without denying these feelings, try to reflect and contain them and avoid acting them out. Try to let go of the personal resentment. This may be hard and challenging but it is necessary for emotional growth. Here, you are taking a critical but constructive stance towards your Child and are exercising foresighted compassion.",
                "2. Find a positive way of re-channeling the aggressive energy invoked by these feelings into productive work (e.g., going for some exercise, talking to a friend, etc.) and ultimately into creative work towards your noble goal in life.",
            ],
            ["Challenge your usual ideological framework to weaken any one sided belief patterns and encourage spontaneity and examination of any issue from multiple perspectives. Practice this with subjects or themes that you have deep rooted beliefs about and you are also interested in. This may include any social, political, or ethical issue, such as marriage, sexual orientation or racism. For example, whatever your political viewpoint on a specific subject is, consider the subject both from a liberal and conservative or from a left wing and right wing point of view and try to understand both sides of the issue and challenge your dominant ideological framework. This does not mean that you would change your viewpoint but it allows you to see the subject from different perspectives and to be able to put yourself in other people's shoes. Consider a different question or issue daily for at least 5 minutes."],
            ["Put together a list of inspirational affirmations by figures you admire. Choose the three that inspire you most. Read them out and repeat slowly for at least three minutes."],
            [
                "The Adult becomes aware of the facets of the trauma triangle: internal persecutor, victim, and rescuer.",
                "The Adult examines the effects of this triangle (narcissism and lack of creativity) in daily life and previous experiences.",
                "The Adult reviews their important life experiences and their social and political points of view as an adult, with awareness how the internal persecutor operates.",
                "The Adult creates a list of examples from their own experiences for the four different ways the internal persecutor operates.",
                "The Adult carefully analyzes their life experiences for examples of being drawn to trauma, being traumatized by the internal persecutor, and projecting the internal persecutor onto others.",
                "Based on the above, the Adult re evaluates their experiences, contains the internal persecutor, victim mentality and blame games, allowing the development of creativity.",
            ],
            [
                "After the Child's arousal level is reduced and as we continue to practice the exercise for modulating negative affects, and the exercises for laughter, we ask our child the following:",
                "- How can you see the crisis as a way of becoming stronger? (hah hah hah).",
                "- How can you interpret the crisis as a way of reaching your noble goal? (hah hah hah).",
                "- Has the internal persecutor been projecting onto others again?",
                "The Adult asks the following questions:",
                "- What is the similarity between this crisis and ones I have faced before?",
                "- How is it similar to the family crisis I experienced as a child?",
                "- Aren't the other person's positive attributes greater than their negative ones?",
                "- How would a mature person interpret the crisis in comparison to my Child?",
                "- Can I see it from the perspective of the other?",
                "- Can I put myself in their place and understand their affects?",
                "- Given my new insights can I find a way to calm the people involved in the crisis so we can find a better solution for it?",
                "- If I cannot, can I just respectfully maintain my distance and end the argument/conflict?",
            ],
            [
                "Our Adult asks our Child if it makes any sense to be subservient to the super profit making system which has brought us to the present abyss.",
                "Do I really need all these desired products, objects and services following the myriad of messages and peer/societal pressures on me?",
                "Does it make sense to crave for a materialistic/hedonistic and selfish lifestyle when life is under the impending threat of destruction?",
                "Do we want to continue to play this zero sum materialistic game or do we want to follow our noble goals in tackling our existential problems?",
                "Can we save the living planet other than by working towards a new global social contract based on universal compassion in which human aggression can be sublimated to creativity for the common good?",
            ],
        ]

        self.EXERCISE_RANKINGS = {
            0: self.EXERCISE_TITLES[9], #overcoming negative emotion
            1: self.EXERCISE_TITLES[10], #overcoming past pain
            2: self.EXERCISE_TITLES[7], #sing a song
            3: self.EXERCISE_TITLES[16], #learning to be playful about your past pain
            4: self.EXERCISE_TITLES[15], #learning to change your perspective
            5: self.EXERCISE_TITLES[17], #identifying patterns of acting out personal resentments
            6: self.EXERCISE_TITLES[18], #planning more constructive actions

            # The rest should just be recommended in numerical order.
        }
        
        self.exercises = [i for i in range(1, 24)]

        # Goes from user id to actual value
        self.current_run_ids = {}
        self.current_exercise_ids = {}
        self.done_exercises = {}

        # Keys: user ids, values: dictionaries describing each choice (in list)
        # and current choice
        self.user_choices = {}

        # Keys: user ids, values: scores for each question
        #self.user_scores = {}

        # Keys: user ids, values: current suggested exercises
        self.suggestions = {}

        # Tracks current emotion of each user after they classify it
        self.user_emotions = {}

        self.guess_emotion_predictions = {}
        # Structure of dictionary: {question: {
        #                           model_prompt: str or list[str],
        #                           choices: {maps user response to next exercise},
        #                           exercises: {maps user response to exercises to suggest},
        #                           }, ...
        #                           }
        # This could be adapted to be part of a JSON file (would need to address
        # mapping callable functions over for parsing).
        
        self.guess_location_predictions = {}
        self.users_location = {}

        self.remaining_choices = {}
        self.recent_questions = {}
        self.datasets = {}

        self.country_finder = CountryFinder()

        self.negative_emotions = ["Sad", "Anxious", "Insecure", "Disgusted", "Disappointed", "Ashamed", "Guilty"]
        self.antisocial_emotions = ["Angry", "Envious", "Jealous"]
        self.positive_emotions = ["Happy", "Loving"]

        self.emotions_map = {
           "Sad": "Sad",
           "Anxious": "Anxious/Scared",
           "Happy": "Happy/Content",
           "Angry": "Angry",
           "Loving": "Loving/Caring",
           "Insecure": "Insecure/Have a sense of instability",
           "Disgusted": "Disgusted",
           "Disappointed": "Disappointed",
           "Ashamed": "Ashamed/Embarrassed",
           "Guilty": "Guilty",
           "Envious": "Envious",
           "Jealous": "Jealous"
        }

        self.QUESTIONS = {
            "ask_location": {
               "model_prompt": "Please enter the country where you are currently located:",
               "choices": {
                   "open_text": lambda user_id, db_session, curr_session, app: self.save_location(user_id, db_session, curr_session, app, again=False)
               },
               "exercises": {"open_text": []},
           },
           "check_location": {
               "model_prompt": lambda user_id, db_session, curr_session, app: self.check_location_prompt(user_id),
               "choices": {
                   "yes": "opening_prompt",
                   "no": "ask_again_location",
               },
               "exercises": {"yes": [], "no": []},
           },
           "ask_again_location": {
               "model_prompt": lambda user_id, db_session, curr_session, app: self.ask_location_prompt(user_id),
               "choices": {
                   "open_text": lambda user_id, db_session, curr_session, app: self.save_location(user_id, db_session, curr_session, app, again=True)
               },
               "exercises": {"open_text": []},
           },
            "opening_prompt": {
                "model_prompt":
                lambda user_id, db_session, curr_session, app: self.
                get_opening_prompt(user_id),

                "choices": {
                    "open_text": lambda user_id, db_session, curr_session, app: self.determine_next_prompt_opening(user_id, app, db_session, restart=False)
                },
                "exercises": {"open_text": []},
            },
            "show_help_options": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_help_options(
                    user_id, app, db_session,
                ),
                "choices": {
                    "continue": "guess_emotion",
                },
                "exercises": {
                    "continue": [],
                    },
            },
            "guess_emotion": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(
                    user_id, app, db_session, "All emotions - From what you have said I believe you are feeling {}. Is this correct?", has_emo=False,
                ),
                "choices": {
                    "yes": {
                        "Sad": "after_classification_negative",
                        "Angry": "after_classification_negative",
                        "Anxious/Scared": "after_classification_negative",
                        "Happy/Content": "after_classification_positive",
                        "Loving/Caring": "after_classification_positive",
                        "Insecure": "after_classification_negative",
                        "Disgusted": "after_classification_negative",
                        "Disappointed": "after_classification_negative",
                        "Ashamed": "after_classification_negative",
                        "Guilty": "after_classification_negative",
                        "Envious": "after_classification_antisocial",
                        "Jealous": "after_classification_antisocial",
                    },
                    "no": "check_emotion",
                },
                "exercises": {
                    "yes": [],
                    "no": []
                    },
            },
            "check_emotion": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(
                    user_id, app, db_session, "All emotions - I am sorry. Please select from the emotions below the one that best reflects what you are feeling:", has_emo=False,
                ),
                "choices": {
                    "Sad":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Sad"),
                    "Angry":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Angry"),
                    "Anxious/Scared":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Anxious"),
                    "Happy/Content":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Happy"),
                    "Loving/Caring":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Loving"),
                    "Insecure/Have a sense of instability":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Insecure"),
                    "Disgusted":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Disgusted"),
                    "Disappointed":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Disappointed"),
                    "Ashamed/Embarrassed":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Ashamed"),
                    "Guilty":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Guilty"),
                    "Envious":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Envious"),
                    "Jealous":
                    lambda user_id, db_session, curr_session, app: self.
                    save_emotion(user_id, "Jealous"),
                },
                "exercises": {
                    "Sad": [],
                    "Angry": [],
                    "Anxious/Scared" : [],
                    "Happy/Content": [],
                    "Loving/Caring": [],
                    "Insecure": [],
                    "Disgusted": [],
                    "Disappointed": [],
                    "Ashamed": [],
                    "Guilty": [],
                    "Envious": [],
                    "Jealous": [],
                },
            },
            ############# NEGATIVE EMOTIONS (SAD, ANXIOUS, INSECURE, DISGUSTED, DISAPPOINTED, ASHAMED, GUILTY) #############
            "after_classification_negative": {
                "model_prompt":
                lambda user_id, db_session, curr_session, app: self.
                get_model_prompt(user_id, app, db_session, " - Was this caused by a specific event/s?", has_emo=True),
                "choices": {
                    "Yes, something happened": "event_is_recent",
                    "No, it's just a general feeling": "more_questions",
                },
                "exercises": {
                    "Yes, something happened": [self.EXERCISE_TITLES[7], self.EXERCISE_TITLES[16], self.EXERCISE_TITLES[15]],
                    "No, it's just a general feeling": [self.EXERCISE_TITLES[7], self.EXERCISE_TITLES[16], self.EXERCISE_TITLES[15], self.EXERCISE_TITLES[9]]
                },
            },
            ############# ANTISOCIAL EMOTIONS (ANGRY, ENVIOUS, JEALOUS) #############
            "after_classification_antisocial": {
                "model_prompt":
                lambda user_id, db_session, curr_session, app: self.
                get_model_prompt(user_id, app, db_session, " - Was this caused by a specific event/s?", has_emo=True),
                "choices": {
                    "Yes, something happened": "event_is_recent",
                    "No, it's just a general feeling": "more_questions",
                },
                "exercises": {
                    "Yes, something happened": [self.EXERCISE_TITLES[17], self.EXERCISE_TITLES[18]],
                    "No, it's just a general feeling": [self.EXERCISE_TITLES[17], self.EXERCISE_TITLES[18]]
                },
            },
            #########################################################################
            "event_is_recent": {
                "model_prompt":
                lambda user_id, db_session, curr_session, app: self.
                get_model_prompt(user_id, app, db_session, " - Was this caused by a recent or distant event (or events)?", has_emo=True),
                "choices": {
                    "It was recent": "more_questions",
                    "It was distant": "revisiting_distant_events",
                },
                "exercises": {
                    "It was recent": [self.EXERCISE_TITLES[9]],
                    "It was distant": []
                },
            },
            "revisiting_distant_events": {
                "model_prompt":
                lambda user_id, db_session, curr_session, app: self.
                get_model_prompt(user_id, app, db_session, " - Have you recently attempted exercise 10 and found this reignited unmanageable emotions as a result of old events?", has_emo=True),
                "choices": {
                    "yes": "more_questions",
                    "no": "more_questions",
                },
                "exercises": {
                    "yes": [self.EXERCISE_TITLES[15]],
                    "no": [self.EXERCISE_TITLES[10]]
                },
            },
            "more_questions": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, " - Thank you. Now I will ask some questions to understand your situation.", has_emo=True),

                "choices": {
                    "Okay": lambda user_id, db_session, curr_session, app: self.get_next_question(user_id),
                    "I'd rather not": "project_emotion",
                },
                "exercises": {
                    "Okay": [],
                    "I'd rather not": [self.EXERCISE_TITLES[15]],
                },
            },
            "displaying_antisocial_behaviour": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, " - Have you strongly felt or expressed any of the following emotions towards someone:", has_emo=True),

                "choices": {
                    "yes": "project_emotion",
                    "no": lambda user_id, db_session, curr_session, app: self.get_next_question(user_id),
                },
                "exercises": {
                    "yes": [self.EXERCISE_TITLES[17], self.EXERCISE_TITLES[18], self.EXERCISE_TITLES[15]],
                    "no": [self.EXERCISE_TITLES[15]],
                },
            },
            "internal_persecutor_saviour": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, " - Do you believe that you should be the saviour of someone else?", has_emo=True),

                "choices": {
                    "yes": "project_emotion",
                    "no": "internal_persecutor_victim",
                },
                "exercises": {
                    "yes": [self.EXERCISE_TITLES[21], self.EXERCISE_TITLES[19], self.EXERCISE_TITLES[11]],
                    "no": [self.EXERCISE_TITLES[15]]
                },
            },
            "internal_persecutor_victim": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, " - Do you see yourself as the victim, blaming someone else for how negative you feel?", has_emo=True),

                "choices": {
                    "yes": "project_emotion",
                    "no": "internal_persecutor_controlling",
                },
                "exercises": {
                    "yes": [self.EXERCISE_TITLES[21], self.EXERCISE_TITLES[19], self.EXERCISE_TITLES[11]],
                    "no": [self.EXERCISE_TITLES[15]]
                },
            },
            "internal_persecutor_controlling": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, " - Do you feel that you are trying to control someone?", has_emo=True),

                "choices": {
                "yes": "project_emotion",
                "no": "internal_persecutor_accusing"
                },
                "exercises": {
                "yes": [self.EXERCISE_TITLES[21], self.EXERCISE_TITLES[19], self.EXERCISE_TITLES[11]],
                "no": [self.EXERCISE_TITLES[15]]
                },
            },
            "internal_persecutor_accusing": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, " - Are you always blaming and accusing yourself for when something goes wrong?", has_emo=True),

                "choices": {
                "yes": "project_emotion",
                "no": lambda user_id, db_session, curr_session, app: self.get_next_question(user_id),
                },
                "exercises": {
                "yes": [self.EXERCISE_TITLES[21], self.EXERCISE_TITLES[19], self.EXERCISE_TITLES[11]],
                "no": [self.EXERCISE_TITLES[15]],
                },
            },
            "rigid_thought": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, " - In previous conversations, have you considered other viewpoints presented?", has_emo=True),

                "choices": {
                    "yes": lambda user_id, db_session, curr_session, app: self.get_next_question(user_id),
                    "no": "project_emotion",
                },
                "exercises": {
                    "yes": [self.EXERCISE_TITLES[15]],
                    "no": [self.EXERCISE_TITLES[19], self.EXERCISE_TITLES[15]],
                },
            },
            "personal_crisis": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, " - Are you undergoing a personal crisis (experiencing difficulties with loved ones e.g. falling out with friends)?", has_emo=True),

                "choices": {
                    "yes": "project_emotion",
                    "no": lambda user_id, db_session, curr_session, app: self.get_next_question(user_id),
                },
                "exercises": {
                    "yes": [self.EXERCISE_TITLES[22], self.EXERCISE_TITLES[15]],
                    "no": [self.EXERCISE_TITLES[15]],
                },
            },
            ################# POSITIVE EMOTION (HAPPY/CONTENT OR LOVING/CARING) #################
            "after_classification_positive": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(
                    user_id, app, db_session, "Happy - That's Good! Let me recommend an exercise you can attempt.", has_emo=False,
                ),
                "choices": {
                    "Okay": "suggestions",
                    "No, thank you": "ending_prompt"
                },
                "exercises": {
                    "Okay": [self.EXERCISE_TITLES[15], self.EXERCISE_TITLES[20], self.EXERCISE_TITLES[7], self.EXERCISE_TITLES[12], self.EXERCISE_TITLES[14],
                             self.EXERCISE_TITLES[8], self.EXERCISE_TITLES[17], self.EXERCISE_TITLES[18], self.EXERCISE_TITLES[23], self.EXERCISE_TITLES[13]],
                    "No, thank you": []
                },
            },
            ############################# ALL EMOTIONS #############################
            "project_emotion": {
               "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt_project_emotion(user_id, app, db_session),

               "choices": {
                   "continue": "suggestions",
               },
               "exercises": {
                   "continue": [],
               },
            },
            "suggestions": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, "All emotions - Here are my recommendations, please select the exercise that you would like to attempt", has_emo=False),

                "choices": {
                     self.EXERCISE_TITLES[k]: "trying_exercise"
                     for k in self.exercises
                },
                "exercises": {
                     self.EXERCISE_TITLES[k]: [self.EXERCISE_TITLES[k]]
                     for k in self.exercises
                },
            },
            "follow_up_suggestions": {
                "model_prompt": "Ok, sure. Below are the remaining suggestions:",

                "choices": {
                     self.EXERCISE_TITLES[k]: "trying_exercise"
                     for k in self.exercises
                },
                "exercises": {
                     self.EXERCISE_TITLES[k]: [self.EXERCISE_TITLES[k]]
                     for k in self.exercises
                },
            },
            "trying_exercise": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, "All emotions - Please try to go through this exercise now. When you finish, press 'continue'", has_emo=False),

                "choices": {"continue": "user_found_useful"},
                "exercises": {"continue": []},
            },
            "user_found_useful": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, "All emotions - Do you feel better or worse after having taken this exercise?", has_emo=False),

                "choices": {
                    "I feel better": "new_exercise_better",
                    "I feel worse": "new_exercise_worse",
                    "I feel no change": "new_exercise_same",
                },
                "exercises": {
                    "I feel better": [],
                    "I feel worse": [],
                    "I feel no change": []
                },
            },
            "new_exercise_better": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, "All emotions - Would you like to attempt another exercise? (Patient feels better)", has_emo=False),

                "choices": {
                    "Yes (show follow-up suggestions)": lambda user_id, db_session, curr_session, app: self.determine_next_prompt_new_exercise(
                        user_id, app
                    ),
                    "Yes (restart questions)": "restart_prompt",
                    "No (end session)": "ending_prompt",
                },
                "exercises": {
                    "Yes (show follow-up suggestions)": [],
                    "Yes (restart questions)": [],
                    "No (end session)": []
                },
            },
            "new_exercise_worse": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, "All emotions - Would you like to attempt another exercise? (Patient feels worse)", has_emo=False),

                "choices": {
                    "Yes (show follow-up suggestions)": lambda user_id, db_session, curr_session, app: self.determine_next_prompt_new_exercise(
                        user_id, app
                    ),
                    "Yes (restart questions)": "restart_prompt",
                    "No (end session)": "ending_prompt",
                },
                "exercises": {
                    "Yes (show follow-up suggestions)": [],
                    "Yes (restart questions)": [],
                    "No (end session)": []
                },
            },
            "new_exercise_same": {
                "model_prompt": [
                                "I am sorry to hear you have not detected any change in your mood.",
                                "That can sometimes happen but if you agree we could try another exercise and see if that is more helpful to you.",
                                "Would you like me to suggest a different exercise?"
                                ],

                "choices": {
                    "Yes (show follow-up suggestions)": lambda user_id, db_session, curr_session, app: self.determine_next_prompt_new_exercise(
                        user_id, app
                    ),
                    "Yes (restart questions)": "restart_prompt",
                    "No (end session)": "ending_prompt",
                },
                "exercises": {
                    "Yes (show follow-up suggestions)": [],
                    "Yes (restart questions)": [],
                    "No (end session)": []
                },
            },
            "ending_prompt": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_model_prompt(user_id, app, db_session, "All emotions - Thank you for taking part. See you soon", has_emo=False),

                "choices": {"any": "opening_prompt"},
                "exercises": {"any": []}
                },
            "restart_prompt": {
                "model_prompt": lambda user_id, db_session, curr_session, app: self.get_restart_prompt(user_id),

                "choices": {
                    "open_text": lambda user_id, db_session, curr_session, app: self.determine_next_prompt_opening(user_id, app, db_session, restart=True)
                },
                "exercises": {"open_text": []},
            },
        }
        self.QUESTION_KEYS = list(self.QUESTIONS.keys())

    def initialise_prev_questions(self, user_id):
        self.recent_questions[user_id] = []

    def clear_location(self):
        self.guess_location_predictions = {}

    def clear_datasets(self, user_id):
        self.datasets[user_id] = pd.DataFrame(columns=['sentences'])

    def initialise_remaining_choices(self, user_id):
        self.remaining_choices[user_id] = ["displaying_antisocial_behaviour", "internal_persecutor_saviour", "personal_crisis", "rigid_thought"]

    def save_location(self, user_id, db_session, curr_session, app, again):
        if again:
            user_response = self.user_choices[user_id]["choices_made"]["ask_again_location"]
        else:
            user_response = self.user_choices[user_id]["choices_made"]["ask_location"]
        country = self.country_finder.get_country(user_response)
        self.guess_location_predictions[user_id] = country
        self.users_location[user_id] = country
        return "check_location"
    
    def ask_location_prompt(self, user_id):
        prompt = ["Apologies about that. Please enter again the country where you are located.",
                  "If possible, please enter the that country's name in English, so I can be sure I understand.",
        ]
        return prompt

    def check_location_prompt(self, user_id):
        prompt = "Thanks. Do I understand correctly that you are located in {}?".format(self.guess_location_predictions[user_id])
        return prompt

    def get_suggestions(self, user_id, app): #from all the lists of exercises collected at each step of the dialogue it puts together some and returns these as suggestions
        reccomendations_collected = []
        final_reccomendations = []

        for curr_suggestions in list(self.suggestions[user_id]):
            for i in range(len(curr_suggestions)):
                if curr_suggestions[i] in self.EXERCISE_TITLES and curr_suggestions[i] not in self.done_exercises[user_id]:
                    reccomendations_collected.append(curr_suggestions[i])
        reccomendations_collected = list(set(reccomendations_collected)) #remove any duplicates
        for _, ranked_exercise in self.EXERCISE_RANKINGS.items():
            if ranked_exercise in reccomendations_collected:
                final_reccomendations.append(ranked_exercise)
                reccomendations_collected.remove(ranked_exercise)
    
        final_reccomendations.extend(reccomendations_collected)
        return final_reccomendations

    def clear_suggestions(self, user_id):
        self.suggestions[user_id] = []
        self.done_exercises[user_id] = []

    def clear_emotion_scores(self, user_id):
        self.guess_emotion_predictions[user_id] = ""

    def create_new_run(self, user_id, db_session, user_session):
        new_run = UserModelRun(session_id=user_session.id)
        db_session.add(new_run)
        db_session.commit()
        self.current_run_ids[user_id] = new_run.id
        return new_run

    def clear_choices(self, user_id):
        self.user_choices[user_id] = {}

    def update_suggestions(self, user_id, exercises, app):
        # Check if user_id already has suggestions
        try:
            self.suggestions[user_id]
        except KeyError:
            self.suggestions[user_id] = []

        if type(exercises) != list:
            self.suggestions[user_id].append(deque([exercises]))
        else:
            self.suggestions[user_id].append(deque(exercises))

    def get_opening_prompt(self, user_id):
        time.sleep(3)
        opening_prompt = [
                "Excellent, thanks.",
                "And how are you feeling today?",
        ]
        return opening_prompt

    def get_restart_prompt(self, user_id):
        time.sleep(3)
        return "Please tell me again, how are you feeling today?"

    def get_next_question(self, user_id):
        if self.remaining_choices[user_id] == []:
            return "project_emotion"
        else:
            selected_choice = np.random.choice(self.remaining_choices[user_id])
            self.remaining_choices[user_id].remove(selected_choice)
            return selected_choice

    def determine_next_prompt_opening(self, user_id, app, db_session, restart):
        if restart:
            user_response = self.user_choices[user_id]["choices_made"]["restart_prompt"]
        else:
            user_response = self.user_choices[user_id]["choices_made"]["opening_prompt"]
        emotion = get_classification(user_response, "emo")
        s_classification = get_classification(user_response, "s")
        
        if emotion == 'fear':
            self.guess_emotion_predictions[user_id] = 'Anxious/Scared'
            self.user_emotions[user_id] = 'Anxious'
        elif emotion == 'sadness':
            self.guess_emotion_predictions[user_id] = 'Sad'
            self.user_emotions[user_id] = 'Sad'
        elif emotion == 'anger':
            self.guess_emotion_predictions[user_id] = 'Angry'
            self.user_emotions[user_id] = 'Angry'
        elif emotion == 'joy':
            self.guess_emotion_predictions[user_id] = 'Happy/Content'
            self.user_emotions[user_id] = 'Happy'
        elif emotion == 'love':
            self.guess_emotion_predictions[user_id] = 'Loving/Caring'
            self.user_emotions[user_id] = 'Loving'
        elif emotion == 'instability':
            self.guess_emotion_predictions[user_id] = 'Insecure/Have a sense of instability'
            self.user_emotions[user_id] = 'Insecure'
        elif emotion == 'disgust':
            self.guess_emotion_predictions[user_id] = 'Disgusted'
            self.user_emotions[user_id] = 'Disgusted'
        elif emotion == 'disappointment':
            self.guess_emotion_predictions[user_id] = 'Disappointed'
            self.user_emotions[user_id] = 'Disappointed'
        elif emotion == 'shame':
            self.guess_emotion_predictions[user_id] = 'Ashamed/Embarrassed'
            self.user_emotions[user_id] = 'Ashamed'
        elif emotion == 'guilt':
            self.guess_emotion_predictions[user_id] = 'Guilty'
            self.user_emotions[user_id] = 'Guilty'
        elif emotion == 'envy':
            self.guess_emotion_predictions[user_id] = 'Envious'
            self.user_emotions[user_id] = 'Envious'
        else:
            self.guess_emotion_predictions[user_id] = 'Jealous'
            self.user_emotions[user_id] = 'Jealous'    
        
        if s_classification == 'not_s':
            return "guess_emotion"
        else:
            return "show_help_options"
        
    def get_help_options(self, user_id, app, db_session):
        current_country = self.users_location[user_id]
        prompt1 = ["From what you just told me, I sensed that you might be feeling suicidal.",
                   "I just want to pause for a moment and check on you.",
                   "There is help available, please do talk to someone about your concerns and how you're feeling. You deserve to be listened to if you're going through a difficult time.",
                   f"Since you've told me you are located in {current_country}, below are some phone numbers that you can call right away.",
                 ]
        numbers = self.country_finder.phoneline_from_country[current_country]
        prompt2 = ["And of course if I have misunderstood I apologise, and you can choose to continue our session by clicking the 'continue' button below."]
        return prompt1 + numbers + prompt2

    def get_best_sentence(self, column, prev_qs):
        maxscore = 0
        chosen = ''
        for row in column.dropna():
            fitscore = get_sentence_score(row, prev_qs)
            if fitscore > maxscore:
                maxscore = fitscore
                chosen = row.split(' <')[0]
        if chosen != '':
            return chosen
        else:
            return random.choice(column.dropna().to_list())

    def split_sentence(self, sentence):
        if type(sentence) == list:
            sentence = " ".join(sentence)
        temp_list = re.split('(?<=[.?!]) +', sentence)
        if '' in temp_list:
            temp_list.remove('')
        temp_list = [i + " " if i[-1] in [".", "?", "!"] else i for i in temp_list]
        if len(temp_list) == 2:
            return temp_list[0], temp_list[1]
        elif len(temp_list) == 3:
            return temp_list[0], temp_list[1], temp_list[2]
        else:
            return sentence

    def save_emotion(self, user_id, emotion):
        self.guess_emotion_predictions[user_id] = self.emotions_map[emotion]
        self.user_emotions[user_id] = emotion
        if emotion in self.negative_emotions:
            return "after_classification_negative"
        elif emotion in self.antisocial_emotions:
            return "after_classification_antisocial"
        else:
            return "after_classification_positive"

    def get_model_prompt(self, user_id, app, db_session, text, has_emo):
        prev_qs = pd.DataFrame(self.recent_questions[user_id],columns=['sentences'])
        if has_emo:
          base_prompt = self.user_emotions[user_id] + text
        else:
          base_prompt = text
        column = self.data[base_prompt].dropna().sample(25, replace=True)
        question = self.get_best_sentence(column, prev_qs)
        if len(self.recent_questions[user_id]) < 50:
            self.recent_questions[user_id].append(question)
        else:
            self.recent_questions[user_id] = []
            self.recent_questions[user_id].append(question)
        if text == " - Have you strongly felt or expressed any of the following emotions towards someone:":
            return [self.split_sentence(question), "Envy, jealousy, greed, hatred, mistrust, malevolence, or revengefulness?"]
        elif text == "All emotions - Thank you for taking part. See you soon":
            return [self.split_sentence(question), "You have been disconnected. Refresh the page if you would like to start over."]
        elif text == "All emotions - From what you have said I believe you are feeling {}. Is this correct?":
            question = question.format(self.guess_emotion_predictions[user_id].lower())
            return self.split_sentence(question)
        elif text == "All emotions - Please try to go through this exercise now. When you finish, press 'continue'":
            curr_exercise = self.current_exercise_ids[user_id][0]
            self.done_exercises[user_id].append(self.EXERCISE_TITLES[curr_exercise])
            question = self.split_sentence(question),
            intro = self.get_exercise_intro_utterance(user_id),
            exercise = self.EXERCISE_TEXTS[curr_exercise]
            return [question] + [intro] + exercise
        else:
            return self.split_sentence(question)

    def get_exercise_intro_utterance(self, user_id):
        prompts = [
            "Ok, here we go:", "Here is the exercise:",
            "So, here's what to do now to complete the exercise:",
            "Here are my instructions to complete the exercise:",
            "Here are my instructions to complete the exercise:"
        ]
        return random.choice(prompts)
    
    def get_model_prompt_project_emotion(self, user_id, app, db_session):
        time.sleep(3)
        prompts = [
            "Ok, thank you. Now, one last important thing: since you've told me you're feeling " + self.user_emotions[user_id].lower() + ", I would like you to try to project this emotion onto your childhood self. You can press 'continue' when you are ready and I'll suggest some exercises I think may be appropriate for you.",
            "Thank you, I will recommend some exercises for you in a moment. Before I do that, could you please try to project your " + self.user_emotions[user_id].lower() + " feeling onto your childhood self? Take your time to try this, and press 'continue' when you feel ready.",
            "Ok, thank you for letting me know that. Before I give you some exercise suggestions, please take some time and try to project your current " + self.user_emotions[user_id].lower() + " feeling onto your childhood self. Press 'continue' when you feel able to do it.",
            "Ok, thank you, I'm going to draw up a list of exercises which I think would be suitable for you today. In the meantime, going back to this " + self.user_emotions[user_id].lower() + " feeling of yours, would you like to try to project it onto your childhood self? You can try now and press 'continue' when you feel ready.",
            "Thank you. While I have a think about which exercises would be best for you, please take your time now and try to project your current " + self.user_emotions[user_id].lower() + " emotion onto your childhood self. When you are able to do this, please press 'continue' to receive your suggestions.",
        ]
        chosen_utterance = random.choice(prompts)
        return self.split_sentence(chosen_utterance)
        
    def determine_next_prompt_new_exercise(self, user_id, app):
        try:
            self.suggestions[user_id]
        except KeyError:
            self.suggestions[user_id] = []
        if len(self.suggestions[user_id]) > 0:
            return "follow_up_suggestions"
        return "more_questions"

    def update_conversation(self, user_id, new_dialogue, db_session, app):
        try:
            session_id = self.user_choices[user_id]["current_session_id"]
            curr_session = UserModelSession.query.filter_by(id=session_id).first()
            if curr_session.conversation is None:
                curr_session.conversation = "" + new_dialogue
            else:
                curr_session.conversation = curr_session.conversation + new_dialogue
            curr_session.last_updated = datetime.datetime.utcnow()
            db_session.commit()
        except KeyError:
            curr_session = UserModelSession(
                user_id=user_id,
                conversation=new_dialogue,
                last_updated=datetime.datetime.utcnow(),
            )

            db_session.add(curr_session)
            db_session.commit()
            self.user_choices[user_id]["current_session_id"] = curr_session.id

    def save_current_choice(
        self, user_id, input_type, user_choice, user_session, db_session, app
    ):
        # Set up dictionary if not set up already
        # with Session() as session:
        try:
            self.user_choices[user_id]
        except KeyError:
            self.user_choices[user_id] = {}

        # Define default choice if not already set
        try:
            current_choice = self.user_choices[user_id]["choices_made"][
                "current_choice"
            ]
        except KeyError:
            current_choice = self.QUESTION_KEYS[0]

        try:
            self.user_choices[user_id]["choices_made"]
        except KeyError:
            self.user_choices[user_id]["choices_made"] = {}

        if current_choice == "ask_location":
            self.clear_suggestions(user_id)
            self.user_choices[user_id]["choices_made"] = {}
            self.create_new_run(user_id, db_session, user_session)

        # Save current choice
        self.user_choices[user_id]["choices_made"]["current_choice"] = current_choice
        self.user_choices[user_id]["choices_made"][current_choice] = user_choice

        curr_prompt = self.QUESTIONS[current_choice]["model_prompt"]
        if callable(curr_prompt):
            curr_prompt = curr_prompt(user_id, db_session, user_session, app)

        else:
            self.update_conversation(
                user_id,
                "Model:{} \nUser:{} \n".format(curr_prompt, user_choice),
                db_session,
                app,
            )

        # Case: update suggestions for next attempt by removing relevant one
        if (
            current_choice == "suggestions" or current_choice == "follow_up_suggestions"
        ):

            # PRE: user_choice is a string representing a number from 1-20,
            # or the title for the corresponding exercise

            try:
                current_exercise = self.TITLE_TO_EXERCISE[user_choice]
            except KeyError:
                current_exercise = int(user_choice)

            exercise_chosen = Protocol(
                protocol_chosen=current_exercise,
                user_id=user_id,
                session_id=user_session.id,
                run_id=self.current_run_ids[user_id],
            )
            db_session.add(exercise_chosen)
            db_session.commit()
            self.current_exercise_ids[user_id] = [current_exercise, exercise_chosen.id]

            for i in range(len(self.suggestions[user_id])):
                curr_exercises = self.suggestions[user_id][i]
                if curr_exercises[0] == self.EXERCISE_TITLES[current_exercise]:
                    curr_exercises.popleft()
                    if len(curr_exercises) == 0:
                        self.suggestions[user_id].pop(i)
                    break

        # PRE: User choice is string in ["Better", "Worse"]
        elif current_choice == "user_found_useful":
            current_exercise = Protocol.query.filter_by(
                id=self.current_exercise_ids[user_id][1]
            ).first()
            current_exercise.exercise_was_useful = user_choice
            db_session.commit()

        if current_choice == "guess_emotion":
            option_chosen = user_choice + " ({})".format(
                self.guess_emotion_predictions[user_id]
            )
        else:
            option_chosen = user_choice
        choice_made = Choice(
            choice_desc=current_choice,
            option_chosen=option_chosen,
            user_id=user_id,
            session_id=user_session.id,
            run_id=self.current_run_ids[user_id],
        )
        db_session.add(choice_made)
        db_session.commit()

        return choice_made

    def determine_next_choice(
        self, user_id, input_type, user_choice, db_session, user_session, app
    ):
        # Find relevant user info by using user_id as key in dict.
        #
        # Then using the current choice and user input, we determine what the next
        # choice is and return this as the output.

        # Some edge cases to consider based on the different types of each field:
        # May need to return list of model responses. For next exercise, may need
        # to call function if callable.

        # If we cannot find the specific choice (or if None etc.) can set user_choice
        # to "any".

        # PRE: Will be defined by save_current_choice if it did not already exist.
        # (so cannot be None)

        current_choice = self.user_choices[user_id]["choices_made"]["current_choice"]
        current_choice_for_question = self.QUESTIONS[current_choice]["choices"]
        current_exercises = self.QUESTIONS[current_choice]["exercises"]
        if input_type != "open_text":
            if (
                current_choice != "suggestions"
                and current_choice != "follow_up_suggestions"
                and current_choice != "event_is_recent"
                and current_choice != "more_questions"
                and current_choice != "after_classification_positive"
                and current_choice != "user_found_useful"
                and current_choice != "check_emotion"
                and current_choice != "new_exercise_better"
                and current_choice != "new_exercise_worse"
                and current_choice != "new_exercise_same"
                and current_choice != "after_classification_negative"
                and current_choice != "after_classification_antisocial"
            ):
                user_choice = user_choice.lower()

            if (
                current_choice == "suggestions" or current_choice == "follow_up_suggestions"
            ):
                try:
                    current_exercise = self.TITLE_TO_EXERCISE[user_choice]
                except KeyError:
                    current_exercise = int(user_choice)
                exercise_choice = self.EXERCISE_TITLES[current_exercise]
                next_choice = current_choice_for_question[exercise_choice]
                exercises_chosen = current_exercises[exercise_choice]

            elif current_choice == "check_emotion":
                if user_choice == "Sad":
                    next_choice = current_choice_for_question["Sad"]
                    exercises_chosen = current_exercises["Sad"]
                elif user_choice == "Angry":
                    next_choice = current_choice_for_question["Angry"]
                    exercises_chosen = current_exercises["Angry"]
                elif user_choice == "Anxious/Scared":
                    next_choice = current_choice_for_question["Anxious/Scared"]
                    exercises_chosen = current_exercises["Anxious/Scared"]
                elif user_choice == "Happy/Content":
                    next_choice = current_choice_for_question["Happy/Content"]
                    exercises_chosen = current_exercises["Happy/Content"]
                elif user_choice == "Loving/Caring":
                    next_choice = current_choice_for_question["Loving/Caring"]
                    exercises_chosen = current_exercises["Loving/Caring"]
                elif user_choice == "Insecure/Have a sense of instability":
                    next_choice = current_choice_for_question["Insecure/Have a sense of instability"]
                    exercises_chosen = current_exercises["Insecure"]
                elif user_choice == "Disgusted":
                    next_choice = current_choice_for_question["Disgusted"]
                    exercises_chosen = current_exercises["Disgusted"]
                elif user_choice == "Disappointed":
                    next_choice = current_choice_for_question["Disappointed"]
                    exercises_chosen = current_exercises["Disappointed"]
                elif user_choice == "Ashamed/Embarrassed":
                    next_choice = current_choice_for_question["Ashamed/Embarrassed"]
                    exercises_chosen = current_exercises["Ashamed"]
                elif user_choice == "Guilty":
                    next_choice = current_choice_for_question["Guilty"]
                    exercises_chosen = current_exercises["Guilty"]
                elif user_choice == "Envious":
                    next_choice = current_choice_for_question["Envious"]
                    exercises_chosen = current_exercises["Envious"]
                else:
                    next_choice = current_choice_for_question["Jealous"]
                    exercises_chosen = current_exercises["Jealous"]
            else:
                next_choice = current_choice_for_question[user_choice]
                exercises_chosen = current_exercises[user_choice]
        else:
            next_choice = current_choice_for_question["open_text"]
            exercises_chosen = current_exercises["open_text"]

        if callable(next_choice):
            next_choice = next_choice(user_id, db_session, user_session, app)

        if current_choice == "guess_emotion" and user_choice.lower() == "yes":
            if self.guess_emotion_predictions[user_id] == "Sad":
                next_choice = next_choice["Sad"]
            elif self.guess_emotion_predictions[user_id] == "Angry":
                next_choice = next_choice["Angry"]
            elif self.guess_emotion_predictions[user_id] == "Anxious/Scared":
                next_choice = next_choice["Anxious/Scared"]
            elif self.guess_emotion_predictions[user_id] == "Happy/Content":
                next_choice = next_choice["Happy/Content"]
            elif self.guess_emotion_predictions[user_id] == "Loving/Caring":
                next_choice = next_choice["Loving/Caring"]
            elif self.guess_emotion_predictions[user_id] == "Insecure/Have a sense of instability":
                next_choice = next_choice["Insecure"]
            elif self.guess_emotion_predictions[user_id] == "Disgusted":
                next_choice = next_choice["Disgusted"]
            elif self.guess_emotion_predictions[user_id] == "Disappointed":
                next_choice = next_choice["Disappointed"]
            elif self.guess_emotion_predictions[user_id] == "Ashamed/Embarrassed":
                next_choice = next_choice["Ashamed"]
            elif self.guess_emotion_predictions[user_id] == "Guilty":
                next_choice = next_choice["Guilty"]
            elif self.guess_emotion_predictions[user_id] == "Envious":
                next_choice = next_choice["Envious"]
            else:
                next_choice = next_choice["Jealous"]

        if callable(exercises_chosen):
            exercises_chosen = exercises_chosen(user_id, db_session, user_session, app)
        next_prompt = self.QUESTIONS[next_choice]["model_prompt"]
        if callable(next_prompt):
            next_prompt = next_prompt(user_id, db_session, user_session, app)
        if (
            len(exercises_chosen) > 0
            and current_choice != "suggestions" and current_choice != "follow_up_suggestions"
        ):
            self.update_suggestions(user_id, exercises_chosen, app)

        # Case: new suggestions being created after first exercise attempted
        if next_choice == "opening_prompt":
            self.clear_suggestions(user_id)
            self.clear_emotion_scores(user_id)
            self.create_new_run(user_id, db_session, user_session)

        if next_choice == "suggestions" or next_choice == "follow_up_suggestions":
            next_choices = self.get_suggestions(user_id, app)
            if len(next_choices) == 0:
                return {"model_prompt": "Unfortunately I have no more exercises to recommend for the current session. You can start a new session by refreshing the page. Goodbye!", 
                        "choices": []}

        else:
            next_choices = list(self.QUESTIONS[next_choice]["choices"].keys())
        self.user_choices[user_id]["choices_made"]["current_choice"] = next_choice
        return {"model_prompt": next_prompt, "choices": next_choices}
