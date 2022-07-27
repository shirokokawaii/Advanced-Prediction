from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from LSTM.func import train_test_split, line_plot, build_lstm_model, prepare_data, get_data

end = "2021-05-05 20:00:00"
time_intervial = '1h'
data_size = 500
window_len = 5
test_size = 0.1

hist = get_data(time_intervial, data_size, end)

hist.to_csv("data.csv")
print(hist.head(5))
print(hist.size)
target_col = 'close'
train, test = train_test_split(hist, test_size)
line_plot(train[target_col], test[target_col], 'training', 'test', title='')
plt.show()

np.random.seed(42)
zero_base = True
lstm_neurons = 100
epochs = 20
batch_size = 32
loss = 'mse'
dropout = 0.2
optimizer = 'adam'
train, test, X_train, X_test, y_train, y_test = prepare_data(
    hist, target_col, window_len=window_len, zero_base=zero_base, test_size=test_size)
model = build_lstm_model(
    X_train, output_size=1, neurons=lstm_neurons, dropout=dropout, loss=loss,
    optimizer=optimizer)
history = model.fit(
    X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size, verbose=1, shuffle=True)

plt.plot(history.history['loss'], 'r', linewidth=2, label='Train loss')
plt.plot(history.history['val_loss'], 'g', linewidth=2, label='Validation loss')
plt.title('LSTM')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.show()

targets = test[target_col][window_len:]
preds = model.predict(X_test).squeeze()
mean_absolute_error(preds, y_test)

MAE = mean_squared_error(preds, y_test)
R2 = r2_score(y_test, preds)

preds = test[target_col].values[:-window_len] * (preds + 1)
preds = pd.Series(index=targets.index, data=preds)
line_plot(targets, preds, 'actual', 'prediction', lw=3)
plt.show()
