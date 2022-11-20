# Importation des librairies 
import streamlit as st
import pandas as pd

# Nom de l'app streamlit
st.title('Mini Projet 1 - PYTHON')

# Recupération du fichier Excel (on peut le changer avec le fichier qui contient 700 Chercheurs)
xl_file = st.secrets["public_gsheets_url"]

# Préparation et nettoyage des dataframes (Deux DF la 1ere principale, la 2éme contient que les membres des structures de recherche partenaires)
df = pd.read_excel(xl_file, usecols=['Id', 'Nom','Prenom','Université','Grade',	'Spécialité','Structure de recherche Porteuse'])
df_1=df.dropna().reset_index(drop=True)
df_1.Id = df_1.Id.astype(int)
df2 = pd.read_excel(xl_file, usecols=['Nom et Prénom'	,'Grade',	'Spécialité','Intitulé de la structure'], header=1)
df3 = pd.read_excel(xl_file, usecols='L,M')
df4=df3.dropna().reset_index(drop=True)
df_3 = df4.rename(columns={"Unnamed: 12":"Nombre"})

# Visualisation des dataframes
#with st.echo() :
 #   print(df_1.to_string(index=False))
#    print(df2.to_string(index=False))

# Creation de la 2éme Dataframe
list_article = []
list_communications = []
list_these = []
for i in range(0, len(df_3), 3):
    list_article.append(int(df_3['Nombre'][i]))

for i in range(1, len(df_3), 3):
    list_communications.append(int(df_3['Nombre'][i]))

for i in range(2, len(df_3), 3):
    list_these.append(int(df_3['Nombre'][i]))
    
df_1['Articles']=list_article
df_1['Communications']=list_communications
df_1['Theses']=list_these
df_stru = pd.read_excel(xl_file, usecols='A', header=1)
df_stru1 = df_stru['Unnamed: 0'].interpolate(method='pad')
df2['id']=df_stru1
df2 = df2.dropna()


# Fonction pour récupérer le total des membres d'une structure
def count_members(i):
    count = 0
    list_membres = []
    for t in df2.index:
        if df2.id[t]==i:
            list_membres.append(df2.id[t])
    
    count = len(list_membres)
    return count


# Fonction pour récupérer la liste des structures associée à un chercheur
def list_structure(i):
    list_structure = list()
    for t in df2.index:
        if df2.id[t]==i:
            list_structure.append(df2['Intitulé de la structure'][t])
    
    list_structure = list(dict.fromkeys(list_structure))
    chaine = str(list_structure)
    chaine = chaine.replace('[','')
    chaine = chaine.replace(']','')
    chaine = chaine.replace('\'','')
    return chaine


# Fonction pour récupérer la liste des specialtés associée d'un chercheur
def list_specialite(i):
    list_specialite = list()
    for t in df2.index:
        if df2.id[t]==i:
            list_specialite.append(df2['Spécialité'][t])
    
    list_specialite = list(dict.fromkeys(list_specialite))
    chaine = str(list_specialite)
    chaine = chaine.replace('[','')
    chaine = chaine.replace(']','')
    chaine = chaine.replace('\'','')
    return chaine

# Fonction pour afficher les informations d'un chercheur selon son id 
def afficher_info(id):
    st.markdown(f'#### id : {id}')
    st.markdown(f'### Nom : {df_1.Nom[id-1]}')
    st.markdown(f'### Prenom : {df_1.Prenom[id-1]} ')
    st.markdown(f'### Université : {df_1.Université[id-1]} ')
    st.markdown(f'### Grade : {df_1.Grade[id-1]} ')
    st.markdown(f'### Spécialité : {df_1.Spécialité[id-1]} ')
    st.markdown(f'### Structure de recherche Porteuse : {df_1["Structure de recherche Porteuse"][id-1]} ')
    st.markdown(f'### Membre des structures de recherche partenaires :')
    struct_df(id)
    st.markdown('### Publications Scientifiques : ')
    st.markdown(f'#### Nombre des articles : {df_1["Articles"][id-1]}') 
    st.markdown(f'#### Nombre des communications : {df_1["Communications"][id-1]}') 
    st.markdown(f'#### Nombre de thèses encadrées : {df_1["Theses"][id-1]}')


# Fonction pour crée un e dataframe contenant les membres des structures de recherche partenaires
def struct_df(id):
    df = df2[df2['id']==id]
    df = df[['Nom et Prénom','Grade','Spécialité','Intitulé de la structure']].copy()
    st.dataframe(df)

#st.dataframe(data=df_1, width=None, height=None, use_container_width=True)
idf = int(df_1.index)

# Creation des tabs streamlit
tabs1, tabs2, tabs3, tabs4, tabs5, tabs6, tabs7, tabs8, tabs9 = st.tabs(['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6', 'Question 7', 'Question 8', 'Question 9'])

# Reponse pour chaque question du miniprojet
with tabs1 :
    st.markdown('### Donner le nombre d’articles pour chaque chercheur ')
    with st.echo():
        for i in df_1.index:
            st.markdown(f"##### {df_1['Nom'][i]}  {df_1['Prenom'][i]} = {df_1['Articles'][i]} articles")


with tabs2 :
    st.markdown('### Donner le nombre de communications pour chaque chercheur')
    with st.echo():
        for i in df_1.index:
            st.markdown(f"##### {df_1['Nom'][i]}  {df_1['Prenom'][i]} = {df_1['Communications'][i]} communications")


with tabs3 :
    st.markdown('### Donner le nombre de thèses encadrées pour chaque chercheur')
    with st.echo():
        for i in df_1.index:
            st.markdown(f"##### {df_1['Nom'][i]}  {df_1['Prenom'][i]} = {df_1['Theses'][i]} Théses")


with tabs4 :
    st.markdown('### Donner le total des publications scientifiques')
    with st.echo():
        for i in df_1.index:
            st.markdown(f"##### {df_1['Nom'][i]}  {df_1['Prenom'][i]} = {df_1['Articles'][i]+df_1['Communications'][i]+df_1['Theses'][i]} publications")


with tabs5 :
    st.markdown('### Donner le nombre des membres des structures de recherche partenaires pour chaque chercheur')
    with st.echo():
        for i in df_1.index:
            st.markdown(f"##### {df_1['Nom'][i]}  {df_1['Prenom'][i]} = {count_members(i+1)} membres")


with tabs6 :
    st.markdown('### Lister les intitulés de la structure pour chaque chercheur (sans les dupliqués)')
    with st.echo():
        for i in df_1.index:
            st.markdown(f"##### {df_1['Nom'][i]}  {df_1['Prenom'][i]} = {list_structure(i+1)}")

with tabs7 :
    st.markdown('### Lister les Spécialités de la structure pour chaque chercheur (sans les dupliqués)')
    with st.echo():
        for i in df_1.index:
            st.markdown(f"##### {df_1['Nom'][i]}  {df_1['Prenom'][i]} = {list_specialite(i+1)}")


with tabs8 :
    st.markdown('### Effectuer une recherche par le champ Id et afficher le nom et le prénom du chercheur')
    id = st.number_input('Selectionner l\'id ', 1, idf, key=1)
    st.markdown(f'####  id : {id} => {df_1.Nom[id-1]} {df_1.Prenom[id-1]}')

with tabs9 :
    st.markdown('### Effectuer une recherche par le champ Id et afficher ses informations')
    id = st.number_input('Selectionner l\'id ', 1, idf, key=2)
    afficher_info(id)



   
