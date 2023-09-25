from flask import Flask,render_template,request,url_for,redirect, jsonify
import nltk,random
from model import words,training,labels,data,translate_english_to_hindi,translate_hindi_to_english,translate_text
from speech_text import speech_to_text,SpeakText
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy as np
import requests
from googletrans import Translator
from keras.models import load_model
model = load_model('model_keras.h5')

sub_head="Introducing LegalLingo"
description="Our website features a chatbot that provides instant answers to the Indian legal queries. Empower yourself with knowledge and get the answers you need with ease on our multilingual legal website."
try_now="Try our chatbot for best user-experience."
Home="home"
abt_us="About Us"
ini="Initiative"
con_us="Contact Us"
welcome="Hey! How can I help you today?"
trychat="Try our chatbot for best user-experience."
chat="Chat"



def translate_text_menu(text, destination_lang=None):
    translator = Translator()
    # # Detect the source language if not provided
    if destination_lang is None:
        detected_lang = translator.detect(text)
        destination_lang = detected_lang.lang

    # Translate the text
    translated_text = translator.translate(text, src="en", dest=destination_lang)
    list=[destination_lang,translated_text.text]
    return list

app=Flask(__name__)

@app.route("/",methods=["GET"])
def homepage():
    return render_template("homepage.html")

@app.route("/aboutus/<string:language>/<string:list>",methods=["GET","POST"])
def select_aboutus(language,list):
    if language=='en':
        return render_template("englishaboutus.html",list=list)
    elif language=="hi":
        return render_template("hindiaboutus.html",list=list)
    elif language=="mr":
        return render_template("marathiaboutus.html",list=list)
    else :
        return render_template("gujrathiaboutus.html",list=list)
    
@app.route("/init/<string:language>/<string:list>",methods=["GET","POST"])
def select_init(language,list):
    if language=='en':
        return render_template("englishinit.html",list=list)
    elif language=="hi":
        return render_template("hindiinit.html",list=list)
    elif language=="mr":
        return render_template("marathiinit.html",list=list)
    else :
        return render_template("gujrathiinit.html",list=list)    

@app.route("/<string:language>/language",methods=["GET","POST"])
def language(language):
        sub_heading=translate_text_menu(sub_head,language)
        info=translate_text_menu(description,language)
        try_n=translate_text_menu(try_now,language)
        home=translate_text_menu(Home,language)
        about_us=translate_text_menu(abt_us,language)
        initiative=translate_text_menu(ini,language)
        contactus=translate_text_menu(con_us,language)
        welcometo=translate_text_menu(welcome,language)
        chatus=translate_text_menu(chat,language)
        try_chat=translate_text_menu(trychat,language)
        list=[sub_heading[1],info[1],home[1],about_us[1],contactus[1],initiative[1],sub_heading[0],info[1],try_n[1],welcometo[1],chatus[1],try_chat[1]]

        return render_template("Eng.html",list=list)

# @app.route("/gj",methods=["GET","POST"])
# def gujrati_language():
#         language="gujrati"
#         sub_heading="वेलकम टू लीगल लिंगो"
#         info="यहाँ आप विभिन्न कानूनी सवालों से जुड़े सवालों को हल कर सकते हैं और यह पूरी तरह से मुफ्त है।"
#         home="होम"
#         typesoflaw="कानून के प्रकार"
#         contactus="संपर्क करें"
#         needassistant="सहायता चाहिए"
#         list=[sub_heading,info,home,typesoflaw,contactus,needassistant,language]
#         list1=list
#         return render_template("languagepage.html",list=list)

# @app.route("/en",methods=["GET","POST"])
# def english_language():
#         language="english"
#         sub_heading="Wekcome to legal lingo"
#         info="blah blah blah"
#         home="home"
#         typesoflaw="types of laws"
#         contactus="contact us"
#         needassistant="need assistant"
#         list=[sub_heading,info,home,typesoflaw,contactus,needassistant,language]
#         list1=list
#         return render_template("deocy2.html",list=list)

# list1=[]
# @app.route("/ma",methods=["GET","POST"])
# def marathi_language():
#     sub_heading="स्वागत आहे वैधिक व्यक्तींसंग"
#     info="इथे आपल्याला विविध कायदेविषयी सवाल विचारून सांगायला मिळेल आहे आणि ते पूर्णपणे विनामूल्य आहे."
#     home="होम"
#     typesoflaw="कायद्याच्या प्रकारे"
#     contactus="संपर्क साधा"
#     needassistant="सहाय्य आवश्यक आहे"
#     list=[sub_heading,info,home,typesoflaw,contactus,needassistant]
#     return render_template("languagepage.html",list=list)

# @app.route("/be",methods=["GET","POST"])
# def bengali_language():
#     sub_heading="লিগ্যাল লিঙ্গো-এ স্বাগতম"
#     info="এটি এটা যেখানে আপনি বিভিন্ন আইন প্রশ্নের সাথে আপনার প্রশ্ন সমাধান করতে পারেন এবং এটি সম্পূর্ণ বিনামূল্যে।"
#     home="হোম"
#     typesoflaw="আইনের প্রকার"
#     contactus="যোগাযোগ করুন"
#     needassistant="সাহায্য চাই"
#     list2=[sub_heading,info,home,typesoflaw,contactus,needassistant]
#     list1=list2
#     return render_template("languagepage.html",list=list2)

# @app.route("/te",methods=["GET","POST"])
# def telugu_language():
#     sub_heading="లీగల్ లింగోకు స్వాగతం"
#     info="ఇక మీరు వివిధ వాణిజ్య ప్రశ్నలకు సంబంధించిన మీ ప్రశ్నలను పరిష్కరించగలరు మరియు ఇది పూర్తిగా ఉచితంగా ఉంది."
#     home="హోమ్"
#     typesoflaw="విధుల ప్రకారాలు"
#     contactus="మాకు సంప్రదించండి"
#     needassistant="సహాయం కావాలి"
#     list=[sub_heading,info,home,typesoflaw,contactus,needassistant]
#     return render_template("languagepage.html",list=list)

# @app.route("/ta",methods=["GET","POST"])
# def tamil_language():
#     sub_heading="சட்ட வாய்ப்பு வார்த்தைக்கு வருக"
#     info="இது இங்கே பல சட்ட கேள்விகளுக்கு உங்கள் கேள்விகளை தீர்க்க முடியும் மற்றும் அது முழுமையாக இலவசம்."
#     home="முகப்பு"
#     typesoflaw="சட்டங்களின் வகைகள்"
#     contactus="தொடர்பு கொள்ளவும்"
#     needassistant="உதவி தேவை"
#     list=[sub_heading,info,home,typesoflaw,contactus,needassistant]
#     return render_template("languagepage.html",list=list)

@app.route("/model",methods=["GET","POST"])
def legal_lingo_model():
    
    inputchat=request.form['q']
    print(inputchat)
    def bag_of_words(s, words):
        bag = [0 for _ in range(len(words))]
        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for s_word in s_words:
            for i, w in enumerate(words):
                if w == s_word:
                    bag[i] = 1

        return np.array(bag)

    def chat():
        # while True:
        translator = Translator()
        input_list = translate_text(inputchat)
        print(input_list[1])
        # if inp.lower() == 'quit':
        #     break
        # Probability of correct response
        results = model.predict(np.array([bag_of_words(input_list[1], words)]).reshape(-1, len(training[0])))

        # Picking the greatest number from probability
        results_index = np.argmax(results)

        tag = labels[results_index]

        for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['response']
                answer=random.choice(responses)
                print(answer)
                answer=translator.translate(random.choice(responses), src='en', dest=input_list[0])
                print(answer.text)
                return answer.text
    
    answer=chat()
    return jsonify({"message": answer})
    
@app.route("/speechtext",methods=["GET","POST"])    
def speech_text():
    
    def bag_of_words1(s, words):
        bag = [0 for _ in range(len(words))]
        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        for s_word in s_words:
            for i, w in enumerate(words):
                if w == s_word:
                    bag[i] = 1

        return np.array(bag)
    

    def chat1(input1):
        # while True:
        translator = Translator()
        input_list = translate_text(input1)
        print(input_list[1])
        # if inp.lower() == 'quit':
        #     break
        # Probability of correct response
        results = model.predict(np.array([bag_of_words1(input_list[1], words)]).reshape(-1, len(training[0])))

        # Picking the greatest number from probability
        results_index = np.argmax(results)

        tag = labels[results_index]

        for tg in data['intents']:
            if tg['tag'] == tag:
                responses = tg['response']
                answer=random.choice(responses)
                print(answer)
                answer=translator.translate(random.choice(responses), src='en', dest=input_list[0])
                print(answer.text)
                return answer.text
            
    print("you are in speechtext")
    inputtext=speech_to_text()
    print(inputtext)
    answer=chat1(inputtext)
    print(answer)
    int1=translate_text(inputtext)
    translated_question=translate_text_menu(inputtext,int1[0])
    SpeakText(answer)
    print(translated_question)
    return jsonify({"message": answer,"question":translated_question[1]})

    
if __name__ == '__main__':
    app.run(debug=True)