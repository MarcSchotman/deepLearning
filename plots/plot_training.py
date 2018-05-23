from utils.fileaccess.utils import load_file
import numpy as np
import matplotlib.pyplot as plt

log = load_file('../out/basic_lstm/log.csv')
epoch = np.array([l[0] for l in log[1:]])
loss = np.array([np.round(float(l[1]), 3) for l in log[1:]])
val_loss = np.array([np.round(float(l[2]), 3) for l in log[1:]])
legend = log[0][1:]
plt.figure(figsize=(10, 5))

plt.plot(epoch, loss)
plt.plot(epoch, val_loss)
plt.legend(legend)
plt.title('Training Process')
plt.xlabel('Epoch')
plt.show()
