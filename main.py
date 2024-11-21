# main.py
import ollama
from utils import retrieve_context

# Fonction pour générer la réponse avec RAG
def generate_response_with_rag(question, search_type='drive'):
    context_docs = retrieve_context(question, search_type)
    
    if not context_docs:
        context = "Aucun document pertinent trouvé."
    else:
        context = "Contextes pertinents : " + " || ".join(context_docs)
    
    full_prompt = f"""
    Context: {context}
    
    Question: {question}
    
    Génère une réponse précise basée sur le contexte fourni. 
    Si aucun contexte n'est pertinent, réponds de manière générale.
    """
    
    # Interroger le modèle Ollama (s'assurer que le modèle est bien configuré)
    response = ollama.chat(
        model="llama3.2",
        messages=[{'role': 'user', 'content': full_prompt}]
    )
    return response['message']['content']

# Fonction principale de l'interface utilisateur
def main():
    print("Chat RAG - Recherche flexible")
    print("Types de recherche : drive, web, all")
    print("Tapez 'exit' pour quitter")
    
    while True:
        search_type = input("Type de recherche (drive/web/all) : ")
        if search_type.lower() == 'exit':
            break
        
        question = input("Votre question : ")
        if question.lower() == 'exit':
            break
        
        print("\nRéponse RAG : ", generate_response_with_rag(question, search_type))
        print("\n" + "-"*50 + "\n")

# Exécution du programme
if __name__ == "__main__":
    main()
