import os

import matplotlib.pyplot as plt

import pandas as pd


class Plot:
    def __init__(
        self,
        column_oriented_json_path: str,
        output_path: str = ".",
        display=True,
        image_type: str = "png",
    ):
        self.column_oriented_json_path = column_oriented_json_path
        self.df = pd.read_json(column_oriented_json_path, orient="column")
        self.columns = self.df.columns
        self.display_plots = display
        self.output_path = output_path
        self.output_filename_list = []
        self.image_type = image_type

    def hist(self, field, *args, **kwargs):
        """Generate a histogram plot for the given field"""

        self.df[field].hist(*args, **kwargs)
        img_fname = os.path.join(self.output_path, f"hist_{field}.{self.image_type}")
        plt.savefig(img_fname)
        self.output_filename_list.append(img_fname)

        if not self.display_plots:
            plt.close()
        else:
            plt.show()

    def pair_plot(
        self,
        plot_type,
        col_1: str,
        col_2: str,
        sort_by_first_column=True,
        *args,
        **kwargs,
    ):
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
        img_fname = os.path.join(
            self.output_path, f"{plot_type_str}_{col_1}_{col_2}.{self.image_type}"
        )
        plt.savefig(img_fname)
        self.output_filename_list.append(img_fname)

        if not self.display_plots:
            plt.close()
        else:
            plt.show()


plot = Plot("./deviation.json")
plot.pair_plot(plt.scatter, "gt_corners", "rb_corners")
