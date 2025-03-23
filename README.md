# LSTM Music Generation in Distributed Environment

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow 2.x](https://img.shields.io/badge/TensorFlow-2.x-orange.svg)](https://www.tensorflow.org/)

> Accelerating LSTM-based music generation using distributed multi-GPU training

## 🎵 Overview

This project implements an LSTM model for music generation with distributed training capabilities across multiple GPU servers. By leveraging distributed computing techniques, we achieve significant improvements in training efficiency and generation performance. We in our case used two GPU servers for implementation.

## 🚀 Features

- LSTM-based architecture for musical sequence generation
- Distributed training across multiple GPU servers
- Customizable sequence length for varied musical outputs
- MIDI file parsing and preprocessing pipeline
- Real-time music generation capabilities


## 📊 Pipeline

```
Parsing MIDI files      Preprocessing        Training in         Music Notes
using Music21      →   MIDI files with    →   distributed     →   Generation
library                identification of      environment on
                       I/O sequence length    multiple servers
```

## 📚 Datasets

Currently, the model is trained on a collection of random compositions in MIDI format. Other potential datasets include:
- JSB Chorales
- VGMidi
- ComMU

For standard datasets related to music generation, visit: [Music Generation Datasets](https://paperswithcode.com/datasets?task=music-generation)

## 🧠 Model Architecture

- Simple LSTM network for generating musical notes
- Capable of generating different notes based on variations in input sequence length
- The architecture can be extended to more complex models for improved training and generation quality

## 🛠️ Technologies Used

- **[Music21](http://web.mit.edu/music21/)**: Library for parsing and generating musical notes
- **[TensorFlow](https://www.tensorflow.org/)**: Framework for building the model and implementing distributed training
- **[midi2audio](https://github.com/bzamecnik/midi2audio)**: Tool for generating audible music by reading MIDI files

## 💻 Distributed Training Approach

- Primarily uses `MultiWorkerMirroredStrategy` from TensorFlow
- Other strategies available at: [TensorFlow Distributed Training](https://www.tensorflow.org/guide/distributed_training)
- Training methodology:
  1. Train the model on a specific server with particular parameters (sequence length, iterations, data volume)
  2. Save the model state
  3. Switch to another server to continue training
  4. Compare convergence and training speed across servers

## 📈 Implementation Results

- Successfully implemented distributed training across two QMUL servers (Dorchester and Bath)
- Evaluated metrics are consistent with expected performance improvements
- Analysis confirms significant gains in training efficiency

## 🔮 Future Improvements

- [ ] Implement alternative strategies for distributed training
- [ ] Develop better visualization methods for analysis
- [ ] Identify and measure additional performance metrics
- [ ] Explore more complex model architectures for improved generation quality

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/username/lstm-music-generation.git
cd lstm-music-generation

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# For midi2audio functionality
# On Ubuntu/Debian:
apt-get install fluidsynth
# On macOS:
brew install fluidsynth
# On Windows:
# Download and install FluidSynth from http://www.fluidsynth.org/
```

## 🚀 Usage
- Run the respective Jupyter Notebooks to get the results



## 🙏 Acknowledgements

- Dr. Ahmed M. A. Sayed, Queen Mary University of London
- Sayed Systems Group @ QMUL [https://sayed-sys-lab.github.io/]
- Queen Mary University of London for providing computing resources (Dorchester and Bath servers)
- [Music21](http://web.mit.edu/music21/) developed by MIT
- TensorFlow team for distributed training capabilities
