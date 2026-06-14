import search

def main():    
    print("\nBem-vindo ao Chat RAG. Digite sua pergunta ou 'sair' para encerrar.\n")
    while True:
        user_question = input("Sua pergunta: ")
        if user_question.lower() == 'sair':
            break
        
        response = search.search_prompt(user_question)
        
        print(f"Resposta: {response}")

if __name__ == "__main__":
    main()