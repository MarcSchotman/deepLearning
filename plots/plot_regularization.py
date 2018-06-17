import matplotlib.pyplot as plt
import numpy as np

from downloadData.functions.file_utils import load_file
csfont = {'fontname': 'Century Gothic'}

model_names = ['1-15-relu-lstm2-1-165-relu-Dropout50', '1-15-relu-lstm2-1-165-relu-Dropout25']
legend = model_names
xs =[]
for i, r in enumerate(model_names):
    mat = np.array(load_file('../out/' + r + '/log.csv'))
    valid_loss = mat[1:, 2].astype(np.float32)
    train_loss = mat[1:, 1].astype(np.float32)
    epoch = mat[1:, 0].astype(np.int)
    xs.extend(epoch)
    plt.plot(epoch, valid_loss, '-x')
    plt.plot(epoch, train_loss, '-x')

plt.legend(['Valid Loss 50% Dropout',])
plt.xticks( range(min(xs),max(xs)+1),range(min(xs),max(xs)+1),fontsize=16, **csfont)
plt.xlabel('Epoch',fontsize=16, **csfont)
plt.ylabel('Loss',fontsize=16, **csfont)
plt.grid('on')
plt.title('Evaluation of Model Complexity', fontsize=16, **csfont)
plt.show()
