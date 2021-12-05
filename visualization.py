import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yaml
import os

#Configuration file
config_localiation = os.path.join(os.getcwd(), 'config.yaml')
config = open(config_localiation, 'r')
config = yaml.safe_load(config)

#Other
yesterday = dt.datetime.today().date() + dt.timedelta(days= -1)
save_path = config['paths']['save_path']

def chart1(dataframe):

    dataframe.plot(kind='bar', x='Produkt', y='Procent portfela', title='Skład portfela w %', color='grey',
                  figsize=(14, 12), legend=False)
    plt.subplots_adjust(left=0.045, right=0.955, bottom=0.31, top=0.948)
    for index, data in enumerate(dataframe['Procent portfela']):
        plt.text(x=index, y=data + 0.6, s=f'{data:.2f}%', fontsize='small', ha='center', ma='left')
        if dataframe.iloc[index, 2] > 0:
            plt.text(x=index, y=data + 0.1, s=f'{dataframe.iloc[index, 2]:.2f}pp.', fontsize='x-small', ha='center',
                     ma='center', color='green')
        elif dataframe.iloc[index, 2] < 0:
            plt.text(x=index, y=data + 0.15, s=f'{dataframe.iloc[index, 2]:.2f}pp.', fontsize='x-small', ha='center',
                     ma='center', va='center', color='red')
        else:
            plt.text(x=index, y=data + 0.1, s=f'{dataframe.iloc[index, 2]:.2f}pp.', fontsize='x-small', ha='center',
                     va='center', ma='center', color='black')
    plt.savefig(f'{save_path}' + f'\{yesterday} chart1 ' + '.jpeg')

def chart2(dataframe):
    dataframe.plot(kind='bar', x='Produkt', y='Wartość w PLN', title='Skład portfela w PLN', color='grey',
                   figsize=(14, 12), legend=False)
    plt.subplots_adjust(left=0.045, right=0.955, bottom=0.31, top=0.948)
    for index, data in enumerate(dataframe['Wartość w PLN']):
        plt.text(x=index, y=data + 900, s=f'{data:.2f}', fontsize='small', ha='center', ma='left')
        if dataframe.iloc[index, 2] > 0:
            plt.text(x=index, y=data + 250, s=f'{dataframe.iloc[index, 2]:.2f}', fontsize='x-small', ha='center',
                     ma='center', color='green')
        elif dataframe.iloc[index, 2] < 0:
            plt.text(x=index, y=data + 300, s=f'{dataframe.iloc[index, 2]:.2f}', fontsize='x-small', ha='center',
                     ma='center', va='center', color='red')
        else:
            plt.text(x=index, y=data + 250, s=f'{dataframe.iloc[index, 2]:.2f}', fontsize='x-small', ha='center',
                     va='center', ma='center', color='black')
    plt.savefig(f'{save_path}' + f'\{yesterday} chart2 ' + '.jpeg')

def chart3(dataframe):
    dataframe.plot(kind='bar', x='Produkt', y='Suma', title='Liczba akcji', color='grey', figsize=(14, 12),
                   legend=False)
    plt.subplots_adjust(left=0.045, right=0.955, bottom=0.31, top=0.948)
    for index, data in enumerate(dataframe['Suma']):
        plt.text(x=index, y=data + 75, s=f'{data:.0f}', fontsize='small', ha='center', ma='left')
        if dataframe.iloc[index, 2] > 0:
            plt.text(x=index, y=data + 25, s=f'{dataframe.iloc[index, 2]:.0f}', fontsize='x-small', ha='center',
                     ma='center', color='green')
        elif dataframe.iloc[index, 2] < 0:
            plt.text(x=index, y=data + 25, s=f'{dataframe.iloc[index, 2]:.0f}', fontsize='x-small', ha='center',
                     ma='center', va='center', color='red')
        else:
            plt.text(x=index, y=data + 25, s=f'{dataframe.iloc[index, 2]:.0f}', fontsize='x-small', ha='center',
                     va='center', ma='center', color='black')
    plt.savefig(f'{save_path}' + f'\{yesterday} chart3 ' + '.jpeg')

def table1(table):
    table = table.round(2).head().reset_index(drop=True)
    table.index = table.index + 1
    title_text = 'Top 5 wygranych spółek'
    # Pop the headers from the data array
    column_headers = list(table.columns)
    row_headers = [x[0] for x in table.itertuples()]

    # Table data needs to be non-numeric text. Format the data
    # while I'm at it.
    cell_text = []
    for row in table.itertuples():
        cell_text.append(row[1:])

    # Get some lists of color specs for row and column headers
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    # Create the figure. Setting a small pad on tight_layout
    # seems to better regulate white space. Sometimes experimenting
    # with an explicit figsize here can produce better outcome.
    plt.figure(linewidth=2,
               tight_layout={'pad': 1},
               figsize=(4, 3)
               )
    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=row_headers,
                          rowColours=rcolors,
                          rowLoc='right',
                          colColours=ccolors,
                          colLabels=column_headers,
                          loc='center')
    # Scaling is the only influence we have over top and bottom cell padding.
    # Make the rows taller (i.e., make cell y scale larger).
    the_table.scale(1.5, 2)
    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    # Add title
    plt.suptitle(title_text)
    # Force the figure to update, so backends center objects correctly within the figure.
    # Without plt.draw() here, the title will center on the axes and not the figure.
    plt.draw()
    # Create image. plt.savefig ignores figure edge and face colors, so map them.
    fig = plt.gcf()
    plt.savefig(f'{save_path}' + f'\{yesterday} table1 ' + '.jpeg',
                # bbox='tight',
                edgecolor=fig.get_edgecolor(),
                facecolor=fig.get_facecolor(),
                dpi=150
                )


def table2(table):
    table = table.round(2).head().reset_index(drop=True)
    table.index = table.index + 1
    title_text = 'Top 5 przegranych spółek'
    # Pop the headers from the data array
    column_headers = list(table.columns)
    row_headers = [x[0] for x in table.itertuples()]

    # Table data needs to be non-numeric text. Format the data
    # while I'm at it.
    cell_text = []
    for row in table.itertuples():
        cell_text.append(row[1:])

    # Get some lists of color specs for row and column headers
    rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
    ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))
    # Create the figure. Setting a small pad on tight_layout
    # seems to better regulate white space. Sometimes experimenting
    # with an explicit figsize here can produce better outcome.
    plt.figure(linewidth=2,
               tight_layout={'pad': 1},
               figsize=(4, 3)
               )
    # Add a table at the bottom of the axes
    the_table = plt.table(cellText=cell_text,
                          rowLabels=row_headers,
                          rowColours=rcolors,
                          rowLoc='right',
                          colColours=ccolors,
                          colLabels=column_headers,
                          loc='center')
    # Scaling is the only influence we have over top and bottom cell padding.
    # Make the rows taller (i.e., make cell y scale larger).
    the_table.scale(1.5, 2)
    # Hide axes
    ax = plt.gca()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # Hide axes border
    plt.box(on=None)
    # Add title
    plt.suptitle(title_text)
    # Force the figure to update, so backends center objects correctly within the figure.
    # Without plt.draw() here, the title will center on the axes and not the figure.
    plt.draw()
    # Create image. plt.savefig ignores figure edge and face colors, so map them.
    fig = plt.gcf()
    plt.savefig(f'{save_path}' + f'\{yesterday} table2 ' + '.jpeg',
                # bbox='tight',
                edgecolor=fig.get_edgecolor(),
                facecolor=fig.get_facecolor(),
                dpi=150
                )
