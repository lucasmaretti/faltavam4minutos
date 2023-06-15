import streamlit as st

st.set_page_config(
    page_title = "Home",
    page_icon = "🏠")


st.sidebar.markdown('# Faltavam só 4 minutos')
st.sidebar.markdown('## Python web app')
st.sidebar.markdown('## Aplicações de ciência de dados ao futebol')
#st.sidebar.image('./pages/2022_FIFA_World_Cup.png', use_column_width=True)
st.sidebar.image('./pages/footy.jpeg', use_column_width=True)
st.sidebar.markdown("""---""")

st.write('# Faltavam só 4 minutos web app')
st.write('## Ciência de dados aplicada a dados de futebol')

st.markdown(""" 

**PT/BR**: O objetivo deste webapp é mostrar na prática aplicações de ciência de dados ao futebol. Para tanto, exploraremos duas das principais etapas de um projeto de ciência de dados: análise exploratória (EDA) e aplicação de machine learning.\\
\\
A análise exploratória de dados se dará em cima dos dados abertos referentes à Copa do Mundo de 2022 no Qatar fornecidos pela empresa Statsbomb (seção "🏆 Brasil na Copa do Mundo 2022" no menu ao lado). O nome deste webapp - Faltavam só 4 minutos - refere-se ao fatídico 9 de Dezembro de 2022 quando a seleção brasileira, com o jogo dominado e vencendo por 1x0 a Croácia com gol de Neymar, cedeu empate aos croatas em um lance inexplicável até hoje faltando 4 minutos para o fim da prorrogação.\\
A aplicação de Machine Learning (seção 📈 Machine Learning no futebol: Expected Goals) é referente a um outro conjunto de dados referentes às principais ligas europeias para a temporada 2017/2018 fornecido pela empresa Wyscout, cujo desenvolvimento fez parte de um projeto de pesquisa do programa de mestrado em ciência de dados do MECAI-USP
\\
________________________
            
Recomenda-se utilizar o tema escuro (`Settings >> Theme >> Dark`) para que as cores nos gráficos tenham aprarência mais agradável à vista.

          
### Como navegar neste webapp
* **Brasil na copa**:\\
Análise exploratória de dados mostrando como a ciência de dados pode ajudar a analisar uma partida de futebol\\
Nesta seção usamos dados da Copa do Mundo de 2022 no Qatar fornecido pela empresa Statsbomb.

* **Expected Goals**: \\
Aqui mostraremos como Machine Learning pode ser aplicado ao futebol através da sua métrica mais famosa: Expected Goals (xG).\\
Nesta seção você poderá simular a probabilidade de um chute resultar em gol com base em algumas features importantes encontradas pelo nosso modelo

          
### Melhorias a serem implementadas:
* Mostrar como xG pode ser usado para tentar prever o resultado de uma partida
* Colocar todas as partidas do Brasil na Copa de 2022

### Recursos adicionais
- [Sobre análise de dados no futebol - parte 1](https://medium.com/zeroeum/sobre-o-uso-de-an%C3%A1lise-de-dados-no-futebol-parte-1-93cabb4fb873)
- [Sobre análise de dados no futebol - parte 2](https://medium.com/zeroeum/sobre-o-uso-de-dados-no-futebol-parte-2-5bab96b26e43)

            
#### Autor:
- Lucas Maretti: lucas.maretti@gmail.com
            """)