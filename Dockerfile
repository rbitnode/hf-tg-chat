# Use Python as the base image
FROM python:3.8-slim

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
RUN pip install transformers accelerate grpcio-tools grpcio protobuf

# Set working directory
WORKDIR /app

# Copy your application code from the local machine
COPY . /app

# Download the model (if not already downloaded)
# RUN python3 -c "from transformers import AutoModelForCausalLM, AutoTokenizer; \
#     model_name = 'google/gemma-2-2b-it'; \
#     model = AutoModelForCausalLM.from_pretrained(model_name); \
#     tokenizer = AutoTokenizer.from_pretrained(model_name);"

# Generate protobuf and grpc code
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto

# Expose the gRPC server port
EXPOSE 50051

# Start the gRPC server
CMD ["python3", "server.py"]
