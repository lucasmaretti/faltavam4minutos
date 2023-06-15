import streamlit as st
from WorldCup import WorldCup as w

st.set_option('deprecation.showPyplotGlobalUse', False)

st.set_page_config(
    page_title = "Brasil na Copa do Mundo 2022",
    page_icon = "🏆")


#st.sidebar.markdown('# Faltavam só 4 minutos app')

options = ['Desempenho geral (todos jogos)', 'Brasil x Croácia']
#for game in df['match_name'].unique():
#    options.append(game)


selected_game = st.sidebar.selectbox(label='Escolha o jogo', 
                       options=options)

st.sidebar.image('./pages/2022_FIFA_World_Cup.png')
#st.sidebar.image('./pages/footy.jpeg', use_column_width=True)
st.sidebar.markdown("""---""")

match_ids = [3857258, 3857269, 3869420, 3869253, 3857280]
brasa = w('Brazil', match_ids)
df = brasa.get_data()


if selected_game == 'Desempenho geral (todos jogos)':

    brasa_danger_passes = brasa.danger_passes()
    brasa_shots = brasa.get_shots()
    danger_passes_count = brasa.danger_pass_count(brasa_danger_passes)

    # with st.container():
    #     col1, col2 = st.columns(2)
    
    # with col1:
    #     st.metric(label='',
    #         value=f'{selected_game}')
    #     with st.container():
    #         col2, col3 = st.columns(2)
    #         with col2:
    #             # st.markdown('#### Team and Position')
    #             st.pyplot(heatmap_danger_passes, use_container_width=True)
    #         with col3:
    #             st.pyplot(heatmap_shots)
    
    st.write('### Desempenho geral do Brasil na Copa de 2022 levando-se em conta os 5 jogos')
    
    st.markdown(""" 

    Uma métrica comum ao se analisar um jogo de futebol usando dados é o passe perigoso (danger pass). Esse é um passe que foi feito por um jogador e que, dentro de uma janela de tempo 
    pré-definida, resulta em uma finalização ao gol. Para esta análise usamos uma janela de 10 segundos, ou seja, cada passe que resultou em uma finalização a gol em até 10 segundos após o passe ser feito conta
    como um passe perigoso. Este exemplo ilustra bem um paradigma que quem trabalha com dados enfrenta: **hipóteses sempre precisam ser feitas** e virão com prós e contras. No nosso caso,
    poderemos deixar de contar passes que geraram finalizações com mais tempo. Mas revendo os jogos e analisando as finalizações entendemos que 10 segundos é uma janela adequada. \\
    \\
    Com base nesta lista de passes perigosos, podemos ver quem foram os jogadores brasileiros que mais contribuíram com passes perigosos na jornada do time na Copa:

    """)  
    st.pyplot(danger_passes_count)

    st.markdown(""" 

    A métrica desenvolvida foi passes/jogo. Em um campeonato curto como a copa do mundo essa métrica favorece jogadores como Dani Alves, que jogou apenas 2 jogos. Mas serve para atestar a regularidade de jogadores como Raphinha, que tendo disputado os 5 jogos teve média de 1 passe perigoso por jogo.
    Em seguida, podemos ver de onde no campo saíram estes passes perigosos com base no mapa de calor a seguir:

    """)  

    st.pyplot(brasa.heatmap_danger_passes(brasa_danger_passes))

    st.markdown(""" 

    Olhando os 5 jogos como um todo podemos ver que o time brasileiro tentou muitas jogadas pelo centro com uma tendência ao lado direito do ataque. Foi do lado direito também de onde saíram a maioria dos cruzamentos de linha de fundo, apesar de não ser um recurso muito utilizado.\\
    \\
    Os exemplos a seguir ajudam a ilustrar a força das jogadas pelo lado direito: o primeiro lance é contra a [Suíça](https://www.youtube.com/watch?v=nexIg1Xygg8&t=14s), o segundo contra a [Sérvia](https://youtu.be/kL0IkvLrQLM?t=15)
    e o último contra [Coreia do Sul](https://youtu.be/c0-ZhEkEFtA?t=48).\\
    \\
    Podemos também plotar um mapa de calor (heatmap) dos chutes do Brasil nos 5 jogos da Copa. O tamanho dos ícones é proporcional ao xG do chute, que seria a probabilidade deste chute resultar em gol (para mais detalhes veja a seção sobre Machine Learning neste webapp).
    É possível notar que tanto o time priorizou chutar de dentro da área, como nenhum gol na Copa foi marcado de fora da área.

    """)  

    st.pyplot(brasa.heatmap_shots(brasa_shots))

elif selected_game == 'Brasil x Croácia':

    st.write('### Brasil x Croácia')
    
    st.image('./pages/wagnermoura.jpg')

    st.markdown(""" 

    Olhando-se individualmente cada jogo algumas outras análises interessantes são possíveis. 
    Uma delas é plotar a rede de passes dos jogadores. Com este gráfico podemos saber tanto o posicionamento médio
    dos jogadores no campo durante a partida bem como com quais jogadores cada um mais interagiu. É mais comum plotar a rede de passes jogo a jogo pois no futebol moderno os times tendem a adequar seu posicionamento ao adversário.
    
    
    """)  
    match_id = 3869420
    brasa_passes_cro = brasa.get_passes(match_id)
    st.pyplot(brasa.plot_passing_network(brasa_passes_cro))

    st.markdown(""" 

    **Como interpretar esta visualização**: o ícone indicativo de cada jogador mostra seu posicionamento médio no campo durante a partida;
    o tamanho do ícone é proporcional ao quanto este jogador foi acionado (isto é, quantos passes recebeu) e a intensidade das linhas que conectam os ícones dos jogadores
    representam a força de interação entre os jogadores (se trocaram muitos passes entre si).\\
    \\
    Neste exemplo podemos ver que nesta partida específica Richarlison foi muito pouco acionado; nas vezes em que foi, recebeu passes apenas de Casemiro e Paquetá, ao contrário de outros jogos em que ele interagiu muito mais com os outros atacantes.\\
    \\
    Em contraste, a rede de passes da Croácia pode ajudar a ilustrar a estatrégia do time contra o Brasil:


    """) 

    cro = w('Croatia', [match_id])
    cro_passes = cro.get_passes(match_id)
    st.pyplot(cro.plot_passing_network(cro_passes))

    st.markdown(""" 

    O time croata congestionou o meio-campo, invalidando a troca de passes entre os jogadores brasileiros, que não souberam muito bem como se desvencilhar.\\
    \\
    Olhando-se o mapa de passes e chutes do time brasileiro no jogo, podemos ver melhor quão bem a Croácia conseguiu "travar" o jogo.


    """) 

    brasa = w('Brazil', [match_id])
    brasa_danger_passes = brasa.danger_passes()
    st.pyplot(brasa.heatmap_danger_passes(brasa_danger_passes)) 

    brasa_shots = brasa.get_shots()
    st.pyplot(brasa.heatmap_shots(brasa_shots))

    st.markdown(""" 

    O lado direito, que funcionou tão nos demais jogos da copa, neste dia não conseguiu levar perigo ao gol croata.
    Olhando-se também a relação entre passes perigosos e finalizações, é possível notar que as finalizações no jogo saíram de tentativas de jogada individual.
    Este [lance de Neymar](https://youtu.be/0uau3vAOwKQ?t=67) ajuda a ilustrar isso.


    """) 