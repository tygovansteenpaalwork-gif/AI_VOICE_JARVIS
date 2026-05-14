import os
import queue
import signal
import threading
import time
from dotenv import load_dotenv

from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from tools import client_tools  

class PausingAudioInterface(DefaultAudioInterface):
    def __init__(self, pause_seconds: float = 2.0):
        super().__init__()
        self.pause_seconds = pause_seconds
        self.input_callback = None
        self.output_queue: queue.Queue[bytes] = queue.Queue()
        self.should_stop = threading.Event()
        self._speaking = threading.Event()
        self._pause_until = 0.0
        self.output_thread = None

    def start(self, input_callback):
        self.input_callback = input_callback
        self.output_queue = queue.Queue()
        self.should_stop = threading.Event()
        self._speaking.clear()
        self._pause_until = 0.0
        self.output_thread = threading.Thread(target=self._output_thread, daemon=True)
        self.p = self.pyaudio.PyAudio()
        self.in_stream = self.p.open(
            format=self.pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            stream_callback=self._in_callback,
            frames_per_buffer=self.INPUT_FRAMES_PER_BUFFER,
            start=True,
        )
        self.out_stream = self.p.open(
            format=self.pyaudio.paInt16,
            channels=1,
            rate=16000,
            output=True,
            frames_per_buffer=self.OUTPUT_FRAMES_PER_BUFFER,
            start=True,
        )
        self.output_thread.start()

    def stop(self):
        self.should_stop.set()
        if self.output_thread is not None:
            self.output_thread.join()
        self.in_stream.stop_stream()
        self.in_stream.close()
        self.out_stream.close()
        self.p.terminate()

    def output(self, audio: bytes):
        self.output_queue.put(audio)

    def interrupt(self):
        try:
            while True:
                self.output_queue.get_nowait()
        except queue.Empty:
            pass
        self._speaking.clear()
        self._pause_until = time.time() + self.pause_seconds

    def _in_callback(self, in_data, frame_count, time_info, status):
        if self._can_send_input():
            self.input_callback(in_data)
        return (None, self.pyaudio.paContinue)

    def _can_send_input(self):
        return not self._speaking.is_set() and time.time() >= self._pause_until

    def _output_thread(self):
        while not self.should_stop.is_set():
            try:
                audio = self.output_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            self._speaking.set()
            print("Agent: ik denk na...")
            self.out_stream.write(audio)

            while not self.should_stop.is_set():
                try:
                    audio = self.output_queue.get(timeout=0.1)
                    self.out_stream.write(audio)
                except queue.Empty:
                    break

            self._speaking.clear()
            self._pause_until = time.time() + self.pause_seconds

load_dotenv()

agent_id = os.getenv("AGENT_ID")
api_key = os.getenv("ELEVENLABS_API_KEY")

elevenlabs = ElevenLabs(api_key=api_key)

conversation = Conversation(
    # API client and agent ID.
    elevenlabs,
    agent_id,
    client_tools=client_tools,

    # Assume auth is required when API_KEY is set.
    requires_auth=bool(api_key),

    # Use a custom audio interface that avoids feedback and waits after speech.
    audio_interface=PausingAudioInterface(pause_seconds=2.0),

    # Simple callbacks that print the conversation to the console.
    callback_agent_response=lambda response: print(f"Agent: {response}"),
    callback_agent_response_correction=lambda original, corrected: print(f"Agent: {original} -> {corrected}"),
    callback_user_transcript=lambda transcript: print(f"User: {transcript}"),

    # Uncomment if you want to see latency measurements.
    # callback_latency_measurement=lambda latency: print(f"Latency: {latency}ms"),

    # Uncomment if you want to receive audio alignment data with character-level timing.
    # callback_audio_alignment=lambda alignment: print(f"Alignment: {alignment.chars}"),
)

conversation.start_session()

signal.signal(signal.SIGINT, lambda sig, frame: conversation.end_session())

conversation_id = conversation.wait_for_session_end()
print(f"Conversation ID: {conversation_id}")
