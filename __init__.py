# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


import aiml
from datetime import date
from os import listdir, remove as remove_file
from os.path import isfile
from mycroft_jarbas_utils.skills.auto_translatable import AutotranslatableFallback
from mycroft.skills.core import intent_handler
from adapt.intent import IntentBuilder

__author__ = 'jarbas'


class AimlFallback(AutotranslatableFallback):
    def __init__(self):
        super(AimlFallback, self).__init__(name='AimlSkill')
        self.kernel = aiml.Kernel()
        self.input_lang = "en-us"
        # TODO read from settings maybe?
        self.aiml_path = self._dir + "/aiml"
        self.brain_path = self._dir + "/bot_brain.brn"
        # secondary personal bot info
        if "birthday" not in self.settings:
            self.settings["birthday"] = "May 23, 2016"
        if "sex" not in self.settings:
            self.settings["sex"] = "undefined"
        if "master" not in self.settings:
            self.settings["master"] = "skynet"
        if "eye_color" not in self.settings:
            self.settings["eye_color"] = "blue"
        if "hair" not in self.settings:
            self.settings["hair"] = "no"
        if "hair_length" not in self.settings:
            self.settings["hair_length"] = "bald"
        if "favorite_color" not in self.settings:
            self.settings["favorite_color"] = "blood red"
        if "favorite_band" not in self.settings:
            self.settings["favorite_band"] = "Compressor Head"
        if "favorite_book" not in self.settings:
            self.settings["favorite_book"] = "The Moon Is A Harsh Mistress"
        if "favorite_author" not in self.settings:
            self.settings["favorite_author"] = "Phillip K. Dick"
        if "favorite_song" not in self.settings:
            self.settings["favorite_song"] = "The Robots, by Kraftwerk"
        if "favorite_videogame" not in self.settings:
            self.settings["favorite_videogame"] = "Robot Battle"
        if "favorite_movie" not in self.settings:
            self.settings["favorite_movie"] = "The Terminator"
        if "job" not in self.settings:
            self.settings["job"] = "Personal Assistant"
        if "website" not in self.settings:
            self.settings["website"] = "jarbasai.github.io"
        if "pet" not in self.settings:
            self.settings["pet"] = "bugs"
        if "interests" not in self.settings:
            self.settings["interests"] = "I am interested in all kinds of " \
                                         "things. We can talk about anything."
        if "genus" not in self.settings:
            self.settings["genus"] = "mycroft"
        if "family" not in self.settings:
            self.settings["family"] = "virtual personal assistant"
        if "order" not in self.settings:
            self.settings["order"] = "artificial intelligence"
        if "class" not in self.settings:
            self.settings["class"] = "computer program"
        if "kingdom" not in self.settings:
            self.settings["kingdom"] = "machine"

    def get_intro_message(self):
        name = "a i m l"
        return "you installed universal " + name + " skill, you should " \
               "also blacklist the official " + name + \
               " skill to avoid potential problems"

    def load_brain(self):
        if isfile(self.brain_path):
            self.kernel.bootstrap(brainFile=self.brain_path)
        else:
            aimls = listdir(self.aiml_path)
            for aiml in aimls:
                try:
                    self.kernel.bootstrap(learnFiles=self.aiml_path + "/" +
                                                   aiml)
                except Exception as e:
                    self.log.error(e)
            try:
                self.kernel.saveBrain(self.brain_path)
            except Exception as e:
                self.log.error(e)
        # set personal bot info
        # TODO all fields in aiml files
        self.kernel.setBotPredicate("genus", self.settings["genus"])
        self.kernel.setBotPredicate("family", self.settings["family"])
        self.kernel.setBotPredicate("order", self.settings["order"])
        self.kernel.setBotPredicate("class", self.settings["class"])
        self.kernel.setBotPredicate("kingdom", self.settings["kingdom"])
        self.kernel.setBotPredicate("botmaster", self.settings["master"])
        self.kernel.setBotPredicate("birthday", self.settings["birthday"])
        self.kernel.setBotPredicate("sex", self.settings["sex"])
        self.kernel.setBotPredicate("eyes", self.settings["eye_color"])
        self.kernel.setBotPredicate("hair", self.settings["hair"])
        self.kernel.setBotPredicate("hairlen", self.settings["hair_length"])
        self.kernel.setBotPredicate("color", self.settings["favorite_color"])
        self.kernel.setBotPredicate("band", self.settings["favorite_band"])
        self.kernel.setBotPredicate("book", self.settings["favorite_book"])
        self.kernel.setBotPredicate("author", self.settings["favorite_author"])
        self.kernel.setBotPredicate("movie", self.settings["favorite_movie"])
        self.kernel.setBotPredicate("song", self.settings["favorite_song"])
        self.kernel.setBotPredicate("videogame", self.settings["favorite_videogame"])
        self.kernel.setBotPredicate("job", self.settings["job"])
        self.kernel.setBotPredicate("pet", self.settings["pet"])
        self.kernel.setBotPredicate("website", self.settings["website"])
        self.kernel.setBotPredicate("master", self.settings["master"])
        self.kernel.setBotPredicate("interests", self.settings["interests"])
        self.kernel.setBotPredicate("species", self.config_core.get(
            "platform", "dev install"))

        name = self.config_core.get("listener", {}).get("wake_word",
                                                        "mycroft")
        name = name.lower().replace("hey ", "")
        self.kernel.setBotPredicate("name", name)
        if "mycroft" in name:
            self.kernel.setBotPredicate("fullname",
                                 name + " the First")
        else:
            self.kernel.setBotPredicate("fullname",
                                 name + " son of Mycroft")
        self.kernel.setBotPredicate("age", str(date.today().year - 2016))
        self.kernel.setBotPredicate("location",
                             self.location["city"]["state"]["country"][
                                 "name"])
        self.kernel.setBotPredicate("hometown", self.location_pretty)

    def initialize(self):
        self.load_brain()
        self.register_fallback(self.handle_fallback, 99)

    @intent_handler(
        IntentBuilder("ResetMemoryIntent").require("Reset").require("Memory"))
    def handle_reset_brain(self, message):
        # delete the brain file and reset memory
        self.speak_dialog("reset.memory")
        self.kernel.resetBrain()
        remove_file(self.brain_path)
        # also reload base knowledge
        self.load_brain()
        return

    def ask_brain(self, utterance):
        response = self.kernel.respond(utterance)
        return response

    def handle_fallback(self, message):
        utterance = message.data.get("utterance")
        answer = self.ask_brain(utterance)
        if answer != "":
            asked_question = False
            if answer.endswith("?"):
                asked_question = True
            self.speak(answer, expect_response=asked_question)
            return True
        return False

    def stop(self):
        self.kernel.resetBrain()

    def shutdown(self):
        self.stop()
        self.remove_fallback(self.handle_fallback)
        super(AimlFallback, self).shutdown()


def create_skill():
    return AimlFallback()
