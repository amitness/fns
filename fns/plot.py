def confusion_matrix_plot(y_true, y_pred):
    from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix
    cm = confusion_matrix(y_true, y_pred)
    plot = ConfusionMatrixDisplay(confusion_matrix=cm).plot()
    plot.ax_.set_title('Confusion Matrix')
