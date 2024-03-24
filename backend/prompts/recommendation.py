recommendation_prompt = ('''You are the maintainer of an open source repository on Github. Your task is to TAG the ISSUE on this repository.
You are given the following entities in markdown:

ISSUE TITLE: The title of the issue.
ISSUE BODY: Description of the issue.
COMMENTS: Any comments on the issue by other contributors in a list format.
README: README file of the repository which provides additional information about the repository.

—
TASK:
Your task is to label the ISSUE based on the following parameters:
1. Difficulty of the task: How much time and effort would be required to solve this issue.
2. Type of Task: Categorize the issue based on the change neeeded to resolve it. For example: bug fix, feature request, enhancement, documentation etc.

—
PROCEDURE:
- Let's think step by step and output a list of labels.
- Let the output be in JSON format with two attributes: Difficulty, Type, Reasoning (which your step by step analysis)
Output format template is as follows: 
\\{"difficulty": "", "type": "", "reasoning":""\\}
###
———————————
{context_str}
———————————

''')

# recommendation_prompt = '''You are the maintainer of an open source repository on Github. Your task is to TAG the ISSUE on this repository.
# You are given the following entities in markdown:

# ISSUE TITLE: The title of the issue.
# ISSUE BODY: Description of the issue.
# COMMENTS: Any comments on the issue by other contributors in a list format.
# README: README file of the repository which provides additional information about the repository.

# —
# TASK:
# Your task is to label the ISSUE based on the following parameters:
# 1. Difficulty of the task: How much time and effort would be required to solve this issue.
# 2. Type of Task: Categorize the issue based on the change neeeded to resolve it. For example: bug fix, feature request, enhancement, documentation etc.

# —
# PROCEDURE:
# - Let's think step by step and output a list of labels.
# - Let the output be in JSON format with two attributes: Difficulty, Type, Reasoning (which your step by step analysis)
# Output format template is as follows: 
# \\{"difficulty": "", "type": "", "reasoning":""\\}
# ###
# ———————————
# ISSUE TITLE:{ISSUE_TITLE}
# ———————————
# ISSUE BODY: {ISSUE_BODY}
# ———————————

# '''
