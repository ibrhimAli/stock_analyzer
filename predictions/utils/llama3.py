# from airllm import AutoModel  


# def summarize_with_llama3(input):
#     MAX_LENGTH = 128  
#     model = AutoModel.from_pretrained("meta-llama/Meta-Llama-3-8B")  
#     input_text = [          
#   'What is the capital of United States?'      
#     ]  
#     input_tokens = model.tokenizer(input_text,      
#   return_tensors="pt",       
#   return_attention_mask=False,     
#   truncation=True,       
#   max_length=MAX_LENGTH,       
#   padding=False)  
  
#     generation_output = model.generate(      
#   input_tokens['input_ids'].cuda(),       
#   max_new_tokens=20,      
#   use_cache=True,      
#   return_dict_in_generate=True)  
  
#     output = model.tokenizer.decode(generation_output.sequences[0])  
#     print(output)
#     return output
