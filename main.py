from Model.HashTable import HashTable

h = HashTable()

h.addElement("text")
h.addElement("abc")
h.addElement("def")
h.addElement("dsad")
h.addElement("daasds")
h.addElement("ident")
h.addElement("identif2")
h.addElement("identif3")
h.addElement("text")

print(h.getElements())
print(h.getElement("identif2"))
