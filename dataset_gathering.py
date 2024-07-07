from datasets import load_dataset

# Set the local cache directory
cache_dir = r'C:\Users\Liviu\Desktop\EVA PROJECT\EVA PROJECT\_fine_tuning\datasets'

# Load the dataset and specify the cache directory
print("downloading...")
name="SODA"



dataset = load_dataset('Salesforce/dialogstudio', name, cache_dir=cache_dir, trust_remote_code=True)

# Print the logs for each dialogue
output_file_path = f"{cache_dir}/{name}.txt"



print(dataset['train'][0])
print( "==="*10)
print(dataset['train'][1])


print("printing in txt...")
# Open the file in write mode with UTF-8 encoding
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Iterate over the dialogues in the training set
    for dialogue in dataset['train']:
        logs = dialogue['log']
        for turn in logs:
            user_utterance = turn['user utterance']
            system_response = turn['system response']
            # Write the dialogue to the file only if user and system responses are present
            if user_utterance and system_response:
                output_file.write(f"User: {user_utterance}\n")
                output_file.write(f"System: {system_response}\n")
                output_file.write("=" * 50 + "\n")
