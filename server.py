import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from concurrent import futures
import time
import grpc
import chat_pb2
import chat_pb2_grpc

model_name = "deepseek-ai/DeepSeek-V2.5"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
# `max_memory` should be set based on your devices
max_memory = {i: "4GB" for i in range(8)}
# `device_map` cannot be set to `auto`
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, device_map="sequential", torch_dtype=torch.bfloat16, max_memory=max_memory, attn_implementation="eager")
model.generation_config = GenerationConfig.from_pretrained(model_name)
model.generation_config.pad_token_id = model.generation_config.eos_token_id

class ChatService(chat_pb2_grpc.ChatServiceServicer):
    def Chat(self, request, context):
        user_input = request.text
        
        messages = [
            {
                "role": "user", "content": user_input
            }
        ]
        input_tensor = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
        outputs = model.generate(input_tensor.to(model.device), max_new_tokens=100)
        
        result = tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)
        print(result)
        
        # Decode the model's output
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return chat_pb2.ChatResponse(response=response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at [::]:50051")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
