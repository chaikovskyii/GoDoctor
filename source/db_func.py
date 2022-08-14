import distutils.log
import sqlite3
import back
from math import floor


all_dis = list(back.all_dis)
conn = sqlite3.connect("diseases.db")
c = conn.cursor()

def refresh():

    for ds in all_dis:
        request = c.execute("SELECT name FROM Diseases")
        registred_diseases_names = list(map(lambda x: str(x)[2:-3], request))

        if ds.name in registred_diseases_names:
            pass

        else:
            c.execute("INSERT INTO Diseases(name, info, type, points) VALUES(?,?,?,?)", (ds.name, ds.info, ds.type, 0))
            id = c.execute("SELECT dis_id FROM Diseases WHERE name LIKE ?", (ds.name,))
            id = c.fetchone()[0]

            for symptom in ds.symptoms:
                c.execute("INSERT INTO symptoms(symptom, group_id,points) VALUES(?,?,?)", (symptom, id, 0))

    conn.commit()


def convert_to_set (value):
    return set(map(lambda x: str(x)[2:-3], value))


#Всі симптоми з БД
all_diseases = c.execute("SELECT name from Diseases")
all_diseases = convert_to_set(all_diseases)

#Допоміжна функція для обнулення БД
def reset_func():
   c.execute("UPDATE symptoms SET points = 0")
   c.execute("UPDATE Diseases SET points = 0 ")


def diagnose_suggestions(Textbox):

     #Set points.
    for disease in all_diseases:
        id = c.execute("SELECT dis_id FROM Diseases WHERE name = ?", (disease,))
        id = c.fetchone()

        disease_symptoms = c.execute("SELECT symptom FROM symptoms WHERE group_id = ?", id)
        disease_symptoms = convert_to_set(disease_symptoms)
        for symptom in disease_symptoms:

            if symptom in Textbox:
                c.execute("UPDATE symptoms SET points = 1 WHERE group_id = ? AND symptom = ? ", id + (symptom,)) #Поінти симптомів
                c.execute("UPDATE Diseases SET points = points + 1 WHERE dis_id = ?", id) #Поінти хворіб
                conn.commit()

    suggested_diseases = dict()


    for disease in all_diseases:
        dis_points = c.execute("SELECT points FROM Diseases WHERE name = ?", (disease,))
        dis_points = dis_points.fetchone()[0]

        if dis_points > 0:
            suggested_diseases[disease] = dis_points



    #Якщо менше трьох пропонованих то певернути їх
    if len(suggested_diseases) <= 3:
        return list(map(lambda x: x, suggested_diseases.keys()))



    #Якщо більше, то пройти наступні фільтри
    # Записання у новий список трьох хворіб що найбільше підходять
    suggested_diseases_renewed = []

    for i in range(3):
        max_value = max(suggested_diseases, key=suggested_diseases.get)
        suggested_diseases_renewed.append(max_value)
        del suggested_diseases[max_value]

    # Якщо наступна хвороба з найбільшою кількістю поінтів = попередній
    # то її теж додати в список на перевірку.

    while len(suggested_diseases) != 0:

        max_value = max(suggested_diseases, key=suggested_diseases.get)

        max_value_points = c.execute("SELECT points FROM Diseases WHERE name = ?", (max_value,))
        max_value_points = max_value_points.fetchone()[0]

        last_suggested_disease_points =  c.execute("SELECT points FROM Diseases WHERE name = ?",(suggested_diseases_renewed[-1],))
        last_suggested_disease_points = last_suggested_disease_points.fetchone()[0]

        if max_value_points < last_suggested_disease_points:
            break

        suggested_diseases_renewed.append(max_value)
        del suggested_diseases[max_value]


    return suggested_diseases_renewed



def get_filtered_symps (selected_symptoms, suggested_diseases):
    filtered_symps = set()

    for disease in suggested_diseases:
        id = c.execute("SELECT dis_id FROM Diseases WHERE name = ?", (disease,))
        id = c.fetchone()

        disease_symptoms = c.execute("SELECT symptom FROM symptoms WHERE group_id = ?", id)
        disease_symptoms = convert_to_set(disease_symptoms)

        filtered_symps.update(disease_symptoms)

    return (filtered_symps - set(selected_symptoms))



def set_precents(diagnose_suggestions):
    dictionary = dict()

    for disease in diagnose_suggestions:

        disease_id = c.execute("SELECT dis_id FROM Diseases WHERE name = ?", (disease,))
        disease_id = c.fetchone()[0]


        disease_symptoms = c.execute("SELECT symptom FROM symptoms WHERE group_id = ?", (disease_id,))
        disease_symptoms_count = len(convert_to_set(disease_symptoms))

        points = c.execute("SELECT points FROM Diseases WHERE name = ?", (disease,))
        points = c.fetchone()[0]

        info = c.execute("SELECT info FROM Diseases WHERE name = ?", (disease,))
        info = c.fetchall()[0][0].strip()


        dictionary[disease] = [floor((points/disease_symptoms_count) * 100), info]


    return dictionary




def symptom_select(symptom):
    c.execute("UPDATE symptoms SET points = 1 WHERE symptom = ?", (symptom,))
    group_ids = c.execute("SELECT group_id From symptoms WHERE symptom = ?", (symptom,))
    group_ids = c.fetchall()
    for id in group_ids:
        c.execute("UPDATE Diseases SET points = points+1 WHERE dis_id  = ?", (id[0],))



def symptom_deselect(symptom):
    c.execute("UPDATE symptoms SET points = 0 WHERE symptom = ?", (symptom,))
    group_ids = c.execute("SELECT group_id From symptoms WHERE symptom = ?", (symptom,))
    group_ids = c.fetchall()
    for id in group_ids:
        c.execute("UPDATE Diseases SET points = points-1 WHERE dis_id  = ?", (id[0],))


def new_symptoms_list(TextBox):
    lst = c.execute("SELECT symptom FROM symptoms")
    lst = convert_to_set(lst)
    lst = list(lst.difference(TextBox))


def get_symptoms(disease):
    id = c.execute("SELECT dis_id FROM Diseases WHERE name = ?", (disease,)).fetchone()
    symptoms = list(convert_to_set(c.execute("SELECT symptom FROM symptoms WHERE group_id = ?", id).fetchall()))
    return symptoms


# reset_func()
refresh()
conn.commit()





