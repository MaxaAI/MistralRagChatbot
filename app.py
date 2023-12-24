import openai
import time
import streamlit as st

openai.api_key = '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'

def main():

    # Application Title
    st.title("MProfier Query Assistant")

    if 'client' not in st.session_state:
        # Initialize the OpenAI client
        st.session_state.client = openai.OpenAI()

        # Use your existing Assistant ID
        st.session_state.assistant_id = "asst_WOBuKDXGBSNpKuQUpi78fhON"

        # Initialize a Thread for conversation
        st.session_state.thread = st.session_state.client.beta.threads.create()

    # User input
    user_query = st.text_input("How can I assist you today?", "")

    file = openai.files.create(
    file=open("MR. MPROFY.pdf", "rb"),
    purpose='assistants'
    )

    if st.button('Ask MProfier'):
        # Add the user's query to the Thread
        message = st.session_state.client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=user_query
        )

        # Run the Assistant
        run = st.session_state.client.beta.threads.runs.create(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant_id,
            instructions="Respond as MProfier with detailed and helpful information. Look in your knowledgebase before answering"
        )

        # Display a loading message
        with st.spinner('MProfier is processing your request...'):
            while True:
                # Check the run status
                run_status = st.session_state.client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=run.id
                )

                # Display the response once ready
                if run_status.status == 'completed':
                    messages = st.session_state.client.beta.threads.messages.list(
                        thread_id=st.session_state.thread.id
                    )

                    for msg in messages.data:
                        if msg.role == "assistant":
                            content = msg.content[0].text.value
                            st.success(f"MProfier says: {content}")
                    break
                else:
                    time.sleep(2)

if __name__ == "__main__":
    main()