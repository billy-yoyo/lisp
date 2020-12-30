
(#macro 
    (seq (read (ast word) as name) \( (read many (seq (read (ast value) into args) ,)) (read (ast value) into args) \))
    (ast (&name &args))
)

print("hello")

