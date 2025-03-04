# type: ignore

import pandas as pd


def average_reports(reports, output_dict=False):
    """Averages multiple classification reports into a single consolidated report.

    Takes a list of classification reports (typically from cross-validation folds)
    and computes the average metrics while properly handling the support counts.

    Parameters:
        reports (list): List of pandas DataFrames, each containing a classification
                       report with columns ['precision', 'recall', 'f1-score', 'support']
        output_dict (bool, optional): If True, returns a dictionary representation
                                    of the report. If False, returns a formatted string.
                                    Defaults to False.

    Returns:
        Union[str, dict]: Consolidated classification report either as:
            - A formatted string if output_dict=False
            - A dictionary if output_dict=True

    Notes:
        - Removes 'micro avg' and 'accuracy' metrics if present
        - Keeps 'macro avg' and 'weighted avg' metrics
        - Sorts classes by support count in descending order
        - Rounds precision, recall, and f1-score to 2 decimal places
        - Sums support counts across reports
        - Averages precision, recall, and f1-score across reports
    """
    df = pd.concat(reports, axis=1)
    df['support'] = df['support'].sum(1)
    df['precision'] = df['precision'].mean(1)
    df['recall'] = df['recall'].mean(1)
    df['f1-score'] = df['f1-score'].mean(1)

    df = pd.DataFrame(df.values[:, :4], index=df.index, columns=df.columns[:4])
    if 'micro avg' in df.index:
        df = df.drop(index=['micro avg'])
    if 'accuracy' in df.index:
        df = df.drop(index=['accuracy'])
    report_final = df.drop(index=['macro avg', 'weighted avg'])\
        .sort_values('support', ascending=False)
    report_final = pd.concat([report_final,
                              df.loc[['macro avg', 'weighted avg']]])
    report_final[report_final.columns[:3]] = report_final[report_final.columns[:3]]\
        .round(2)
    report_final[['support']] = report_final[['support']].astype(int)

    if output_dict:
        report_final = report_final.T.to_dict()
    else:
        report_final = report_final.to_string()

    return report_final
