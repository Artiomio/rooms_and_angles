import os
import matplotlib.pyplot as plt
import pandas as pd

class Plot:
    def __init__(self, column_oriented_json_path: str, output_path: str=".", display=True, image_type: str='png'):
        """
        Initialize the Plot class with the path to a column-oriented JSON file, an output path for plots, 
        a flag to display plots, and the image type for saved plots.

        :param column_oriented_json_path: Path to the column-oriented JSON file.
        :param output_path: Path where the plots will be saved. Defaults to the current directory.
        :param display: Boolean flag to indicate whether to display the plots. Defaults to True.
        :param image_type: The file format for saving plots (e.g., 'png', 'jpg'). Defaults to 'png'.
        """
        self.column_oriented_json_path = column_oriented_json_path
        self.df = pd.read_json(column_oriented_json_path, orient="column")
        self.columns = self.df.columns
        self.display_plots = display
        self.output_path = output_path
        self.output_filename_list = []
        self.image_type = image_type

    def hist(self, field, *args, **kwargs):
        """
        Generate and save a histogram plot for the specified field in the DataFrame.

        :param field: The column name in the DataFrame for which the histogram will be generated.
        """
        
        self.df[field].hist(*args, **kwargs)
        img_fname = os.path.join(self.output_path, f"hist_{field}.{self.image_type}")
        plt.savefig(img_fname)
        self.output_filename_list.append(img_fname)
    
        if not self.display_plots:
            plt.close()
        else:
            plt.show()

    def draw_plot(self, plot_type, col_1: str, col_2: str, sort_by_first_column=True, *args, **kwargs):
        """
        Generate and save a plot of the specified type comparing two columns in the DataFrame.

        :param plot_type: The type of plot to generate (either a string like 'scatter' or a matplotlib function).
        :param col_1: The name of the first column in the DataFrame.
        :param col_2: The name of the second column in the DataFrame.
        :param sort_by_first_column: Boolean flag indicating whether to sort data by the first column. Defaults to True.
        """
        
        if isinstance(plot_type, str):
            plot_func = getattr(plt, plot_type, None)
            plot_type_str = plot_type
            if plot_func is None:
                raise ValueError(f"Plot type '{plot_type}' is not valid.")
        elif callable(plot_type):
            plot_func = plot_type
            plot_type_str = plot_func.__name__
        else:
            raise ValueError("plot_type must be a string or a callable function")

        if sort_by_first_column:
            sorted_by_first_column = sorted(zip(self.df[col_1], self.df[col_2]))
            x, y = zip(*sorted_by_first_column)
        else:
            x, y = self.df[col_1], self.df[col_2]
        
        plot_func(x, y, *args, **kwargs)
        img_fname = os.path.join(self.output_path, f"{plot_type_str}_{col_1}_{col_2}.{self.image_type}")
        plt.savefig(img_fname)
        self.output_filename_list.append(img_fname)

        if not self.display_plots:
            plt.close()
        else:
            plt.show()    

