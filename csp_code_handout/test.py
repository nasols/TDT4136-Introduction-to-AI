

dict = {"hei" : ["1", "2", "3"], "hade" : [4, 5, 6]}

dict["hei"].remove("2")
dict["hei"].remove("1")

print(dict.get("hei"))
print(dict)