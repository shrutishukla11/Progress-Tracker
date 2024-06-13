import streamlit_authenticator as stauth
from deta import Deta
import streamlit as st
from dotenv import load_dotenv
import os
from openpyxl import Workbook

# Fetching credentials
load_dotenv('.env')
DETA_KEY = os.getenv('DETA_KEY')
deta = Deta(DETA_KEY)
db = deta.Base("users_db")


def insert_user(username, name, password):
    return db.put({"key": username, "name": name, "password": password})


def fetch_all_users():
    res = db.fetch()
    return res.items


users = fetch_all_users()
usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
passwords = [user["password"] for user in users]
hashed_passwords = stauth.Hasher(passwords).generate()
credentials = {
    "usernames": {

    }
}

# Authentication
for i in range(len(usernames)):
    credentials['usernames'][usernames[i]] = {'name': names[i], 'password': hashed_passwords[i]}
authenticator = stauth.Authenticate(credentials,
                                    "YoutTrack", "abcdef", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.info('Please login to track your progress')

if authentication_status == False or authentication_status == None:

    with st.expander('NOT A USER YET?', expanded=False):
        st.header('Register for YouTrack')
        name_user = st.text_input('Name')
        username = st.text_input('username')
        password = st.text_input('Password', type='password', placeholder='password must be atleast 8 characters')
        if len(password) < 8:
            valid2 = False
        else:
            valid2 = True
        confirm_pass = st.text_input('Confirm password', type='password')

        if confirm_pass == password:
            valid = True
            pass
        else:
            valid = False
            st.write('passwords do not match')

        if st.button('Register') and valid and valid2:
            insert_user(username, name_user, password)
            st.success('Registered Successfully,scroll up and login ')

if authentication_status ==  True:
    # Home page starts here
    st.header(f'Welcome {name}')
    authenticator.logout('Log out', 'sidebar')
