import asyncio
import json
import websockets
import wave
import numpy as np
from vosk import Model, KaldiRecognizer

model = Model(r"./vosk-model-small-cn-0.22/vosk-model-small-cn-0.22")

# 创建识别器


async def on_connect(websocket):
    #print(f"New connection: {websocket.remote_address}")
    rec = KaldiRecognizer(model, 16000)

    try:
         

        async for message in websocket:
            #print(message)
            #if isinstance(message, bytes):
            #    audio_buffer.extend(message)

                #while len(audio_buffer) >= target_bytes_float32:
                 #   chunk = bytes(audio_buffer[:target_bytes_float32])
                    #del audio_buffer[:target_bytes_float32]
                    #save_float32_chunk_to_wav(
                     #   chunk, f"audio_{file_count}.wav", sample_rate, num_channels
                    #)
                    #file_count += 1
            #else:
             #   print(f"Received text message: {message}")
            if isinstance(message, bytes):
                if rec.AcceptWaveform(message):
                    result = json.loads(rec.Result())
                    print("识别结果:", result["text"])
                    
                    if any(k in result["text"] for k in ["饺子","小痣","小是","小事", "小智","小字","小子","小紫","小自","小四","小志"]):
                       await websocket.send("yes") 
                
                

  
 


           # await websocket.send("Message received")

    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
 

def save_float32_chunk_to_wav(raw_bytes, filename, sample_rate, num_channels):
    # bytes -> float32
    audio_f32 = np.frombuffer(raw_bytes, dtype=np.float32)

    # 防止残缺采样（非4字节对齐）
    usable_len = (audio_f32.size // num_channels) * num_channels
    audio_f32 = audio_f32[:usable_len]

    # float32(-1~1) -> int16 PCM
    audio_i16 = np.clip(audio_f32, -1.0, 1.0)
    audio_i16 = (audio_i16 * 32767.0).astype(np.int16)

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(2)  # int16 = 2字节
        wf.setframerate(sample_rate)
        wf.writeframes(audio_i16.tobytes())

    print(f"Saved {filename}, samples={audio_i16.size}")

async def main():
    # WebSocket服务器配置
    host = "0.0.0.0"
    port = 10096
    backlog = 50  # 允许的待处理连接数
    
    # 启动WebSocket服务器
    server = await websockets.serve(
        on_connect, 
        host, 
        port, 
        backlog=backlog,
        max_size=None,  # 允许任意大小的消息
        ping_interval=20,  # 心跳检测间隔
        ping_timeout=10    # 心跳超时时间
    )
    
    print(f"WebSocket服务器已启动，监听地址: ws://{host}:{port}")
    print(f"服务器配置: 最大并发连接数={backlog}")
    print("等待客户端连接...")
    
    # 保持服务器运行
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n服务器已被用户中断")
    except Exception as e:
        print(f"服务器启动失败: {e}")
