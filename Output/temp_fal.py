import fal
fal.client.api_key = ''
result = fal.subscribe('fal-ai/flux.1-dev', input={'prompt': 'Gritty Welder material waste killing margins B-roll, abandoned workshop, rusty tools, cinematic horror', 'num_inference_steps': 20})
result.save('videos/broll_Welder material waste killing margins.jpg')
