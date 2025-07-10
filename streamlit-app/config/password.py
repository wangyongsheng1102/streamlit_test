from streamlit_authenticator import Hasher

result = Hasher.check_pw("wangys", "$2b$12$1ilRl6xUMu0wl09BAuefeuhtZhp9kw7jMdr.VEF13dzEnCzPklgH6")
print(result)
