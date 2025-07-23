# Task 1: TensorFlow Autoencoder

**You have 20 minutes start from now to complete the following tasks.**

## Background  

This project is a Sparse Autoencoder implemented using TensorFlow and Keras. The autoencoder is designed to learn an efficient latent-space representation of MNIST images by enforcing sparsity constraints in the encoding process.

## Modification Requirements

*Note that in this task, the actual loss value and visualization vary and are not important. You just need to ensure your modifications make the code runnable. The reference code location is provided in parentheses for your reference.*

**1. Update Model Architecture** (`__init__` function of `SparseAutoencoder`)
- Change the architecture of the **encoder** and **decoder** while maintaining the fully connected structure.  
- In the **encoder**:  
  - Replace `ReLU` activation with **Leaky ReLU** with an `alpha` of **0.1** in the first dense layer.  
  - Add **Batch Normalization** after the activation to stabilize training, as well as **Dropout** with a rate of **0.2** for regularization.  
  - Change the final encoding layer activation from `sigmoid` to **tanh**.
- In the **decoder**:  
  - Use **Leaky ReLU** with an `alpha` of **0.1** instead of `ReLU`.  
  - Include **Batch Normalization** and **Dropout** with a rate of **0.2** similar to the encoder.  
  
**2. Use KL Divergence as Sparsity Loss** (`compute_sparsity_loss` function of `SparseAutoencoder`)
- Instead of using **L1 regularization**, compute the sparsity loss using **Kullback-Leibler (KL) divergence**.
- The KL divergence formula for each neuron should be:
  $$
  \text{KL}(\rho || \hat{\rho}) = \rho \log \frac{\rho}{\hat{\rho}} + (1 - \rho) \log \frac{1 - \rho}{1 - \hat{\rho}}
  $$
  where:
  - $\rho$ is the desired sparsity level, and should be set to **0.05**.
  - $\hat{\rho}$ is the **average activation** of each neuron across the batch.
- Sum the KL divergence over all neurons in the encoding layer and apply the sparsity penalty to the total loss.

**3. Customize Learning Rate Schedule** (`optimizer` assignment statement)
- Write a customized learning rate schedule function that uses the **Cosine Decay** instead of a fixed learning rate, with the following formula:
  $$
  \eta_t = \eta_0 \times \frac{1 + \cos\left(\frac{\pi t}{T}\right)}{2}
  $$
  where:
  - $\eta_0 = 0.001$ is the initial learning rate,
  - $t$ is the current epoch index,
  - $T = 10$ is the total number of epochs.
