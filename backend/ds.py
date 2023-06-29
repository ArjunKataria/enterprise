from backend import qa






while True:
    query = input("USER: ")
    if query.lower() == "quit":
        break

    # Generate response
    #response = qa(dict(question=query))
    result = qa({"question": query})

    print("Rajesh: " + result)
