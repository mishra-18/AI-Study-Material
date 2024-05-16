from PyPDF2 import PdfReader
import openai
import time
import os
from dotenv import load_dotenv
# Loading .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        
        text += page.extract_text() + "\n"
    return text




def FlashCards(pdf, resourceType=1, depth=10):
    text = extract_text_from_pdf(pdf)[:1200]


    if resourceType == 1:
        flashcards= openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output Twenty (10) Flash Card on the topics in the given content in the EXACT FORMAT as this: \n \
                @1. Title of The Topic@\
                1st Point\
                2nd Point \
                3rd Point \
                4th Point \
                NOTE: Create 10 more of such, also make sure no flash card SHOULD 'NOT' exceed 250 words"},

            {"role": "user", "content": text }
            ]

        )
    else:
        flashcards= openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output Twenty (10) Flash Card on the topics in the given content in the EXACT FORMAT as this: \n \
                @1. Title of The Topic@\
                1st Point\
                2nd Point \
                3rd Point \
                4th Point \
                NOTE: Create 10 more of such, also make sure no flash card should NOT exceed 200 words. NOTE: Make sure you only include 3 - 4 important Point, one's that someone \
                would want to look a night before exam"},

            {"role": "user", "content": text }
            ]

        )
    text = flashcards.choices[0].message.content
    # print(text)
    text = text.split("@")[1:]
    # print(text)
    flashcards = []
    fc = {"title": "",
          "content": [] }
    
    for i, card in enumerate(text):
        if (i + 1)%2 == 0:
            lines = card.strip().split('\n')
            int_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            list_items = [] 
            for line in lines:
                if line and line[0] in int_list:
                    list_items.append(line[2:])
                elif line :
                    list_items.append(line)
            fc["content"] = list_items
            print(fc)
            flashcards.append(fc)
            fc = {"title": "",
                  "content": []}
        else:
            fc["title"] = card[3:]

    if len(flashcards) >= depth: 
        return flashcards[:depth]
    else:
        time.sleep(0.1)
        flashcards+= FlashCards(pdf, depth=depth-len(flashcards))
    print("The FlashCards are Generated Successfully (Total 10)")
    return flashcards
# FlashCards(pdf="kebo101.pdf")
def Quiz(pdf):
    text = extract_text_from_pdf(pdf)[:12000]
    
    quiz = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
             {"role": "system", "content": "You are a helpful assistant designed to output Twenty (20) multiple choice questions on the topics in the given content in the EXACT FORMAT as this: \n \
               @1. Which of the following is correct? \
               @1 something \
               @2 another option \
               @3 another option \
               @4 another option \
               @Answer:   something\n \
              NOTE: Create 20 more of such, also Please add the symbol '@' before every, question and option as shown in the above format."},

           {"role": "user", "content": text }
        ]

    )
    text = quiz.choices[0].message.content
    print(text)
    quizes = text.split("@")[1:]
    # print(quizes)
    mcqs = []


    q_idx = 1
    for i, quiz in enumerate(quizes):
        
        if i + 1 == q_idx:
            # print(i)
            mcq = { "question": "",
                "options": [],
                "answer": "" }

            mcq["question"] = quiz[3:]
            q_idx += 6
        elif i + 1 == q_idx - 1:
            # print(i)
            print(quiz[10:].strip())
            mcq["answer"] = quiz[8:].strip()
            mcqs.append(mcq)
        else:
            # print(i)
            # print(quiz[2:])
            mcq["options"].append(quiz[2:].strip())
    
    print(f"Total No. of Generated MCQs: {len(mcqs)}")
    return mcqs

# Quiz(pdf="kesp108.pdf")
def QuestionBank(pdf, resourceType):
    text = extract_text_from_pdf(pdf)[:12000]
    
    if resourceType == 1:
        print("W")
        quiz = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to create 10 Very Long detailed questions and Answers on the topics in the given content, NOTE: in the EXACT FORMAT as this: \n \
                @Question:  \n\
                @Answer:   \n\
                NOTE: CREATE 10 more of such. Also please add the symbol '@' BEFORE EVERY Question and Answer as shown in the above format. NOTE: EVERY ANSWER SHOULD BE OF ATLEAST 300 WORDS"},

            {"role": "user", "content": text }
            ]

        )
    else:
            quiz = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to create 10 detailed Questions and Answers, on the topics in the given content, NOTE: in the EXACT FORMAT as this: \n \
                @Question: \n\
                @Answer:  \n\
                NOTE: CREATE 10 more of such. Also please add the symbol '@' BEFORE EVERY Question and Answer as shown in the above FORMAT. Make the questions and answers, short concise and \
                 to the point, as something to look at a night before exam."},

            {"role": "user", "content": text }
            ]

        )
    text = quiz.choices[0].message.content
    print(text)
    text = text.split("@")[1:]
    QnAs = []
    QnA = {"question": "",
          "answer": "" }
    
    for i, qna in enumerate(text):
        if (i + 1)%2 == 0:

            QnA["answer"] = qna[7:].strip()
            print(QnA)
            QnAs.append(QnA)
            QnA = {"question": "",
                  "answer": ""}
        else:
            print(QnA["question"])
            QnA["question"] = qna[9:].strip()
    
    print(f"Total No. of Generated QnAs: {len(QnAs)}")

    return QnAs
