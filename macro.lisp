

(#macro (
    (seq (read (token (name word)) as name) \( (read many (seq (read (ast value) into args) ,)) (read (ast value) into args) \))
) (
    ($name $args)
))

print("hello")

