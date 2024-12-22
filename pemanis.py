from keperluan_modul import *

def menyapa_user():
    pesan = st.toast('Knock.. Knock..')
    time.sleep(2)
    pesan.toast('🚪 Open the door...')
    time.sleep(2)
    pesan.toast('😄 WELCOME TO GEMILANG`S WEBAPP! 😄', icon = "🎉")

def ucapan():        
    pesan = st.toast('Hello! How Are You?', icon = '😊')    
    time.sleep(2)
    pesan.toast('Gwenchana-yo?', icon = "🤕")    
    time.sleep(2)
    pesan.toast('Have a nice day', icon='😇')    
    time.sleep(2)
    pesan.toast('😄 ENJOY WITH OUR APP! 😄', icon = "🎉")

def sukses():
    st.balloons()
    pesan = st.toast('BIG THANKS!', icon='🥰') 
    time.sleep(2)
    pesan.toast('Thank you for using our service', icon='🤗')    

def profil():    
    time.sleep(5)
    pesan = st.toast('Hallo!', icon='🤗')    
    time.sleep(2)
    pesan.toast('We are behind the scene of', icon='😇')
    time.sleep(2)
    pesan.toast('😄 GEMILANG! 😄', icon = "🎉")

