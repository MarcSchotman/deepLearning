import matplotlib.pyplot as plt
import numpy as np

from downloadData.functions.file_utils import load_file

model_names = ['gru100', 'gru200', 'gru300']
legend = model_names
xs =[]
for i, r in enumerate(model_names):
    mat = np.array(load_file('../out/' + r + '/log.csv'))
    valid_loss = mat[1:, 2].astype(np.float32)
    train_loss = mat[1:, 1].astype(np.float32)
    epoch = mat[1:, 0].astype(np.int)
    xs.extend(epoch)
    plt.plot(epoch, valid_loss/train_loss, '-x')

plt.legend(model_names)
plt.xticks( range(min(xs),max(xs)+1),range(min(xs),max(xs)+1))
plt.xlabel('Epoch')
plt.ylabel('Validation Loss/Training Loss')
plt.grid('on')
plt.title('Evaluation of Model Complexity')
plt.show()
