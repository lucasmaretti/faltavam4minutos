# soccer analytics imports

import mplsoccer as mpl
from mplsoccer import Pitch, Sbopen, VerticalPitch

# data wrangling imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



class WorldCup():
    
    
    def __init__(
        self,
        team: str, 
        match_ids: list
                )-> None:
        
        
        self.team = team
        self.match_ids = match_ids
        self.parser = Sbopen()
        self.red = [x/256 for x in (215,25,28)]
        self.blue = [x/256 for x in (44,123,182)]
        self.nomes = {
                    "Carlos Henrique Casimiro": "Casimiro",
                    "Thiago Emiliano da Silva": "T. Silva",
                    "Marcos Aoás Corrêa": "Marquinhos",
                    "Éder Gabriel Militão": "Militao",
                    'Danilo Luiz da Silva': "Danilo", 
                    'Neymar da Silva Santos Junior': "Neymar",
                    'Raphael Dias Belloli': "Raphinha", 
                    'Lucas Tolentino Coelho de Lima': "L. Paquetá",
                    'Alisson Ramsés Becker': "Alisson", 
                    'Richarlison de Andrade': "Richarlison",
                    'Vinícius José Paixão de Oliveira Júnior': "Vini Jr",
                    'Antony Matheus dos Santos': "Antony", 
                    'Rodrygo Silva de Goes': "Rodrygo",
                    'Pedro Guilherme Abreu dos Santos': "Pedro",
                    'Frederico Rodrigues Santos': "Fred",
                    'Alex Sandro Lobo Silva': "Alex Sandro",
                    'Daniel Alves da Silva' : "Dani Alves",
                    'Gabriel Teodoro Martinelli Silva': "Gabriel Martinelli"
    }
    
        self.times = {
        'Brazil' : 'Brasil',
        'Croatia': 'Croácia',
        'Switzerland': 'Suíça',
        'Serbia': 'Sérvia',
        'South Korea': 'Coreia do Sul'
    }
        
        self.opponent = {
            3857258: 'Sérvia', 
            3857269: 'Suíça', 
            3869420: 'Croácia', 
            3869253: 'Coreia do Sul', 
            3857280: 'Camarões'
            
        }
        
        self.match_name = {
            3857258: 'Brasil x Sérvia', 
            3857269: 'Brasil x Suíça', 
            3869420: 'Brasil x Croácia', 
            3869253: 'Brasil x Coreia do Sul', 
            3857280: 'Brasil x Camarões'
            
        }
        
        
    def get_data(self) -> pd.DataFrame:
        parser = Sbopen()
        matches = parser.match(competition_id=43, season_id=106) 
        matches = matches[matches['match_id'].isin(self.match_ids)]
        matches['opponent'] = matches['match_id'].map(self.match_name)
        return matches
    
    def __get_no_games(self):
        no_games = len(self.match_ids)
        return no_games
    
    def get_passes(self, match_id):
        df, related, freeze, tactics = self.parser.event(match_id)
        #check for index of first sub
        sub = df.loc[df["type_name"] == "Substitution"].loc[df["team_name"] == self.team].iloc[0]["index"]
        #make df with successfull passes by England until the first substitution
        mask = (df.type_name == 'Pass') & (df.team_name == self.team) & (df.index < sub) & (df.outcome_name.isnull()) & (df.sub_type_name != "Throw-in")
        df_pass = df.loc[mask, ['x', 'y', 'end_x', 'end_y', "player_name", "pass_recipient_name", "match_id"]]
        
        if self.team == 'Brazil':
            df_pass['player_name'] = df_pass['player_name'].map(self.nomes)
            df_pass['pass_recipient_name'] = df_pass['pass_recipient_name'].map(self.nomes)
        return df_pass
    
    def danger_passes(self, shot_window:int = 5, xg:float = 0.1) -> pd.DataFrame:
        no_games = len(self.match_ids)
        #declare an empty dataframe
        df_danger_passes = pd.DataFrame()
        for idx in self.match_ids:
            #open the event data from this game 
            df = self.parser.event(idx)[0]
            for period in [1, 2]:
                #keep only accurate passes by England that were not set pieces in this period
                mask_pass = (df.team_name == self.team) & (df.type_name == "Pass") & (df.outcome_name.isnull()) & (df.period == period) & (df.sub_type_name.isnull())
                #keep only necessary columns
                passes = df.loc[mask_pass, ["x", "y", "end_x", "end_y", "minute", "second", "player_name", "match_id"]]
                #keep only Shots by England in this period
                mask_shot = (df.team_name == self.team) & (df.type_name == "Shot") & (df.period == period) & (df.shot_statsbomb_xg > xg)
                #keep only necessary columns
                shots = df.loc[mask_shot, ["minute", "second"]]
                #convert time to seconds
                shot_times = shots['minute']*60+shots['second']
                #find starts of the window
                shot_start = shot_times - shot_window
                #condition to avoid negative shot starts
                shot_start = shot_start.apply(lambda i: i if i>0 else (period-1)*45)
                #convert to seconds
                pass_times = passes['minute']*60+passes['second']
                #check if pass is in any of the windows for this half
                pass_to_shot = pass_times.apply(lambda x: True in ((shot_start < x) & (x < shot_times)).unique())

                #keep only danger passes
                danger_passes_period = passes.loc[pass_to_shot]
                #concatenate dataframe with a previous one to keep danger passes from the whole tournament
                df_danger_passes = pd.concat([df_danger_passes, danger_passes_period])
        df_danger_passes['player_name'] = df_danger_passes['player_name'].map(self.nomes)        
        return df_danger_passes
    
    
    def danger_pass_count(self, df_danger_passes):
        pass_count = df_danger_passes.groupby(["player_name"]).x.count()/self.__get_no_games()
        pass_count = pass_count.sort_values(ascending = False)
        #make a histogram
        ax = pass_count.plot.bar(pass_count)
        #make legend
        ax.set_xlabel("")
        plt.xticks(rotation = 75)
        ax.set_ylabel("Número de passes perigosos por jogo")
        plt.show()
        
    def danger_pass_count1(self, df_danger_passes):
        pass_count = df_danger_passes.groupby(["player_name"]).x.count() / self.__get_no_games()
        pass_count = pass_count.sort_values(ascending=False)

        # Create a figure with a transparent background
        fig, ax = plt.subplots(facecolor='none')

        # Plot the bar chart
        pass_count.plot.bar(ax=ax)

        # Set the x-axis label and rotate the tick labels
        ax.set_xlabel("")
        plt.xticks(rotation=75)

        # Set the y-axis label
        ax.set_ylabel("Número de passes perigosos por jogo")

        # Show the plot
        plt.show()
    

    def heatmap_danger_passes(self, df_danger_passes):
            
        #plot vertical pitch
        pitch = VerticalPitch(pitch_color = 'grass', line_zorder=2, line_color='black', half = True)
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                                 endnote_height=0.04, title_space=0, endnote_space=0)
        #get the 2D histogram 
        bin_statistic = pitch.bin_statistic(df_danger_passes.x, df_danger_passes.y, statistic='count', bins=(6, 5), normalize=False)
        #normalize by number of games
        bin_statistic["statistic"] = bin_statistic["statistic"]/self.__get_no_games()
        #make a heatmap
        pcm  = pitch.heatmap(bin_statistic, cmap='Reds', edgecolor='grey', ax=ax['pitch'])
        #legend to our plot
        ax_cbar = fig.add_axes((1, 0.093, 0.03, 0.786))
        cbar = plt.colorbar(pcm, cax=ax_cbar)
        fig.suptitle(f'Passes que levaram a finalizações perigosas da seleção: {self.times[self.team]}', fontsize = 20)
        plt.show()
        
        
    def get_shots(self):
        
        allgames = pd.DataFrame()
        for match_id in self.match_ids:
            df, related, freeze, tactics = self.parser.event(match_id)
            allgames = pd.concat([allgames, df])
            
        shots = allgames[(allgames['type_name'] == "Shot") & 
           (allgames['team_name'] == self.team) &
           (allgames['sub_type_name'] != "Penalty")]
        
        return shots
    
    def heatmap_shots(self, shots):
        
        x, y = np.array(shots.x), np.array(shots.y)
        xg = np.array(shots['shot_statsbomb_xg'].tolist())
        goal = [self.red if g == "Goal" else 'black' for g in shots['outcome_name'].to_list()]
        
        red_patch = mpatches.Patch(color='red', label='Gol')
        blue_patch = mpatches.Patch(color='black', label='Não Gol')

        pitch = mpl.VerticalPitch(pitch_color='grass', line_color='white', stripe=True, half = True)
        fig, ax = pitch.draw(figsize=(9, 6))
        p = pitch.scatter(x, y, s=xg*100, c=goal, alpha=0.8, ax=ax)

        #txt = ax.text(x=40, y=77, s=f'Todos os chutes do {self.times[self.team]}\nna Copa do Mundo',
        #              size=10,
        #              va='center', ha='center')

        ax.legend(handles = [red_patch, blue_patch], loc='upper right')
        
    def plot_passing_network(self, df_pass):
        scatter_df = pd.DataFrame()
        for i, name in enumerate(df_pass["player_name"].unique()):
            passx = df_pass.loc[df_pass["player_name"] == name]["x"].to_numpy()
            recx = df_pass.loc[df_pass["pass_recipient_name"] == name]["end_x"].to_numpy()
            passy = df_pass.loc[df_pass["player_name"] == name]["y"].to_numpy()
            recy = df_pass.loc[df_pass["pass_recipient_name"] == name]["end_y"].to_numpy()
            scatter_df.at[i, "player_name"] = name
            #make sure that x and y location for each circle representing the player is the average of passes and receptions
            scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
            scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
            #calculate number of passes
            scatter_df.at[i, "no"] = df_pass.loc[df_pass["player_name"] == name].count().iloc[0]

        #adjust the size of a circle so that the player who made more passes
        scatter_df['marker_size'] = (scatter_df['no'] / scatter_df['no'].max() * 1500)
        #counting passes between players
        df_pass["pair_key"] = df_pass.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])), axis=1)
        lines_df = df_pass.groupby(["pair_key"]).x.count().reset_index()
        lines_df.rename({'x':'pass_count'}, axis='columns', inplace=True)
        #setting a treshold. You can try to investigate how it changes when you change it.
        lines_df = lines_df[lines_df['pass_count']>2]
        
        
        #plot once again pitch and vertices
        pitch = Pitch(pitch_color = 'grass', line_color='white', stripe=True)
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                             endnote_height=0.04, title_space=0, endnote_space=0)
        pitch.scatter(scatter_df.x, scatter_df.y, s=scatter_df.marker_size, color='white', edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)
        for i, row in scatter_df.iterrows():
            pitch.annotate(row.player_name, xy=(row.x, row.y), c='black', va='center', ha='center', weight = "bold", size=16, ax=ax["pitch"], zorder = 4)

        for i, row in lines_df.iterrows():
                player1 = row["pair_key"].split("_")[0]
                player2 = row['pair_key'].split("_")[1]
                #take the average location of players to plot a line between them
                player1_x = scatter_df.loc[scatter_df["player_name"] == player1]['x'].iloc[0]
                player1_y = scatter_df.loc[scatter_df["player_name"] == player1]['y'].iloc[0]
                player2_x = scatter_df.loc[scatter_df["player_name"] == player2]['x'].iloc[0]
                player2_y = scatter_df.loc[scatter_df["player_name"] == player2]['y'].iloc[0]
                num_passes = row["pass_count"]
                #adjust the line width so that the more passes, the wider the line
                line_width = (num_passes / lines_df['pass_count'].max() * 10)
                #plot lines on the pitch
                pitch.lines(player1_x, player1_y, player2_x, player2_y,
                                alpha=1, lw=line_width, zorder=2, color="white", ax = ax["pitch"])

        fig.suptitle(f"Rede de passes do {self.times[self.team]}", fontsize = 20)
        #contra {self.opponent[df_pass['match_id'].iloc[0]]   

        plt.show()