import matplotlib.pyplot as plt
import numpy as np

from downloadData.functions.file_utils import load_file

csfont = {'fontname': 'Century Gothic'}
std = 10.72991139
post = ['3-10-relu-lstm1-1-55-relu', '3-10-relu-lstm1-2-55-relu', '3-10-relu-lstm1-4-55-relu',
        '3-10-relu-lstm1-8-55-relu']
pre = ['1-10-relu-lstm1-3-165-relu', '2-10-relu-lstm1-3-82-relu', '4-10-relu-lstm1-3-41-relu',
       '8-10-relu-lstm1-3-20-relu']
memory = ['3-10-relu-lstm1-3-55-relu', '3-10-relu-lstm2-3-55-relu', '3-10-relu-lstm4-3-55-relu',
          '3-10-relu-lstm8-3-55-relu']
layers = np.array([1, 2, 4, 8])
plt.subplot(2, 1, 1)
performances = []
for i, r in enumerate(post):
    mat = np.array(load_file('../out/' + r + '/log.csv'))
    valid_loss = mat[1:, 2].astype(np.float32)
    y = np.sqrt(np.min(valid_loss) * std ** 2)
    performances.append(y)
plt.bar(layers, performances, width=0.2, color='b', align='center')
performances = []
for i, r in enumerate(pre):
    mat = np.array(load_file('../out/' + r + '/log.csv'))
    valid_loss = mat[1:, 2].astype(np.float32)
    y = np.sqrt(np.min(valid_loss) * std ** 2)
    performances.append(y)
plt.bar(layers - 0.2, performances, width=0.2, color='g', align='center')
layers = np.array([1, 2, 4, 8])
performances = []
for i, r in enumerate(memory):
    mat = np.array(load_file('../out/' + r + '/log.csv'))
    valid_loss = mat[1:, 2].astype(np.float32)
    y = np.sqrt(np.min(valid_loss) * std ** 2)
    performances.append(y)
plt.bar(layers + 0.2, performances, width=0.2, color='r', align='center')
plt.legend(['Postprocessing', 'Preprocessing', 'Memory'], fontsize=16, prop={'family': 'Century Gothic'})
plt.xlabel('Layers', fontsize=16, **csfont)
plt.ylabel('RMSE [°C]', fontsize=16, **csfont)
plt.grid('on')
plt.title('Evaluation of Model Architecture in Terms of Validation Loss ', fontsize=20, **csfont)
plt.subplot(2, 1, 2)

width = [0.2, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
model_names = ['3-2-relu-lstm1-3-13-relu',
               '3-5-relu-lstm1-3-55-relu',
               '3-10-relu-lstm1-3-55-relu',
               '3-15-relu-lstm1-3-55-relu',
               '3-20-relu-lstm1-3-55-relu',
               '3-25-relu-lstm1-3-55-relu', '3-30-relu-lstm1-3-55-relu']
performances = []
for i, r in enumerate(model_names):
    mat = np.array(load_file('../out/' + r + '/log.csv'))
    valid_loss = mat[1:, 2].astype(np.float32)
    y = np.sqrt(np.min(valid_loss) * std ** 2)
    performances.append(y)
plt.plot(width, performances, '--*')

plt.xlabel('*N_Nodes', fontsize=16, **csfont)
plt.ylabel('RMSE [°C]', fontsize=16, **csfont)
plt.grid('on')
plt.show()
