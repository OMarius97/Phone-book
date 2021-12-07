from flask import Flask, render_template, request
import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-3JCOP6K;'
                      'Database=PHONEBOOKDB;'
                      'UID=DESKTOP-3JCOP6K/mariu;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

app = Flask(__name__)


# Homepage
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html')


# Search
@app.route('/Search', methods=['GET', 'POST'])
def search():
    search_by = []
    result = []

    if request.method == 'POST' and 'name' or 'lastname' or 'phone' in request.form:
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        search_by = [name, lastname, phone]
        contact = ['CONTACT_NAME', 'CONTACT_LASTNAME', 'CONTACT_PHONE']

    for element in search_by:
        if element:
            cursor.execute(f"""SELECT CONTACT_NAME, CONTACT_LASTNAME, CONTACT_NICKNAME, CONTACT_COMPANY, CONTACT_PHONE, 
            CONTACT_EMAIL, CONTACT_ADDRESS, CONTACT_BIRTHDAY FROM PHONEBOOK WHERE {contact[search_by.index(element)]}
             LIKE '%{element}%'""")
            for row in cursor:
                result.append(row)

    return render_template('Search.html', result=result)


# Add contact Page
@app.route('/Add', methods=['GET', 'POST'])
def add():
    data = ''

    if request.method == 'POST' and 'name' in request.form:
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        nickname = request.form.get('nickname')
        company = request.form.get('company')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        birthday = request.form.get('birthday')
        data = (name, lastname, nickname, company, phone, email, address, birthday)

        insert = ("INSERT INTO PHONEBOOK (CONTACT_NAME, CONTACT_LASTNAME, CONTACT_NICKNAME, CONTACT_COMPANY,"
                  "CONTACT_PHONE, CONTACT_EMAIL, CONTACT_ADDRESS, CONTACT_BIRTHDAY)"
                  "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")

        cursor.execute(insert, data)
        conn.commit()

    return render_template('Add.html', data=data)


@app.route('/Delete', methods=['GET', 'POST'])
def delete():
    search_by = []
    result = []
    confirm = False

    if request.method == 'POST' and 'name' in request.form:
        name = request.form.get('name')
        phone = request.form.get('phone')
        search_by = [name, phone]
        contact = ['CONTACT_NAME', 'CONTACT_PHONE']

    for element in search_by:
        if element:
            cursor.execute(f"""SELECT CONTACT_NAME, CONTACT_LASTNAME, CONTACT_NICKNAME, CONTACT_COMPANY, CONTACT_PHONE, 
            CONTACT_EMAIL, CONTACT_ADDRESS, CONTACT_BIRTHDAY FROM PHONEBOOK WHERE {contact[search_by.index(element)]}
             LIKE '%{element}%'""")
            for row in cursor:
                result.append(row)


    if request.method == 'POST' and 'name_confirm' and 'phone_confirm' in request.form:
        name_confirm = request.form.get('name_confirm')
        phone_confirm = request.form.get('phone_confirm')

        cursor.execute(f"""DELETE FROM PHONEBOOK WHERE CONTACT_NAME = '{name_confirm}'
        AND CONTACT_PHONE = '{phone_confirm}'""")
        conn.commit()
        confirm = True


    return render_template('Delete.html', result=result, confirm=confirm)


def run():
    if __name__ == '__main__':
        app.run(debug=True)
