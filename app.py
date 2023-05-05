from flask import Flask,request,jsonify, render_template
import re
import spacy
import pickle
import urllib.request
import pickle


import PyPDF2
def load_nlp(text):
    nlp=spacy.load('en_core_web_lg')
    skills='abc.jsonl'
    ruler=nlp.add_pipe('entity_ruler',before='ner')
    ruler.from_disk(skills)
    patterns=[
    
    {
        'label':'EMAIL','pattern':[{"TEXT":{"REGEX":"([^@|\s]+@[^@]+\.[^@|\s]+)"}}]
        
    },
    {
        'label':'MOBILE','pattern':[{"TEXT":{"REGEX":"\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}"}}]
        
    },
     {
        'label':'Name','pattern':[{"TEXT":{"REGEX":"/^[a-zA-Z ]*$/"}}]
        
    }
    
    
    ]
    EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]
    for i in range(len(EDUCATION)):
        patterns.append( {
            'label':'Education','pattern':[{"TEXT":{"REGEX":EDUCATION[i]}}]
        
                    }
                )
    ruler.add_patterns(patterns)
    doc = nlp(text)
    return doc    
#model = pickle.load(open('nlp1.pkl','rb'))

app = Flask(__name__)



   
@app.route('/cv')
def get_users():
    
    if 'file' not in request.files:
        return 'No file uploaded', 400

    # Get file object from request
    file = request.files['file']

    # Check if file is a pdf
    if file.filename.split('.')[-1].lower() != 'pdf':
        return 'File must be a pdf', 400

    # Read pdf file
    pdf = PyPDF2.PdfReader(file)
    text = ''

    # Iterate through all pages and extract text
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        text += page.extract_text()

   

    
    
    
    
    text.replace(" ", "")
    print("Using jsonify")
    cv=request.files.getlist('file')
    file=cv[0]
    

    

    #r=request.form.get("text")
    print(text)
    #m1=model(text)
    m1=load_nlp(text)
    #from spacy import displacy
    #displacy.render(m1, style="ent", jupyter=True)
    dict_data={}
    skills=[]
    email=[]
    phone=[]
    i=0
    dict_data=dict({})
    skills=[]
    email=[]
    phone=[]
    i=0
    name=""
    for i in range(len(m1.ents)):
        if m1.ents[i].label_=="PERSON":
            name=str(m1.ents[i])
        elif m1.ents[i].label_=='EMAIL':
            email.append(str(m1.ents[i]))
        elif m1.ents[i].label_=='MOBILE':
            phone.append(str(m1.ents[i]))    
        elif m1.ents[i].label_=='SKILL':
            skills.append(str(m1.ents[i])) 
    #skills=[j.capitalize() for j in set([k.lower() for k in skills])]   
    # 
    #print(type(json.dumps(skills)))  
    # 
    dict_data['TEXT']=text  
    dict_data['NAME']=name
    dict_data["SKILLS"]=(list(skills))
    dict_data["EMAIL"]=(list(email))
    dict_data["Phone"]=(list(phone))            
       
    print("Using jsonify")
    
            
    return jsonify({'data': dict_data})
 

if __name__ == '__main__':
    app.run(debug=True,port=5000)


