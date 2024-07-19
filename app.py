import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.write("""
# Building and Housing
Bu ma'lumotlar AQSH ning San-Fransisko shtatida qurilish va ta'mirlash ishlari uchun berilgan **ruhsatnomalar**

| Ruhsatnoma turi    | Soni |
| -------- | ------- |
| Kichik va oddiy tuzatishlar  | 363690    |
| Qurilish yoki ta'mirlash | 52956     |
| Yog'och ramkali yangi qurilishlar uchun   | 3    |
| Reklama taxtalarini o'rnatish uchun   | 1    |
""")


df = pd.read_csv("finalData3.csv")

with st.sidebar:
    range_year = st.slider(
        "Yilni Tanlang",
        min_value=1982,
        max_value=2025,
        value=(1982, 2024)
    )
    st.write("Tanlangan diapazon:", range_year)

    pBins = st.select_slider(
        'Okruglar Soni',
        options=list(range(0, 12)),
        value=11
    )
    st.write('Districts:', pBins)




    
data = df[(df['Permit Creation Year'] > range_year[0])&(df['Permit Creation Year'] < range_year[1])]

# har 10 yillikda baholash
tenYears1 = (df['Permit Creation Date'] >= '1983') & (df['Permit Creation Date'] < '1993')
tenYears2 = (df['Permit Creation Date'] >= '1993') & (df['Permit Creation Date'] < '2003')
tenYears3 = (df['Permit Creation Date'] >= '2003') & (df['Permit Creation Date'] < '2013')
tenYears4 = (df['Permit Creation Date'] >= '2013') & (df['Permit Creation Date'] < '2024')

st.title("Har 10 yillikda qurilishni baholanishi")
fig, ([ax0, ax1], [ax2, ax3]) = plt.subplots(nrows=2, ncols=2, sharey=True, figsize=(8, 8))
# sns.barplot(df[tenYears1][(df['Estimated Cost'] > 100)& (df['Revised Cost'] > 100)][['Estimated Cost', 'Revised Cost']], ci=None, ax=ax0)
# sns.barplot(df[tenYears1][(df['Estimated Cost'] > 100)& (df['Revised Cost'] > 100)][['Estimated Cost', 'Revised Cost']], ci=None, ax=ax1)
# sns.barplot(df[tenYears1][(df['Estimated Cost'] > 100)& (df['Revised Cost'] > 100)][['Estimated Cost', 'Revised Cost']], ci=None, ax=ax2)
# sns.barplot(df[tenYears1][(df['Estimated Cost'] > 100)& (df['Revised Cost'] > 100)][['Estimated Cost', 'Revised Cost']], ci=None, ax=ax3)
sns.barplot(df[tenYears1][['Estimated Cost', 'Revised Cost']], errorbar=None, ax=ax0)
sns.barplot(df[tenYears2][['Estimated Cost', 'Revised Cost']], errorbar=None, ax=ax1)
sns.barplot(df[tenYears3][['Estimated Cost', 'Revised Cost']], errorbar=None, ax=ax2)
sns.barplot(df[tenYears4][['Estimated Cost', 'Revised Cost']], errorbar=None, ax=ax3)
ax0.set_title('1983-1992')
ax1.set_title('1993-2002')
ax2.set_title('2003-2012')
ax3.set_title('2013-2023')
st.pyplot(fig)




# estimated, revised barplot
st.title("Umumiy narxlarni o'rtachasi")
fig, ax = plt.subplots()
sns.set_style('dark')
sns.barplot(data[['Estimated Cost', 'Revised Cost']], ax=ax)
st.pyplot(fig)



# Har bir yilga ruhsatnomalar soni (hist)
sBins = st.select_slider(
    'Histplot bins',
    options=(list(range(1, 31))),
    value=25
)
st.write('Hist bins:', sBins)

fig, ax = plt.subplots()
sns.set_style('dark')
sns.histplot(x='Permit Creation Year', data=data, bins=sBins, ax=ax)
ax.set_title('Har bir yilgi ruhsatnomalar soni')
st.pyplot(fig)





fig, ax = plt.subplots()
sns.scatterplot(x='Permit Creation Year', y='Number of Existing Stories', data=df, ax=ax, hue='Permit Type Definition')
ax.set_ylabel('Qavatlar soni')
ax.set_xlabel('Yil')
st.pyplot(fig)



# pie chart okruglar uchun
dct = df[df['Supervisor District'] != 'Missing']['Supervisor District'].value_counts().to_dict()
pieSizes = list(dct.values())
pieLabels = list(dct.keys())
fig, ax = plt.subplots()
ax.pie(pieSizes[:pBins], labels=pieLabels[:pBins], autopct='%1.1f%%')
ax.set_title('SF districts')
st.pyplot(fig)



fig, ax = plt.subplots()
corr_cols = ['Permit Type', 'Revised Cost', 'Proposed Units', 'Number of Proposed Stories', 'Districts', 'Duration', 'Permit Creation Year']
tabb = df[corr_cols].corr(numeric_only=True)
sns.heatmap(tabb, annot=True, cmap='YlGnBu', fmt='.3f', ax=ax)
st.pyplot(fig)


# qavatlar
# fig, ax = plt.subplots()
# sns.scatterplot(x='Permit Creation Year', y='Number of Existing Stories', data=df, ax=ax)
# ax.set_ylabel('Qavatlar soni')
# ax.set_xlabel('Yil')


# st.dataframe(df, hide_index=True)