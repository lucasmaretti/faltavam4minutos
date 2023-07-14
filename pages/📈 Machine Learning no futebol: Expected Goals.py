import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title = 'Expected Goals', page_icon = '👤') #layout='wide',

st.sidebar.markdown('# Faltavam 4 minutos')
st.sidebar.markdown('## Python web app')
st.sidebar.markdown('## Aplicações de ciência de dados ao futebol')
st.sidebar.image('./pages/footy.jpeg', use_column_width=True)
st.sidebar.markdown("""---""")


#st.image('./logloss.jpg', caption='Perda logarítmica', width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.write('### Machine Learning aplicado aos dados de futebol: Entendendo Expected Goals (xG) na prática')
#st.write('### Ciência de dados aplicada aos dados da Copa do Mundo Qatar 2022')

st.markdown(""" 

A definição de xG é a probabilidade de que um chute resulte em gol em um jogo de futebol. Costuma ser baseado em medidas de muitos chutes dentro de uma mesma liga e temporada, ou agregando-se dados de diferentes ligas (estratégia usada neste projeto).\\
        
\\
Com base em uma base de dados de centenas de partidas e milhares de chutes que resultaram e não em gol, aplicamos técnicas de machine learning para converter isto em um problema da seguinte natureza: atribuímos uma probabilidade entre 0 e 1 a cada finalização feita por um jogador em um jogo (0 indicando nenhuma
possibilidade de a finalização ser um gol e 1 indicando certeza de gol). Com base nisto podemos tem um diagrama como o abaixo que mostra, para diferentes regiões da grande área, de onde é mais provável um chute resultar em gol.
Clubes de futebol podem usar o xG para avaliar e comparar o desempenho de jogadores. Ao analisar o xG de um jogador, os clubes podem avaliar sua capacidade de criar ou converter chances de gol. Isso ajuda a identificar jogadores que geram consistentemente chances de alta qualidade ou possuem excelentes habilidades de finalização.
\\
""")
                
st.image('./pages/squashxG.png', width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
            
st.markdown(""" Para mais informações sobre este tema recomendamos assistir a este [video](https://www.youtube.com/watch?v=Xc6IG9-Dt18).

\\
Em termos de machine learning, portanto, estamos falando de um problema de classificação.
O modelo disponibilizado aqui para simulação dos valores de xG foi desenvolvido na disciplina MAI5024 do programa de mestrado em ciência de dados do MECAI-USP. O repositório referente a este projeto com o detalhamento completo da modelagem pode ser acessado [aqui](https://github.com/lucasmaretti/football_analytics). \\
\\
Para o modelo final disponibilizado neste webapp 5 features mostraram-se mais importantes para um desempenho preditivo:
* Distância do chute ao gol em metros
* Ângulo do chute em radianos. O ângulo do chute é calculado a partir do triângulo cujos vértices estão na bola e nas duas traves do gol adversário. A figura abaixo ilustra isto:

""")           
st.image('./pages/angulo_chute.jpg', width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")

st.markdown(""" 

* Variável binária indicando se o chute partiu de um lance de bola parada
* Variável binária indicando se o chute partiu de um lance de contra-ataque
* Variável binária indicando se o chute partiu após uma enfiada de bola ('smart pass')\\
\\
**Simule abaixo diferentes valores para estas features para entender como elas contribuem para a probabilidade final de um chute resultar em gol**

""")

# Load the Random Forest Classifier model
model = joblib.load('rf_model.pkl')

# Define the feature names
feature_names = ['distance', 'angle', 'free_kick', 'counter_attack', 'prev_smart_pass']  # Replace with your actual feature names

# Create a function to predict the class label
def predict_class(features):
    # Preprocess the features if necessary
    # ...

    # Make predictions using the loaded model
    probabilities = model.predict_proba([features])

    # Return the predicted class label
    return probabilities[0][1]

# Create the Streamlit app
def main():
    st.write('### Modelo de Expected Goals (xG) usando Random Forest Classifier')
    st.write('Insira valores para as seguintes features:')

    # Create input fields for each feature
    inputs = []
    #for feature in feature_names:
    #    value = st.number_input(f'Enter {feature}:')
    #    inputs.append(value)

    distance = st.number_input("Distância do gol em metros (range: 1 - 100)", value=20.0, min_value = 0.68, max_value = 100.0)
    inputs.append(distance)
    angle = st.number_input("Angulo do chute em radianos (range: 0.03 - 3.1415)", value=0.5, min_value = 0.0275, max_value = 3.1415)
    inputs.append(angle)
    free_kick = st.number_input("Chute originado de uma bola parada? (0: não / 1: sim)", value = 0.0, step = 1.0, min_value = 0.0, max_value = 1.0)
    inputs.append(free_kick)
    counter_attack = st.number_input("Chute originado de um contra-ataque? (0: não / 1: sim)", value = 0.0, step = 1.0, min_value = 0.0, max_value = 1.0)
    inputs.append(counter_attack)
    prev_smart_pass = st.number_input("Chute originado de uma enfiada de bola? (0: não / 1: sim)", value = 0.0, step = 1.0, min_value = 0.0, max_value = 1.0) # , value = 0.0, step = 1.0, min_value = 0.0, max_value = 1.0
    inputs.append(prev_smart_pass)

    if st.button('Predict'):
        # Convert input values to a numpy array
        features = np.array(inputs)

        # Call the predict_class function to get the predicted class label
        prediction = predict_class(features)

        st.write(f'A probabilidade de se marcar um gol com os parâmetros selecionados é de: {100*prediction:.2f} %')

if __name__ == '__main__':
    main()
