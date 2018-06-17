import matplotlib.pyplot as plt
import numpy as np

from downloadData.functions.file_utils import load_file

model_names = ['1-10-relu-lstm1-3-41-relu', '2-10-relu-lstm1-3-20-relu', '3-2-relu-lstm1-3-13-relu',
               '3-5-relu-lstm1-3-13-relu',
               '3-10-relu-lstm1-1-13-relu', '3-10-relu-lstm1-2-13-relu', '3-10-relu-lstm1-4-13-relu',
               '3-10-relu-lstm1-8-13-relu', '3-10-relu-lstm2-3-13-relu', '3-10-relu-lstm4-3-13-relu',
               '3-10-relu-lstm8-3-13-relu', '3-15-relu-lstm1-3-13-relu', '3-20-relu-lstm1-3-13-relu',
               '3-25-relu-lstm1-3-13-relu', '3-30-relu-lstm1-3-13-relu', '4-10-relu-lstm1-3-10-relu',
               '8-10-relu-lstm1-3-5-relu']
legend = ['pre1-mem1-post3', 'pre2-mem1-post3', 'pre2-mem1-post3','pre3-mem1-post3', 'pre3-mem1-post1', 'pre3-mem1-post2',
          'pre3-mem1-post4',
          'pre3-mem1-post8', 'pre3-mem2-post3', 'pre3-mem4-post3', 'pre3-mem8-post3', 'pre3-mem1-post3',
          'pre3-mem1-post3',
          'pre3-mem1-post3', 'pre3-mem1-post3', 'pre4-mem1-post3', 'pre8-mem1-post3']
legend = model_names
layers = [5, 6, 6,7,5, 6, 8, 12, 8, 10, 14, 7, 7, 7, 7, 8, 12]
for i, r in enumerate(model_names):
    mat = np.array(load_file('../out/' + r + '/log.csv'))
    valid_loss = mat[1:, 2].astype(np.float32)
    x = layers[i]
    y = np.min(valid_loss)
    plt.plot(x, y, '*')
    plt.annotate(legend[i], xy=(x, y))

plt.xlabel('Layers')
plt.ylabel('Normalized Mean Squared Error [°C^2]')
plt.grid('on')
plt.title('Evaluation of Model Architecture in Terms of Validation Loss')
plt.show()
