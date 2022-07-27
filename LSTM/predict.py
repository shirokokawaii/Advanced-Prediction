from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

from LSTM.func import data_split, line_plot, build_lstm_model, prepare_data, get_data, line_plot4

end = "2022-07-05 20:00:00"
time_interval = '1d'
data_size = 500
valid_size = 0.1
test_size = 0.1


hist = get_data(time_interval, data_size, end)

hist.to_csv("data.csv")
print(hist.head(5))
print(hist.size)
target_col = 'close'
train, valid, test = data_split(hist, valid_size, test_size)
line_plot(train[target_col], valid[target_col], test[target_col], 'training', 'valid', 'test', title='')
plt.show()

np.random.seed(42)
window_len = 5
zero_base = True
lstm_neurons = 100
epochs = 30
batch_size = 32
loss = 'mse'
dropout = 0.2
optimizer = 'adam'

train, valid, test, X_train, X_valid, y_train, y_valid = prepare_data(
    hist, target_col, window_len=window_len, zero_base=zero_base, valid_size=valid_size, test_size=test_size)

model = build_lstm_model(
    X_train, output_size=1, neurons=lstm_neurons, dropout=dropout, loss=loss,
    optimizer=optimizer)

history = model.fit(
    X_train, y_train, validation_data=(X_valid, y_valid), epochs=epochs, batch_size=batch_size, verbose=1, shuffle=True)

plt.plot(history.history['loss'], 'r', linewidth=2, label='Train loss')
plt.plot(history.history['val_loss'], 'g', linewidth=2, label='Validation loss')
plt.title('LSTM')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.show()

targets1 = valid[target_col][window_len:]
targets2 = test[target_col][window_len:]

preds = model.predict(X_valid).squeeze()
tests = model.predict(X_valid).squeeze()

mean_absolute_error(preds, y_valid)
MAE = mean_squared_error(preds, y_valid)
R2 = r2_score(y_valid, preds)

preds = valid[target_col].values[:-window_len] * (preds + 1)
preds = pd.Series(index=targets1.index, data=preds)

tests = test[target_col].values[:-window_len] * (tests + 1)
tests = pd.Series(index=targets2.index, data=tests)

line_plot4(targets1, targets2, preds, tests, 'fit', 'predict', lw=2)
plt.show()
