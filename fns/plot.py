def confusion_matrix_plot(y_true, y_pred) -> None:
    """
    Plot a confusion matrix.

    Args:
        y_true: List of true labels
        y_pred: List of prediction labels

    Returns:
    """
    from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
    cm = confusion_matrix(y_true, y_pred)
    plot = ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plot.ax_.set_title('Confusion Matrix')
