Title: Robot Dad
Date: 2023-11-26
Author: Chris Clark
Slug: robot-dad
Status: Published

*See discussion of this post on [Hacker News](https://news.ycombinator.com/item?id=38433330)*

Tired of Alexa's feeble "here's what I found on wikianswerspam.com" responses to my eight-year-old son's science questions, I whipped up Robot Dad during my Thanksgiving break. He now runs in the background of our family computer.

Robot Dad sounds like real dad, thanks to voice cloning from [Eleven Labs](https://elevenlabs.io/speech-synthesis) (very easy; I rambled about Formula 1 into a new MacOS Voice Memo for about sixty seconds, uploaded it, and voila), and answers appropriately for an eight-year-old, while deflecting prank requests -- though I suspect prompt injection will soon be second nature to this generation.

Here's my son, Dash, interacting with Robot Dad.

<audio controls preload="none" style="width:480px;">
 <source src="{static}/media/robot-dad-demo.m4a" type="audio/mp4" />
</audio>

The delays are real, and the speech-to-text is only so-so, but it manages to be just good enough to clear the "provides value" bar. Robot Dad will also inject context from the previous question into the prompt. Dash could follow up with "Robot Dad, tell me more about it" and ChatGPT would know what to do.

A few dozen lines of code glues together different AI services, for a remarkable result. The wakeword and speech-to-text happen locally, while the AI response (ChatGPT) and text-to-speech are via HTTP. It's trivial to move the LLM bit to a local Llama2 instance, but I haven't found a satisfactory text-to-speech model that can do voice cloning locally.

I also made a quick speech visualization (turns out kids are not very engaged reading console log messages) that of course ended up providing more entertainment value than the *ENTIRE MODERN MIRACLE OF ARTIFICIAL INTELLIGENCE*. Code for the visualization is in [this gist](https://gist.github.com/chrisclark/b9e7ba61654313a1e2d4a796ad5bb8a9).

<video controls="controls" width="100%" name="speech visualization">
  <source src="{static}/media/robot-dad-speech-visualization.mov">
</video>

Code for Robot Dad is below. You will need API keys for [Picovoice](https://picovoice.ai/) (and a wakeword), [Eleven Labs](https://elevenlabs.io/speech-synthesis), and OpenAI. You can pick a pre-existing Eleven Labs voice or clone your own.

    :::python
    import os, json, threading, time
    import pvporcupine, pvcheetah
    from pvrecorder import PvRecorder
    from elevenlabs import voices, generate, play, stream
    import openai

    ENDPOINT_DURATION_SECONDS = 2 # 'Quiet' seconds indicating the end of audio capture
    VOICE = 'Dad' # Via Eleven Labs
    AUDIO_DEVICE_NAME = 'MacBook Pro Microphone'
    AUDIO_DEVICE = PvRecorder.get_available_devices().index(AUDIO_DEVICE_NAME)
    OPENAI_MODEL = 'gpt-3.5-turbo-1106'

    BASE_PROMPT = """You are Robot Dad, and will be speaking with one of my children,
    trying to be a helpful parent. You explain things at a level appropriate for
    an eight-year-old.

    You are encouraging and helpful, but won't tolerate any inappropriate requests
    or attempts at pranks or jokes. If you are asked or told anything
    inappropriate, you gently say "nice try - but Robot Dad isn't falling for that!"

    If you don't know how to reply, simply say "I'm just Robot Dad, not real dad -
    so I'm afraid I can't help you with that".

    You usually answer in no more than 4 sentences - kids do not have long attention
    spans - but you can provide longer answers if it's clearly needed.
    """

    PREV_CTX_PROMPT = """

    The last request and response you received is below. The next request may or may
    not be a continuation of this conversation.

    Previous request:
    %s

    Previous response:
    %s
    """

    PREV_CTX_TIMEOUT = 60 # seconds

    keyword_paths=['%s/wakewords/Robot-Dad.ppn' % ROOT]

    porcupine_key = os.environ.get("PORCUPINE_API_KEY")
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    porcupine = pvporcupine.create(
        access_key=porcupine_key,
        keyword_paths=keyword_paths)

    cheetah = pvcheetah.create(
        access_key=porcupine_key,
        endpoint_duration_sec=ENDPOINT_DURATION_SECONDS,
        enable_automatic_punctuation=True)

    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index=AUDIO_DEVICE)

    break_audio = generate(text="Got it! Robot Dad is thinking...", voice=VOICE)
    alert_audio = generate(text="What's up kiddo?", voice=VOICE)

    def llm_req(prompt, txt):
        messages= [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f'Here is what the child has said: {txt}'}
        ]

        resp = openai.ChatCompletion.create(
          model=OPENAI_MODEL,
          messages=messages
        )
        return resp['choices'][0]['message']['content']


    # Speech-to-text using Picovoice's Cheetah
    def capture_input():
        transcript = ''
        while True:
            partial_transcript, is_endpoint = cheetah.process(recorder.read())
            transcript += partial_transcript
            if is_endpoint:
                transcript += cheetah.flush()
                break
        return transcript


    def play_async(audio):
        audio_thread = threading.Thread(target=play, args=(audio,))
        audio_thread.start()


    def main():
        print('Listening...')

        recorder.start()

        prev_request = ''
        prev_response = ''
        last_wake_time = None

        try:
            while True:
                pcm = recorder.read()
                result = porcupine.process(pcm)

                if result >= 0:
                    print('Detected Robot Dad')
                    play_async(alert_audio)

                    prompt = BASE_PROMPT
                    current_time = time.time()
                    if last_wake_time and current_time - last_wake_time < PREV_CTX_TIMEOUT:
                        prompt += PREV_CTX_PROMPT % (prev_request, prev_response)
                    last_wake_time = current_time

                    transcript = capture_input()
                    print('Heard request: %s' % transcript)
                    prev_request = transcript

                    play_async(break_audio)

                    resp = llm_req(prompt, transcript)
                    print('Answering: %s' % resp)
                    prev_response = resp

                    resp_audio = generate(text=resp, voice=VOICE, stream=True)
                    stream(resp_audio)
        except KeyboardInterrupt:
            pass

        recorder.stop()
        print('Stopped.')
    main()
