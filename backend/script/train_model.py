import json
from transformers import GPTNeoXForCausalLM, GPTNeoXTokenizerFast, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
from huggingface_hub import login

# Log in to Hugging Face
login()

# Load the model and tokenizer
model_name = "EleutherAI/gpt-neox-20b"
tokenizer = GPTNeoXTokenizerFast.from_pretrained(model_name, token=True)
model = GPTNeoXForCausalLM.from_pretrained(model_name, token=True)

# Prepare your dataset
def load_dataset(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines]

# Create a TextDataset
def create_dataset(tokenizer, file_path, block_size=512):
    dataset = load_dataset(file_path)
    texts = [item['prompt'] + " " + item['completion'] for item in dataset]
    encodings = tokenizer(texts, truncation=True, padding=True, max_length=block_size, return_tensors="pt")
    return TextDataset(tokenizer=tokenizer, file_path=file_path, block_size=block_size)

# Load the dataset
train_file_path = '../data/dataset.jsonl'
train_dataset = create_dataset(tokenizer, train_file_path)

# Data collator
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Training arguments
training_args = TrainingArguments(
    output_dir='../models/fine_tuned_model',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=10_000,
    save_total_limit=2,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# Train the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained('../models/fine_tuned_model')
tokenizer.save_pretrained('../models/fine_tuned_model')

# Save the fine-tuned model ID (optional)
fine_tuned_model_id = model_name + "-fine-tuned"
with open('../models/fine_tuned_model/model_id.txt', 'w') as f:
    f.write(fine_tuned_model_id)