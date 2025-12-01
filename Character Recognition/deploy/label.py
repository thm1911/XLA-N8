import pandas as pd

def get_label_df():
    label_map = pd.read_csv(
        "../emnist_dataset/emnist-bymerge-mapping.txt",
        delimiter=" ",
        index_col=0,
        header=None
    ).iloc[:, 0]

    label_df = pd.DataFrame({
        'ascii': label_map,
        'char': label_map.apply(chr)
    })

    return label_df