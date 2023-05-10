from nlu.intents.intent_detection import IntentDetection


deteksi_intent = IntentDetection()
# detect intent
teks = 'login'
intent = deteksi_intent.prediction(teks)
print(intent)

if intent == 9:
    print('ini controller text2sql')
elif intent == 0 or intent == 1:
    print('ini controller form manager')