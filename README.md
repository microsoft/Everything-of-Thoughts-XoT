

# Everything of Thoughts (XoT): Defying the Law of Penrose Triangle for Thought Generation

![Compare](/assets/compare.jpg "Compare")
 
This repository contains the implementation of our novel thought prompting approach, **"Everything of Thoughts" (XoT)**. XoT combines pretrained reinforcement learning and Monte Carlo Tree Search (MCTS) to incorporate external domain knowledge into thoughts, thereby enhancing Large Language Models' (LLMs) capabilities and enabling them to generalize to unseen problems efficiently. This approach is designed to address the limitations of existing thought paradigms, particularly the "Penrose triangle" issue which suggests that a thought can at most exhibit two attributes out of performance, efficiency, and flexibility.

## Set Up
 
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1. In order to use the framework, you need to have access to an GPT. Set up OpenAI API key and store in environment variable OPENAI_API_KEY ([see here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)).

2. Clone the repository and install the required packages.
```bash
git clone https://github.com/your_username/EverythingOfThought.git  
cd EverythingOfThought  
conda create -n xot python=3.8
conda activate xot
pip install -r requirements.txt  
```

## Training
 
* The ```./xot_mcts/``` directory contains everything needed for training.

* Dataset of Game of 24, 8-Puzzle, and Pocket Cube are under ```./xot_mcts/{env}/data/```, separately.

* You can specify the parameters for self-play in main.py. To begin training a model for a specific task, use the provided training and test data. For example:
```bash
python main.py --env game24 --mode train --training_env game24/data/train.csv --numMCTSSims 5000 --arenaCompare 100 --numEps 10 --numIters 3
```
Args: 
* ```--env```: Select your desired framework and game. 
* ```--mode```: train / test. 
* ```--training_env```: Training data path.
* ```--numMCTSSims```: Number of games moves for MCTS to simulate.
* ```--arenaCompare```: Number of games to play during arena play to determine if new net will be accepted.
* ```--numEps```: Number of complete self-play games to simulate during a new iteration.
* ```--numIters```: Number of iteration.
    
The scripts for replicating the MCTS module, as mentioned in the paper, can be found in ```./xot_mcts/scripts/```.

* The core training loop is contained within ```./xot_mcts/Coach.py```.

* ```./xot_mcts/MCTS.py``` is used to perform the Monte Carlo Tree Search.

* Additional parameters for the Policy/Value network are located in ```./xot_mcts/{env}/pytorch/NNet.py```. Here, you can specify options such as the cuda flag, batch size, epochs, learning rate, and more.
 
* Once training is complete, you can find the trained models in the ```./xot_mcts/temp/{env}/``` directory. For inference usage, move the trained Policy/Value model to ```./xot_all_in_one/models/{env}/```.

* To evaluate the performance of single MCTS module, use the test mode. Here's an example:

(single solution)
```bash
python main.py --env game24 --mode test --test_env game24/data/test.csv --numMCTSSims 2000 --arenaCompare 137 --multi_sol 0
```

(multi solution)
```bash
python main.py --env game24 --mode test --test_env game24/data/test.csv --numMCTSSims 2000 --arenaCompare 137 --multi_sol 1 --multi_times 500
```

* Training and testing logs for MCTS modules will be stored under ```./xot_mcts/logs/```.


## Inference
 
* The ```./xot_all_in_one/``` directory houses all the necessary resources for performing inference. In addition to our XoT, we also offer implementations for IO, CoT, CoT(sc), ToT, and GoT. For each method, we provide a corresponding solver located in ```./xot_all_in_one/xot/controller/solver/{method}.py```.


### Model Path
For inference usage, the trained Policy/Value model for MCTS module should be put in ```./xot_all_in_one/models/{env}/```.

### Executing the Scripts
 
* We provide a variety of scripts to execute XoT on several tasks such as Game of 24, 8-Puzzle, and Pocket Cube, located in ```./xot_all_in_one/scripts/```.

* Here are some sample commands for the scripts:
```bash
python main.py --config config/cube/single_sol/cube_single_xot_laststep0_revised0.yaml  
python main.py --config config/cube/single_sol/cube_single_xot_laststep1_revised0.yaml  
python main.py --config config/cube/single_sol/cube_single_xot_laststep1_revised1.yaml  
```

### Configuration

* The configuration file is a YAML file that provides various parameters to control the running of XoT. Here's an illustration of the parameters in the configuration file:
```bash
env: cube # The environment in which the task will be executed

method: xot  # The method used for the task.

task:  
  data: data/cube/cube_test.csv  # The path to the CSV file containing the test data.
  total_game_step: 4  # The total number of game steps to be executed.
  task_start_index: 0  # The start data indices for the tasks.
  task_end_index: 1  # The end data indices for the tasks.
  
gpt:  # gpt: Configuration for the GPT model:
  backend: gpt-35-turbo-20220309 # The specific GPT model to use.
  temperature: 0.0  
  stop: None    
  
param:
  n_generate_sample: 1  # The number of samples to generate.
  n_evaluate_sample: None # The number of samples to evaluate.
  n_select_sample: None # The number of samples to select.
  last_step: 1 # A boolean flag indicating whether including the last step of thoughts (1) or not (0).
  
multi_solution: 0  # A boolean flag indicating whether multiple solutions are allowed (1) or not (0).
  
################## ONLY FOR XoT #####################################################
xot:  
  numMCTSSims: 10  # The number of Monte Carlo Tree Search simulations to be executed.
  multi_numMCTSSims: 10  # The number of MCTS simulations to be executed when multiple solutions are allowed.
  multi_solution_exploration: 50  # The number of explorations to be performed when multiple solutions are allowed.
  
  revised: 1  # A boolean flag indicating whether revision is allowed (1) or not (0).
  revise_times: 1  # The number of times revision should be performed.
  revise_total_game_step: 7 # The total number of game steps to be executed for revision.
  revise_numMCTSSims: 500  # The number of MCTS simulations to be executed during revision.
  
model: 
  checkpoint: ./models/cube # The path to the model checkpoint.
  filename: best.pth.tar # The filename of the model checkpoint.
  cpuct: 1 # The exploration parameter for the MCTS.
################## ONLY FOR XoT End #################################################
```

* For more details about configurations for other baselines, refer to the files located in the ```./xot_all_in_one/config/``` directory.

* Note that the default value for ```task_end_index``` in the config is set to ```1```. However, this value should be adjusted based on the data size of each specific task. To perform a complete inference, set task_end_index to ```137``` for Game of 24, ```119``` for 8-Puzzle, and ```183``` for Pocket Cube.


## Paper Results

We evaluated XoT on both single-solution and multi-solution problem-solving tasks. Our results demonstrate that XoT significantly outperforms existing approaches in various dimensions, showcasing its remarkable proficiency in addressing complex problems across diverse domains. All the paper results can be found in `./xot_all_in_one/experiments/`.


## Citations
Your support would be greatly appreciated if you find XoT interesting or useful. Please acknowledge our work by citing the paper and giving this repository a star. For any inquiries, don't hesitate to contact us at rmding@gatech.edu or simply open an issue. Thank you!

```
@article{ding2023thoughts,
      title={Everything of Thoughts: Defying the Law of Penrose Triangle for Thought Generation}, 
      author={Ruomeng Ding and Chaoyun Zhang and Lu Wang and Yong Xu and Minghua Ma and Wei Zhang and Si Qin and Saravan Rajmohan and Qingwei Lin and Dongmei Zhang},
      year={2023},
      journal={arXiv preprint arXiv:2311.04254},
}
```


## Contributing

This project welcomes contributions and suggestions. Most contributions require you to
agree to a Contributor License Agreement (CLA) declaring that you have the right to,
and actually do, grant us the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need
to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the
instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## License
 
This project is licensed under the MIT License. See the LICENSE file for details.


## Trademarks 

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft trademarks or logos is subject to and must follow Microsoft’s Trademark & Brand Guidelines. Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship. Any use of third-party trademarks or logos are subject to those third-party’s policies.