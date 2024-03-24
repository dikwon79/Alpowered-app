"# Alpowered-app" 


## goal
- This project is to listen to what someone is saying and turn it into a different language voice.


- part1 : idea (together)
  IDEA about service ----decide which LLM we can use(HuggingFace)
  ex :  1. automatic speech recognition -> text -> translate 
        2. english text -> translate hindi -> textTovoice
- part2 :divide role
  sign in / sign out page  :  form ex) email, password   ___admin(Admin-id : 'admin@admin.com' Admin-pass: '111')   //Tushar
  admin /user landing page   // jack
  bonus) forget password feature  // jackson
  database organization : DB ERD, and DB table   //jackson

  front part : jack, tushar
  back end part : dongil
  Database part: jackson

  
## install to run the program
pip install -r requirements.txt   

## how to run : 
    - app.cmd
    - flask db init
    - flask run

    * reference : (venv) myblog(.cmd)  
                  (venv) flask db migrate  
                  (venv) flask db upgrade  

## if you want to make virtual environment,
    - python -m venv venv
    - F1 or Ctrl + Shift + P (Palette command)
    - enter "Python Interpreter" and click  "Python: Select Interpreter"
    - choice .\venv\Scripts\python.exe 







### requirements.txt 
    pip freeze > requirements.txt
