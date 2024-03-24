import inspect, json
import textwrap

from prompt import INFERENCE_PROMPT
import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from collections import defaultdict
from model_requests import generate_response, generate_mistral_response


def main():
    
    st.title("IssueMatcha 🍵")
    recs = st.empty()
    recs.text('Choose preferences to get started...')
    
    with st.sidebar:
        st.header("Preferences")
        with st.form('pref'):
            domain = st.selectbox(
                'Domain',
                ('AI/ML', 'Systems', 'Web dev', 'Backend', 'Data Science', 'Game Dev', 'README typos only'))
            
            languages = st.multiselect(
                'Language',
                ('Python', 'Java', 'Javascript', 'C++', 'C', 'Angular', 'React', 'C#', 'Swift', 'Ruby', 'Go'))
            details = st.text_input('Enter additional details (optional)')
            submitted = st.form_submit_button('Mistral')

    
    if submitted:
        with recs.container():
            st.subheader("Recommended Issues")
            # prompt = '''You are an expert on open source contributions and different things software engineering. Now you are in a mentor role. Based on the given USER_INPUT and DOMAIN you are to share a list of github issues that you think would be relevant for the user. Respond with top 6 issue titles with URLs in the form of an ordered, numbered list in markdown format.
            # DOMAIN: {domain}
            # USER_INPUT: {user_input}
            # '''
            
            # make a request to the backend to get issues
            
            links = ["https://github.com/piskvorky/gensim/issues/2766", "https://github.com/piskvorky/gensim/issues/2766", "https://github.com/piskvorky/gensim/issues/2766"]
            
            issues = [
                {
                    "title": "CI failed on linux_arm64_wheel",
                    "summary": "ERROR  - ValueError: numpy.broadcast size changed, may indicate binary incompatibility. Expected 816 from C header, got 560 from PyObject"
                },
                {
                    "title": "Polars not mentioned as requirement to build documentation",
                    "summary": "The developer documentation here lists the dependencies required to build the documentation. However, polars is not mentioned as a required dependency leading to the following error:     ModuleNotFoundError: No module named 'polars'"
                },
                {
                    "title": "[Bug] sklearn.base.BaseEstimator subclasses not decoratable",
                    "summary": " @beartype cannot provide \"metadata routing\" support - because the sklearn.base.BaseEstimator subclass fails to support decoration at a core level. That's outside our scope of control."
                }
            ]
            past_contributions = ''
            user_preferences = '''
            Domain: {domain}
            Programming Languages: {languages_comma}
            Preferences: {details}
            '''.format(domain = domain, languages_comma = ','.join(languages), details = details)
            print(json.dumps(issues))
            prompt_filled = INFERENCE_PROMPT.format(USER_PREFERENCES=user_preferences,PAST_CONTRIBUTIONS=past_contributions, ISSUES=json.dumps(issues))
            # chat_response = generate_response(prompt_filled)
            # chat_response = chat_response['choices'][0]['message']['content']
            # print(chat_response)
            # chat_response = generate_mistral_response(prompt_filled)
            # chat_response = json.loads(chat_response['choices'][0]['message']['content'])
            chat_response = [{'LABEL': 'NOT_RECOMMENDED', 'EXPLANATION': "This issue seems to be related to CI/CD and numpy, which are not mentioned in the user's preferences or past contributions."}, {'LABEL': 'UNABLE_TO_DETERMINE', 'EXPLANATION': "While 'polars' could potentially be used in AI/ML, it's not clear from the issue if this is the case. The user's past contributions and preferences don't provide enough context."}, {'LABEL': 'UNABLE_TO_DETERMINE', 'EXPLANATION': "This issue seems to be related to sklearn, which could be used in AI/ML. However, the user's preferences and past contributions don't mention sklearn or Python."}]
            results = defaultdict(list)
            
            print(chat_response)
            print(type(chat_response))
            
            for idx, response in enumerate(chat_response):
                if response['LABEL'] == 'HIGHLY RECOMMENDED':
                    results['HIGHLY RECOMMENDED'].append([links[idx], issues[idx]['title'], issues[idx]['summary'], response['EXPLANATION']])
                if response['LABEL'] == 'UNABLE_TO_DETERMINE':
                    results['UNABLE_TO_DETERMINE'].append([links[idx], issues[idx]['title'], issues[idx]['summary'], response['EXPLANATION']])
            
            c1, c2, c3 = st.columns([2,6,2])
            with c1:
                st.subheader("Repository")
                st.button("dummy 1")
                st.button("dummy 2")
                
            with c2:
                st.subheader("Issue")
                r1 = results['HIGHLY RECOMMENDED']
                for r in r1:
                    st.link_button("#1662 " + r[1], "https://www.google.com", help=r[2])
                    # expander = st.expander(r[1])
                    # expander.write(r[2])
                    
                r2 = results['UNABLE_TO_DETERMINE']
                for r in r2:
                    st.link_button("#1662 " + r[1], "https://www.google.com", help=r[2])
                    # expander = st.expander(f"[{r[1]}](https://www.google.com)")
                    # expander.write(r[2])
                    
            # with c3:
            #     st.subheader("Info")
            #     st.info('This is a purely informational message')
            #     st.button("dummy 3")
            #     st.button("dummy 4")
                    
                

            
            with open('tmp.txt', 'w') as fp:
                fp.write(json.dumps(chat_response))
           
            # st.link_button("#152, Help about the Scatter: Scatter Single Axis chart code not working #4", '')
            # st.link_button("#152, [Bug] sklearn.base.BaseEstimator subclasses not decoratable", '')
            # st.text(chat_response)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
    # with st.sidebar:
        # st.markdown("---")
        # st.markdown(
        #     '<h6>Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="16">&nbsp by <a href="https://twitter.com/andfanilo">@andfanilo</a></h6>',
        #     unsafe_allow_html=True,
        # )
        # st.markdown(
        #     '<div style="margin-top: 0.75em;"><a href="https://www.buymeacoffee.com/andfanilo" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
        #     unsafe_allow_html=True,
        # )