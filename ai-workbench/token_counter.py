import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

samples = [
    "The capital of France is Paris.",
    "Unbelievable tokenization, isn't it?", 
    "def fibonacci(n): return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)",
]

for text in samples:
    tokens = enc.encode(text)
    print(f"{len(tokens): 3d} tokens | {text[:50]}")
    print(f"          pieces: {enc.decode_tokens_bytes(tokens)[:12]}")
    
