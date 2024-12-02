# import streamlit as st
# from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
# import torch

# # Model and tokenizer loading
# checkpoint = "LaMini-Flan-T5-248M"
# tokenizer = T5Tokenizer.from_pretrained(checkpoint)
# base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)


# def summarize_text(input_text):
#     # Check if the tokenizer has pad_token, otherwise assign a fallback
#     if tokenizer.pad_token is None:
#         if tokenizer.eos_token is not None:
#             tokenizer.pad_token = tokenizer.eos_token
#         else:
#             # Fallback to using <pad> token or </s> token if eos_token is missing
#             tokenizer.pad_token = tokenizer.special_tokens_map.get('pad_token', '</s>')

#     # Initialize the summarization pipeline
#     pipe_sum = pipeline(
#         'summarization',
#         model=base_model,
#         tokenizer=tokenizer,
#         max_length=500,
#         min_length=50
#     )

#     # Perform summarization
#     result = pipe_sum(input_text)
#     return result[0]['summary_text']


# # Streamlit app
# def main():
#     print("Inside main function")
#     st.set_page_config("Text Summarizer")
#     st.header("Text Summarization App using Language Model")
#     # st.title("Text Summarization App using Language Model")

#     # Text input box
#     input_text = st.text_area("Enter the text you want to summarize", height=300)


#     # Summarize button
#     if st.button("Summarize"):
#         if input_text:
#             # Process and display summary
#             summary = summarize_text(input_text)
#             st.info("Summarization Complete")
#             st.success(summary)
#         else:
#             st.warning("Please enter some text to summarize.")

# if __name__ == "__main__":
#     main()


import streamlit as st
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline
import torch

# Model and tokenizer loading
checkpoint = "LaMini-Flan-T5-248M"
tokenizer = T5Tokenizer.from_pretrained(checkpoint)
base_model = T5ForConditionalGeneration.from_pretrained(checkpoint, device_map='auto', torch_dtype=torch.float32)

def summarize_text(input_text):
    # Check if the tokenizer has pad_token, otherwise assign a fallback
    if tokenizer.pad_token is None:
        if tokenizer.eos_token is not None:
            tokenizer.pad_token = tokenizer.eos_token
        else:
            # Fallback to using <pad> token or </s> token if eos_token is missing
            tokenizer.pad_token = tokenizer.special_tokens_map.get('pad_token', '</s>')

    # Initialize the summarization pipeline
    pipe_sum = pipeline(
        'summarization',
        model=base_model,
        tokenizer=tokenizer,
        max_length=500,
        min_length=50
    )

    # Perform summarization
    result = pipe_sum(input_text)
    return result[0]['summary_text']

# Streamlit app

def main():
    # st.set_page_config(page_title="My App", theme="light")
    st.set_page_config("Text Summarizer")
    st.header("Text Summarization App ")

    # Text input box
    input_text = st.text_area("Enter the text you want to summarize", height=300)

    # Summarize button
    if st.button("Summarize"):
        if input_text:
            # Process and display summary
            summary = summarize_text(input_text)
            st.info("Summarization Complete")
            st.success(summary)

            # Store the input and summary in session state
            if 'history' not in st.session_state:
                st.session_state['history'] = []
            st.session_state['history'].append({'input': input_text, 'summary': summary})
        else:
            st.warning("Please enter some text to summarize.")
    
    # Display history in the sidebar
    st.sidebar.title("Summary History")
    if 'history' in st.session_state:
        for idx, entry in enumerate(st.session_state['history']):
            with st.sidebar.expander(f"Summary {idx+1}"):
                st.write(f"**Input:** {entry['input']}")
                st.write(f"**Summary:** {entry['summary']}")
    else:
        st.sidebar.write("No history yet.")

if __name__ == "__main__":
    main()
