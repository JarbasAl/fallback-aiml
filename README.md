## Auto Translatable Fallback-aiml
AIML fallback

## Description
This is a AIML fallback using the Alice chatbot files. Use auto translate to
support non english input, auto translate output to configured language

## logs

    19:54:32.476 - SKILLS - DEBUG - {"type": "recognizer_loop:utterance", "data": {"utterances": ["como te chamas"]}, "context": null}
    19:54:32.483 - SKILLS - DEBUG - {"type": "intent_failure", "data": {"lang": "en-us", "utterance": "como te chamas"}, "context": {}}
    19:54:32.484 - mycroft.skills.padatious_service:handle_fallback:107 - DEBUG - Padatious fallback attempt: como te chamas
    19:54:33.339 - SKILLS - DEBUG - {"type": "mycroft.skill.handler.start", "data": {"handler": "fallback"}, "context": null}
    19:54:33.340 - mycroft.skills.intent_service:send_metrics:244 - DEBUG - Sending metric
    19:54:52.296 - SKILLS - DEBUG - {"type": "speak", "data": {"expect_response": false, "utterance": "Meu nome e Nameless.", "metadata": null}, "context": {"target_lang": "pt", "auto_translated": true, "source_lang": "en"}}
    19:54:52.299 - SKILLS - DEBUG - {"type": "active_skill_request", "data": {"skill_id": -5628364534345396726}, "context": null}
    19:54:52.303 - SKILLS - DEBUG - {"type": "mycroft.skill.handler.complete", "data": {"handler": "fallback", "fallback_handler": "AimlSkill._universal_fallback_handler"}, "context": null}

## Examples
* "Hey Mycroft, are you a robot?"
* "Hey Mycroft, what is the name of my dog?"

## Credits
JarbasAI
nielstron
forslund