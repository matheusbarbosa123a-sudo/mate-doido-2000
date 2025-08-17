import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("❌ Defina a variável de ambiente OPENAI_API_KEY no seu sistema ou no arquivo .env")
else:
    client = OpenAI(api_key=api_key)

    st.set_page_config(page_title="Mate Doido 2000 🤖💥", page_icon="🤖")
    st.title("🤖💥 Assistente IA - Mate Doido 2000")

    # Função para resetar histórico
    def reset_chat():
        st.session_state["messages"] = [
            {"role": "system", "content": "Você é Mate Doido 2000, um assistente engraçado, descontraído e útil."}
        ]

    # Inicializar histórico de mensagens
    if "messages" not in st.session_state:
        reset_chat()

    # Botão para resetar
    if st.button("🔄 Resetar Chat"):
        reset_chat()
        st.success("Histórico apagado! O Mate Doido 2000 começou do zero 🤖💥")

    # Mostrar histórico no chat
    for msg in st.session_state.messages[1:]:  # Ignora o primeiro (system)
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])

    # Entrada do usuário
    if prompt := st.chat_input("Digite sua mensagem para o Mate Doido 2000..."):
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Gerar resposta
        with st.spinner("Mate Doido 2000 pensando... ⚡🤯"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                reply = response.choices[0].message.content

                # Guardar e mostrar resposta
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            except Exception as e:
                st.error(f"Erro: {e}")
