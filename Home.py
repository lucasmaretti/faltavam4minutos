import streamlit as st

st.set_page_config(
    page_title = "Home",
    page_icon = "🏠")

st.image('./pages/7_jogadores.jpg')
st.image('./pages/4mins1.jpg')

st.sidebar.markdown('# Faltavam 4 minutos')
st.sidebar.markdown('## Python web app')
st.sidebar.markdown('## Aplicações de ciência de dados ao futebol')
#st.sidebar.image('./pages/2022_FIFA_World_Cup.png', use_column_width=True)
st.sidebar.image('./pages/footy.jpeg', use_column_width=True)
st.sidebar.markdown("""---""")

st.write('# Faltavam 4 minutos web app')
st.write('## Ciência de dados aplicada a dados de futebol')

st.markdown(""" 

O objetivo deste webapp é mostrar aplicações de ciência de dados ao futebol. Para tanto, exploraremos duas das principais etapas de um projeto de ciência de dados: análise exploratória (EDA) e aplicação de machine learning.

- A análise exploratória de dados se dará em cima dos dados abertos referentes à Copa do Mundo de 2022 no Qatar fornecidos pela empresa Statsbomb (seção "🏆 Brasil na Copa do Mundo 2022" no menu ao lado). O nome deste webapp - Faltavam 4 minutos - refere-se ao fatídico 9 de Dezembro de 2022 quando a seleção brasileira, com o jogo dominado e vencendo por 1x0 a Croácia com gol de Neymar, cedeu empate aos croatas em um lance inexplicável até hoje faltando 4 minutos para o fim da prorrogação.

- A aplicação de Machine Learning (seção 📈 Machine Learning no futebol: Expected Goals) mostra como o aprendizado de máquina é utilizado em dados de futebol através da sua métrica mais famosa: expected goals (xG). Aqui utilizamos outro conjunto de dados, referente às principais ligas europeias de clubes para a temporada 2017/2018 fornecido pela empresa Wyscout, e cujo desenvolvimento fez parte de um projeto de pesquisa do programa de mestrado em ciência de dados do MECAI-USP.
________________________
            
Recomenda-se utilizar o tema escuro (`Settings >> Theme >> Dark`) para que as cores nos gráficos tenham aprarência mais agradável à vista.

          
### Melhorias a serem implementadas:
* Mostrar como xG pode ser usado para tentar prever o resultado de uma partida
* Colocar todas as partidas do Brasil na Copa de 2022

### Recursos adicionais
- [Sobre análise de dados no futebol - parte 1](https://medium.com/zeroeum/sobre-o-uso-de-an%C3%A1lise-de-dados-no-futebol-parte-1-93cabb4fb873)
- [Sobre análise de dados no futebol - parte 2](https://medium.com/zeroeum/sobre-o-uso-de-dados-no-futebol-parte-2-5bab96b26e43)

            
#### Autor:
- Lucas Maretti: lucas.maretti@gmail.com
            """)