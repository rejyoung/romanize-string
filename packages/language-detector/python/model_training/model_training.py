import subprocess

subprocess.run(["python", "training_steps/prepare_dataset.py"], check=True)
subprocess.run(["python", "training_steps/vectorize_data.py"], check=True)
subprocess.run(["python", "training_steps/split_data.py"], check=True)
subprocess.run(["python", "training_steps/train_data.py"], check=True)
subprocess.run(["python", "training_steps/run_test_data.py"], check=True)