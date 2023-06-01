class CiradLegend:
    def __init__(self):
        pass

    @staticmethod
    def get_legend(classes):
        # Create an empty list to store the legend
        legend = []

        # Level 1
        if classes[0] == 1:
            legend.append('Agriculture')
        elif classes[0] == 2:
            legend.append('Natural and semi-natural vegetation')
        elif classes[0] == 3:
            legend.append('Waterbodies')
        elif classes[0] == 4:
            legend.append('Build-up and related land')

        # Level 2
        if classes[1] == 1:
            legend.append('Sugarcane')
        elif classes[1] == 2:
            legend.append('Grassland')
        elif classes[1] == 3:
            legend.append('Market gardening')
        elif classes[1] == 4:
            legend.append('Greenhouses')
        elif classes[1] == 5:
            legend.append('Orchards')
        elif classes[1] == 6:
            legend.append('Woodland')
        elif classes[1] == 7:
            legend.append('Savanna')
        elif classes[1] == 8:
            legend.append('Rock')
        elif classes[1] == 9:
            legend.append('Terrain shadow')
        elif classes[1] == 10:
            legend.append('Waterbodies')
        elif classes[1] == 11:
            legend.append('Build-up and related land')

        # Level 3
        if classes[2] == 1:
            legend.append('Sugarcane')
        elif classes[2] == 2:
            legend.append('Grazed meadow')
        elif classes[2] == 3:
            legend.append('Mowed meadow')
        elif classes[2] == 4:
            legend.append('Pineapple')
        elif classes[2] == 5:
            legend.append('Other vegetables')
        elif classes[2] == 6:
            legend.append('Greenhouses')
        elif classes[2] == 7:
            legend.append('Citrus')
        elif classes[2] == 8:
            legend.append('Lychee or longan')
        elif classes[2] == 9:
            legend.append('Mango')
        elif classes[2] == 10:
            legend.append('Coconut')
        elif classes[2] == 11:
            legend.append('Banana')
        elif classes[2] == 12:
            legend.append('Forest and mountains')
        elif classes[2] == 13:
            legend.append('Other woody vegetation')
        elif classes[2] == 14:
            legend.append('Forest plantation')
        elif classes[2] == 15:
            legend.append('Altimontane vegetation')
        elif classes[2] == 16:
            legend.append('Rampart heath')
        elif classes[2] == 17:
            legend.append('Savanna')
        elif classes[2] == 18:
            legend.append('Shrubby vegetation')
        elif classes[2] == 19:
            legend.append('Giant bramble')
        elif classes[2] == 20:
            legend.append('Vegetation on lava')
        elif classes[2] == 21:
            legend.append('Rock')
        elif classes[2] == 22:
            legend.append('Swamp')
        elif classes[2] == 23:
            legend.append('Waterbodies')
        elif classes[2] == 24:
            legend.append('Buildings')
        elif classes[2] == 25:
            legend.append('Photovoltaic farm')
        elif classes[2] == 26:
            legend.append('Roads and parking')

        return legend
    
    # Def color legend
    @staticmethod
    def get_color_legend():
        # List of labels corresponding to each class
        labels = ['Sugarcane',
                    'Grazed meadow',
                    'Mowed meadow',
                    'Pineapple',
                    'Other vegetables',
                    'Greenhouses',
                    'Citrus',
                    'Lychee or longan',
                    'Mango',
                    'Coconut',
                    'Banana',
                    'Forest and mountains',
                    'Other woody vegetation',
                    'Forest plantation',
                    'Altimontane vegetation',
                    'Rampart heath',
                    'Savanna',
                    'Shrubby vegetation',
                    'Giant bramble',
                    'Vegetation on lava',
                    'Rock',
                    'Swamp',
                    'Waterbodies',
                    'Buildings',
                    'Photovoltaic farm',
                    'Roads and parking']
        # List of colors corresponding to each class
        colors = ['#7d7e3c',
                    '#44f414',
                    '#53ebb8',
                    '#fb7405',
                    '#d7d79e',
                    '#cc0101',
                    '#7030a0',
                    '#b889db',
                    '#dcc5ed',
                    '#dd4fc2',
                    '#891b74',
                    '#364d1f',
                    '#72ac3e',
                    '#01a884',
                    '#a9d08e',
                    '#84bf4d',
                    '#cac10c',
                    '#7c7607',
                    '#83d31a',
                    '#9adf5a',
                    '#b67412',
                    '#606060',
                    '#00768e',
                    '#01cccc',
                    '#ff0101',
                    '#ffabab',
                    '#d2b2c5']
        
        return labels, colors




