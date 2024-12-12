from utils import generate

userPrompt = """Write a summary of this Instagram profile:

Instagram Handle:
@

Bio:

Post 1:

Post 2:

Post 3:

Post 4:

Post 5:

"""

out = generate(client=client, 
               TASK_TYPE='summarize_influencer',
               userPrompt=userPrompt
               )

print(out)