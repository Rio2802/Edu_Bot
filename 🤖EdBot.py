import os

import streamlit as st
from streamlit_google_auth import Authenticate

from openai_key import get_openai_key
from chatbot import render_chatbot
from modules.sqlrag_module import get_tables 
from settings import initialize_settings, save_prompt
from modules.sqlrag_module import create_users_table, get_engine, upsert_user, get_user_by_email, create_pjs_points_table


st.set_page_config(
    page_title="EdBot",
    page_icon="🤖",
    menu_items={
        'Get Help': 'https://github.com/Rio2802',
    }
)

st.title('🤖🎓EdBot')

st.sidebar.title('🤖🎓EdBot')
st.sidebar.markdown("**Chatbot for personalizing teaching materials**")

st.sidebar.markdown(
    "EdBot🤖🎓 is a chatbot for students and teachers of the Faculty of Informatics in Leaning Plaform. It uses large-scale language models (LLM) and modern RAG techniques to retrieve relevant information and generate answers.\n\n"
    "EdBot can answer questions from documents stored in the knowledge base (📚Files). The user can add, delete and define which files will be used to enrich EdBot's knowledge.\n\n"
    "The user can store information about himself (👤User profile) in order for EdBot to adapt its answers, for example according to the user's programming knowledge.\n\n"
    "EdBot can also retrieve data from the database and website of the University of Pula."
)

st.sidebar.write("Autor: [Luka Blašković](https://github.com/Rio2802)")

st.sidebar.write("Source Code(https://github.com/Rio2802/edu_bot).")


authenticator = Authenticate(
    secret_credentials_path='google_credentials.json',
    cookie_name='EdBot_cookie',
    cookie_key=os.getenv('COOKIE_KEY'),
    cookie_expiry_days=30,
    redirect_uri='http://localhost:8501',
)

authenticator.check_authentification()


if st.session_state['connected']:
    initialize_settings()
    
    #st.session_state["llm_selection"]["selected_model"]
    #st.session_state["llm_selection"]["selected_gpt"]
    #st.session_state["llm_selection"]["selected_embedding_model"]
    #st.session_state["intent_agent_settings"]["retriever_mode"]
    #st.session_state["intent_agent_settings"]["similarity_top_k"]
    #st.session_state["user_context_included"]
  
    email = st.session_state['user_info'].get('email')
    user_details = get_user_by_email(email) 
            
    if 'study_year' not in st.session_state["user_info"]:
        st.session_state["user_info"]["study_year"] = "1. prijediplomski"
    if 'about_me' not in st.session_state["user_info"]:
        st.session_state["user_info"]["about_me"] = ""
    if 'programming_knowledge' not in st.session_state["user_info"]:
        st.session_state["user_info"]["programming_knowledge"] = 0
    
    
    study_year = user_details.get('study_year') if user_details else "1. prijediplomski"
    about_me = user_details.get('about_me') if user_details else ""
    programming_knowledge = user_details.get('programming_knowledge') if user_details else 0

    st.session_state["user_info"]["study_year"] = study_year
    st.session_state["user_info"]["about_me"] = about_me
    st.session_state["user_info"]["programming_knowledge"] = programming_knowledge
    
def raptor_settings():
    st.radio(
        "RAPTOR Retriever Mode",
        options=["collapsed", "tree_traversal",],
        help="Odaberi način pretraživanja klastera u RAPTOR-u. 'collapsed' pristup postavlja sve čvorove na istu razinu i evaluira sličnost čvorova simultano. 'tree_traversal' pristup koristi stablo za pretraživanje klastera i evaluira sličnost čvorova po razini stabla.",
        on_change=lambda: st.session_state["intent_agent_settings"].update(
            {"retriever_mode": st.session_state["temp_retriever_mode"]}
        ),
        key="temp_retriever_mode"
    )
    st.number_input("Unesi top-k", 
                    min_value=1, 
                    max_value=10,
                    help="Odaberi broj najrelevantnijih klastera koje će RAPTOR koristiti za pretraživanje.",  
                    key="temp_similarity_top_k",
                    value=st.session_state["intent_agent_settings"]["similarity_top_k"],
                    on_change=lambda: st.session_state["intent_agent_settings"].update(
                        {"similarity_top_k": st.session_state["temp_similarity_top_k"]} 
                    )
    )
    
    selected_embedding_model = st.radio(
                "Odaberi embedding model koji želiš koristiti",
                ('text-embedding-3-small', 'text-embedding-3-large'),
                help="Embedding model koji će se koristiti za embedding klastera prilikom izrade RAPTOR stabla i pozivanja RAPTOR Retriever-a.",
                
                on_change=lambda: st.session_state["llm_selection"].update(
                    {"selected_embedding_model": st.session_state["temp_selected_embedding_model"]}
                ),
                key="temp_selected_embedding_model",
            )

def sql_rag_settings():
    st.write("Označi tablice iz baze podataka koje će se koristiti za SQL-RAG")
    
    # Tables which will be used for SQL-RAG        
    tables = get_tables()
    selected_tables = {}
    
    for table in tables:
        selected_tables[table] = st.checkbox(table, 
                                                key=f"sql_rag_table_{table}", 
                                                on_change= lambda: st.session_state["sql_rag_tables"].update(
                                                    {table: st.session_state[f"sql_rag_table_{table}"]}),
                                                value=st.session_state["sql_rag_tables"][table]
                                                )

def web_scraper_settings():
    st.write("Web Scraper Settings (To-Do)")
    
    
    slider_value = st.slider(
        "Odaberi maksimalni broj najnovijih objava koje želiš da proučim sa stranica Sveučilišta/Fakulteta",
        min_value=1, 
        max_value=100,
        value=st.session_state["web_scraper_settings"]["max_number_of_posts"],
        key="temp_web_scraper_max_number_of_posts",
        on_change= lambda: st.session_state["web_scraper_settings"].update(
            {"max_number_of_posts": st.session_state["temp_web_scraper_max_number_of_posts"]}
        )
    )
    
    selected_web_url = st.radio(
                "Odaberi stranicu koju želiš da proučim",
                ('https://www.unipu.hr/novosti', 'https://fipu.unipu.hr/fipu/novosti'),
                help="Odaberi stranicu sastavnice Sveučilišta u Puli koju želiš da proučim.",
                
                on_change=lambda: st.session_state["web_scraper_settings"].update(
                    {"selected_web_url": st.session_state["temp_selected_web_url"]}
                ),
                key="temp_selected_web_url",
            )

def intent_recognition_settings():
    st.checkbox("Koristi cijeli razgovor kao kontekst", key="use_full_conversation", value=False)
    st.checkbox("Koristi podatke o korisniku kao kontekst", key="user_context_included", value=True)
    st.text_area(
        label="Direct LLM Prompt",
        value=st.session_state["intent_agent_settings"]["direct_llm_prompt"],
        on_change=lambda: st.session_state["intent_agent_settings"].update(
            {"direct_llm_prompt": st.session_state["temp_direct_llm_prompt"]}
        ),
        key="temp_direct_llm_prompt", 
        height=200
    )
    st.button(label="Spremi", key="btn_save_direct_llm_settings", type="primary", on_click=lambda: save_prompt("./prompts/DIRECT_LLM_PROMPT.txt", st.session_state["temp_direct_llm_prompt"]))

    st.text_area(
        label="Query Engine Description",
        value=st.session_state["intent_agent_settings"]["llm_query_tool_description"],
        on_change=lambda: st.session_state["intent_agent_settings"].update(
            {"llm_query_tool_description": st.session_state["temp_llm_query_tool_description"]}
        ),
        key="temp_llm_query_tool_description", 
        height=200
    )
    st.button(label="Spremi", key="btn_save_query_engine_desc", type="primary", on_click=lambda: save_prompt("./prompts/LLM_QUERY_TOOL_DESCRIPTION.txt", st.session_state["temp_llm_query_tool_description"]))

    st.divider()
    
    use_raptor = st.checkbox("Koristi RAPTOR Engine", 
                                value= st.session_state["intent_agent_settings"]["use_raptor"],
                                on_change=lambda: st.session_state["intent_agent_settings"].update(
                                    {"use_raptor": st.session_state["temp_use_raptor"]}
                                ), 
                                key="temp_use_raptor")
    if use_raptor:
        st.text_area(
            label="RAPTOR Engine Description",
            value=st.session_state["intent_agent_settings"]["raptor_query_tool_description"],
            on_change=lambda: st.session_state["intent_agent_settings"].update(
                {"raptor_query_tool_description": st.session_state["temp_raptor_query_tool_description"]}
            ),
            key="temp_raptor_query_tool_description",
            height=200
        )
    st.button(label="Spremi", key="btn_save_raptor_settings", type="primary", on_click=lambda: save_prompt("./prompts/RAPTOR_QUERY_TOOL_DESCRIPTION.txt", st.session_state["temp_raptor_query_tool_description"]))
    st.divider()
    
    use_sql_rag = st.checkbox("Koristi SQL-RAG Engine", 
                                value= st.session_state["intent_agent_settings"]["use_sql_rag"],
                                on_change=lambda: st.session_state["intent_agent_settings"].update(
                                    {"use_sql_rag": st.session_state["temp_use_sql_rag"]}
                                ), 
                                key="temp_use_sql_rag")
    if use_sql_rag:
        st.text_area(
            label="SQL-RAG Engine Description",
            value=st.session_state["intent_agent_settings"]["sql_rag_query_tool_description"],
            on_change=lambda: st.session_state["intent_agent_settings"].update(
                {"sql_rag_query_tool_description": st.session_state["temp_sql_rag_query_tool_description"]}
            ),
            key="temp_sql_rag_query_tool_description",
            height=200
        )
        
    st.button(label="Spremi", key="btn_save_sqlrag_settings", type="primary", on_click=lambda: save_prompt("./prompts/SQL_RAG_QUERY_TOOL_DESCRIPTION.txt", st.session_state["temp_sql_rag_query_tool_description"]))

    use_web_scraper = st.checkbox("Koristi Web Scraper Engine", 
                                value= st.session_state["intent_agent_settings"]["use_web_scraper"],
                                on_change=lambda: st.session_state["intent_agent_settings"].update(
                                    {"use_web_scraper": st.session_state["temp_use_web_scraper"]}
                                ), 
                                key="temp_use_web_scraper")
    if use_web_scraper:
        st.text_area(
            label="Web Scraper Engine Description",
            value=st.session_state["intent_agent_settings"]["web_scraper_query_tool_description"],
            on_change=lambda: st.session_state["intent_agent_settings"].update(
                {"sql_web_scraper_query_tool_description": st.session_state["temp_web_scraper_query_tool_description"]}
            ),
            key="temp_web_scraper_query_tool_description",
            height=200
        )
        
    st.button(label="Spremi", key="btn_save_webscraper_settings", type="primary", on_click=lambda: save_prompt("./prompts/WEB_SCRAPER_QUERY_TOOL_DESCRIPTION.txt", st.session_state["temp_web_scraper_query_tool_description"]))
    
if st.session_state['connected']:
    
    col1, col2 = st.columns([3, 1])

    with col1:
        st.write(f"Hej, {st.session_state['user_info'].get('name')}👋🏻")
        st.write("Uspješna prijava! Huuray! 🎉")
        st.write("""Tu sam da ti olakšam studentsku avanturu na [Fakultetu informatike](https://fipu.unipu.hr/). Bilo da imaš pitanja o studiju, predmetima, profesorima, projektima, ili nečemu drugome, tu sam da ti pomognem.""")
        st.write("Ako ti nije jasan silabus nekog kolegija, tražiš objašnjenje teorije iz skripte, imaš problem s programiranjem, ili te zanima koliko ti bodova nedostaje za prolaz iz nekog kolegija, slobodno me pitaj!😊")

    with col2:
        debug_mode_on = st.toggle("Ispod haube", key="debug_mode", value=True)

    with st.sidebar:
        if st.button('Odjava'):
            authenticator.logout()
        container = st.sidebar.container(border=True)
        
        with st.expander("Postavke | Odabir modela", expanded=False):
            st.radio(
                "Odaberi LLM koji želiš koristiti za pogon EdBota🤖",
                options=["GPT", "mistral:7b", "gemma:7b", "llama3:8b", "Claude 3 Opus", "Claude 3 Sonnet", "Claude 3 Haiku"],
                on_change=lambda: st.session_state["llm_selection"].update(
                    {"selected_model": st.session_state["temp_selected_model"]}
                ),
                help="",
                key="temp_selected_model",
            )
            if(st.session_state["llm_selection"]["selected_model"] == "GPT"):
                st.session_state["openai_api_key"] = get_openai_key()
                st.checkbox("Učitaj OpenAI API ključ iz okruženja", key="use_openai_env", help="Chekiraj ovu opciju ako želiš da se ključ učita iz okruženja. Potrebno je u `.env` datoteku dodati `OPENAI_API_KEY` ključ.")

                selected_gpt = st.radio(
                    "Odaberi GPT model koji želiš koristiti",
                    ('gpt-4o', 'gpt-4', 'gpt-3.5-turbo'),
                    on_change=lambda: st.session_state["llm_selection"].update(
                        {"selected_gpt": st.session_state["temp_selected_gpt"]}
                    ),
                    key="temp_selected_gpt",
                )

                
            elif(st.session_state["llm_selection"]["selected_model"] == "Mistral"):
                st.success("Odabran model Mistral7B - lokalni deployment preko Ollame🦙")
            elif(st.session_state["llm_selection"]["selected_model"] == "Gemma"):
                st.success("Odabran model Gemma - lokalni deployment preko Ollame🦙")
                
        with st.expander("Postavke | Intent Recognition", expanded=False):
            intent_recognition_settings()

        with st.expander("Postavke | RAPTOR", expanded=False):
            raptor_settings()
            
        with st.expander("Postavke | SQL-RAG", expanded=False):
            sql_rag_settings()
        
        with st.expander("Postavke | Web Scraper", expanded=False):
            web_scraper_settings()
            
    render_chatbot()

    # Reset conversation.
    if(st.button("Resetiraj razgovor")):
        st.session_state["messages"] = [{"role": "assistant", "content": "Tu sam! Kako ti mogu pomoći?🤖"}]
        st.rerun()

else:
    st.write("Bok👋🏻 Kako bi mogao koristiti EdBot, moraš se prijaviti.")
    
    authenticator.login(justify_content="start")
