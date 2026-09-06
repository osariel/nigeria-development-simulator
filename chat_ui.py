"""Streamlit chat surface for the existing simulator datasets."""
import streamlit as st
from models.chat import answer


def render_chat(states, costs):
    st.markdown('''<style>
    .stMainBlockContainer {max-width: 960px; padding-top: 4.5rem;}
    [data-testid="stChatMessage"] {border: 1px solid #dce6e2; border-radius: 16px; margin-bottom: 1rem;}
    h1 {font-size: 2.3rem !important; letter-spacing: -.06rem;}
    </style>''', unsafe_allow_html=True)
    years = sorted(states.year.unique().tolist(), reverse=True)
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []
        st.session_state.chat_context = {'year': years[0], 'states': []}
    with st.sidebar:
        st.markdown('### Nigeria Development Simulator')
        st.caption('Explore public budgets through conversation.')
        if st.button('＋ New conversation', width='stretch'):
            st.session_state.conversation = []
            st.session_state.chat_context = {'year': years[0], 'states': []}
            st.rerun()
        context = st.session_state.chat_context
        st.markdown('**Current context**')
        st.write(f"Budget year: {context['year']}")
        st.write('States: ' + (', '.join(context['states']) or 'Choose in chat'))
        st.caption('Mention a different state or year to switch context.')
        st.divider()
        st.caption('Dataset assistant · no external AI service. Supports budget lookups, comparisons, rankings and project estimates. Conversations last for this session.')
        if st.session_state.conversation:
            transcript = '\n\n'.join(m['role'].upper() + '\n' + m['text'] + ('\n' + m['table'].to_csv(index=False) if 'table' in m else '') for m in st.session_state.conversation)
            st.download_button('Download conversation', transcript, 'budget-conversation.txt', 'text/plain')
    st.caption('PUBLIC MONEY, MADE UNDERSTANDABLE')
    st.title('Let’s talk about Nigeria’s budgets.')
    st.write('Explore your state. Compare spending plans. See what an investment could build.')
    quick = None
    if not st.session_state.conversation:
        with st.chat_message('assistant'):
            st.write('What would you like to explore? I can use the budget figures and project assumptions in this simulator. Start below or type your own question.')
        examples = ['Lagos budget 2026', 'Compare Lagos and Kano', 'What could ₦1 billion build?', 'Rank states by budget per person']
        cols = st.columns(2)
        for i, example in enumerate(examples):
            if cols[i % 2].button(example, width='stretch'):
                quick = example
    for message in st.session_state.conversation:
        with st.chat_message(message['role']):
            st.markdown(message['text'])
            if 'table' in message:
                st.dataframe(message['table'], hide_index=True, width='stretch')
            if message.get('sources') or message.get('assumptions'):
                with st.expander('Sources and assumptions'):
                    for src in message.get('sources', []):
                        st.write(f"{src['state']} · {src['budget_status']} · {src['status']}")
                        st.write(src['name'])
                        if src['url'].startswith(('https://', 'http://')):
                            st.link_button('Budget source', src['url'])
                        st.caption(src['notes'])
                    for src in message.get('assumptions', []):
                        st.write(src['item'])
                        st.caption(src['notes'])
                        if str(src['source_url']).startswith(('https://', 'http://')):
                            st.link_button(src['source_name'], src['source_url'])
    prompt = st.chat_input('Ask about a state, compare budgets, or try an investment…', max_chars=2000) or quick
    if prompt:
        with st.spinner('Checking the data…'):
            response = answer(prompt, st.session_state.chat_context, states, costs)
        st.session_state.chat_context = response.pop('context')
        st.session_state.conversation.extend([{'role': 'user', 'text': prompt}, {'role': 'assistant', **response}])
        st.rerun()
